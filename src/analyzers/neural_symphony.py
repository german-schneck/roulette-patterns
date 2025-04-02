#!/usr/bin/env python3
"""
Neural Symphony Strategy Analyzer

Implementation of a strategy that interprets roulette outcomes as musical patterns,
analyzing rhythmic and harmonic structures to identify emergent sequences.
"""

import numpy as np
from collections import defaultdict
import math
from src.utils.analysis import validate_numbers_performance

def analyze_neural_symphony(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze optimal number selection using musical pattern analysis.
    
    This strategy incorporates:
    1. Rhythmic pattern detection (sequential analysis)
    2. Harmonic analysis (frequency relationships)
    3. Musical scale mapping
    4. Melodic contour analysis
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nGenerando combinación con estrategia Neural Symphony (Sinfonía Neural)...")
    
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
    
    # Generate different musical analysis combinations
    combinations = []
    
    # 1. Rhythmic Pattern Analysis
    rhythmic_numbers = analyze_rhythmic_patterns(numeric_history)
    combinations.append(("Rhythmic Patterns", rhythmic_numbers))
    
    # 2. Harmonic Analysis
    harmonic_numbers = analyze_harmonic_structures(numeric_history)
    combinations.append(("Harmonic Structures", harmonic_numbers))
    
    # 3. Musical Scale Mapping
    scale_numbers = analyze_musical_scales(numeric_history)
    combinations.append(("Musical Scales", scale_numbers))
    
    # 4. Melodic Contour Analysis
    contour_numbers = analyze_melodic_contours(numeric_history)
    combinations.append(("Melodic Contours", contour_numbers))
    
    # Test each musical-based combination
    best_win_rate = 0
    best_combination_name = ""
    best_symphony_numbers = []
    
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
            best_symphony_numbers = numbers
    
    # If sorted_numbers is provided, enhance our selection with top performers
    if sorted_numbers:
        # Create a blend with top numbers from pre-sorted list
        symphony_enhanced = []
        
        # Include top 4 numbers from our Neural Symphony analysis
        symphony_enhanced.extend(best_symphony_numbers[:4])
        
        # Add top ranked numbers from sorted_numbers that aren't already included
        for num in sorted_numbers:
            if num not in symphony_enhanced and len(symphony_enhanced) < 8:
                symphony_enhanced.append(num)
        
        # Validate the enhanced combination
        print("\nValidando combinación Neural Symphony mejorada...")
        symphony_win_rate = validate_numbers_performance(
            validation_analyzer, symphony_enhanced, validation_spins)
        
        symphony_coverage = len(symphony_enhanced) / 38 * 100
        symphony_performance = (symphony_win_rate / symphony_coverage - 1) * 100
        
        print(f"Combinación Neural Symphony final: {', '.join(symphony_enhanced)}")
        print(f"Tasa de victoria: {symphony_win_rate:.2f}%")
        print(f"Rendimiento: {symphony_performance:+.2f}%")
        
        final_numbers = symphony_enhanced
        final_win_rate = symphony_win_rate
        final_performance = symphony_performance
    else:
        final_numbers = best_symphony_numbers
        final_win_rate = best_win_rate
        final_performance = (final_win_rate / (len(final_numbers) / 38 * 100) - 1) * 100
    
    # Return results
    return {
        'neural_symphony_numbers': final_numbers,
        'neural_symphony_win_rate': final_win_rate,
        'neural_symphony_performance': final_performance,
        'best_combination_type': best_combination_name
    }

def analyze_rhythmic_patterns(history):
    """
    Analyze rhythmic patterns in the number sequence.
    
    Rhythmic patterns are defined as recurring intervals between numbers.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Calculate intervals between consecutive numbers
    intervals = []
    for i in range(1, len(history)):
        interval = (history[i] - history[i-1]) % 38
        intervals.append(interval)
    
    # Identify recurring rhythmic patterns (interval sequences)
    pattern_length = 3  # Look for patterns of 3 consecutive intervals
    
    if len(intervals) < pattern_length:
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Find all patterns
    patterns = {}
    for i in range(len(intervals) - pattern_length + 1):
        pattern = tuple(intervals[i:i+pattern_length])
        if pattern in patterns:
            patterns[pattern].append(i)
        else:
            patterns[pattern] = [i]
    
    # Filter to patterns that occur at least twice
    recurring_patterns = {pattern: positions for pattern, positions in patterns.items() if len(positions) >= 2}
    
    if not recurring_patterns:
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Calculate the "next number" for each recurring pattern
    next_numbers = []
    
    for pattern, positions in recurring_patterns.items():
        for pos in positions:
            pattern_end_idx = pos + pattern_length - 1
            if pattern_end_idx < len(intervals) - 1:
                # Get the number that followed this pattern
                next_number_idx = pattern_end_idx + 2  # +1 for interval to idx conversion, +1 for next
                if next_number_idx < len(history):
                    next_numbers.append(history[next_number_idx])
    
    # Count frequency of next numbers
    next_number_freq = defaultdict(int)
    for num in next_numbers:
        next_number_freq[num] += 1
    
    # Get top next numbers
    sorted_next = sorted(next_number_freq.items(), key=lambda x: x[1], reverse=True)
    top_next = [num for num, _ in sorted_next[:4]]
    
    # Calculate the most commonly "resolved" intervals
    # (i.e., what intervals tend to lead to stable patterns)
    resolved_intervals = defaultdict(int)
    for i in range(1, len(intervals) - 1):
        # Check if this sequence forms a "resolution" 
        # (i.e., returns to a number close to the starting point)
        if abs(intervals[i] - intervals[i-1]) <= 3:
            resolved_intervals[intervals[i]] += 1
    
    # Use the most common resolved intervals to predict next numbers
    recent_num = history[-1] if history else 0
    predicted_nums = []
    
    sorted_intervals = sorted(resolved_intervals.items(), key=lambda x: x[1], reverse=True)
    
    for interval, _ in sorted_intervals[:4]:
        predicted_num = (recent_num + interval) % 38
        if predicted_num not in predicted_nums:
            predicted_nums.append(predicted_num)
    
    # Combine top next numbers and predicted numbers
    recommended_numbers = []
    
    for num in top_next:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers:
            recommended_numbers.append(num_str)
    
    for num in predicted_nums:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num_str)
    
    # Ensure we have 8 numbers
    defaults = [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    for num in defaults:
        if num not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num)
    
    return recommended_numbers[:8]

def analyze_harmonic_structures(history):
    """
    Analyze harmonic structures in the roulette sequence.
    
    Harmonic structures are defined as relationships between numbers
    based on musical intervals and frequency ratios.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Map roulette numbers to a musical scale (C major)
    # We'll use a 38-tone equal temperament scale (dividing the octave into 38 equal parts)
    frequency_ratios = {}
    
    for i in range(38):
        # Calculate frequency ratio (equal temperament)
        # 2^(i/38) represents the frequency ratio from the base note
        frequency_ratios[i] = 2 ** (i / 38)
    
    # Define "consonant" intervals (harmonic relationships)
    # These are approximate ratios in 38-tone equal temperament
    consonant_intervals = [
        3,   # Minor third (approximately 3/38 = 0.079 of an octave)
        6,   # Major third (approximately 6/38 = 0.158 of an octave)
        11,  # Perfect fifth (approximately 11/38 = 0.289 of an octave)
        19,  # Octave (approximately 19/38 = 0.5 of an octave)
        22,  # Octave + minor third
        25,  # Octave + major third
        30   # Octave + perfect fifth
    ]
    
    # Calculate consonance scores for each number
    consonance_scores = defaultdict(int)
    
    for i in range(len(history) - 1):
        current = history[i]
        
        # Look at numbers within a "phrase" (next 7 numbers)
        phrase_length = min(7, len(history) - i - 1)
        
        for j in range(1, phrase_length + 1):
            next_num = history[i + j]
            
            # Calculate interval
            interval = abs(next_num - current) % 38
            
            # Check if this is a consonant interval
            if interval in consonant_intervals:
                consonance_scores[next_num] += 1 / j  # Weight by proximity
    
    # Get numbers with highest consonance scores
    sorted_consonance = sorted(consonance_scores.items(), key=lambda x: x[1], reverse=True)
    consonant_numbers = [num for num, _ in sorted_consonance[:4]]
    
    # Find "harmonic cadences" - sequences that lead to resolution
    cadence_target_numbers = []
    
    for i in range(len(history) - 2):
        # Look for a sequence where two intervals form a cadence
        # In music, a common cadence is a fourth followed by a fifth (or vice versa)
        interval1 = (history[i+1] - history[i]) % 38
        interval2 = (history[i+2] - history[i+1]) % 38
        
        # Check if this pair of intervals forms a cadence
        # In our system, intervals close to 10 and 11 (approximately fourth and fifth)
        is_cadence = (
            (9 <= interval1 <= 11 and 9 <= interval2 <= 11) or
            # Or harmonic resolution (large interval followed by small)
            (interval1 > 15 and interval2 < 5)
        )
        
        if is_cadence:
            cadence_target_numbers.append(history[i+2])
    
    # Count cadence targets
    cadence_counts = defaultdict(int)
    for num in cadence_target_numbers:
        cadence_counts[num] += 1
    
    # Get top cadence targets
    sorted_cadences = sorted(cadence_counts.items(), key=lambda x: x[1], reverse=True)
    cadence_numbers = [num for num, _ in sorted_cadences[:4]]
    
    # Combine consonant numbers and cadence numbers
    recommended_numbers = []
    
    for num in consonant_numbers:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers:
            recommended_numbers.append(num_str)
    
    for num in cadence_numbers:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num_str)
    
    # Ensure we have 8 numbers
    defaults = [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    for num in defaults:
        if num not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num)
    
    return recommended_numbers[:8]

