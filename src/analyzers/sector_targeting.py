#!/usr/bin/env python3
"""
Sector Targeting Analysis Module.

This module implements the sector targeting strategy used by professional
players in Las Vegas casinos to focus on advantageous sectors of the wheel.
"""
import numpy as np
from collections import defaultdict
from src.utils.analysis import validate_numbers_performance

def analyze_sector_targeting(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Implement sector targeting strategy to identify high-probability wheel sections.
    
    Sector targeting is a strategic approach where players identify and focus on specific
    sections of the wheel that have shown to yield better results over time. This is often
    combined with other techniques to increase effectiveness.
    
    Args:
        analyzer: The main roulette analyzer instance
        validation_analyzer: Analyzer used for validation
        validation_spins: Number of spins to use for validation
        sorted_numbers: List of numbers sorted by performance (optional)
    
    Returns:
        dict: Results of the sector targeting analysis including:
            - sector_numbers: List of numbers from the identified target sectors
            - sector_win_rate: Win rate achieved with these numbers
            - sector_performance: Performance vs expected random outcome
    """
    print("\nPerforming sector targeting analysis...")
    
    # Get the wheel configuration
    wheel_order = analyzer.wheel_order
    wheel_size = len(wheel_order)
    
    # In real sector targeting, professionals identify sectors of the wheel that:
    # 1. Have historically performed better than random
    # 2. Contain favorable number distributions (e.g., mix of high/low, even/odd)
    # 3. May have physical advantages due to wheel construction
    
    # Define sector sizes to analyze (sectors of varying sizes)
    sector_sizes = [6, 8, 10]
    
    # Get historical spin data
    history = analyzer.history[-3000:]
    
    # Track performance of each possible sector
    sector_performance = {}
    
    # Evaluate all possible sectors of each size
    for size in sector_sizes:
        for start_position in range(wheel_size):
            # Define the sector
            sector = [wheel_order[(start_position + i) % wheel_size] for i in range(size)]
            
            # Count hits in this sector
            hits = sum(1 for spin in history if spin in sector)
            hit_rate = hits / len(history) * 100
            
            # Calculate the expected hit rate for random distribution
            expected_hit_rate = size / wheel_size * 100
            
            # Calculate performance against random expectation
            performance = (hit_rate / expected_hit_rate - 1) * 100
            
            # Store the sector and its performance
            sector_performance[tuple(sector)] = {
                'hit_rate': hit_rate,
                'expected_hit_rate': expected_hit_rate,
                'performance': performance,
                'size': size
            }
    
    # Sort sectors by performance
    sorted_sectors = sorted(
        sector_performance.items(),
        key=lambda x: x[1]['performance'],
        reverse=True
    )
    
    # Print top performing sectors
    print("Top performing wheel sectors:")
    for i, (sector, stats) in enumerate(sorted_sectors[:3]):
        print(f"  Sector {i+1}: {list(sector)}")
        print(f"    Hit rate: {stats['hit_rate']:.2f}% (Expected: {stats['expected_hit_rate']:.2f}%)")
        print(f"    Performance: {stats['performance']:+.2f}%")
    
    # Select the best performing sector as our base
    best_sector = sorted_sectors[0][0]
    
    # Select numbers for betting
    # We'll combine the best sector with top performing individual numbers if available
    if sorted_numbers and len(sorted_numbers) > 0:
        # Start with numbers that are both in the best sector and among top performers
        sector_numbers = []
        for num in sorted_numbers:
            if num in best_sector and len(sector_numbers) < 8:
                sector_numbers.append(num)
        
        # If we don't have enough numbers, add more from the sector
        remaining = 8 - len(sector_numbers)
        if remaining > 0:
            for num in best_sector:
                if num not in sector_numbers and len(sector_numbers) < 8:
                    sector_numbers.append(num)
        
        # If we still don't have enough, add top performing numbers not in the sector
        remaining = 8 - len(sector_numbers)
        if remaining > 0:
            for num in sorted_numbers:
                if num not in sector_numbers and len(sector_numbers) < 8:
                    sector_numbers.append(num)
    else:
        # Without performance data, just use the best sector numbers
        # If the sector has more than 8 numbers, take the first 8
        sector_numbers = list(best_sector)[:8]
    
    # Validate the sector targeting strategy
    print(f"\nValidating sector targeting numbers: {sector_numbers}")
    
    # Calculate win rate with these numbers
    wins = 0
    for _ in range(validation_spins):
        result, color = validation_analyzer.spin()  # Desempaquetar tupla correctamente
        if result in sector_numbers:
            wins += 1
    
    sector_win_rate = (wins / validation_spins) * 100
    
    # Calculate performance metrics
    sector_coverage = len(sector_numbers) / 38 * 100
    sector_performance = (sector_win_rate / sector_coverage - 1) * 100
    
    print(f"Sector Targeting Analysis results:")
    print(f"  Numbers: {sector_numbers}")
    print(f"  Win rate: {sector_win_rate:.2f}%")
    print(f"  Performance vs random: {sector_performance:+.2f}%")
    
    return {
        "sector_numbers": sector_numbers,
        "sector_win_rate": sector_win_rate,
        "sector_performance": sector_performance
    } 