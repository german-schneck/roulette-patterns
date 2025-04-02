#!/usr/bin/env python3
"""
Mechanical Bias Analysis Module.

This module analyzes potential physical biases in roulette wheels,
based on techniques used by professional players in Las Vegas casinos.
"""
import numpy as np
from collections import defaultdict


def analyze_mechanical_bias(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze mechanical biases in the roulette wheel to identify numbers with higher probability.
    
    In real casinos, physical imperfections in wheels can cause certain numbers to hit more frequently.
    This simulation models the detection of such biases by statistical analysis.
    
    Args:
        analyzer: The main roulette analyzer instance
        validation_analyzer: Analyzer used for validation
        validation_spins: Number of spins to use for validation
        sorted_numbers: List of numbers sorted by performance (optional)
    
    Returns:
        dict: Results of the mechanical bias analysis including:
            - bias_numbers: List of numbers identified with mechanical bias
            - bias_win_rate: Win rate achieved with these numbers
            - bias_performance: Performance vs expected random outcome
    """
    print("\nAnalyzing mechanical biases in the roulette wheel...")
    
    # In real wheels, biases often occur in specific areas due to:
    # - Slight tilting of the wheel (causing bias in certain sectors)
    # - Loose frets between pockets (causing neighboring numbers to hit more)
    # - Worn ball tracks (causing the ball to drop in specific areas)
    
    # Simulate these physical imperfections by analyzing the history data
    history = analyzer.history[-2000:]  # Use last 2000 spins
    
    # Count occurrences of each number
    number_counts = defaultdict(int)
    for result in history:
        number_counts[result] += 1
    
    # Calculate the expected count for each number in a perfectly balanced wheel
    expected_count = len(history) / 38
    
    # Calculate the deviation from expected for each number
    deviations = {}
    for num, count in number_counts.items():
        deviations[num] = (count - expected_count) / expected_count * 100
    
    # Sort numbers by their deviation (highest positive deviation first)
    sorted_by_deviation = sorted(deviations.items(), key=lambda x: x[1], reverse=True)
    
    # Print top positive deviations (indicating potential bias)
    print("Top numbers showing potential mechanical bias:")
    for num, dev in sorted_by_deviation[:10]:
        print(f"  Number {num}: {dev:+.2f}% from expected")
    
    # Check for pocket neighbor patterns (loose frets)
    wheel_order = analyzer.wheel_order
    neighbor_hit_rates = {}
    
    for i, num in enumerate(wheel_order):
        left_neighbor = wheel_order[(i - 1) % len(wheel_order)]
        right_neighbor = wheel_order[(i + 1) % len(wheel_order)]
        
        # Calculate the ratio of hits between adjacent pockets
        if left_neighbor in number_counts and num in number_counts:
            left_ratio = abs(number_counts[num] - number_counts[left_neighbor]) / expected_count
            neighbor_hit_rates[(left_neighbor, num)] = left_ratio
        
        if right_neighbor in number_counts and num in number_counts:
            right_ratio = abs(number_counts[num] - number_counts[right_neighbor]) / expected_count
            neighbor_hit_rates[(num, right_neighbor)] = right_ratio
    
    # Sort neighbor pairs by highest difference (possible loose fret)
    sorted_neighbors = sorted(neighbor_hit_rates.items(), key=lambda x: x[1], reverse=True)
    
    # Print top neighbor differences
    print("\nPotential loose frets between pockets:")
    for (num1, num2), ratio in sorted_neighbors[:5]:
        print(f"  Between {num1} and {num2}: {ratio:.2f}x expected difference")
    
    # Select bias candidates based on statistical anomalies
    bias_candidates = [num for num, _ in sorted_by_deviation[:15]]
    
    # Add numbers from potential loose fret areas
    for (num1, num2), _ in sorted_neighbors[:5]:
        if num1 not in bias_candidates:
            bias_candidates.append(num1)
        if num2 not in bias_candidates:
            bias_candidates.append(num2)
    
    # If we have sorted performance numbers, prioritize those with bias evidence
    if sorted_numbers and len(sorted_numbers) > 0:
        bias_numbers = []
        # First add numbers that are both in top performers and show bias
        for num in sorted_numbers:
            if num in bias_candidates and len(bias_numbers) < 8:
                bias_numbers.append(num)
        
        # If we don't have enough numbers, add more from bias candidates
        remaining = 8 - len(bias_numbers)
        if remaining > 0:
            for num in bias_candidates:
                if num not in bias_numbers and len(bias_numbers) < 8:
                    bias_numbers.append(num)
    else:
        # Without performance data, use top 8 bias candidates
        bias_numbers = bias_candidates[:8]
    
    # Validate the bias-based selection
    print(f"\nValidating mechanical bias numbers: {bias_numbers}")
    
    # Calculate win rate with these numbers
    wins = 0
    for _ in range(validation_spins):
        result, color = validation_analyzer.spin()  # Desempaquetar tupla correctamente
        if result in bias_numbers:
            wins += 1
    
    bias_win_rate = (wins / validation_spins) * 100
    
    # Calculate performance metrics
    bias_coverage = len(bias_numbers) / 38 * 100
    bias_performance = (bias_win_rate / bias_coverage - 1) * 100
    
    print(f"Mechanical Bias Analysis results:")
    print(f"  Numbers: {bias_numbers}")
    print(f"  Win rate: {bias_win_rate:.2f}%")
    print(f"  Performance vs random: {bias_performance:+.2f}%")
    
    return {
        "bias_numbers": bias_numbers,
        "bias_win_rate": bias_win_rate,
        "bias_performance": bias_performance
    } 