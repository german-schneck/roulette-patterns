#!/usr/bin/env python3
"""
Butterfly Effect Strategy Analyzer

Implementation of a strategy that applies chaos theory principles
to identify sensitive patterns in roulette outcomes.
"""

import numpy as np
from collections import defaultdict
import math
from src.utils.analysis import validate_numbers_performance

def analyze_butterfly_effect(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze optimal number selection using chaos theory principles.
    
    This strategy incorporates:
    1. Calculation of Lyapunov exponents to detect chaotic behavior
    2. Bifurcation point analysis to identify regime changes
    3. Strange attractor mapping for pattern detection
    4. Sensitive dependence analysis for prediction
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nGenerando combinación con estrategia Butterfly Effect (Efecto Mariposa)...")
    
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
    
    # Generate different chaos-based combinations
    combinations = []
    
    # 1. Lyapunov Analysis (sensitive dependence)
    lyapunov_numbers = analyze_lyapunov_exponents(numeric_history)
    combinations.append(("Lyapunov Exponents", lyapunov_numbers))
    
    # 2. Bifurcation Analysis (regime changes)
    bifurcation_numbers = analyze_bifurcation_points(numeric_history)
    combinations.append(("Bifurcation Points", bifurcation_numbers))
    
    # 3. Strange Attractor Mapping
    attractor_numbers = analyze_strange_attractors(numeric_history)
    combinations.append(("Strange Attractors", attractor_numbers))
    
    # 4. Phase Space Trajectory Analysis
    trajectory_numbers = analyze_phase_space(numeric_history)
    combinations.append(("Phase Space", trajectory_numbers))
    
    # Test each chaos-based combination
    best_win_rate = 0
    best_combination_name = ""
    best_butterfly_numbers = []
    
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
            best_butterfly_numbers = numbers
    
    # If sorted_numbers is provided, enhance our selection with top performers
    if sorted_numbers:
        # Create a blend with top numbers from pre-sorted list
        butterfly_enhanced = []
        
        # Include top 4 numbers from our Butterfly Effect analysis
        butterfly_enhanced.extend(best_butterfly_numbers[:4])
        
        # Add top ranked numbers from sorted_numbers that aren't already included
        for num in sorted_numbers:
            if num not in butterfly_enhanced and len(butterfly_enhanced) < 8:
                butterfly_enhanced.append(num)
        
        # Validate the enhanced combination
        print("\nValidando combinación Butterfly Effect mejorada...")
        butterfly_win_rate = validate_numbers_performance(
            validation_analyzer, butterfly_enhanced, validation_spins)
        
        butterfly_coverage = len(butterfly_enhanced) / 38 * 100
        butterfly_performance = (butterfly_win_rate / butterfly_coverage - 1) * 100
        
        print(f"Combinación Butterfly Effect final: {', '.join(butterfly_enhanced)}")
        print(f"Tasa de victoria: {butterfly_win_rate:.2f}%")
        print(f"Rendimiento: {butterfly_performance:+.2f}%")
        
        final_numbers = butterfly_enhanced
        final_win_rate = butterfly_win_rate
        final_performance = butterfly_performance
    else:
        final_numbers = best_butterfly_numbers
        final_win_rate = best_win_rate
        final_performance = (final_win_rate / (len(final_numbers) / 38 * 100) - 1) * 100
    
    # Return results
    return {
        'butterfly_effect_numbers': final_numbers,
        'butterfly_effect_win_rate': final_win_rate,
        'butterfly_effect_performance': final_performance,
        'best_combination_type': best_combination_name
    }

def calculate_lyapunov_exponent(series, m=2, tau=1, eps=0.01, max_steps=20):
    """
    Calculate the maximum Lyapunov exponent of a time series.
    
    Args:
        series: Numeric time series
        m: Embedding dimension
        tau: Time delay
        eps: Neighborhood size
        max_steps: Maximum number of steps to follow trajectories
        
    Returns:
        float: Estimated maximum Lyapunov exponent
    """
    n = len(series)
    if n < m * tau + max_steps:
        return 0  # Not enough data
    
    # Create embedding vectors
    Y = np.zeros((n - (m-1) * tau, m))
    for i in range(m):
        Y[:, i] = series[i * tau:n - (m-1) * tau + i * tau]
    
    # Find nearest neighbors
    norms = np.zeros(n - (m-1) * tau)
    d_sum = 0.0
    n_pairs = 0
    
    for i in range(n - (m-1) * tau - max_steps):
        # Exclude neighbors that are too close in time
        candidates = np.arange(n - (m-1) * tau)
        candidates = candidates[(candidates < i - 2*tau) | (candidates > i + 2*tau)]
        
        if len(candidates) == 0:
            continue
        
        # Find distances to all candidates
        distances = np.linalg.norm(Y[candidates] - Y[i], axis=1)
        
        # Find nearest neighbor
        if len(distances) > 0:
            j = candidates[np.argmin(distances)]
            min_dist = distances.min()
            
            if min_dist < eps:
                n_pairs += 1
                
                # Follow the distance between trajectories
                for k in range(1, max_steps + 1):
                    if i + k < len(Y) and j + k < len(Y):
                        d_k = np.linalg.norm(Y[i + k] - Y[j + k])
                        if d_k > 0:
                            d_sum += np.log(d_k / min_dist)
    
    # Calculate Lyapunov exponent
    if n_pairs > 0:
        lya = d_sum / (n_pairs * max_steps)
    else:
        lya = 0
        
    return lya

def analyze_lyapunov_exponents(history):
    """
    Analyze and identify numbers based on Lyapunov exponents.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 100:
        # Not enough data for meaningful analysis
        # Return some common numbers as fallback
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Normalize the history data to [0,1] for stability in calculations
    normalized_history = [num / 37 for num in history]
    
    # Calculate Lyapunov exponents for different segments of the history
    segment_lyapunovs = []
    segment_lengths = [50, 100, 200, 300]
    
    for length in segment_lengths:
        if len(normalized_history) >= length:
            # Calculate for overlapping segments
            for start in range(0, len(normalized_history) - length, length // 2):
                segment = normalized_history[start:start+length]
                lyapunov = calculate_lyapunov_exponent(segment)
                segment_lyapunovs.append((start, length, lyapunov))
    
    # Identify segments with highest chaos (positive Lyapunov exponents)
    chaotic_segments = sorted(segment_lyapunovs, key=lambda x: x[2], reverse=True)
    
    # Identify segments with lowest chaos (negative or near-zero Lyapunov exponents)
    stable_segments = sorted(segment_lyapunovs, key=lambda x: x[2])
    
    # Look at transitions between chaotic and stable regimes
    transitions = []
    
    for i in range(len(segment_lyapunovs) - 1):
        current = segment_lyapunovs[i]
        next_seg = segment_lyapunovs[i + 1]
        
        # If segments overlap and show a significant change in chaos
        if (current[0] + current[1] > next_seg[0] and 
            abs(current[2] - next_seg[2]) > 0.1):
            transitions.append((current[0] + current[1], abs(current[2] - next_seg[2])))
    
    # Score numbers based on their sensitivity as butterfly effect indicators
    number_scores = defaultdict(float)
    
    # 1. Score based on appearance in chaotic regimes
    for start, length, lyapunov in chaotic_segments[:5]:  # Top 5 most chaotic
        if lyapunov > 0:  # Positive Lyapunov = chaotic
            end = min(start + length, len(history))
            segment = history[start:end]
            
            # Count frequencies in chaotic regimes
            for num in segment:
                # Higher weight for higher chaos
                weight = lyapunov * 2
                number_scores[num] += weight
    
    # 2. Score based on appearance near regime transitions
    for transition_point, magnitude in transitions:
        if transition_point < len(history):
            # Look at numbers around the transition point
            window = history[max(0, transition_point-10):min(len(history), transition_point+10)]
            
            for i, num in enumerate(window):
                # Distance from transition point (closer = higher weight)
                distance = abs(i - min(10, transition_point))
                weight = magnitude * (1 - distance/10)
                number_scores[num] += weight
    
    # 3. Look for numbers that appear in both chaotic and stable regimes
    chaotic_nums = set()
    stable_nums = set()
    
    for start, length, lyapunov in chaotic_segments[:3]:
        end = min(start + length, len(history))
        chaotic_nums.update(history[start:end])
    
    for start, length, lyapunov in stable_segments[:3]:
        end = min(start + length, len(history))
        stable_nums.update(history[start:end])
    
    # Numbers appearing in both regimes might be special "bridge" numbers
    bridge_numbers = chaotic_nums.intersection(stable_nums)
    for num in bridge_numbers:
        number_scores[num] += 3.0
    
    # Convert scores to roulette number format
    recommended_numbers = []
    sorted_scores = sorted(number_scores.items(), key=lambda x: x[1], reverse=True)
    
    for wheel_num, _ in sorted_scores[:8]:
        recommended_numbers.append(str(wheel_num) if wheel_num != 37 else '00')
    
    # If we don't have enough (e.g., not enough data for analysis)
    if len(recommended_numbers) < 8:
        # Add some based on general frequency
        frequencies = defaultdict(int)
        for num in history:
            frequencies[num] += 1
        
        sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        for num, _ in sorted_freq:
            if str(num) if num != 37 else '00' not in recommended_numbers:
                recommended_numbers.append(str(num) if num != 37 else '00')
                if len(recommended_numbers) >= 8:
                    break
    
    return recommended_numbers

def analyze_bifurcation_points(history):
    """
    Identify bifurcation points where the system behavior changes.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 100:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Use a simplified model of the form x_{n+1} = r * x_n * (1 - x_n)
    # where r is a parameter and x_n is the normalized roulette number
    normalized_history = [num / 37 for num in history]
    
    # Find the parameter r that best fits each transition
    bifurcation_candidates = []
    
    window_size = 30  # Look at windows of 30 spins
    if len(normalized_history) >= window_size:
        for i in range(len(normalized_history) - window_size):
            window = normalized_history[i:i+window_size]
            
            # Try to find r that fits this window
            best_r = 1.0
            min_error = float('inf')
            
            for r in np.linspace(1.0, 4.0, 30):  # Test r values in logistic map range
                error = 0
                for j in range(len(window) - 1):
                    predicted = r * window[j] * (1 - window[j])
                    error += (predicted - window[j+1])**2
                
                if error < min_error:
                    min_error = error
                    best_r = r
            
            # Check if r is in a known bifurcation region
            bifurcation_regions = [
                (3.0, 3.45),  # Period-2 region
                (3.45, 3.54), # Period-4 region
                (3.54, 3.56), # Period-8 region
                (3.57, 4.0)   # Chaotic region
            ]
            
            for lower, upper in bifurcation_regions:
                if lower <= best_r <= upper:
                    # Find where this bifurcation ends
                    end_i = i + window_size
                    for j in range(i + window_size, min(len(normalized_history), i + 2*window_size)):
                        # Calculate r for one more point
                        next_r = 0
                        count = 0
                        for k in range(j-window_size, j-1):
                            if normalized_history[k] != 0 and normalized_history[k] != 1:
                                next_r += normalized_history[k+1] / (normalized_history[k] * (1 - normalized_history[k]))
                                count += 1
                        
                        if count > 0:
                            next_r /= count
                            
                            # If r changes significantly, we found the end of this regime
                            if abs(next_r - best_r) > 0.5:
                                end_i = j
                                break
                    
                    # Record this bifurcation regime
                    bifurcation_candidates.append({
                        'start': i,
                        'end': end_i,
                        'r': best_r,
                        'region': (lower, upper)
                    })
    
    # Score numbers based on their appearance near bifurcation points
    number_scores = defaultdict(float)
    
    for bifurcation in bifurcation_candidates:
        start = bifurcation['start']
        end = bifurcation['end']
        r = bifurcation['r']
        region_lower, region_upper = bifurcation['region']
        
        # Calculate transition strength - how close to exact bifurcation point
        region_width = region_upper - region_lower
        position_in_region = (r - region_lower) / region_width
        
        # Transitions at exact bifurcation points are most significant
        # e.g., r ~= 3.0, 3.45, 3.54, 3.57 are the main bifurcation points
        bifurcation_points = [3.0, 3.45, 3.54, 3.57]
        transition_strength = min([abs(r - bp) for bp in bifurcation_points])
        transition_weight = 1.0 / (transition_strength + 0.1)  # +0.1 to avoid division by zero
        
        # Look at numbers around the transition point
        for i in range(max(0, start-5), min(len(history), end+5)):
            num = history[i]
            
            # Higher weight for numbers closer to the transition
            distance_from_transition = min(abs(i - start), abs(i - end))
            distance_weight = 1.0 / (distance_from_transition + 1)
            
            number_scores[num] += transition_weight * distance_weight
    
    # Also analyze the current state of the system
    if len(history) >= window_size:
        recent_history = normalized_history[-window_size:]
        
        # Find current r
        current_r = 0
        count = 0
        for i in range(len(recent_history) - 1):
            if recent_history[i] != 0 and recent_history[i] != 1:
                current_r += recent_history[i+1] / (recent_history[i] * (1 - recent_history[i]))
                count += 1
        
        if count > 0:
            current_r /= count
            
            # Predict next values based on current r and the logistic map
            last_value = recent_history[-1]
            predictions = []
            
            # Generate several iterations
            for _ in range(20):
                next_value = current_r * last_value * (1 - last_value)
                # Convert back to roulette number
                predicted_num = round(next_value * 37)
                if predicted_num > 36:  # Handle overflow
                    predicted_num = 36
                predictions.append(predicted_num)
                last_value = next_value
            
            # Score predicted numbers
            for num in predictions:
                number_scores[num] += 2.0
    
    # Convert scores to roulette number format
    recommended_numbers = []
    sorted_scores = sorted(number_scores.items(), key=lambda x: x[1], reverse=True)
    
    for wheel_num, _ in sorted_scores[:8]:
        recommended_numbers.append(str(wheel_num) if wheel_num != 37 else '00')
    
    # If we don't have enough, add some based on general frequency
    if len(recommended_numbers) < 8:
        frequencies = defaultdict(int)
        for num in history:
            frequencies[num] += 1
        
        sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        for num, _ in sorted_freq:
            num_str = str(num) if num != 37 else '00'
            if num_str not in recommended_numbers:
                recommended_numbers.append(num_str)
                if len(recommended_numbers) >= 8:
                    break
    
    return recommended_numbers

def analyze_strange_attractors(history):
    """
    Map roulette outcomes onto a strange attractor and analyze patterns.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 100:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Create a 2D phase space representation
    # Use pairs of consecutive numbers as (x,y) coordinates
    points = []
    for i in range(len(history) - 1):
        x = history[i] / 37  # Normalize to [0,1]
        y = history[i+1] / 37
        points.append((x, y))
    
    # Create a density map for the phase space
    resolution = 10  # Grid resolution
    density_map = np.zeros((resolution, resolution))
    
    for x, y in points:
        # Map to grid coordinates
        grid_x = min(int(x * resolution), resolution - 1)
        grid_y = min(int(y * resolution), resolution - 1)
        density_map[grid_y, grid_x] += 1
    
    # Find attractors (high density regions)
    attractors = []
    threshold = np.mean(density_map) + np.std(density_map)
    
    for y in range(resolution):
        for x in range(resolution):
            if density_map[y, x] > threshold:
                # Convert grid coordinates back to roulette number space
                center_x = (x + 0.5) / resolution * 37
                center_y = (y + 0.5) / resolution * 37
                
                # Record this attractor
                attractors.append({
                    'x': center_x,
                    'y': center_y,
                    'density': density_map[y, x]
                })
    
    # Sort attractors by density
    attractors.sort(key=lambda a: a['density'], reverse=True)
    
    # Score numbers based on attractor proximity
    number_scores = defaultdict(float)
    
    # For each number, calculate its proximity to attractors
    for num in range(38):  # 0-37 (including 00 as 37)
        normalized = num / 37
        
        for attractor in attractors:
            # Distance to this attractor in phase space
            distance_x = min(abs(normalized - attractor['x']), 1 - abs(normalized - attractor['x']))
            distance_y = min(abs(normalized - attractor['y']), 1 - abs(normalized - attractor['y']))
            distance = np.sqrt(distance_x**2 + distance_y**2)
            
            # Score inversely proportional to distance, weighted by attractor density
            if distance < 0.2:  # Only consider close attractors
                number_scores[num] += attractor['density'] / (distance + 0.01)
    
    # Also look for basin boundaries (regions between attractors)
    if len(attractors) >= 2:
        for i in range(len(attractors)):
            for j in range(i+1, len(attractors)):
                a1 = attractors[i]
                a2 = attractors[j]
                
                # Calculate midpoint between attractors
                mid_x = (a1['x'] + a2['x']) / 2
                mid_y = (a1['y'] + a2['y']) / 2
                
                # Find numbers near this boundary
                for num in range(38):
                    normalized = num / 37
                    
                    # Distance to the boundary
                    distance_x = min(abs(normalized - mid_x), 1 - abs(normalized - mid_x))
                    distance_y = min(abs(normalized - mid_y), 1 - abs(normalized - mid_y))
                    distance = np.sqrt(distance_x**2 + distance_y**2)
                    
                    # Numbers near boundaries often lead to bifurcations
                    if distance < 0.1:
                        number_scores[num] += 2.0
    
    # Convert scores to roulette number format
    recommended_numbers = []
    sorted_scores = sorted(number_scores.items(), key=lambda x: x[1], reverse=True)
    
    for wheel_num, _ in sorted_scores[:8]:
        recommended_numbers.append(str(wheel_num) if wheel_num != 37 else '00')
    
    # If we don't have enough, add some based on proximity to recent outcomes
    if len(recommended_numbers) < 8:
        recent = history[-5:]  # Last 5 outcomes
        
        for num in range(38):
            if str(num) if num != 37 else '00' not in recommended_numbers:
                # Check proximity to recent outcomes
                for recent_num in recent:
                    if abs(num - recent_num) <= 3 or abs(num - recent_num) >= 34:
                        recommended_numbers.append(str(num) if num != 37 else '00')
                        break
                
                if len(recommended_numbers) >= 8:
                    break
    
    # If still not enough, add some based on general frequency
    if len(recommended_numbers) < 8:
        frequencies = defaultdict(int)
        for num in history:
            frequencies[num] += 1
        
        sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        for num, _ in sorted_freq:
            num_str = str(num) if num != 37 else '00'
            if num_str not in recommended_numbers:
                recommended_numbers.append(num_str)
                if len(recommended_numbers) >= 8:
                    break
    
    return recommended_numbers

def analyze_phase_space(history):
    """
    Analyze the phase space trajectories of roulette outcomes.
    
    Args:
        history: List of past outcomes as integers
        
    Returns:
        list: 8 recommended numbers
    """
    if len(history) < 100:
        # Not enough data for meaningful analysis
        return [str(n) for n in [0, 00, 1, 2, 3, 32, 35, 36]]
    
    # Create a 3D phase space using triplets of consecutive numbers
    points = []
    for i in range(len(history) - 2):
        x = history[i] / 37
        y = history[i+1] / 37
        z = history[i+2] / 37
        points.append((x, y, z))
    
    # Calculate trajectory statistics
    trajectory_length = 0
    for i in range(len(points) - 1):
        dx = points[i+1][0] - points[i][0]
        dy = points[i+1][1] - points[i][1]
        dz = points[i+1][2] - points[i][2]
        segment_length = np.sqrt(dx**2 + dy**2 + dz**2)
        trajectory_length += segment_length
    
    # Calculate average segment length
    avg_segment = trajectory_length / (len(points) - 1) if len(points) > 1 else 0
    
    # Identify recurring patterns in trajectories
    pattern_scores = defaultdict(float)
    
    # Look for repeating patterns of different lengths
    for pattern_length in range(2, 6):
        if len(history) < pattern_length * 2:
            continue
            
        pattern_counts = defaultdict(int)
        for i in range(len(history) - pattern_length + 1):
            pattern = tuple(history[i:i+pattern_length])
            pattern_counts[pattern] += 1
        
        # Identify significant patterns
        for pattern, count in pattern_counts.items():
            if count > 1:
                # Score based on pattern frequency and length
                pattern_weight = count * pattern_length / len(history)
                
                # Score the numbers in the pattern
                for num in pattern:
                    pattern_scores[num] += pattern_weight
    
    # Calculate recurrence statistics
    recurrence_matrix = np.zeros((38, 38))
    for i in range(len(history) - 1):
        curr = history[i]
        next_val = history[i+1]
        recurrence_matrix[next_val, curr] += 1
    
    # Normalize recurrence matrix
    row_sums = recurrence_matrix.sum(axis=1, keepdims=True)
    row_sums[row_sums == 0] = 1  # Avoid division by zero
    transition_probs = recurrence_matrix / row_sums
    
    # Calculate entropy of transitions for each number
    entropies = np.zeros(38)
    for i in range(38):
        probs = transition_probs[i]
        # Filter out zeros to avoid log(0)
        probs = probs[probs > 0]
        if len(probs) > 0:
            entropies[i] = -np.sum(probs * np.log2(probs))
    
    # Score numbers based on phase space analysis
    number_scores = defaultdict(float)
    
    # 1. Score based on pattern recurrence
    for num, score in pattern_scores.items():
        number_scores[num] += score * 3
    
    # 2. Score based on entropy (higher entropy = more unpredictable = possible bifurcation points)
    for num in range(38):
        number_scores[num] += entropies[num] * 2
    
    # 3. Score based on recent trajectory direction
    if len(history) >= 3:
        # Get the most recent triplet
        recent_x = history[-3] / 37
        recent_y = history[-2] / 37
        recent_z = history[-1] / 37
        
        # Calculate velocity vector
        vx = recent_y - recent_x
        vy = recent_z - recent_y
        
        # Predict next position based on velocity
        predicted_x = recent_z + vx
        predicted_y = recent_z + vy
        
        # Wrap around if necessary
        predicted_x = predicted_x % 1
        predicted_y = predicted_y % 1
        
        # Convert to roulette numbers
        predicted_num1 = round(predicted_x * 37)
        predicted_num2 = round(predicted_y * 37)
        
        # Adjust for valid range
        predicted_num1 = max(0, min(37, predicted_num1))
        predicted_num2 = max(0, min(37, predicted_num2))
        
        # Boost scores for predicted numbers
        number_scores[predicted_num1] += 5
        number_scores[predicted_num2] += 5
    
    # Convert scores to roulette number format
    recommended_numbers = []
    sorted_scores = sorted(number_scores.items(), key=lambda x: x[1], reverse=True)
    
    for wheel_num, _ in sorted_scores[:8]:
        recommended_numbers.append(str(wheel_num) if wheel_num != 37 else '00')
    
    # If we don't have enough, add some based on general frequency
    if len(recommended_numbers) < 8:
        frequencies = defaultdict(int)
        for num in history:
            frequencies[num] += 1
        
        sorted_freq = sorted(frequencies.items(), key=lambda x: x[1], reverse=True)
        for num, _ in sorted_freq:
            num_str = str(num) if num != 37 else '00'
            if num_str not in recommended_numbers:
                recommended_numbers.append(num_str)
                if len(recommended_numbers) >= 8:
                    break
    
    return recommended_numbers 