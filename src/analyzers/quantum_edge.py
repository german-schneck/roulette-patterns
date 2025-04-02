#!/usr/bin/env python3
"""
Quantum Edge Strategy Analyzer

Implementation of a strategy that applies quantum mechanics principles
to identify patterns in roulette outcomes.
"""

import numpy as np
from collections import defaultdict
import math
from src.utils.analysis import validate_numbers_performance

def analyze_quantum_edge(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze optimal number selection using quantum mechanics-inspired algorithms.
    
    This strategy incorporates:
    1. Von Neumann entropy analysis for identifying ordered vs. chaotic regions
    2. Quantum decoherence modeling to predict pattern collapse
    3. Quantum entanglement analysis for correlated numbers
    4. Quantum interference patterns to identify constructive probability zones
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nGenerando combinación con estrategia Quantum Edge (Ventaja Cuántica)...")
    
    # Get history 
    history = analyzer.history[-5000:] if len(analyzer.history) > 5000 else analyzer.history
    
    # Convert history strings to integers for numerical analysis
    numeric_history = []
    for num in history:
        if isinstance(num, str):
            if num == '00':
                numeric_history.append(37)
            else:
                numeric_history.append(int(num))
        else:
            numeric_history.append(num)
    
    # Generate different quantum-based combinations
    combinations = []
    
    # 1. Von Neumann Entropy Analysis
    entropy_numbers = analyze_von_neumann_entropy(numeric_history)
    combinations.append(("Von Neumann Entropy", entropy_numbers))
    
    # 2. Quantum Decoherence Analysis
    decoherence_numbers = analyze_quantum_decoherence(numeric_history)
    combinations.append(("Quantum Decoherence", decoherence_numbers))
    
    # 3. Quantum Entanglement Analysis
    entanglement_numbers = analyze_quantum_entanglement(numeric_history)
    combinations.append(("Quantum Entanglement", entanglement_numbers))
    
    # 4. Quantum Interference Analysis
    interference_numbers = analyze_quantum_interference(numeric_history)
    combinations.append(("Quantum Interference", interference_numbers))
    
    # Test each quantum-based combination
    best_win_rate = 0
    best_combination_name = ""
    best_quantum_numbers = []
    
    for name, numbers in combinations:
        print(f"\nValidando combinación {name}...")
        win_rate = validate_numbers_performance(validation_analyzer, numbers, validation_spins // 4)
        coverage = len(numbers) / 38 * 100
        performance = (win_rate / coverage - 1) * 100
        
        print(f"Combination: {name}")
        print(f"Numbers: {', '.join(numbers)}")
        print(f"Win rate: {win_rate:.2f}%")
        print(f"Performance vs random: {performance:+.2f}%")
        
        if win_rate > best_win_rate:
            best_win_rate = win_rate
            best_combination_name = name
            best_quantum_numbers = numbers
    
    # If sorted_numbers is provided, enhance our selection with top performers
    if sorted_numbers:
        # Create a blend with top numbers from pre-sorted list
        quantum_enhanced = []
        
        # Include top 4 numbers from our Quantum Edge analysis
        quantum_enhanced.extend(best_quantum_numbers[:4])
        
        # Add top ranked numbers from sorted_numbers that aren't already included
        for num in sorted_numbers:
            if num not in quantum_enhanced and len(quantum_enhanced) < 8:
                quantum_enhanced.append(num)
        
        # Validate the enhanced combination
        print("\nValidando combinación Quantum Edge mejorada...")
        quantum_win_rate = validate_numbers_performance(
            validation_analyzer, quantum_enhanced, validation_spins)
        
        quantum_coverage = len(quantum_enhanced) / 38 * 100
        quantum_performance = (quantum_win_rate / quantum_coverage - 1) * 100
        
        print(f"Combinación Quantum Edge final: {', '.join(quantum_enhanced)}")
        print(f"Tasa de victoria: {quantum_win_rate:.2f}%")
        print(f"Rendimiento: {quantum_performance:+.2f}%")
        
        final_numbers = quantum_enhanced
        final_win_rate = quantum_win_rate
        final_performance = quantum_performance
    else:
        final_numbers = best_quantum_numbers
        final_win_rate = best_win_rate
        final_performance = (final_win_rate / (len(final_numbers) / 38 * 100) - 1) * 100
    
    # Return results
    return {
        'quantum_edge_numbers': final_numbers,
        'quantum_edge_win_rate': final_win_rate,
        'quantum_edge_performance': final_performance,
        'best_combination_type': best_combination_name
    }

def create_density_matrix(history, window_size=5):
    """
    Create a quantum density matrix from a segment of the history.
    
    Args:
        history: List of roulette outcomes as integers
        window_size: Size of the sliding window
        
    Returns:
        numpy.ndarray: Density matrix
    """
    # Normalize history to range [0, 1]
    normalized = np.array(history) / 37
    
    # Create density matrix
    density_matrix = np.zeros((window_size, window_size), dtype=complex)
    
    for i in range(len(history) - window_size):
        # Extract window
        window = normalized[i:i+window_size]
        
        # Create "pure state" vector
        state = window / np.linalg.norm(window)
        
        # Add contribution to density matrix (|ψ⟩⟨ψ|)
        density_matrix += np.outer(state, np.conj(state))
    
    # Normalize density matrix
    if len(history) > window_size:
        density_matrix /= (len(history) - window_size)
    
    return density_matrix

def calculate_von_neumann_entropy(density_matrix):
    """
    Calculate the von Neumann entropy of a density matrix.
    
    S(ρ) = -Tr(ρ log ρ) = -∑ λᵢ log λᵢ (where λᵢ are eigenvalues of ρ)
    
    Args:
        density_matrix: Quantum density matrix
        
    Returns:
        float: Von Neumann entropy
    """
    # Calculate eigenvalues
    eigenvalues = np.linalg.eigvalsh(density_matrix)
    
    # Keep only positive eigenvalues (numerical precision issues)
    eigenvalues = eigenvalues[eigenvalues > 1e-10]
    
    # Calculate entropy: -∑ λᵢ log λᵢ
    entropy = -np.sum(eigenvalues * np.log2(eigenvalues))
    
    return entropy

def analyze_von_neumann_entropy(history):
    """
    Analyze the von Neumann entropy of segments of the history.
    
    Lower entropy = more ordered = potential patterns
    Higher entropy = more chaotic = more random
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Split history into segments
    segment_size = 30
    step_size = 15
    
    if len(history) >= segment_size:
        segments = []
        segment_entropies = []
        
        for i in range(0, len(history) - segment_size, step_size):
            segment = history[i:i+segment_size]
            segments.append(segment)
            
            # Create density matrix
            density_matrix = create_density_matrix(segment)
            
            # Calculate entropy
            entropy = calculate_von_neumann_entropy(density_matrix)
            segment_entropies.append((i, entropy))
    
        # Identify low entropy segments (most ordered, potentially predictable)
        low_entropy_segments = sorted(segment_entropies, key=lambda x: x[1])[:3]
        
        # Look for numbers that appear in these ordered segments
        ordered_numbers = []
        for idx, _ in low_entropy_segments:
            ordered_numbers.extend(history[idx:idx+segment_size])
        
        # Count frequencies in ordered regions
        number_counts = defaultdict(int)
        for num in ordered_numbers:
            number_counts[num] += 1
        
        # Score numbers by their frequency in ordered regions
        # Higher frequency in low-entropy regions = higher score
        number_scores = {num: count / len(ordered_numbers) for num, count in number_counts.items()}
        
        # Get top 8 numbers
        sorted_scores = sorted(number_scores.items(), key=lambda x: x[1], reverse=True)
        recommended_numbers = [str(num) if num != 37 else '00' for num, _ in sorted_scores[:8]]
        
        return recommended_numbers
    else:
        # Not enough data for segmentation
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]

def analyze_quantum_decoherence(history):
    """
    Analyze the history for quantum decoherence patterns.
    
    In quantum mechanics, decoherence is the loss of quantum coherence.
    Here we model the process of decoherence to predict potential outcomes.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 30:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # We'll focus on the most recent part of the history
    recent_history = history[-30:]
    
    # Create the initial "quantum state" based on recent frequency
    state = np.zeros(38)
    for num in recent_history:
        state[num] += 1
    
    # Normalize the state
    state = state / np.linalg.norm(state)
    
    # Model decoherence by applying noise and damping
    # This simulates how quantum states lose coherence over time
    decoherence_rates = np.linspace(0.1, 0.9, 5)  # Various decoherence rates
    
    # Store decohered states
    decohered_states = []
    
    for rate in decoherence_rates:
        # Apply decoherence model
        # 1. Add quantum noise
        noise = np.random.normal(0, 0.1, 38)
        noisy_state = state + noise * rate
        
        # 2. Normalize
        noisy_state = noisy_state / np.linalg.norm(noisy_state)
        
        # 3. Damping (collapse towards classical distribution)
        uniform_dist = np.ones(38) / 38
        damped_state = (1 - rate) * noisy_state + rate * uniform_dist
        
        # 4. Normalize again
        damped_state = damped_state / np.linalg.norm(damped_state)
        
        decohered_states.append(damped_state)
    
    # Calculate the average decohered state
    avg_decohered = np.mean(decohered_states, axis=0)
    
    # Get the 8 highest probability numbers from the final decohered state
    top_indices = np.argsort(avg_decohered)[-8:]
    
    # Convert to strings
    recommended_numbers = [str(idx) if idx != 37 else '00' for idx in top_indices]
    
    return recommended_numbers

def analyze_quantum_entanglement(history):
    """
    Analyze the history for quantum entanglement patterns.
    
    This models "entangled" numbers - pairs that show correlated outcomes.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 100:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Calculate the correlation matrix between numbers
    correlation_matrix = np.zeros((38, 38))
    
    # For each number, calculate which numbers tend to appear within
    # a small window after it (modeling quantum correlations)
    window_size = 5
    
    for i in range(len(history) - window_size):
        current = history[i]
        
        # Look at numbers that appear in the window after current
        for j in range(1, window_size + 1):
            if i + j < len(history):
                future = history[i + j]
                
                # Stronger correlation for closer numbers (quantum entanglement decays with distance)
                weight = (window_size - j + 1) / window_size
                correlation_matrix[current, future] += weight
    
    # Normalize to get probabilities - fixing the indexing issue
    for i in range(correlation_matrix.shape[0]):
        row_sum = np.sum(correlation_matrix[i])
        if row_sum > 0:
            correlation_matrix[i] = correlation_matrix[i] / row_sum
    
    # Get the most recent numbers
    recent_nums = history[-3:]
    
    # Calculate "entangled" numbers for each recent number
    entangled_scores = np.zeros(38)
    
    for num in recent_nums:
        # Get correlation vector for this number
        correlations = correlation_matrix[num]
        
        # Add to scores, weighted by recency
        entangled_scores += correlations
    
    # Select top 8 entangled numbers
    top_indices = np.argsort(entangled_scores)[-8:]
    
    # Convert to strings
    recommended_numbers = [str(idx) if idx != 37 else '00' for idx in top_indices]
    
    return recommended_numbers

def analyze_quantum_interference(history):
    """
    Analyze the history for quantum interference patterns.
    
    This models how quantum waves can constructively or destructively interfere,
    creating patterns in the probabilities.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Convert history to a time series of phases
    # Each number corresponds to a phase angle on the wheel
    phases = []
    for num in history:
        # Convert number to a phase angle (0 to 2π)
        phase = (num / 38) * 2 * np.pi
        phases.append(phase)
    
    # Calculate interference pattern across all wheel positions
    positions = np.linspace(0, 2*np.pi, 38, endpoint=False)
    interference_pattern = np.zeros(38)
    
    # Each past outcome contributes a wave that propagates forward
    for phase in phases:
        # Calculate phase difference at each position
        phase_diff = positions - phase
        
        # Apply quantum wave function (simplified as cosine)
        # Recent outcomes have stronger amplitudes (quantum memory effect)
        recency_weight = 0.9  # Decay factor
        
        for i in range(38):
            # Calculate contribution at this position
            contribution = np.cos(phase_diff[i]) * recency_weight
            interference_pattern[i] += contribution
            
            # Decay weight for next outcome (earlier in history)
            recency_weight *= 0.95
    
    # Normalize to get probabilities
    if np.max(np.abs(interference_pattern)) > 0:
        interference_pattern = (interference_pattern - np.min(interference_pattern))
        interference_pattern = interference_pattern / np.sum(interference_pattern)
    
    # Calculate constructive interference points (peaks)
    interference_scores = interference_pattern.copy()
    
    # Get the 8 highest interference scores
    top_indices = np.argsort(interference_scores)[-8:]
    
    # Convert to strings
    recommended_numbers = [str(idx) if idx != 37 else '00' for idx in top_indices]
    
    return recommended_numbers 