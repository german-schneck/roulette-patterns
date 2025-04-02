#!/usr/bin/env python3
"""
Dealer Signature Analysis Module.

This module analyzes patterns in dealer behavior to identify tendencies
in roulette spins. Based on professional techniques used in Las Vegas casinos.
"""
import numpy as np
from collections import defaultdict


def analyze_dealer_signature(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze dealer signature patterns to identify biased landing zones.
    
    In real casinos, dealers develop unconscious patterns in their spin technique,
    resulting in somewhat predictable landing areas. This simulation models that behavior.
    
    Args:
        analyzer: The main roulette analyzer instance
        validation_analyzer: Analyzer used for validation
        validation_spins: Number of spins to use for validation
        sorted_numbers: List of numbers sorted by performance (optional)
    
    Returns:
        dict: Results of the dealer signature analysis including:
            - signature_numbers: List of numbers from the identified signature pattern
            - signature_win_rate: Win rate achieved with these numbers
            - signature_performance: Performance vs expected random outcome
    """
    # Define virtual dealer profiles with biased release points and velocities
    dealer_profiles = [
        {"name": "Dealer A", "sector_bias": [0, 32, 15, 19], "consistency": 0.65},
        {"name": "Dealer B", "sector_bias": [26, 3, 35, 12], "consistency": 0.58},
        {"name": "Dealer C", "sector_bias": [14, 31, 9, 22], "consistency": 0.72},
    ]
    
    # Extract the wheel order from the analyzer
    wheel_order = analyzer.wheel_order
    
    # Define sectors (groups of adjacent numbers on the wheel)
    sectors = []
    for i in range(0, len(wheel_order), 4):
        sector = wheel_order[i:i+4]
        if len(sector) == 4:  # Only use complete sectors
            sectors.append(sector)
    
    # Analyze spin results from history to identify dealer signature
    spin_history = analyzer.history[-1000:]  # Use last 1000 spins
    
    # Count occurrences of numbers in each sector
    sector_hits = defaultdict(int)
    for spin in spin_history:
        for i, sector in enumerate(sectors):
            if spin in sector:
                sector_hits[i] += 1
    
    # Identify the most frequently hit sectors (simulating dealer signature)
    top_sectors = sorted(sector_hits.items(), key=lambda x: x[1], reverse=True)[:3]
    
    print(f"Top sectors identified in dealer signature analysis:")
    for i, (sector_idx, hits) in enumerate(top_sectors):
        sector = sectors[sector_idx]
        print(f"  Sector {i+1}: {sector} - {hits} hits")
    
    # Create combined list of numbers from top sectors
    signature_candidates = []
    for sector_idx, _ in top_sectors:
        signature_candidates.extend(sectors[sector_idx])
    
    # If we have sorted performance numbers, prioritize those that are also in signature zones
    if sorted_numbers and len(sorted_numbers) > 0:
        signature_numbers = []
        # First add numbers that are both in top performers and signature zones
        for num in sorted_numbers:
            if num in signature_candidates and len(signature_numbers) < 8:
                signature_numbers.append(num)
        
        # If we don't have enough numbers, add more from signature zones
        remaining = 8 - len(signature_numbers)
        if remaining > 0:
            for num in signature_candidates:
                if num not in signature_numbers and len(signature_numbers) < 8:
                    signature_numbers.append(num)
    else:
        # Without performance data, use top 8 unique numbers from signature zones
        signature_numbers = list(dict.fromkeys(signature_candidates))[:8]
    
    # Validate the signature pattern
    print(f"\nValidating dealer signature numbers: {signature_numbers}")
    
    # Calculate win rate with these numbers
    wins = 0
    for _ in range(validation_spins):
        result, color = validation_analyzer.spin()  # Desempaquetar tupla correctamente
        if result in signature_numbers:
            wins += 1
    
    signature_win_rate = (wins / validation_spins) * 100
    
    # Calculate performance metrics
    signature_coverage = len(signature_numbers) / 38 * 100
    signature_performance = (signature_win_rate / signature_coverage - 1) * 100
    
    print(f"Dealer Signature Analysis results:")
    print(f"  Numbers: {signature_numbers}")
    print(f"  Win rate: {signature_win_rate:.2f}%")
    print(f"  Performance vs random: {signature_performance:+.2f}%")
    
    return {
        "signature_numbers": signature_numbers,
        "signature_win_rate": signature_win_rate,
        "signature_performance": signature_performance
    } 