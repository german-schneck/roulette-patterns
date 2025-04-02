#!/usr/bin/env python3
"""
Golden Ratio Strategy Analyzer

Implementation of a strategy that applies the golden ratio and Fibonacci sequences
to identify natural patterns and harmonics in roulette outcomes.
"""

import numpy as np
from collections import defaultdict
import math
from src.utils.analysis import validate_numbers_performance

def analyze_golden_ratio(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze optimal number selection using golden ratio principles.
    
    This strategy incorporates:
    1. Fibonacci sequence analysis for number selection
    2. Golden spiral mapping on the roulette wheel
    3. Golden section analysis for revealing natural patterns
    4. Golden angle adjacency analysis
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nGenerando combinación con estrategia Golden Ratio (Proporción Áurea)...")
    
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
    
    # Generate different golden ratio-based combinations
    combinations = []
    
    # 1. Fibonacci Sequence Analysis
    fibonacci_numbers = analyze_fibonacci_sequence(numeric_history)
    combinations.append(("Fibonacci Sequence", fibonacci_numbers))
    
    # 2. Golden Spiral Mapping
    spiral_numbers = analyze_golden_spiral(numeric_history)
    combinations.append(("Golden Spiral", spiral_numbers))
    
    # 3. Golden Section Analysis
    section_numbers = analyze_golden_section(numeric_history)
    combinations.append(("Golden Section", section_numbers))
    
    # 4. Golden Angle Analysis
    angle_numbers = analyze_golden_angle(numeric_history)
    combinations.append(("Golden Angle", angle_numbers))
    
    # Test each golden ratio-based combination
    best_win_rate = 0
    best_combination_name = ""
    best_golden_numbers = []
    
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
            best_golden_numbers = numbers
    
    # If sorted_numbers is provided, enhance our selection with top performers
    if sorted_numbers:
        # Create a blend with top numbers from pre-sorted list
        golden_enhanced = []
        
        # Include top 4 numbers from our Golden Ratio analysis
        golden_enhanced.extend(best_golden_numbers[:4])
        
        # Add top ranked numbers from sorted_numbers that aren't already included
        for num in sorted_numbers:
            if num not in golden_enhanced and len(golden_enhanced) < 8:
                golden_enhanced.append(num)
        
        # Validate the enhanced combination
        print("\nValidando combinación Golden Ratio mejorada...")
        golden_win_rate = validate_numbers_performance(
            validation_analyzer, golden_enhanced, validation_spins)
        
        golden_coverage = len(golden_enhanced) / 38 * 100
        golden_performance = (golden_win_rate / golden_coverage - 1) * 100
        
        print(f"Combinación Golden Ratio final: {', '.join(golden_enhanced)}")
        print(f"Tasa de victoria: {golden_win_rate:.2f}%")
        print(f"Rendimiento: {golden_performance:+.2f}%")
        
        final_numbers = golden_enhanced
        final_win_rate = golden_win_rate
        final_performance = golden_performance
    else:
        final_numbers = best_golden_numbers
        final_win_rate = best_win_rate
        final_performance = (final_win_rate / (len(final_numbers) / 38 * 100) - 1) * 100
    
    # Return results
    return {
        'golden_ratio_numbers': final_numbers,
        'golden_ratio_win_rate': final_win_rate,
        'golden_ratio_performance': final_performance,
        'best_combination_type': best_combination_name
    }

def analyze_fibonacci_sequence(history):
    """
    Analyze the history for Fibonacci sequence patterns.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Generate Fibonacci sequence up to 38 (roulette wheel size)
    fibonacci = [1, 1]
    while fibonacci[-1] + fibonacci[-2] < 38:
        fibonacci.append(fibonacci[-1] + fibonacci[-2])
    
    # Map to roulette numbers (0-37)
    fibonacci_numbers = [f % 38 for f in fibonacci]
    
    # Calculate occurrence frequencies of each number in the history
    frequencies = defaultdict(int)
    for num in history:
        frequencies[num] += 1
    
    # Calculate occurrence rate of each Fibonacci number
    fibonacci_rates = {}
    for num in fibonacci_numbers:
        rate = frequencies.get(num, 0) / len(history)
        fibonacci_rates[num] = rate
    
    # Compare with expected rate (uniform distribution)
    expected_rate = 1 / 38
    fibonacci_performance = {
        num: (rate / expected_rate - 1) * 100 
        for num, rate in fibonacci_rates.items()
    }
    
    # Select top performing Fibonacci numbers
    sorted_performance = sorted(fibonacci_performance.items(), key=lambda x: x[1], reverse=True)
    top_fibonacci = [num for num, _ in sorted_performance[:4]]
    
    # Analyze differences between consecutive numbers in history
    differences = []
    for i in range(1, len(history)):
        diff = abs(history[i] - history[i-1])
        differences.append(diff)
    
    # Count frequencies of Fibonacci differences
    fibonacci_diff_count = defaultdict(int)
    for diff in differences:
        if diff in fibonacci:
            fibonacci_diff_count[diff] += 1
    
    # Calculate which numbers would be next based on recent Fibonacci differences
    recent_num = history[-1]
    predicted_next = []
    
    # Sort Fibonacci differences by frequency
    sorted_diff = sorted(fibonacci_diff_count.items(), key=lambda x: x[1], reverse=True)
    
    for diff, _ in sorted_diff[:3]:
        # Both adding and subtracting the difference
        predicted_up = (recent_num + diff) % 38
        predicted_down = (recent_num - diff) % 38
        
        if predicted_up not in predicted_next:
            predicted_next.append(predicted_up)
        if predicted_down not in predicted_next:
            predicted_next.append(predicted_down)
    
    # Combine top Fibonacci numbers and predicted next numbers
    recommended_numbers = []
    
    for num in top_fibonacci:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers:
            recommended_numbers.append(num_str)
    
    for num in predicted_next:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num_str)
    
    # Ensure we have 8 numbers
    # Add remaining Fibonacci numbers if needed
    for num in fibonacci_numbers:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num_str)
    
    # If still needed, add default numbers
    defaults = [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    for num in defaults:
        if num not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num)
    
    return recommended_numbers[:8]

def analyze_golden_spiral(history):
    """
    Analyze the history using a golden spiral mapping on the roulette wheel.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Get the wheel layout for an American roulette wheel
    wheel_layout = get_default_wheel_layout()
    
    # Convert to numerical representation
    numeric_layout = []
    for num in wheel_layout:
        if num == '00':
            numeric_layout.append(37)
        else:
            numeric_layout.append(int(num))
    
    # Generate golden spiral points on the wheel
    # The golden spiral grows by a factor of phi (golden ratio) with each quarter turn
    phi = (1 + math.sqrt(5)) / 2
    
    # Map wheel positions to angles (0 to 2π)
    angles = [2 * math.pi * i / len(numeric_layout) for i in range(len(numeric_layout))]
    
    # Generate spiral points
    spiral_points = []
    for i in range(8):  # Generate 8 points on the spiral
        # Calculate radius and angle
        radius = phi ** (i / 2)
        angle = i * math.pi / 2  # Quarter turns
        
        # Find the closest wheel position
        closest_idx = min(range(len(angles)), key=lambda j: abs(angles[j] - (angle % (2 * math.pi))))
        spiral_points.append(numeric_layout[closest_idx])
    
    # Analyze frequencies of numbers on the golden spiral
    frequencies = defaultdict(int)
    for num in history:
        frequencies[num] += 1
    
    # Calculate hit rates for spiral points
    spiral_rates = {}
    for num in spiral_points:
        rate = frequencies.get(num, 0) / len(history)
        spiral_rates[num] = rate
    
    # Compare with expected rate
    expected_rate = 1 / 38
    spiral_performance = {
        num: (rate / expected_rate - 1) * 100 
        for num, rate in spiral_rates.items()
    }
    
    # Select top performing spiral points
    sorted_performance = sorted(spiral_performance.items(), key=lambda x: x[1], reverse=True)
    top_spiral = [num for num, _ in sorted_performance[:4]]
    
    # Also check if recent history follows a spiral pattern
    spiral_matches = 0
    for i in range(min(5, len(history))):
        if history[-(i+1)] in spiral_points:
            spiral_matches += 1
    
    spiral_continuation = []
    if spiral_matches >= 2:  # If we have multiple matches to the spiral pattern
        # Find the last matching point
        last_match_idx = -1
        for i in range(len(history)):
            if history[-(i+1)] in spiral_points:
                last_match_idx = spiral_points.index(history[-(i+1)])
                break
        
        if last_match_idx != -1:
            # Predict next spiral points
            for i in range(1, 4):
                next_idx = (last_match_idx + i) % len(spiral_points)
                spiral_continuation.append(spiral_points[next_idx])
    
    # Combine top spiral numbers and continuation predictions
    recommended_numbers = []
    
    for num in top_spiral:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers:
            recommended_numbers.append(num_str)
    
    for num in spiral_continuation:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num_str)
    
    # Ensure we have 8 numbers
    # Add remaining spiral points if needed
    for num in spiral_points:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num_str)
    
    # If still needed, add default numbers
    defaults = [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    for num in defaults:
        if num not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num)
    
    return recommended_numbers[:8]

