#!/usr/bin/env python3
"""
Pachinko Progression Strategy Analyzer

Implementation of a Japanese-inspired betting strategy for roulette, 
based on the principles of pachinko gambling machines and cascading probability distributions.
"""

import numpy as np
import random
from collections import defaultdict
import math

def analyze_pachinko_progression(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze optimal number selection using principles inspired by Japanese Pachinko machines.
    
    This strategy incorporates:
    1. Cascading probability distributions based on mechanical principles
    2. Progressive betting patterns adapted from Pachinko gameplay
    3. The concept of 'pins' and 'pathways' that create non-random distributions
    4. Pattern recognition similar to how Pachinko experts track machine behavior
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nGenerando combinación con estrategia Pachinko Progression...")
    
    # The roulette wheel mapped as a Pachinko machine
    # We'll divide the wheel into regions that simulate Pachinko pins and paths
    
    # In Pachinko, the ball has a higher probability of falling into certain pockets
    # based on the arrangement of pins and the physics of the ball's path
    
    # Define regions based on the physical American roulette wheel layout
    # American wheel sequence: 0, 28, 9, 26, 30, 11, 7, 20, 32, 17, 5, 22, 34, 15, 3, 24, 36, 13, 1, 00, 27, 10, 25, 29, 12, 8, 19, 31, 18, 6, 21, 33, 16, 4, 23, 35, 14, 2
    
    # Convert wheel layout to a list if it's not already
    wheel_order = analyzer.wheel_order if hasattr(analyzer, 'wheel_order') else [
        '0', '28', '9', '26', '30', '11', '7', '20', '32', '17', '5', '22', '34', '15', 
        '3', '24', '36', '13', '1', '00', '27', '10', '25', '29', '12', '8', '19', '31', 
        '18', '6', '21', '33', '16', '4', '23', '35', '14', '2'
    ]
    
    # Define Pachinko-like path regions (sectors of the wheel with simulated pin arrangements)
    path_regions = {
        'dense_pins': ['0', '28', '9', '26', '30', '11', '7'], # High resistance area (many pins)
        'medium_pins': ['20', '32', '17', '5', '22', '34', '15'], # Medium resistance
        'spread_pins': ['3', '24', '36', '13', '1', '00'], # More spread out pins
        'fast_path': ['27', '10', '25', '29', '12', '8'], # Path with fewer obstacles
        'bounce_zone': ['19', '31', '18', '6', '21'], # Area with high bounce probability
        'target_pocket': ['33', '16', '4', '23', '35', '14', '2'] # Area where ball tends to settle
    }
    
    # Calculate "deviation factors" based on historical data vs expected probability
    # This simulates how Pachinko machines develop biases over time
    deviation_factors = {}
    recent_spins = min(5000, len(analyzer.history))
    recent_history = analyzer.history[-recent_spins:]
    
    # Count occurrences of each number
    number_counts = defaultdict(int)
    for num in recent_history:
        number_counts[num] += 1
    
    # Calculate deviation from expected probability
    expected_prob = 1.0 / 38  # For American roulette
    for num in wheel_order:
        actual_prob = number_counts[num] / recent_spins if recent_spins > 0 else expected_prob
        deviation_factors[num] = (actual_prob / expected_prob) - 1.0
        
    # Define Pachinko-style cascading patterns
    # In Pachinko, balls follow certain paths more often, creating "cascades"
    
    # Calculate "cascade paths" based on consecutive number patterns
    cascade_patterns = {}
    for i in range(len(recent_history) - 3):
        # Create a 3-number pattern
        pattern = (recent_history[i], recent_history[i+1], recent_history[i+2])
        next_num = recent_history[i+3]
        
        if pattern not in cascade_patterns:
            cascade_patterns[pattern] = defaultdict(int)
        cascade_patterns[pattern][next_num] += 1
    
    # Identify the strongest cascade patterns
    strong_cascades = {}
    for pattern, outcomes in cascade_patterns.items():
        if sum(outcomes.values()) >= 5:  # Only consider patterns that occurred at least 5 times
            # Find the most likely outcome for this pattern
            most_common = max(outcomes.items(), key=lambda x: x[1])
            probability = most_common[1] / sum(outcomes.values())
            if probability >= 0.3:  # 30% or higher probability suggests a non-random cascade
                strong_cascades[pattern] = most_common[0]
    
    # Generate pachinko-inspired number combinations
    combinations = []
    
    # 1. High Density Path: Numbers where the ball encounters more "pins" (higher resistance)
    high_density_numbers = []
    for region in ['dense_pins', 'medium_pins']:
        if region in path_regions:
            # Prioritize numbers with positive deviation (they hit more than expected)
            region_nums = sorted(
                [(num, deviation_factors.get(num, 0)) for num in path_regions[region]], 
                key=lambda x: x[1], 
                reverse=True
            )
            high_density_numbers.extend([num for num, _ in region_nums[:4]])
    
    if len(high_density_numbers) > 8:
        high_density_numbers = high_density_numbers[:8]
    elif len(high_density_numbers) < 8:
        # Fill with other numbers if needed
        remaining = 8 - len(high_density_numbers)
        other_nums = sorted(
            [(num, deviation_factors.get(num, 0)) for num in wheel_order if num not in high_density_numbers],
            key=lambda x: x[1],
            reverse=True
        )
        high_density_numbers.extend([num for num, _ in other_nums[:remaining]])
    
    combinations.append(("High Density Path", high_density_numbers))
    
    # 2. Cascade Pattern: Numbers that often follow in sequences (from strong_cascades)
    cascade_numbers = []
    for pattern, outcome in strong_cascades.items():
        for num in pattern:
            if num not in cascade_numbers and len(cascade_numbers) < 6:
                cascade_numbers.append(num)
        if outcome not in cascade_numbers and len(cascade_numbers) < 7:
            cascade_numbers.append(outcome)
    
    # If we don't have enough strong cascades, add numbers from target_pocket region
    if len(cascade_numbers) < 8 and 'target_pocket' in path_regions:
        pocket_nums = [num for num in path_regions['target_pocket'] if num not in cascade_numbers]
        cascade_numbers.extend(pocket_nums[:8-len(cascade_numbers)])
    
    # Ensure we have exactly 8 numbers
    if len(cascade_numbers) > 8:
        cascade_numbers = cascade_numbers[:8]
    elif len(cascade_numbers) < 8:
        # Fill with numbers that have high deviation factors
        remaining = 8 - len(cascade_numbers)
        high_deviation = sorted(
            [(num, deviation_factors.get(num, 0)) for num in wheel_order if num not in cascade_numbers],
            key=lambda x: x[1],
            reverse=True
        )
        cascade_numbers.extend([num for num, _ in high_deviation[:remaining]])
    
    combinations.append(("Cascade Pattern", cascade_numbers))
    
    # 3. Bounce Zone Strategy: Focus on the bounce_zone and adjacent numbers
    bounce_zone_numbers = []
    if 'bounce_zone' in path_regions:
        bounce_zone_numbers.extend(path_regions['bounce_zone'])
        
        # Find numbers adjacent to bounce zone on the wheel
        for num in path_regions['bounce_zone']:
            idx = wheel_order.index(num)
            adjacent_nums = [
                wheel_order[(idx - 1) % len(wheel_order)],
                wheel_order[(idx + 1) % len(wheel_order)]
            ]
            bounce_zone_numbers.extend([n for n in adjacent_nums if n not in bounce_zone_numbers])
    
    bounce_zone_numbers = bounce_zone_numbers[:8]  # Limit to 8 numbers
    combinations.append(("Bounce Zone Strategy", bounce_zone_numbers))
    
    # 4. Ball Speed Distribution: Simulate how different ball speeds affect landing positions
    # In Pachinko, the initial ball speed affects where it's likely to land
    
    # Define "speed tiers" and their corresponding wheel sections
    fast_ball_section = wheel_order[0:13]  # First third of wheel
    medium_ball_section = wheel_order[13:25]  # Middle section
    slow_ball_section = wheel_order[25:]  # Last section
    
    # Analyze recent results to see which speed tier has been most successful
    fast_count = sum(number_counts[num] for num in fast_ball_section)
    medium_count = sum(number_counts[num] for num in medium_ball_section)
    slow_count = sum(number_counts[num] for num in slow_ball_section)
    
    # Choose the most successful section for our strategy
    best_section = fast_ball_section
    best_count = fast_count
    best_name = "Fast Ball"
    
    if medium_count > best_count:
        best_section = medium_ball_section
        best_count = medium_count
        best_name = "Medium Ball"
        
    if slow_count > best_count:
        best_section = slow_ball_section
        best_name = "Slow Ball"
    
    # Get top 8 numbers from the best section based on deviation factors
    ball_speed_numbers = sorted(
        [(num, deviation_factors.get(num, 0)) for num in best_section],
        key=lambda x: x[1],
        reverse=True
    )
    ball_speed_numbers = [num for num, _ in ball_speed_numbers[:8]]
    combinations.append((f"{best_name} Speed", ball_speed_numbers))
    
    # Test each Pachinko combination
    best_win_rate = 0
    best_combination_name = ""
    best_pachinko_numbers = []
    
    for name, numbers in combinations:
        print(f"\nValidando combinación {name}...")
        win_rate = validation_analyzer.validate_numbers(numbers, validation_spins // 4)
        coverage = len(numbers) / 38 * 100
        performance = (win_rate / coverage - 1) * 100
        
        print(f"Combination: {name}")
        print(f"Numbers: {', '.join(numbers)}")
        print(f"Win rate: {win_rate:.2f}%")
        print(f"Performance vs random: {performance:+.2f}%")
        
        if win_rate > best_win_rate:
            best_win_rate = win_rate
            best_combination_name = name
            best_pachinko_numbers = numbers
    
    # If sorted_numbers is provided, enhance our selection
    if sorted_numbers:
        # Create a blend with top numbers from pre-sorted list
        pachinko_enhanced = []
        
        # Include top 4 numbers from our Pachinko analysis
        pachinko_enhanced.extend(best_pachinko_numbers[:4])
        
        # Add top ranked numbers from sorted_numbers that aren't already included
        for num in sorted_numbers:
            if num not in pachinko_enhanced and len(pachinko_enhanced) < 8:
                pachinko_enhanced.append(num)
        
        # Validate the enhanced combination
        print("\nValidando combinación Pachinko mejorada...")
        from src.utils.analysis import validate_numbers_performance
        pachinko_win_rate = validate_numbers_performance(
            validation_analyzer, pachinko_enhanced, validation_spins)
        
        pachinko_coverage = len(pachinko_enhanced) / 38 * 100
        pachinko_performance = (pachinko_win_rate / pachinko_coverage - 1) * 100
        
        print(f"Combinación Pachinko final: {', '.join(pachinko_enhanced)}")
        print(f"Tasa de victoria: {pachinko_win_rate:.2f}%")
        print(f"Rendimiento: {pachinko_performance:+.2f}%")
        
        final_numbers = pachinko_enhanced
        final_win_rate = pachinko_win_rate
        final_performance = pachinko_performance
    else:
        final_numbers = best_pachinko_numbers
        final_win_rate = best_win_rate
        final_performance = (final_win_rate / (len(final_numbers) / 38 * 100) - 1) * 100
    
    # Return results
    return {
        'pachinko_numbers': final_numbers,
        'pachinko_win_rate': final_win_rate,
        'pachinko_performance': final_performance,
        'best_combination_type': best_combination_name
    } 