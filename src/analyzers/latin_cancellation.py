#!/usr/bin/env python3
"""
Latin Cancellation Analysis Module.

This module implements the Latin Cancellation strategy, a variant of the Labouchere system
that is popular in Latin American casinos, particularly in Argentina and Brazil.
"""
import numpy as np
from collections import defaultdict


def analyze_latin_cancellation(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze optimal number selection using the Latin Cancellation strategy.
    
    This variant of the Labouchere system adjusts the sequence based on pattern recognition
    and is popular in Latin American casinos. It involves a special sequence method
    to identify numbers with higher probability.
    
    Args:
        analyzer: The main roulette analyzer instance
        validation_analyzer: Analyzer used for validation
        validation_spins: Number of spins to use for validation
        sorted_numbers: List of numbers sorted by performance (optional)
    
    Returns:
        dict: Results of the Latin Cancellation analysis including:
            - cancellation_numbers: List of numbers identified by the cancellation system
            - cancellation_win_rate: Win rate achieved with these numbers
            - cancellation_performance: Performance vs expected random outcome
    """
    print("\nPerforming Latin Cancellation analysis...")
    
    # Get historical spin data
    history = analyzer.history[-3000:]
    
    # Latin Cancellation systems focus on specific sequences
    # In traditional Labouchere, sequences are created based on past results
    # In this Latin American variant, we analyze sequence patterns
    
    # Track consecutive patterns (similar to the "columnar" system used in Uruguay)
    sequence_analysis = {}
    pattern_length = 5  # Analyze patterns of 5 consecutive results
    
    # Analyze patterns in historical data
    for i in range(len(history) - pattern_length):
        sequence = tuple(history[i:i+pattern_length])
        next_number = history[i+pattern_length]
        
        if sequence in sequence_analysis:
            sequence_analysis[sequence].append(next_number)
        else:
            sequence_analysis[sequence] = [next_number]
    
    # Identify patterns with consistent follow-up numbers
    consistent_patterns = {}
    for sequence, results in sequence_analysis.items():
        # Count occurrences of each result
        result_counts = defaultdict(int)
        for result in results:
            result_counts[result] += 1
        
        # Calculate the most common follow-up number and its consistency
        if results:
            most_common = max(result_counts.items(), key=lambda x: x[1])
            consistency = most_common[1] / len(results)
            
            if consistency > 0.3:  # At least 30% consistency
                consistent_patterns[sequence] = {
                    'follow_up': most_common[0],
                    'consistency': consistency,
                    'count': most_common[1]
                }
    
    # Sort patterns by consistency
    sorted_patterns = sorted(
        consistent_patterns.items(), 
        key=lambda x: (x[1]['consistency'], x[1]['count']), 
        reverse=True
    )
    
    # Print top consistent patterns
    print("Top patterns identified by Latin Cancellation analysis:")
    for i, (pattern, info) in enumerate(sorted_patterns[:5]):
        print(f"  Pattern {i+1}: {pattern}")
        print(f"    Most likely to be followed by: {info['follow_up']}")
        print(f"    Consistency: {info['consistency']*100:.1f}%")
    
    # Create a cancellation sequence - in the Latin Cancellation method, 
    # we identify numbers that appear frequently in patterns
    pattern_numbers = defaultdict(int)
    
    # Count numbers appearing in top patterns
    for pattern, info in sorted_patterns[:15]:  # Use top 15 patterns
        # Count the pattern numbers
        for num in pattern:
            pattern_numbers[num] += 1
        
        # Also count the follow-up number with higher weight
        pattern_numbers[info['follow_up']] += 2
    
    # Select top numbers from pattern analysis
    top_pattern_numbers = sorted(
        pattern_numbers.items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    # If we have sorted performance numbers, combine with pattern analysis
    if sorted_numbers and len(sorted_numbers) > 0:
        # Create a scoring system that combines pattern presence and historical performance
        combined_scores = {}
        
        # Create a set of top performers for quick lookups
        top_performer_set = set(sorted_numbers[:20])
        
        for num, pattern_score in top_pattern_numbers:
            # Calculate a combined score favoring numbers that appear in both lists
            performance_bonus = 3 if num in top_performer_set else 0
            combined_scores[num] = pattern_score + performance_bonus
        
        # Fill in scores for top performers that aren't in patterns
        for num in top_performer_set:
            if num not in combined_scores:
                combined_scores[num] = 1  # Lower base score
        
        # Select top 8 numbers by combined score
        cancellation_numbers = [
            num for num, _ in sorted(
                combined_scores.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:8]
        ]
    else:
        # Without performance data, use top 8 numbers from pattern analysis
        cancellation_numbers = [num for num, _ in top_pattern_numbers[:8]]
    
    # Validate the Latin Cancellation selection
    print(f"\nValidating Latin Cancellation numbers: {cancellation_numbers}")
    
    # Calculate win rate with these numbers
    wins = 0
    for _ in range(validation_spins):
        result, color = validation_analyzer.spin()  # Desempaquetar tupla correctamente
        if result in cancellation_numbers:
            wins += 1
    
    cancellation_win_rate = (wins / validation_spins) * 100
    
    # Calculate performance metrics
    cancellation_coverage = len(cancellation_numbers) / 38 * 100
    cancellation_performance = (cancellation_win_rate / cancellation_coverage - 1) * 100
    
    print(f"Latin Cancellation Analysis results:")
    print(f"  Numbers: {cancellation_numbers}")
    print(f"  Win rate: {cancellation_win_rate:.2f}%")
    print(f"  Performance vs random: {cancellation_performance:+.2f}%")
    
    return {
        "cancellation_numbers": cancellation_numbers,
        "cancellation_win_rate": cancellation_win_rate,
        "cancellation_performance": cancellation_performance
    } 