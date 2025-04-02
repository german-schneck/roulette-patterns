#!/usr/bin/env python3
"""
Martingale Strategy Analyzer
Implementation of the classic Martingale betting system, one of the oldest 
and most famous betting strategies in gambling history.
"""

import numpy as np
import random
from collections import defaultdict

def analyze_martingale_strategy(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze the Martingale betting strategy on roulette.
    
    The classic Martingale system involves:
    1. Start with a base bet on an even-money bet (red/black, odd/even, etc.)
    2. After each loss, double the bet
    3. After each win, return to the base bet
    
    This adaptation applies the core concept to specific number selection.
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nGenerando combinación con sistema Martingala clásico...")
    
    # Define various Martingale approaches to test
    approaches = [
        # Red numbers - classic red/black approach
        ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36'],
        # Black numbers
        ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35'],
        # Even numbers (Pares)
        ['2', '4', '6', '8', '10', '12', '14', '16', '18', '20', '22', '24', '26', '28', '30', '32', '34', '36'],
        # Odd numbers (Impares)
        ['1', '3', '5', '7', '9', '11', '13', '15', '17', '19', '21', '23', '25', '27', '29', '31', '33', '35'],
        # First half (1-18)
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18'],
        # Second half (19-36)
        ['19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
        # First dozen (1-12)
        ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
        # Second dozen (13-24)
        ['13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24'],
        # Third dozen (25-36)
        ['25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36'],
    ]
    
    # Track best performance for pure Martingale
    best_approach = None
    best_win_rate = 0
    best_performance = 0
    
    # Simulate each classic Martingale approach
    for bet_numbers in approaches:
        # Create descriptive name
        if len(bet_numbers) == 18:
            if '1' in bet_numbers and '3' in bet_numbers:
                approach_name = "Red numbers"
            elif '2' in bet_numbers and '4' in bet_numbers:
                approach_name = "Black numbers"
            elif '2' in bet_numbers and '4' in bet_numbers and '6' in bet_numbers:
                approach_name = "Even numbers"
            else:
                approach_name = "Odd numbers"
        elif len(bet_numbers) == 18 and '1' in bet_numbers and '2' in bet_numbers:
            approach_name = "First half (1-18)"
        elif len(bet_numbers) == 18:
            approach_name = "Second half (19-36)"
        elif len(bet_numbers) == 12 and '1' in bet_numbers:
            approach_name = "First dozen (1-12)"
        elif len(bet_numbers) == 12 and '13' in bet_numbers:
            approach_name = "Second dozen (13-24)"
        else:
            approach_name = "Third dozen (25-36)"
            
        # Test this approach with martingale progression
        results = validation_analyzer.spin_batch(validation_spins // 3)
        
        wins = 0
        base_unit = 1
        current_bet = base_unit
        bankroll = 100 * base_unit  # Start with 100 units
        max_bankroll = bankroll
        min_bankroll = bankroll
        
        for result in results:
            if bankroll < current_bet:
                # Cannot place bet, broke!
                break
                
            # Place bet
            bankroll -= current_bet
            
            if result in bet_numbers:
                # Win!
                wins += 1
                if len(bet_numbers) == 18:
                    # Even-money bet (1:1 payout)
                    bankroll += current_bet * 2
                elif len(bet_numbers) == 12:
                    # Dozen bet (2:1 payout)
                    bankroll += current_bet * 3
                
                # Reset to base bet after win
                current_bet = base_unit
            else:
                # Loss - double bet (Martingale progression)
                current_bet *= 2
                
                # Cap the maximum bet at 256 units to be realistic
                if current_bet > 256 * base_unit:
                    current_bet = base_unit  # Reset after cap
            
            # Track bankroll stats
            max_bankroll = max(max_bankroll, bankroll)
            min_bankroll = min(min_bankroll, bankroll)
            
        # Calculate win rate and performance
        win_rate = (wins / len(results)) * 100
        coverage = len(bet_numbers) / 38 * 100
        performance = (win_rate / coverage - 1) * 100
        
        # Log results
        print(f"Validation completed for Martingale on {approach_name}: {wins} hits from {len(results)} spins ({win_rate:.2f}%)")
        print(f"Final bankroll: {bankroll} units (Min: {min_bankroll}, Max: {max_bankroll})")
        print(f"Performance vs random: {performance:+.2f}%")
        
        # Track best approach
        if win_rate > best_win_rate:
            best_approach = approach_name
            best_win_rate = win_rate
            best_performance = performance
            best_bet_numbers = bet_numbers
    
    # For roulette number selection, we need 8 specific numbers
    # We'll select numbers from the best even-money approach
    if sorted_numbers:
        # Use top numbers that are also in our best approach
        martingale_numbers = []
        for num in sorted_numbers:
            if num in best_bet_numbers and len(martingale_numbers) < 8:
                martingale_numbers.append(num)
        
        # If we don't have 8 numbers yet, add top numbers from best approach
        if len(martingale_numbers) < 8:
            for num in best_bet_numbers:
                if num not in martingale_numbers and len(martingale_numbers) < 8:
                    martingale_numbers.append(num)
    else:
        # Without sorted numbers, just take 8 random numbers from best approach
        martingale_numbers = random.sample(best_bet_numbers, min(8, len(best_bet_numbers)))
    
    # Validate the final selection
    print("\nValidando combinación Martingala final...")
    from src.utils.analysis import validate_numbers_performance
    martingale_win_rate = validate_numbers_performance(
        validation_analyzer, martingale_numbers, validation_spins)
    
    martingale_coverage = len(martingale_numbers) / 38 * 100
    martingale_performance = (martingale_win_rate / martingale_coverage - 1) * 100
    
    print(f"Combinación Martingala: {', '.join(martingale_numbers)}")
    print(f"Tasa de victoria: {martingale_win_rate:.2f}%")
    print(f"Rendimiento: {martingale_performance:+.2f}%")
    
    # Return results
    return {
        'martingale_numbers': martingale_numbers,
        'martingale_win_rate': martingale_win_rate,
        'martingale_performance': martingale_performance,
        'best_approach': best_approach,
        'progression_type': 'Clásica - Duplicar después de cada pérdida'
    } 