def analyze_musical_scales(history):
    """
    Analyze history for patterns that follow musical scales.
    
    Maps roulette numbers onto traditional musical scales and identifies
    which scales best fit the historical data.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Define musical scales as patterns of intervals
    scales = {
        'major': [0, 2, 4, 5, 7, 9, 11],            # Major scale
        'natural_minor': [0, 2, 3, 5, 7, 8, 10],    # Natural minor scale
        'harmonic_minor': [0, 2, 3, 5, 7, 8, 11],   # Harmonic minor scale
        'pentatonic': [0, 2, 4, 7, 9],              # Major pentatonic scale
        'whole_tone': [0, 2, 4, 6, 8, 10],          # Whole tone scale
        'chromatic': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # Chromatic scale
    }
    
    # Map the roulette wheel to a 12-tone system
    # We'll use modulo 12 to map numbers 0-37 to 0-11
    # This is like mapping to the 12 notes in an octave
    mapped_history = [num % 12 for num in history]
    
    # Calculate how well each scale fits recent history
    recent_history = mapped_history[-50:]
    scale_fits = {}
    
    for scale_name, scale_intervals in scales.items():
        # Count how many recent numbers fall within this scale
        in_scale_count = sum(1 for num in recent_history if num % 12 in scale_intervals)
        scale_fits[scale_name] = in_scale_count / len(recent_history)
    
    # Find the best fitting scale
    best_scale_name = max(scale_fits.items(), key=lambda x: x[1])[0]
    best_scale = scales[best_scale_name]
    
    # Determine the most likely "tonic" (starting note) for this scale
    possible_tonics = list(range(12))
    tonic_counts = defaultdict(int)
    
    # For each possible tonic, count how many recent numbers would be "in scale"
    for tonic in possible_tonics:
        for num in recent_history:
            # Check if this number is in the scale with this tonic
            degree = (num - tonic) % 12
            if degree in best_scale:
                tonic_counts[tonic] += 1
    
    # Get the most likely tonic
    best_tonic = max(tonic_counts.items(), key=lambda x: x[1])[0]
    
    # Now we know the scale and tonic, we can predict which numbers are likely
    # We'll map the scale notes back to roulette numbers
    
    # Get the next few scale degrees
    recent = history[-1] % 12
    recent_position_in_scale = -1
    
    for i, degree in enumerate(best_scale):
        if (recent - best_tonic) % 12 == degree:
            recent_position_in_scale = i
            break
    
    # If we found the position, predict next numbers based on scale progression
    predicted_scale_positions = []
    
    if recent_position_in_scale != -1:
        # Next 4 positions in the scale (wrapping around if needed)
        for i in range(1, 5):
            next_pos = (recent_position_in_scale + i) % len(best_scale)
            predicted_scale_positions.append(next_pos)
    else:
        # If recent doesn't fit in scale, use first 4 positions
        predicted_scale_positions = list(range(min(4, len(best_scale))))
    
    # Convert scale positions to actual numbers
    scale_based_numbers = []
    
    for pos in predicted_scale_positions:
        degree = best_scale[pos]
        number = (best_tonic + degree) % 12
        
        # Map back to roulette numbers (find all matches)
        for i in range(38):
            if i % 12 == number:
                scale_based_numbers.append(i)
    
    # Take up to 8 unique numbers
    unique_scale_numbers = []
    for num in scale_based_numbers:
        if num not in unique_scale_numbers and len(unique_scale_numbers) < 8:
            unique_scale_numbers.append(num)
    
    # Convert to strings
    recommended_numbers = [str(num) if num != 37 else '00' for num in unique_scale_numbers]
    
    # Ensure we have 8 numbers
    defaults = [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    for num in defaults:
        if num not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num)
    
    return recommended_numbers[:8]

def analyze_melodic_contours(history):
    """
    Analyze melodic contours in the roulette sequence.
    
    Melodic contours describe the shape of a melody (ascending, descending, etc.)
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Calculate direction changes in the sequence
    # 1 = ascending, 0 = same, -1 = descending
    directions = []
    for i in range(1, len(history)):
        if history[i] > history[i-1]:
            directions.append(1)
        elif history[i] < history[i-1]:
            directions.append(-1)
        else:
            directions.append(0)
    
    # Identify contour patterns (e.g., up-up-down, down-up-down)
    contour_length = 4  # Look for contours of 4 consecutive directions
    
    if len(directions) < contour_length:
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Find all contours
    contours = {}
    for i in range(len(directions) - contour_length + 1):
        contour = tuple(directions[i:i+contour_length])
        if contour in contours:
            contours[contour].append(i)
        else:
            contours[contour] = [i]
    
    # Filter to contours that occur at least twice
    recurring_contours = {contour: positions for contour, positions in contours.items() if len(positions) >= 2}
    
    if not recurring_contours:
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Calculate the "next number" for each recurring contour
    next_numbers = []
    
    for contour, positions in recurring_contours.items():
        for pos in positions:
            contour_end_idx = pos + contour_length - 1
            if contour_end_idx < len(directions) - 1:
                # Get the number that followed this contour
                next_number_idx = contour_end_idx + 2  # +1 for direction to idx conversion, +1 for next
                if next_number_idx < len(history):
                    next_numbers.append(history[next_number_idx])
    
    # Count frequency of next numbers
    next_number_freq = defaultdict(int)
    for num in next_numbers:
        next_number_freq[num] += 1
    
    # Get top next numbers
    sorted_next = sorted(next_number_freq.items(), key=lambda x: x[1], reverse=True)
    top_next = [num for num, _ in sorted_next[:4]]
    
    # Calculate the most recent contour
    recent_contour = tuple(directions[-contour_length:]) if len(directions) >= contour_length else None
    
    # If we've seen this contour before, predict based on history
    predicted_numbers = []
    
    if recent_contour and recent_contour in recurring_contours:
        for pos in recurring_contours[recent_contour]:
            contour_end_idx = pos + contour_length - 1
            if contour_end_idx < len(directions) - 1:
                next_number_idx = contour_end_idx + 2
                if next_number_idx < len(history):
                    predicted_numbers.append(history[next_number_idx])
    
    # Count frequencies
    predicted_freq = defaultdict(int)
    for num in predicted_numbers:
        predicted_freq[num] += 1
    
    # Get top predictions
    sorted_predicted = sorted(predicted_freq.items(), key=lambda x: x[1], reverse=True)
    top_predicted = [num for num, _ in sorted_predicted[:4]]
    
    # Combine next numbers and predictions
    recommended_numbers = []
    
    for num in top_next:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers:
            recommended_numbers.append(num_str)
    
    for num in top_predicted:
        num_str = str(num) if num != 37 else '00'
        if num_str not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num_str)
    
    # Ensure we have 8 numbers
    defaults = [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    for num in defaults:
        if num not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num)
    
    return recommended_numbers[:8] 