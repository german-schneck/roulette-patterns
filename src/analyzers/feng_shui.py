#!/usr/bin/env python3
"""
Feng Shui Harmony Strategy Analyzer

Implementation of a traditional Chinese Feng Shui approach to roulette number selection, 
based on the principles of balance, harmony, and Chinese numerology.
"""

import numpy as np
import random
from collections import defaultdict

def analyze_feng_shui_strategy(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze optimal number selection using traditional Chinese Feng Shui principles.
    
    This strategy incorporates:
    1. Wu Xing (Five Elements): Wood, Fire, Earth, Metal, Water
    2. Yin-Yang balance
    3. Bagua energy mapping
    4. Lucky/unlucky number associations in Chinese culture
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nGenerando combinación con estrategia Feng Shui...")
    
    # Define lucky numbers in Chinese culture
    # 8: Prosperity, 6: Smooth/Flow, 9: Longevity, 2: Balance, 3: Growth
    lucky_numbers = ['8', '6', '9', '2', '3']
    
    # Unlucky numbers in Chinese culture (4 sounds like "death", 7 is associated with ghosts)
    unlucky_numbers = ['4', '7']
    
    # Five Elements (Wu Xing) correspondences - each element mapped to roulette numbers
    five_elements = {
        'wood': ['1', '8', '15', '22', '29', '36'],  # Green/growth
        'fire': ['2', '9', '16', '23', '30'],        # Red/energy
        'earth': ['5', '12', '19', '26', '33'],      # Yellow/stability
        'metal': ['3', '10', '17', '24', '31'],      # White/precision
        'water': ['6', '13', '20', '27', '34']       # Blue/flow
    }
    
    # Yin-Yang classification
    yin_numbers = ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36']  # Even numbers
    yang_numbers = ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35']  # Odd numbers
    
    # Bagua compass sectors (eight sides)
    bagua_sectors = {
        'north': ['0', '2', '14', '35'],
        'northeast': ['17', '5', '23', '4'],
        'east': ['16', '33', '1', '20'],
        'southeast': ['36', '13', '27', '10'],
        'south': ['24', '3', '15', '34'],
        'southwest': ['22', '18', '9', '31'],
        'west': ['6', '21', '11', '30'],
        'northwest': ['19', '8', '12', '29']
    }
    
    # 0/00 represent "void" or "center" in this system
    center = ['0', '00']
    
    # Calculate number rankings based on Feng Shui principles
    feng_shui_ranking = {}
    
    # Function to add points for Feng Shui ranking
    def add_points(number, points):
        if number in feng_shui_ranking:
            feng_shui_ranking[number] += points
        else:
            feng_shui_ranking[number] = points
    
    # Add points based on different criteria
    
    # Lucky/unlucky numbers
    for num in range(37):  # Including 0
        num_str = str(num)
        # Lucky numbers get high points
        if num_str in lucky_numbers:
            add_points(num_str, 5)
        # Unlucky numbers get negative points
        elif num_str in unlucky_numbers:
            add_points(num_str, -5)
        # 8 is especially lucky (sounds like "prosperity")
        if num_str == '8':
            add_points(num_str, 3)
        # 6 is also very auspicious (smooth/flow)
        if num_str == '6':
            add_points(num_str, 2)
    
    # Balance of elements - each element should be represented
    for element, numbers in five_elements.items():
        for num in numbers:
            add_points(num, 2)
    
    # Yin-Yang balance - need both energies
    for num in yin_numbers:
        add_points(num, 1)  # Slightly favor Yin (even) for stability
    for num in yang_numbers:
        add_points(num, 0.8)
    
    # Bagua favorable sectors (traditional auspicious areas)
    auspicious_sectors = ['southeast', 'south', 'east']
    for sector in auspicious_sectors:
        for num in bagua_sectors[sector]:
            add_points(num, 2)
    
    # Center represents balance point
    for num in center:
        add_points(num, 1.5)
    
    # Account for recent history (avoid numbers that appeared too recently)
    recent_history = analyzer.history[-20:]
    recent_frequencies = defaultdict(int)
    for num in recent_history:
        num_str = str(num)
        recent_frequencies[num_str] += 1
    
    # Prefer numbers with balanced recent frequency
    for num_str, freq in recent_frequencies.items():
        if freq == 0:  # Not appeared recently - potential "ripeness"
            add_points(num_str, 1.5)
        elif freq == 1:  # Appeared once - good balance
            add_points(num_str, 1)
        elif freq > 3:  # Appeared too often - potential exhaustion
            add_points(num_str, -2)
    
    # Sort numbers by Feng Shui ranking
    sorted_feng_shui = sorted(feng_shui_ranking.items(), key=lambda x: x[1], reverse=True)
    
    # Create various Feng Shui combinations based on principles
    combinations = []
    
    # 1. Pure Luck: Top lucky numbers
    pure_luck = [num for num, _ in sorted_feng_shui[:8]]
    combinations.append(("Pure Luck", pure_luck))
    
    # 2. Five Elements Balance: One or two from each element
    balanced_elements = []
    for element, numbers in five_elements.items():
        # Sort numbers in this element by ranking
        sorted_element = [num for num in numbers if num in feng_shui_ranking]
        sorted_element.sort(key=lambda x: feng_shui_ranking.get(x, 0), reverse=True)
        balanced_elements.extend(sorted_element[:2])  # Take top 1-2 from each element
    balanced_elements = balanced_elements[:8]  # Limit to 8 numbers
    combinations.append(("Five Elements Balance", balanced_elements))
    
    # 3. Yin-Yang Harmony: Balance of odd/even
    yin_yang_harmony = []
    top_yin = [num for num in sorted_feng_shui if num[0] in yin_numbers][:4]
    top_yang = [num for num in sorted_feng_shui if num[0] in yang_numbers][:4]
    yin_yang_harmony.extend([num[0] for num in top_yin])
    yin_yang_harmony.extend([num[0] for num in top_yang])
    combinations.append(("Yin-Yang Harmony", yin_yang_harmony))
    
    # 4. Bagua Prosperity: Focus on southeast/south wealth areas
    prosperity_numbers = []
    for sector in ['southeast', 'south', 'east']:
        prosperity_numbers.extend(bagua_sectors[sector])
    prosperity_numbers.sort(key=lambda x: feng_shui_ranking.get(x, 0), reverse=True)
    prosperity_numbers = prosperity_numbers[:8]
    combinations.append(("Bagua Prosperity", prosperity_numbers))
    
    # Test each Feng Shui combination
    best_win_rate = 0
    best_combination_name = ""
    best_feng_shui_numbers = []
    
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
            best_feng_shui_numbers = numbers
    
    # If sorted_numbers is provided, enhance our selection
    if sorted_numbers:
        # Create a blend with top numbers from pre-sorted list
        feng_shui_enhanced = []
        
        # Include top 4 lucky numbers from our Feng Shui analysis
        feng_shui_enhanced.extend(best_feng_shui_numbers[:4])
        
        # Add top ranked numbers from sorted_numbers that aren't already included
        for num in sorted_numbers:
            if num not in feng_shui_enhanced and len(feng_shui_enhanced) < 8:
                feng_shui_enhanced.append(num)
        
        # Fill up to 8 if needed
        if len(feng_shui_enhanced) < 8:
            for num, _ in sorted_feng_shui:
                if num not in feng_shui_enhanced and len(feng_shui_enhanced) < 8:
                    feng_shui_enhanced.append(num)
        
        # Validate the enhanced combination
        print("\nValidando combinación Feng Shui mejorada...")
        from src.utils.analysis import validate_numbers_performance
        feng_shui_win_rate = validate_numbers_performance(
            validation_analyzer, feng_shui_enhanced, validation_spins)
        
        feng_shui_coverage = len(feng_shui_enhanced) / 38 * 100
        feng_shui_performance = (feng_shui_win_rate / feng_shui_coverage - 1) * 100
        
        print(f"Combinación Feng Shui final: {', '.join(feng_shui_enhanced)}")
        print(f"Tasa de victoria: {feng_shui_win_rate:.2f}%")
        print(f"Rendimiento: {feng_shui_performance:+.2f}%")
        
        final_numbers = feng_shui_enhanced
        final_win_rate = feng_shui_win_rate
        final_performance = feng_shui_performance
    else:
        final_numbers = best_feng_shui_numbers
        final_win_rate = best_win_rate
        final_performance = (final_win_rate / (len(final_numbers) / 38 * 100) - 1) * 100
    
    # Return results
    return {
        'feng_shui_numbers': final_numbers,
        'feng_shui_win_rate': final_win_rate,
        'feng_shui_performance': final_performance,
        'best_combination_type': best_combination_name
    } 