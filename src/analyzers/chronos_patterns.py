#!/usr/bin/env python3
"""
Chronos Patterns Strategy Analyzer

Implementation of a strategy that focuses on the temporal dimension of roulette outcomes,
analyzing patterns related to time, dealer fatigue, and session dynamics.
"""

import numpy as np
from collections import defaultdict
import datetime
import random
from src.utils.analysis import validate_numbers_performance

def analyze_chronos_patterns(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze optimal number selection using temporal pattern analysis.
    
    This strategy incorporates:
    1. Time-based segmentation of results
    2. Croupier fatigue modeling
    3. Session boundary analysis
    4. Circadian rhythm pattern detection
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nGenerando combinación con estrategia Chronos Patterns (Patrones Temporales)...")
    
    # Get history 
    history = analyzer.history[-5000:] if len(analyzer.history) > 5000 else analyzer.history
    
    # Convert history strings to integers and simulate timestamps
    numeric_history = []
    for num in history:
        if isinstance(num, str):
            if num == '00':
                numeric_history.append(37)
            else:
                numeric_history.append(int(num))
        else:
            numeric_history.append(num)
    
    # Since we don't have actual timestamps, simulate them
    simulated_timestamps = simulate_timestamps(len(numeric_history))
    
    # Generate different temporal analysis combinations
    combinations = []
    
    # 1. Time Segment Analysis
    time_segment_numbers = time_segment_analysis(numeric_history, simulated_timestamps)
    combinations.append(("Time Segments", time_segment_numbers))
    
    # 2. Fatigue Pattern Analysis
    fatigue_numbers = fatigue_pattern_analysis(numeric_history, simulated_timestamps)
    combinations.append(("Fatigue Patterns", fatigue_numbers))
    
    # 3. Session Boundary Analysis
    boundary_numbers = session_boundary_analysis(numeric_history, simulated_timestamps)
    combinations.append(("Session Boundaries", boundary_numbers))
    
    # 4. Circadian Rhythm Analysis
    circadian_numbers = circadian_rhythm_analysis(numeric_history, simulated_timestamps)
    combinations.append(("Circadian Rhythms", circadian_numbers))
    
    # Test each temporal-based combination
    best_win_rate = 0
    best_combination_name = ""
    best_chronos_numbers = []
    
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
            best_chronos_numbers = numbers
    
    # If sorted_numbers is provided, enhance our selection with top performers
    if sorted_numbers:
        # Create a blend with top numbers from pre-sorted list
        chronos_enhanced = []
        
        # Include top 4 numbers from our Chronos analysis
        chronos_enhanced.extend(best_chronos_numbers[:4])
        
        # Add top ranked numbers from sorted_numbers that aren't already included
        for num in sorted_numbers:
            if num not in chronos_enhanced and len(chronos_enhanced) < 8:
                chronos_enhanced.append(num)
        
        # Validate the enhanced combination
        print("\nValidando combinación Chronos Patterns mejorada...")
        chronos_win_rate = validate_numbers_performance(
            validation_analyzer, chronos_enhanced, validation_spins)
        
        chronos_coverage = len(chronos_enhanced) / 38 * 100
        chronos_performance = (chronos_win_rate / chronos_coverage - 1) * 100
        
        print(f"Combinación Chronos Patterns final: {', '.join(chronos_enhanced)}")
        print(f"Tasa de victoria: {chronos_win_rate:.2f}%")
        print(f"Rendimiento: {chronos_performance:+.2f}%")
        
        final_numbers = chronos_enhanced
        final_win_rate = chronos_win_rate
        final_performance = chronos_performance
    else:
        final_numbers = best_chronos_numbers
        final_win_rate = best_win_rate
        final_performance = (final_win_rate / (len(final_numbers) / 38 * 100) - 1) * 100
    
    # Return results
    return {
        'chronos_patterns_numbers': final_numbers,
        'chronos_patterns_win_rate': final_win_rate,
        'chronos_patterns_performance': final_performance,
        'best_combination_type': best_combination_name
    }

def simulate_timestamps(history_length):
    """
    Create simulated timestamps for historical data.
    
    Args:
        history_length: Length of the history to generate timestamps for
        
    Returns:
        list: Simulated timestamps
    """
    # Start from a base time 24 hours ago
    base_time = datetime.datetime.now() - datetime.timedelta(days=1)
    timestamps = []
    
    # Create 3-4 session blocks, with gaps between them
    sessions = []
    remaining_spins = history_length
    session_count = min(4, max(1, history_length // 200))
    
    for i in range(session_count):
        session_length = remaining_spins // (session_count - i)
        remaining_spins -= session_length
        
        # Session start time
        session_start = base_time + datetime.timedelta(hours=i*6)
        
        # Each session is about 3-4 hours
        session_duration_minutes = random.randint(180, 240)
        
        # Calculate timestamps evenly distributed through the session
        for j in range(session_length):
            minutes_offset = (j / session_length) * session_duration_minutes
            timestamp = session_start + datetime.timedelta(minutes=minutes_offset)
            sessions.append((timestamp, i))
    
    # Sort by timestamp
    sessions.sort(key=lambda x: x[0])
    
    # Extract just the timestamps
    timestamps = [session[0] for session in sessions]
    
    return timestamps

def time_segment_analysis(history, timestamps):
    """
    Analyze outcomes based on time segments through a session.
    
    Args:
        history: List of past outcomes as integers
        timestamps: Corresponding timestamps
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Divide each session into segments (early, middle, late)
    segment_frequencies = [defaultdict(int), defaultdict(int), defaultdict(int)]
    
    # Find session boundaries to identify early, middle, and late segments
    session_times = []
    current_session_start = timestamps[0]
    
    for i in range(1, len(timestamps)):
        # If gap between spins is more than 30 minutes, consider it a new session
        if (timestamps[i] - timestamps[i-1]).total_seconds() > 30 * 60:
            session_times.append((current_session_start, timestamps[i-1]))
            current_session_start = timestamps[i]
    
    # Add the last session
    if timestamps:
        session_times.append((current_session_start, timestamps[-1]))
    
    # Classify each spin into early, middle, or late segment
    for i, timestamp in enumerate(timestamps):
        if i >= len(history):
            break
            
        for session_start, session_end in session_times:
            if session_start <= timestamp <= session_end:
                # Calculate position in session (0-1)
                position = (timestamp - session_start).total_seconds() / (session_end - session_start).total_seconds()
                
                # Determine segment
                if position < 0.33:
                    segment = 0  # Early
                elif position < 0.66:
                    segment = 1  # Middle
                else:
                    segment = 2  # Late
                
                segment_frequencies[segment][history[i]] += 1
                break
    
    # Identify which segment shows most deviation from expected
    segment_deviations = []
    
    for segment_freq in segment_frequencies:
        # Calculate expected frequency for each number
        total_spins = sum(segment_freq.values())
        expected = total_spins / 38
        
        # Calculate chi-square deviation
        deviation = sum((freq - expected)**2 / expected for freq in segment_freq.values() if freq > 0)
        segment_deviations.append(deviation)
    
    # Select segment with highest deviation (most non-random)
    best_segment = segment_deviations.index(max(segment_deviations))
    
    # Get top 8 numbers from that segment
    sorted_numbers = sorted(segment_frequencies[best_segment].items(), key=lambda x: x[1], reverse=True)
    recommended_numbers = [str(num) if num != 37 else '00' for num, _ in sorted_numbers[:8]]
    
    # If we don't have 8 numbers yet, add some from next best segment
    if len(recommended_numbers) < 8:
        segment_deviations[best_segment] = -1  # Mark as used
        next_best_segment = segment_deviations.index(max(segment_deviations))
        
        sorted_numbers = sorted(segment_frequencies[next_best_segment].items(), key=lambda x: x[1], reverse=True)
        for num, _ in sorted_numbers:
            num_str = str(num) if num != 37 else '00'
            if num_str not in recommended_numbers:
                recommended_numbers.append(num_str)
                if len(recommended_numbers) >= 8:
                    break
    
    # If we still don't have 8 numbers, add some defaults
    defaults = [str(n) for n in [0, '00', 1, 2, 3, 32, 35, 36]]
    for num in defaults:
        if num not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num)
    
    return recommended_numbers[:8]

def fatigue_pattern_analysis(history, timestamps):
    """
    Analyze outcomes considering croupier fatigue patterns.
    
    This models how dealer precision may change throughout a session,
    affecting the distribution of landing positions.
    
    Args:
        history: List of past outcomes as integers
        timestamps: List of timestamps corresponding to each outcome
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50 or len(timestamps) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Typical dealer shift durations in minutes
    shift_duration = 45  # typical roulette dealer rotation
    
    # Model dealer rotations/shifts - convert timestamps to minutes since start
    start_time = timestamps[0]
    minutes_elapsed = [(ts - start_time).total_seconds() / 60 for ts in timestamps]
    
    # Determine dealer shifts
    shift_boundaries = []
    current_shift = 0
    for i, elapsed in enumerate(minutes_elapsed):
        shift_number = int(elapsed / shift_duration)
        if shift_number > current_shift:
            shift_boundaries.append(i)
            current_shift = shift_number
    
    # If no shift changes detected, create artificial boundaries
    if not shift_boundaries:
        shift_size = len(history) // 3
        shift_boundaries = [shift_size, shift_size * 2]
    
    # Prepare to analyze early, middle, and late sections of each shift
    section_results = []
    
    # Maximum wheel number (37 for single zero, 38 for double zero wheels)
    max_wheel_number = 38
    
    for i in range(len(shift_boundaries) + 1):
        # Define shift start and end
        shift_start = shift_boundaries[i-1] if i > 0 else 0
        shift_end = shift_boundaries[i] if i < len(shift_boundaries) else len(history)
        
        # Skip shifts that are too short
        if shift_end - shift_start < 30:
            continue
        
        # Split shift into early, middle, late sections
        section_size = (shift_end - shift_start) // 3
        
        if section_size == 0:
            continue  # Skip if sections would be empty
            
        early_start = shift_start
        early_end = shift_start + section_size
        
        middle_start = early_end
        middle_end = middle_start + section_size
        
        late_start = middle_end
        late_end = shift_end
        
        # Count hits in each section
        early_section_hits = [0] * max_wheel_number
        middle_section_hits = [0] * max_wheel_number
        late_section_hits = [0] * max_wheel_number
        
        for i in range(early_start, early_end):
            if i < len(history):  # Ensure index is within range
                num = history[i]
                if num < max_wheel_number:  # Ensure number is within range
                    early_section_hits[num] += 1
        
        for i in range(middle_start, middle_end):
            if i < len(history):  # Ensure index is within range
                num = history[i]
                if num < max_wheel_number:  # Ensure number is within range
                    middle_section_hits[num] += 1
        
        for i in range(late_start, late_end):
            if i < len(history):  # Ensure index is within range
                num = history[i]
                if num < max_wheel_number:  # Ensure number is within range
                    late_section_hits[num] += 1
        
        # Calculate precision drift (variation between sections)
        precision_drift = []
        for num in range(max_wheel_number):
            early_freq = early_section_hits[num] / section_size if section_size > 0 else 0
            middle_freq = middle_section_hits[num] / section_size if section_size > 0 else 0
            late_freq = late_section_hits[num] / (late_end - late_start) if (late_end - late_start) > 0 else 0
            
            # Calculate drift trend (positive = increasing frequency toward end of shift)
            drift = (late_freq - early_freq)
            precision_drift.append((num, drift))
        
        section_results.append(precision_drift)
    
    # Find numbers that show consistent patterns across shifts
    consistent_drifts = {}
    for num in range(max_wheel_number):
        drifts = [shift[num][1] for shift in section_results if num < len(shift)]
        if drifts:
            avg_drift = sum(drifts) / len(drifts)
            consistency = sum(1 for d in drifts if (d > 0 and avg_drift > 0) or (d < 0 and avg_drift < 0))
            consistency_score = consistency / len(drifts) if drifts else 0
            consistent_drifts[num] = (avg_drift, consistency_score)
    
    # Select numbers with strong consistent drift patterns
    strong_drift_numbers = []
    
    # 1. Numbers that consistently increase in frequency (dealer gets tired/less precise)
    positive_drifts = [(num, data[0], data[1]) 
                     for num, data in consistent_drifts.items() 
                     if data[0] > 0 and data[1] > 0.5]
    
    positive_drifts.sort(key=lambda x: (x[2], x[1]), reverse=True)
    
    # 2. Numbers that consistently decrease (dealer gets into rhythm)
    negative_drifts = [(num, abs(data[0]), data[1]) 
                      for num, data in consistent_drifts.items() 
                      if data[0] < 0 and data[1] > 0.5]
    
    negative_drifts.sort(key=lambda x: (x[2], x[1]), reverse=True)
    
    # Combine results with preference for strongest patterns
    for _, group in enumerate([positive_drifts, negative_drifts]):
        for num, _, _ in group[:4]:  # Take up to 4 from each group
            if len(strong_drift_numbers) < 8:
                strong_drift_numbers.append(str(num) if num != 37 else '00')
    
    # Fill remaining with zeros if needed
    while len(strong_drift_numbers) < 8:
        strong_drift_numbers.append('0')
    
    return strong_drift_numbers

def session_boundary_analysis(history, timestamps):
    """
    Analyze outcomes at session boundaries.
    
    Args:
        history: List of past outcomes as integers
        timestamps: Corresponding timestamps
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 50:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Find session boundaries
    session_boundaries = []
    
    for i in range(1, len(timestamps)):
        # If gap between spins is more than 30 minutes, consider it a session boundary
        if (timestamps[i] - timestamps[i-1]).total_seconds() > 30 * 60:
            session_boundaries.append(i)
    
    # Collect numbers at start and end of sessions
    session_start_numbers = []
    session_end_numbers = []
    
    # Start of first session
    session_start_numbers.extend(history[:min(10, len(history))])
    
    # End of last session
    session_end_numbers.extend(history[max(0, len(history)-10):])
    
    # Boundaries in the middle
    for boundary in session_boundaries:
        # End of previous session
        end_idx = boundary
        session_end_numbers.extend(history[max(0, end_idx-10):end_idx])
        
        # Start of next session
        start_idx = boundary
        session_start_numbers.extend(history[start_idx:min(start_idx+10, len(history))])
    
    # Analyze early and late session spins
    early_frequencies = defaultdict(int)
    for num in session_start_numbers:
        early_frequencies[num] += 1
    
    late_frequencies = defaultdict(int)
    for num in session_end_numbers:
        late_frequencies[num] += 1
    
    # Compare frequencies to find biggest differences
    differential_scores = {}
    
    for num in set(early_frequencies.keys()).union(set(late_frequencies.keys())):
        early_count = early_frequencies.get(num, 0)
        late_count = late_frequencies.get(num, 0)
        
        # Calculate the differential (positive means appears more in early sessions)
        if early_count + late_count > 0:
            differential_scores[num] = (early_count - late_count) / (early_count + late_count)
    
    # Get top numbers that appear more in early sessions (positive differential)
    early_biased = sorted(differential_scores.items(), key=lambda x: x[1], reverse=True)[:4]
    
    # Get top numbers that appear more in late sessions (negative differential)
    late_biased = sorted(differential_scores.items(), key=lambda x: x[1])[:4]
    
    # Combine recommendations
    recommended_numbers = []
    
    for num, _ in early_biased:
        recommended_numbers.append(str(num) if num != 37 else '00')
    
    for num, _ in late_biased:
        recommended_numbers.append(str(num) if num != 37 else '00')
    
    # Ensure we have 8 numbers
    defaults = [str(n) for n in [0, '00', 1, 2, 3, 32, 35, 36]]
    for num in defaults:
        if num not in recommended_numbers and len(recommended_numbers) < 8:
            recommended_numbers.append(num)
    
    return recommended_numbers[:8]

def circadian_rhythm_analysis(history, timestamps):
    """
    Analyze outcomes based on circadian rhythm patterns.
    
    Args:
        history: List of past outcomes as integers
        timestamps: Corresponding timestamps
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 100:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Divide day into 4 circadian periods
    # 1. Peak alertness (9am-12pm, 6pm-9pm)
    # 2. Alertness declining (12pm-3pm, 9pm-12am)
    # 3. Low alertness (3pm-6pm, 12am-3am)
    # 4. Rising alertness (6am-9am, 3am-6am)
    
    period_frequencies = [defaultdict(int) for _ in range(4)]
    
    for i, timestamp in enumerate(timestamps):
        if i >= len(history):
            break
            
        hour = timestamp.hour
        
        # Classify hour into period
        if hour in [9, 10, 11, 18, 19, 20]:
            period = 0  # Peak alertness
        elif hour in [12, 13, 14, 21, 22, 23]:
            period = 1  # Alertness declining
        elif hour in [15, 16, 17, 0, 1, 2]:
            period = 2  # Low alertness
        else:  # 3-8
            period = 3  # Rising alertness
        
        # Record number in this period
        period_frequencies[period][history[i]] += 1
    
    # Calculate contrast between peak and low alertness periods
    peak_frequencies = period_frequencies[0]
    low_frequencies = period_frequencies[2]
    
    # Normalize frequencies
    peak_total = sum(peak_frequencies.values()) or 1
    low_total = sum(low_frequencies.values()) or 1
    
    peak_normalized = {num: count / peak_total for num, count in peak_frequencies.items()}
    low_normalized = {num: count / low_total for num, count in low_frequencies.items()}
    
    # Find numbers with biggest difference between periods
    contrast_scores = {}
    
    for num in set(peak_normalized.keys()).union(set(low_normalized.keys())):
        peak_freq = peak_normalized.get(num, 0)
        low_freq = low_normalized.get(num, 0)
        
        # Calculate contrast score (absolute difference)
        contrast_scores[num] = abs(peak_freq - low_freq)
    
    # Get top 8 numbers with highest contrast
    sorted_contrast = sorted(contrast_scores.items(), key=lambda x: x[1], reverse=True)[:8]
    recommended_numbers = [str(num) if num != 37 else '00' for num, _ in sorted_contrast]
    
    # Ensure we have 8 numbers
    defaults = [str(n) for n in [0, '00', 1, 2, 3, 32, 35, 36]]
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