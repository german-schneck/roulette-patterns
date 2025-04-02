#!/usr/bin/env python3
"""
Mexican Progression Analysis Module.

This module implements the Mexican Progression strategy, a modified Martingale system
that is popular in Mexican and Central American casinos.
"""
import numpy as np
from collections import defaultdict


def analyze_mexican_progression(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze optimal number selection using the Mexican Progression strategy.
    
    This variant of the Martingale system uses a complex pattern of repeated numbers
    and modified progression to identify high-probability betting patterns.
    Commonly used in Mexican and Central American casinos.
    
    Args:
        analyzer: The main roulette analyzer instance
        validation_analyzer: Analyzer used for validation
        validation_spins: Number of spins to use for validation
        sorted_numbers: List of numbers sorted by performance (optional)
    
    Returns:
        dict: Results of the Mexican Progression analysis including:
            - progression_numbers: List of numbers identified by the progression system
            - progression_win_rate: Win rate achieved with these numbers
            - progression_performance: Performance vs expected random outcome
    """
    print("\nPerforming Mexican Progression analysis...")
    
    # Get historical spin data
    history = analyzer.history[-3000:]
    
    # In Mexican Progression, repeating numbers and their neighbors are important
    # The strategy focuses on identifying numbers that appear in bunches
    
    # Identify repeating numbers (numbers that hit multiple times in a short window)
    repeat_scores = defaultdict(int)
    
    # Look for repeats in various window sizes (3, 5, 10 spins)
    window_sizes = [3, 5, 10]
    
    for window_size in window_sizes:
        for i in range(len(history) - window_size):
            window = history[i:i+window_size]
            # Count repeats in the window
            counts = defaultdict(int)
            for num in window:
                counts[num] += 1
            
            # Score numbers that appear multiple times
            for num, count in counts.items():
                if count > 1:
                    # More weight to more recent windows and higher repeat counts
                    # The weight decays with window size and increases with proximity to the end
                    recency_factor = 1 + (i / len(history))
                    repeat_scores[num] += count * (1 / window_size) * recency_factor
    
    # Get the wheel configuration
    wheel_order = analyzer.wheel_order
    
    # Calculate neighbor information
    neighbors = {}
    
    for i, num in enumerate(wheel_order):
        # In Mexican Progression, neighbors are defined as 2 numbers on each side
        left_neighbors = [wheel_order[(i - j) % len(wheel_order)] for j in range(1, 3)]
        right_neighbors = [wheel_order[(i + j) % len(wheel_order)] for j in range(1, 3)]
        neighbors[num] = left_neighbors + right_neighbors
    
    # Score numbers based on their repeating neighbors
    neighbor_scores = defaultdict(float)
    for num, neighbor_list in neighbors.items():
        for neighbor in neighbor_list:
            # If a neighbor has a high repeat score, this number gets a bonus
            neighbor_scores[num] += repeat_scores.get(neighbor, 0) * 0.5
    
    # Combine repeat scores and neighbor scores
    combined_scores = {}
    for num in analyzer.numbers:
        combined_scores[num] = repeat_scores.get(num, 0) + neighbor_scores.get(num, 0)
    
    # Calculate the "hot-cold balance" (a key aspect of Mexican Progression)
    # Divide the history into recent and older periods
    recent_history = history[-100:]
    older_history = history[-1000:-100]
    
    recent_counts = defaultdict(int)
    older_counts = defaultdict(int)
    
    for num in recent_history:
        recent_counts[num] += 1
    
    for num in older_history:
        older_counts[num] += 1
    
    # Calculate hot-cold balance score
    hot_cold_scores = {}
    for num in analyzer.numbers:
        recent_rate = recent_counts.get(num, 0) / max(len(recent_history), 1)
        older_rate = older_counts.get(num, 0) / max(len(older_history), 1)
        
        # Mexican Progression favors numbers that are "cooling down" or "heating up"
        # rather than consistently hot or cold
        hot_cold_scores[num] = 1 - abs(recent_rate - older_rate * 1.5)
    
    # Final calculation - combine all scores
    final_scores = {}
    for num in analyzer.numbers:
        # Weighted combination of all factors
        final_scores[num] = (
            combined_scores.get(num, 0) * 0.6 +  # 60% weight to repeat and neighbor patterns
            hot_cold_scores.get(num, 0) * 0.4     # 40% weight to hot-cold balance
        )
    
    # Select top numbers by final score
    top_progression_numbers = sorted(
        final_scores.items(),
        key=lambda x: x[1],
        reverse=True
    )
    
    # If we have sorted performance numbers, incorporate them
    if sorted_numbers and len(sorted_numbers) > 0:
        # Mix top progression numbers with top performers
        progression_numbers = []
        
        # Create a set of top performers for quick lookups
        top_performer_set = set(sorted_numbers[:15])
        
        # First add numbers that appear in both analyses
        for num, _ in top_progression_numbers:
            if num in top_performer_set and len(progression_numbers) < 8:
                progression_numbers.append(num)
        
        # Then add remaining top progression numbers
        for num, _ in top_progression_numbers:
            if num not in progression_numbers and len(progression_numbers) < 8:
                progression_numbers.append(num)
    else:
        # Without performance data, use top 8 numbers by progression score
        progression_numbers = [num for num, _ in top_progression_numbers[:8]]
    
    # Validate the Mexican Progression selection
    print(f"\nValidating Mexican Progression numbers: {progression_numbers}")
    
    # Calculate win rate with these numbers
    wins = 0
    for _ in range(validation_spins):
        result, color = validation_analyzer.spin()  # Desempaquetar tupla correctamente
        if result in progression_numbers:
            wins += 1
    
    progression_win_rate = (wins / validation_spins) * 100
    
    # Calculate performance metrics
    progression_coverage = len(progression_numbers) / 38 * 100
    progression_performance = (progression_win_rate / progression_coverage - 1) * 100
    
    print(f"Mexican Progression Analysis results:")
    print(f"  Numbers: {progression_numbers}")
    print(f"  Win rate: {progression_win_rate:.2f}%")
    print(f"  Performance vs random: {progression_performance:+.2f}%")
    
    return {
        "progression_numbers": progression_numbers,
        "progression_win_rate": progression_win_rate,
        "progression_performance": progression_performance
    } 