#!/usr/bin/env python3
"""
Chaotic Domain Analysis Module.

This module analyzes chaotic patterns in roulette outcomes using advanced
mathematical concepts from chaos theory and nonlinear dynamics.
"""
import numpy as np
from collections import defaultdict
from src.utils.analysis import validate_numbers_performance

def analyze_chaotic_domain(analyzer, validation_analyzer, validation_spins, number_hits=None):
    """
    Analyze chaotic patterns in roulette outcomes to identify strange attractors.
    
    While roulette is fundamentally a random process, chaos theory suggests that
    complex systems can exhibit patterns within randomness that are based on sensitive
    dependence on initial conditions. This analysis attempts to identify such patterns.
    
    Args:
        analyzer: The main roulette analyzer instance
        validation_analyzer: Analyzer used for validation
        validation_spins: Number of spins to use for validation
        number_hits: Dictionary of hit counts for each number (optional)
    
    Returns:
        dict: Results of the chaotic domain analysis including:
            - chaotic_numbers: List of numbers from the identified chaotic domain
            - chaotic_win_rate: Win rate achieved with these numbers
            - chaotic_performance: Performance vs expected random outcome
    """
    print("\nPerforming chaotic domain analysis...")
    
    # Get historical spin data
    history = analyzer.history[-5000:]  # Use last 5000 spins for better pattern detection
    
    if len(history) < 1000:
        print("Insufficient historical data for chaotic analysis")
        return {
            "chaotic_numbers": [],
            "chaotic_win_rate": 0,
            "chaotic_performance": 0
        }
    
    # In chaos theory, we look for strange attractors - regions where outcomes
    # tend to cluster despite the underlying randomness
    
    # 1. Phase space reconstruction
    # Convert the sequence of numbers into a multi-dimensional phase space
    embedding_dimension = 3  # Embed in 3D space
    time_delay = 2  # Use every 2nd value
    
    # Create phase space vectors
    phase_vectors = []
    for i in range(len(history) - (embedding_dimension-1) * time_delay):
        vector = [history[i + j*time_delay] for j in range(embedding_dimension)]
        phase_vectors.append(vector)
    
    # 2. Recurrence analysis
    # Look for recurring patterns in the phase space
    recurrence_counts = defaultdict(int)
    
    # Count recurrences of similar patterns
    for i, vec1 in enumerate(phase_vectors):
        for j in range(i+1, min(i+100, len(phase_vectors))):  # Look ahead up to 100 steps
            vec2 = phase_vectors[j]
            # Check if vectors are similar (contain same numbers in any order)
            if sorted(vec1) == sorted(vec2):
                # Record the number that follows this pattern
                if j+1 < len(history):
                    recurrence_counts[history[j+1]] += 1
    
    # 3. Lyapunov exponent approximation
    # In chaos theory, positive Lyapunov exponents indicate chaos
    # We'll approximate this by measuring how quickly similar states diverge
    
    divergence_rates = defaultdict(list)
    for i, vec1 in enumerate(phase_vectors[:-20]):  # Leave room to track future states
        for j in range(i+1, min(i+50, len(phase_vectors)-20)):
            # Find similar initial states
            if sum(1 for a, b in zip(vec1, phase_vectors[j]) if a == b) >= 2:
                # Track numbers that appear after increasingly divergent future states
                for steps in range(1, 20):
                    if i+steps < len(history) and j+steps < len(history):
                        divergence_rates[history[i+steps]].append(abs(i-j)/steps)
    
    # Calculate average divergence rate for each number
    average_divergence = {}
    for num, rates in divergence_rates.items():
        if rates:
            average_divergence[num] = sum(rates) / len(rates)
    
    # 4. Identify strange attractors
    # Numbers with high recurrence but low divergence are potential attractors
    attractor_scores = {}
    for num in analyzer.numbers:
        recurrence_score = recurrence_counts.get(num, 0)
        divergence_score = average_divergence.get(num, 0)
        
        if divergence_score > 0:
            # Higher recurrence and lower divergence indicate stronger attractors
            attractor_scores[num] = recurrence_score / (1 + divergence_score)
        else:
            attractor_scores[num] = recurrence_score
    
    # Sort numbers by attractor score
    sorted_attractors = sorted(attractor_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Print top attractors
    print("Top strange attractors identified:")
    for num, score in sorted_attractors[:10]:
        print(f"  Number {num}: Attractor score {score:.2f}")
    
    # Identify the chaotic domain (numbers with highest attractor scores)
    chaotic_domain = [num for num, _ in sorted_attractors[:8]]
    
    # Incorporate hit frequency data if available
    if number_hits:
        # Blend chaotic analysis with empirical hit frequency
        blended_scores = {}
        total_hits = sum(number_hits.values())
        
        for num in analyzer.numbers:
            # 70% weight to chaotic analysis, 30% to empirical frequency
            attractor_score = attractor_scores.get(num, 0)
            hit_frequency = number_hits.get(num, 0) / total_hits if total_hits > 0 else 0
            
            blended_scores[num] = 0.7 * attractor_score + 0.3 * hit_frequency * 100
        
        # Re-sort based on blended scores
        sorted_blended = sorted(blended_scores.items(), key=lambda x: x[1], reverse=True)
        chaotic_numbers = [num for num, _ in sorted_blended[:8]]
    else:
        chaotic_numbers = chaotic_domain
    
    # Validate the chaotic domain analysis
    print(f"\nValidating chaotic domain numbers: {chaotic_numbers}")
    
    # Calculate win rate with these numbers
    wins = 0
    for _ in range(validation_spins):
        result, color = validation_analyzer.spin()  # Desempaquetar tupla correctamente
        if result in chaotic_numbers:
            wins += 1
    
    chaotic_win_rate = (wins / validation_spins) * 100
    
    # Calculate performance metrics
    chaotic_coverage = len(chaotic_numbers) / 38 * 100
    chaotic_performance = (chaotic_win_rate / chaotic_coverage - 1) * 100
    
    print(f"Chaotic Domain Analysis results:")
    print(f"  Numbers: {chaotic_numbers}")
    print(f"  Win rate: {chaotic_win_rate:.2f}%")
    print(f"  Performance vs random: {chaotic_performance:+.2f}%")
    
    return {
        "chaotic_numbers": chaotic_numbers,
        "chaotic_win_rate": chaotic_win_rate,
        "chaotic_performance": chaotic_performance
    } 