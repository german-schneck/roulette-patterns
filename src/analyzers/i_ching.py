#!/usr/bin/env python3
"""
I Ching Oracle System Analyzer

Implementation of an ancient Chinese divination methodology for roulette number selection,
based on the 64 hexagrams of the I Ching (Book of Changes).
"""

import numpy as np
import random
from collections import defaultdict
from src.utils.analysis import validate_numbers_performance

def analyze_i_ching_oracle(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze optimal number selection using the I Ching (Book of Changes) divination system.
    
    This strategy incorporates:
    1. Hexagram mapping: Correlating roulette numbers with the 64 I Ching hexagrams
    2. Trigram associations: Eight basic trigrams associated with directions and elements
    3. Changing lines: Dynamic transitions between hexagrams
    4. Auspicious/inauspicious hexagrams based on traditional I Ching meanings
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nGenerando combinación con estrategia I Ching Oracle...")
    
    # Define the eight basic trigrams (Ba Gua)
    trigrams = {
        'qian': {'element': 'heaven', 'direction': 'northwest', 'numbers': ['1', '14', '34']},
        'kun': {'element': 'earth', 'direction': 'southwest', 'numbers': ['2', '19', '29']},
        'zhen': {'element': 'thunder', 'direction': 'east', 'numbers': ['3', '16', '25']},
        'gen': {'element': 'mountain', 'direction': 'northeast', 'numbers': ['8', '23', '32']},
        'kan': {'element': 'water', 'direction': 'north', 'numbers': ['6', '27', '36']},
        'li': {'element': 'fire', 'direction': 'south', 'numbers': ['9', '18', '30']},
        'xun': {'element': 'wind', 'direction': 'southeast', 'numbers': ['4', '17', '33']},
        'dui': {'element': 'lake', 'direction': 'west', 'numbers': ['7', '22', '31']}
    }
    
    # Map remaining numbers to the trigrams
    all_numbers = [str(i) for i in range(37)] + ['00']
    mapped_numbers = [num for trigram in trigrams.values() for num in trigram['numbers']]
    unmapped_numbers = [num for num in all_numbers if num not in mapped_numbers]
    
    # Distribute remaining numbers among trigrams
    for i, num in enumerate(unmapped_numbers):
        trigram_key = list(trigrams.keys())[i % len(trigrams)]
        trigrams[trigram_key]['numbers'].append(num)
    
    # Define auspicious hexagrams (traditionally favorable in I Ching)
    auspicious_hexagrams = {
        'hex_1': {'name': 'qian_qian', 'meaning': 'Creative Heaven', 'numbers': []},  # Heaven over Heaven
        'hex_16': {'name': 'kun_zhen', 'meaning': 'Enthusiasm', 'numbers': []},       # Thunder over Earth
        'hex_11': {'name': 'qian_kun', 'meaning': 'Peace', 'numbers': []},            # Heaven over Earth
        'hex_14': {'name': 'li_qian', 'meaning': 'Great Possession', 'numbers': []},  # Fire over Heaven
        'hex_34': {'name': 'zhen_qian', 'meaning': 'Great Power', 'numbers': []},     # Thunder over Heaven
        'hex_9': {'name': 'xun_qian', 'meaning': 'Small Accumulation', 'numbers': []} # Wind over Heaven
    }
    
    # Map numbers to hexagrams
    for hex_name, hex_data in auspicious_hexagrams.items():
        # Extract the trigram names from the hexagram name
        try:
            lower_trigram, upper_trigram = hex_data['name'].split('_')
            # Combine numbers from both trigrams with some selection logic
            if lower_trigram in trigrams and upper_trigram in trigrams:
                lower_nums = trigrams[lower_trigram]['numbers']
                upper_nums = trigrams[upper_trigram]['numbers']
                
                # Select a few numbers from each trigram to form the hexagram numbers
                hex_data['numbers'] = lower_nums[:2] + upper_nums[:2]
        except ValueError:
            # Fallback if the hexagram name is not in the expected format
            hex_data['numbers'] = random.sample(all_numbers, 4)
    
    # Generate combinations based on I Ching principles
    combinations = []
    
    # 1. Heaven's Prosperity: Focus on numbers from the most auspicious hexagrams
    heaven_prosperity = []
    for hex_data in auspicious_hexagrams.values():
        heaven_prosperity.extend(hex_data['numbers'][:2])  # Take 2 numbers from each auspicious hexagram
    heaven_prosperity = list(dict.fromkeys(heaven_prosperity))[:8]  # Remove duplicates and limit to 8
    combinations.append(("Heaven's Prosperity", heaven_prosperity))
    
    # 2. Five Elements Balance: Select numbers from trigrams representing the five elements
    # Map trigrams to the five elements (Wu Xing)
    element_mapping = {
        'metal': ['qian', 'dui'],  # Heaven and Lake
        'water': ['kan'],          # Water
        'wood': ['zhen', 'xun'],   # Thunder and Wind
        'fire': ['li'],            # Fire
        'earth': ['kun', 'gen']    # Earth and Mountain
    }
    
    five_elements_balance = []
    for element, trigram_list in element_mapping.items():
        element_numbers = []
        for trigram_name in trigram_list:
            if trigram_name in trigrams:
                element_numbers.extend(trigrams[trigram_name]['numbers'])
        
        # Take 1-2 numbers from each element
        if element_numbers:
            count = 2 if element == 'metal' or element == 'wood' else 1  # More numbers from metal and wood
            five_elements_balance.extend(element_numbers[:count])
    
    five_elements_balance = list(dict.fromkeys(five_elements_balance))[:8]  # Remove duplicates and limit to 8
    combinations.append(("Five Elements Balance", five_elements_balance))
    
    # 3. Changing Lines: Represent dynamic transitions in the I Ching
    # Analyze recent history to identify potential changing lines
    recent_history = analyzer.history[-30:]
    transitions = defaultdict(int)
    
    for i in range(len(recent_history) - 1):
        from_num = recent_history[i]
        to_num = recent_history[i + 1]
        transitions[(from_num, to_num)] += 1
    
    # Find the most frequent transitions
    sorted_transitions = sorted(transitions.items(), key=lambda x: x[1], reverse=True)
    changing_lines = []
    
    # Add both numbers from top transitions
    for (from_num, to_num), _ in sorted_transitions[:4]:
        if from_num not in changing_lines and len(changing_lines) < 8:
            changing_lines.append(from_num)
        if to_num not in changing_lines and len(changing_lines) < 8:
            changing_lines.append(to_num)
    
    # Fill with other numbers if needed
    all_nums_in_transitions = list(set([num for (from_num, to_num), _ in sorted_transitions for num in [from_num, to_num]]))
    for num in all_nums_in_transitions:
        if num not in changing_lines and len(changing_lines) < 8:
            changing_lines.append(num)
    
    combinations.append(("Changing Lines", changing_lines))
    
    # 4. Cardinal Directions: Based on the traditional association of trigrams with directions
    cardinal_directions = {
        'north': trigrams['kan']['numbers'],
        'south': trigrams['li']['numbers'],
        'east': trigrams['zhen']['numbers'],
        'west': trigrams['dui']['numbers'],
        'northeast': trigrams['gen']['numbers'],
        'southeast': trigrams['xun']['numbers'],
        'southwest': trigrams['kun']['numbers'],
        'northwest': trigrams['qian']['numbers']
    }
    
    # Select numbers from auspicious directions (traditional: south, east, southeast)
    auspicious_directions = []
    for direction in ['south', 'east', 'southeast']:
        auspicious_directions.extend(cardinal_directions[direction][:2])  # Take 2 numbers from each direction
    
    # Add a few from northwest (heaven) for balance
    auspicious_directions.extend(cardinal_directions['northwest'][:2])
    
    auspicious_directions = list(dict.fromkeys(auspicious_directions))[:8]  # Remove duplicates and limit to 8
    combinations.append(("Auspicious Directions", auspicious_directions))
    
    # Test each I Ching combination
    best_win_rate = 0
    best_combination_name = ""
    best_i_ching_numbers = []
    
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
            best_i_ching_numbers = numbers
    
    # If sorted_numbers is provided, enhance our selection
    if sorted_numbers:
        # Create a blend with top numbers from pre-sorted list
        i_ching_enhanced = []
        
        # Include top 4 numbers from our I Ching analysis
        i_ching_enhanced.extend(best_i_ching_numbers[:4])
        
        # Add top ranked numbers from sorted_numbers that aren't already included
        for num in sorted_numbers:
            if num not in i_ching_enhanced and len(i_ching_enhanced) < 8:
                i_ching_enhanced.append(num)
        
        # Validate the enhanced combination
        print("\nValidando combinación I Ching mejorada...")
        i_ching_win_rate = validate_numbers_performance(
            validation_analyzer, i_ching_enhanced, validation_spins)
        
        i_ching_coverage = len(i_ching_enhanced) / 38 * 100
        i_ching_performance = (i_ching_win_rate / i_ching_coverage - 1) * 100
        
        print(f"Combinación I Ching final: {', '.join(i_ching_enhanced)}")
        print(f"Tasa de victoria: {i_ching_win_rate:.2f}%")
        print(f"Rendimiento: {i_ching_performance:+.2f}%")
        
        final_numbers = i_ching_enhanced
        final_win_rate = i_ching_win_rate
        final_performance = i_ching_performance
    else:
        final_numbers = best_i_ching_numbers
        final_win_rate = best_win_rate
        final_performance = (final_win_rate / (len(final_numbers) / 38 * 100) - 1) * 100
    
    # Return results
    return {
        'i_ching_numbers': final_numbers,
        'i_ching_win_rate': final_win_rate,
        'i_ching_performance': final_performance,
        'best_combination_type': best_combination_name
    }

# Create an alias for the function to match the import in __init__.py
analyze_i_ching_strategy = analyze_i_ching_oracle 