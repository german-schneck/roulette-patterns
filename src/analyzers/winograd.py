#!/usr/bin/env python3
"""
Winograd Strategy Analyzer

Implementation of Jacobo Winograd's famous betting strategy for roulette,
based on focusing predominantly on the last 15 numbers (22-36) of the roulette wheel.
"""

import numpy as np
import random
from collections import defaultdict
from src.utils.analysis import validate_numbers_performance

def analyze_winograd_strategy(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze optimal number selection using Jacobo Winograd's famous strategy.
    
    This strategy incorporates:
    1. Primary focus on numbers 22-36 (last 15 numbers)
    2. Progressive inclusion of specific lower numbers
    3. Adaptation based on recent performance
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nGenerando combinación con estrategia Winograd...")
    
    # Define the core number ranges according to Winograd's strategy
    core_numbers = [str(i) for i in range(22, 37)]  # 22-36, the core of Winograd's strategy
    
    # Define the additional numbers that Winograd incorporates in different stages
    first_tier_extras = ['0', '3', '7']  # First additional numbers
    second_tier_extras = ['4', '9', '12', '15', '18']  # Second additional numbers
    occasional_extras = ['2', '19', '20', '21']  # Occasional additions
    
    # Calculate hit rates from history to identify which numbers perform best
    recent_spins = min(5000, len(analyzer.history))
    recent_history = analyzer.history[-recent_spins:]
    
    # Count occurrences of each number
    number_hits = defaultdict(int)
    for num in recent_history:
        number_hits[num] += 1
    
    # Calculate hit rates
    hit_rates = {}
    for num_str in (core_numbers + first_tier_extras + second_tier_extras + occasional_extras):
        hit_rates[num_str] = number_hits[num_str] / recent_spins if recent_spins > 0 else 0
    
    # Create different implementations of Winograd's strategy
    combinations = []
    
    # 1. Classic Winograd: Core 22-36 + first tier extras
    classic_winograd = core_numbers + first_tier_extras
    # Since we need exactly 8 numbers for the standard selection, we'll select based on historical performance
    sorted_core = sorted([(num, hit_rates[num]) for num in core_numbers], key=lambda x: x[1], reverse=True)
    sorted_tier1 = sorted([(num, hit_rates[num]) for num in first_tier_extras], key=lambda x: x[1], reverse=True)
    
    classic_selection = [num for num, _ in sorted_core[:5]] + [num for num, _ in sorted_tier1[:3]]
    combinations.append(("Classic Winograd", classic_selection))
    
    # 2. Extended Winograd: Core + first & second tier extras, optimized for performance
    extended_winograd = []
    
    # Start with best performers from core numbers
    extended_winograd.extend([num for num, _ in sorted_core[:4]])
    
    # Add best performers from first tier extras
    sorted_tier1 = sorted([(num, hit_rates[num]) for num in first_tier_extras], key=lambda x: x[1], reverse=True)
    extended_winograd.extend([num for num, _ in sorted_tier1[:2]])
    
    # Add best performers from second tier extras
    sorted_tier2 = sorted([(num, hit_rates[num]) for num in second_tier_extras], key=lambda x: x[1], reverse=True)
    extended_winograd.extend([num for num, _ in sorted_tier2[:2]])
    
    combinations.append(("Extended Winograd", extended_winograd))
    
    # 3. Complete Winograd: Includes all number categories
    complete_winograd = []
    
    # Include best performers from core numbers
    complete_winograd.extend([num for num, _ in sorted_core[:3]])
    
    # Include best performers from first tier extras
    complete_winograd.extend([num for num, _ in sorted_tier1[:2]])
    
    # Include best performers from second tier extras
    complete_winograd.extend([num for num, _ in sorted_tier2[:2]])
    
    # Include top occasional extras
    sorted_occasional = sorted([(num, hit_rates[num]) for num in occasional_extras], key=lambda x: x[1], reverse=True)
    complete_winograd.extend([num for num, _ in sorted_occasional[:1]])
    
    combinations.append(("Complete Winograd", complete_winograd))
    
    # 4. "Golden Section" Winograd: Focus on the geometric center of Winograd's range
    # This is a variation inspired by the golden ratio concept
    golden_section = []
    
    # Identify the central numbers of Winograd's range (around 29)
    central_core = ['27', '28', '29', '30', '31']
    sorted_central = sorted([(num, hit_rates[num]) for num in central_core], key=lambda x: x[1], reverse=True)
    golden_section.extend([num for num, _ in sorted_central[:3]])
    
    # Add some high-performing numbers from the extremes of the core range
    high_core = ['34', '35', '36']
    low_core = ['22', '23', '24']
    sorted_high = sorted([(num, hit_rates[num]) for num in high_core], key=lambda x: x[1], reverse=True)
    sorted_low = sorted([(num, hit_rates[num]) for num in low_core], key=lambda x: x[1], reverse=True)
    golden_section.extend([sorted_high[0][0], sorted_low[0][0]])
    
    # Add best performers from extras
    all_extras = first_tier_extras + second_tier_extras + occasional_extras
    sorted_extras = sorted([(num, hit_rates[num]) for num in all_extras], key=lambda x: x[1], reverse=True)
    golden_section.extend([num for num, _ in sorted_extras[:3]])
    
    combinations.append(("Golden Section", golden_section))
    
    # Test each Winograd combination
    best_win_rate = 0
    best_combination_name = ""
    best_winograd_numbers = []
    
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
            best_winograd_numbers = numbers
    
    # If sorted_numbers is provided, enhance our selection with top performers
    if sorted_numbers:
        # Create a blend with top numbers from pre-sorted list
        winograd_enhanced = []
        
        # Include top 4 numbers from our Winograd analysis
        winograd_enhanced.extend(best_winograd_numbers[:4])
        
        # Add top ranked numbers from sorted_numbers that aren't already included
        for num in sorted_numbers:
            if num not in winograd_enhanced and len(winograd_enhanced) < 8:
                winograd_enhanced.append(num)
        
        # Validate the enhanced combination
        print("\nValidando combinación Winograd mejorada...")
        winograd_win_rate = validate_numbers_performance(
            validation_analyzer, winograd_enhanced, validation_spins)
        
        winograd_coverage = len(winograd_enhanced) / 38 * 100
        winograd_performance = (winograd_win_rate / winograd_coverage - 1) * 100
        
        print(f"Combinación Winograd final: {', '.join(winograd_enhanced)}")
        print(f"Tasa de victoria: {winograd_win_rate:.2f}%")
        print(f"Rendimiento: {winograd_performance:+.2f}%")
        
        final_numbers = winograd_enhanced
        final_win_rate = winograd_win_rate
        final_performance = winograd_performance
    else:
        final_numbers = best_winograd_numbers
        final_win_rate = best_win_rate
        final_performance = (final_win_rate / (len(final_numbers) / 38 * 100) - 1) * 100
    
    # Return results
    return {
        'winograd_numbers': final_numbers,
        'winograd_win_rate': final_win_rate,
        'winograd_performance': final_performance,
        'best_combination_type': best_combination_name
    } 