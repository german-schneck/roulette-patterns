#!/usr/bin/env python3
"""
GPU and parallel processing utilities for roulette simulations.
"""
import numpy as np
import os
import platform
import time
import psutil

# Optional imports
try:
    import numba
    from numba import cuda, jit, prange, vectorize
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False

# Global configuration
CUDA_AVAILABLE = False
APPLE_SILICON = False
GPU_INFO = None
USE_GPU = False
THREADS_PER_BLOCK = 256
PARALLEL_BATCH_SIZE = 250000

def setup_gpu_environment():
    """
    Setup and configure GPU environment for accelerated computations.
    Detects available hardware and optimizes settings accordingly.
    
    Returns:
        dict: Environment configuration
    """
    global CUDA_AVAILABLE, APPLE_SILICON, GPU_INFO, USE_GPU, THREADS_PER_BLOCK, PARALLEL_BATCH_SIZE
    
    print("Checking hardware capabilities...")
    
    # Check for Apple Silicon
    system = platform.system()
    machine = platform.machine()
    
    if system == "Darwin" and machine == "arm64":
        APPLE_SILICON = True
        print("Detected Apple Silicon (M1/M2)")
    
    # Check for CUDA
    if NUMBA_AVAILABLE:
        try:
            CUDA_AVAILABLE = cuda.is_available()
            if CUDA_AVAILABLE:
                device = cuda.get_current_device()
                GPU_INFO = {
                    "name": device.name,
                    "max_threads_per_block": device.MAX_THREADS_PER_BLOCK,
                    "compute_capability": device.compute_capability,
                    "total_memory": device.total_memory
                }
                print(f"CUDA GPU available: {GPU_INFO['name']}")
            else:
                print("CUDA GPU not available")
        except Exception as e:
            print(f"Error checking CUDA: {e}")
            CUDA_AVAILABLE = False
    else:
        print("Numba not available - GPU acceleration disabled")
    
    # Check CPU resources
    cpu_count = psutil.cpu_count(logical=True)
    memory_gb = psutil.virtual_memory().total / (1024 ** 3)
    
    print(f"CPU cores: {cpu_count}")
    print(f"System memory: {memory_gb:.1f} GB")
    
    # Determine optimal configuration
    if CUDA_AVAILABLE and GPU_INFO:
        USE_GPU = True
        # Optimize thread configuration for detected GPU
        THREADS_PER_BLOCK = min(GPU_INFO["max_threads_per_block"], 512)
        
        # Smaller batch size for older GPUs
        if GPU_INFO["compute_capability"][0] < 5:
            PARALLEL_BATCH_SIZE = 100000
    elif APPLE_SILICON and NUMBA_AVAILABLE:
        # Use CPU parallelism on Apple Silicon
        USE_GPU = False
        PARALLEL_BATCH_SIZE = 200000
        print("Using optimized CPU parallelism for Apple Silicon")
    elif cpu_count >= 8 and NUMBA_AVAILABLE:
        # Good CPU, use parallelism
        USE_GPU = False
        PARALLEL_BATCH_SIZE = 150000
        print("Using CPU parallelism")
    else:
        # Basic system
        USE_GPU = False
        PARALLEL_BATCH_SIZE = 50000
        print("Using standard CPU processing")
    
    config = {
        "use_gpu": USE_GPU,
        "cuda_available": CUDA_AVAILABLE,
        "apple_silicon": APPLE_SILICON,
        "cpu_count": cpu_count,
        "memory_gb": memory_gb,
        "threads_per_block": THREADS_PER_BLOCK,
        "batch_size": PARALLEL_BATCH_SIZE
    }
    
    return config

def get_optimal_blocks_threads(array_size):
    """
    Calculate optimal CUDA grid configuration for a given array size.
    
    Args:
        array_size: Size of the array to process
        
    Returns:
        tuple: (blocks_per_grid, threads_per_block)
    """
    if not CUDA_AVAILABLE or not USE_GPU:
        return None, None
        
    # Use optimal thread count for the device
    threads = THREADS_PER_BLOCK
    
    # Calculate blocks needed
    blocks = (array_size + threads - 1) // threads
    
    return blocks, threads

if NUMBA_AVAILABLE:
    # Numba-accelerated functions

    @cuda.jit
    def spin_batch_cuda(states, wheel_array, results, n_spins):
        """
        CUDA kernel for parallel roulette spins.
        
        Args:
            states: Random states for each thread
            wheel_array: Array of wheel numbers
            results: Output array for results
            n_spins: Number of spins to simulate
        """
        # Get thread position
        pos = cuda.grid(1)
        if pos < n_spins:
            # Use xoroshiro128p algorithm for random generation
            state = states[pos]
            # Generate random index
            random_val = cuda.random.xoroshiro128p_uniform_float32(state)
            wheel_idx = int(random_val * len(wheel_array))
            # Store result
            results[pos] = wheel_array[wheel_idx]

    @jit(nopython=True, parallel=True)
    def spin_batch_numba(n_spins, wheel_numbers=None):
        """
        Numba-accelerated parallel CPU implementation of batch spins.
        
        Args:
            n_spins: Number of spins to simulate
            wheel_numbers: Optional list of wheel numbers
            
        Returns:
            ndarray: Array of spin results
        """
        if wheel_numbers is None:
            # Default American roulette wheel
            wheel_numbers = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 
                                   14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 
                                   25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37])
            
        results = np.zeros(n_spins, dtype=np.int32)
        
        # Parallel loop over spins
        for i in prange(n_spins):
            # Simple random selection
            idx = np.random.randint(0, len(wheel_numbers))
            results[i] = wheel_numbers[idx]
            
        return results

    @jit(nopython=True)
    def count_hits_numba(spins, target_numbers):
        """
        Numba-accelerated function to count hits in spin results.
        
        Args:
            spins: Array of spin results
            target_numbers: Array of target numbers to count
            
        Returns:
            int: Number of hits
        """
        hit_count = 0
        for spin in spins:
            for target in target_numbers:
                if spin == target:
                    hit_count += 1
                    break
        return hit_count

    @cuda.jit
    def count_hits_cuda(spins, targets, count, length, targets_length):
        """
        CUDA kernel for counting hits in parallel.
        
        Args:
            spins: Array of spin results
            targets: Array of target numbers
            count: Output array for hit count
            length: Length of spins array
            targets_length: Length of targets array
        """
        pos = cuda.grid(1)
        
        # Count hits for this thread's position
        if pos < length:
            for i in range(targets_length):
                if spins[pos] == targets[i]:
                    cuda.atomic.add(count, 0, 1)
                    break 