def analyze_golden_section(history):
    """
    Analyze the history using golden section principles.
    
    The golden section divides a line so that the ratio of the whole to the larger part
    equals the ratio of the larger part to the smaller part (approx 1.618:1).
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # The golden ratio
    phi = (1 + math.sqrt(5)) / 2  # Approximately 1.618
    
    # Create golden sections of the roulette wheel (0-37)
    sections = []
    
    # Divide the wheel into golden sections
    section_size = 38 / phi
    current_pos = 0
    
    while current_pos < 38:
        end_pos = min(38, current_pos + section_size)
        sections.append((int(current_pos), int(end_pos)))
        current_pos = end_pos
    
    # Count frequencies in each section
    section_frequencies = defaultdict(int)
    
    for num in history:
        for i, (start, end) in enumerate(sections):
            if start <= num < end:
                section_frequencies[i] += 1
                break
    
    # Identify sections with higher frequencies
    total_spins = len(history)
    section_rates = {section: count / total_spins for section, count in section_frequencies.items()}
    
    # Expected rate assuming uniform distribution
    expected_section_rates = {i: (end - start) / 38 for i, (start, end) in enumerate(sections)}
    
    # Calculate performance vs expected
    section_performance = {
        section: (rate / expected_section_rates.get(section, 1)) - 1 
        for section, rate in section_rates.items()
    }
    
    # Select top performing sections
    sorted_sections = sorted(section_performance.items(), key=lambda x: x[1], reverse=True)
    top_sections = [sections[section] for section, _ in sorted_sections[:2]]
    
    # Get all numbers in these sections
    section_numbers = []
    for start, end in top_sections:
        section_numbers.extend(range(start, end))
    
    # Analyze recent history to see if we're following a pattern of movement between sections
    recent_sections = []
    for num in history[-10:]:
        for i, (start, end) in enumerate(sections):
            if start <= num < end:
                recent_sections.append(i)
                break
    
    # Look for patterns in section transitions
    transitions = defaultdict(lambda: defaultdict(int))
    for i in range(len(recent_sections) - 1):
        from_section = recent_sections[i]
        to_section = recent_sections[i + 1]
        transitions[from_section][to_section] += 1
    
    # Predict next section based on recent transitions
    predicted_section = None
    if recent_sections:
        last_section = recent_sections[-1]
        if last_section in transitions:
            # Find most common transition
            sorted_transitions = sorted(transitions[last_section].items(), key=lambda x: x[1], reverse=True)
            if sorted_transitions:
                predicted_section = sorted_transitions[0][0]
    
    # Get numbers from predicted section
    predicted_numbers = []
    if predicted_section is not None:
        start, end = sections[predicted_section]
        predicted_numbers = list(range(start, end))
    
    # Also find numbers that appear at golden ratio positions in the history
    golden_position_numbers = []
    
    # Look at positions that are at golden ratio intervals from the end
    for i in range(1, 5):
        position = -int(i * phi)
        if abs(position) < len(history):
            golden_position_numbers.append(history[position])
    
    # Combine all analyses
    recommended_numbers = []
    
    # First add golden position numbers (highest priority)
    for num in golden_position_numbers:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num_str)
    
    # Then add numbers from predicted section
    for num in predicted_numbers:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num_str)
    
    # Then add numbers from top performing sections
    for num in section_numbers:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num_str)
    
    # Ensure we have 8 numbers
    defaults = [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    for num in defaults:
        if num not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num)
    
    return recommended_numbers[:8]

def analyze_golden_angle(history):
    """
    Analyze the history using golden angle principles.
    
    The golden angle is 2π/φ² or about 137.5 degrees, which creates
    the most optimal packing of elements in a circle (as seen in sunflower seeds).
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # The golden ratio
    phi = (1 + math.sqrt(5)) / 2
    
    # The golden angle in radians
    golden_angle = 2 * math.pi - 2 * math.pi / (phi * phi)  # Approximately 2.4 radians or 137.5 degrees
    
    # Get the wheel layout for an American roulette wheel
    wheel_layout = get_default_wheel_layout()
    
    # Convert to numerical representation
    numeric_layout = []
    for num in wheel_layout:
        if num == '00':
            numeric_layout.append(37)
        else:
            numeric_layout.append(int(num))
    
    # Map wheel positions to angles (0 to 2π)
    angles = [2 * math.pi * i / len(numeric_layout) for i in range(len(numeric_layout))]
    
    # For each number on the wheel, find the numbers at golden angle intervals
    golden_neighbors = {}
    for i, num in enumerate(numeric_layout):
        angle = angles[i]
        
        # Find numbers at +/- golden angle
        plus_angle = (angle + golden_angle) % (2 * math.pi)
        minus_angle = (angle - golden_angle) % (2 * math.pi)
        
        # Find closest wheel positions
        plus_idx = min(range(len(angles)), key=lambda j: abs(angles[j] - plus_angle))
        minus_idx = min(range(len(angles)), key=lambda j: abs(angles[j] - minus_angle))
        
        golden_neighbors[num] = [numeric_layout[plus_idx], numeric_layout[minus_idx]]
    
    # Analyze how often golden angle adjacencies appear in history
    adjacency_count = 0
    for i in range(1, len(history)):
        prev = history[i-1]
        curr = history[i]
        
        if prev in golden_neighbors and curr in golden_neighbors[prev]:
            adjacency_count += 1
    
    # Calculate adjacency rate
    adjacency_rate = adjacency_count / (len(history) - 1) if len(history) > 1 else 0
    
    # Expected rate with random selection would be 2/37 (two golden neighbors out of 37 possible next numbers)
    expected_rate = 2 / 37
    
    # Determine if golden angle adjacencies are significant
    is_significant = adjacency_rate > expected_rate * 1.2  # 20% above expected
    
    # If significant, predict based on golden angle from recent numbers
    recommended_numbers = []
    
    if is_significant and history:
        # Get the most recent numbers
        recent_numbers = history[-3:]
        
        # Find their golden neighbors
        recent_neighbors = []
        for num in recent_numbers:
            if num in golden_neighbors:
                recent_neighbors.extend(golden_neighbors[num])
        
        # Count frequencies of neighbors
        neighbor_freq = defaultdict(int)
        for num in recent_neighbors:
            neighbor_freq[num] += 1
        
        # Get top frequent neighbors
        sorted_neighbors = sorted(neighbor_freq.items(), key=lambda x: x[1], reverse=True)
        
        for num, _ in sorted_neighbors:
            num_str = str(num) if num != 37 else '00'
            if num_str not in recommended_numbers and len(recommended_numbers) < 8:
                recommended_numbers.append(num_str)
    
    # If not significant or not enough recommendations, use another approach
    if len(recommended_numbers) < 4:
        # Generate numbers using golden angle iteration
        # This creates an optimal distribution of points around a circle
        optimal_points = []
        current_angle = 0
        
        for _ in range(8):
            # Convert angle to wheel position
            position = (current_angle / (2 * math.pi)) * len(numeric_layout)
            wheel_idx = int(position) % len(numeric_layout)
            optimal_points.append(numeric_layout[wheel_idx])
            
            # Increment by golden angle
            current_angle = (current_angle + golden_angle) % (2 * math.pi)
        
        # Add these points to recommendations
        for num in optimal_points:
            num_str = str(num) if num != 37 else '00'
            if num_str not in recommended_numbers and len(recommended_numbers) < 8:
                recommended_numbers.append(num_str)
    
    # Ensure we have 8 numbers
    defaults = [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    for num in defaults:
        if num not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num)
    
    return recommended_numbers[:8]

def get_default_wheel_layout():
    """
    Returns the default American roulette wheel layout.
    
    Returns:
        list: Wheel layout in order
    """
    return [
        '0', '28', '9', '26', '30', '11', '7', '20', '32', '17', '5', '22', '34', '15', 
        '3', '24', '36', '13', '1', '00', '27', '10', '25', '29', '12', '8', '19', '31', 
        '18', '6', '21', '33', '16', '4', '23', '35', '14', '2'
    ] 