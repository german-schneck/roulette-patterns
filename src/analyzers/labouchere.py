#!/usr/bin/env python3
"""
Labouchere Strategy Analyzer

Implementation of the Labouchere (also known as Split Martingale or Cancellation) 
betting strategy for roulette.
"""

import random
from src.utils.analysis import validate_numbers_performance

def analyze_labouchere_strategy(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze the Labouchere betting strategy for roulette.
    
    The Labouchere system uses a sequence of numbers to determine bet sizes.
    After a win, the first and last numbers are removed from the sequence.
    After a loss, the bet amount is added to the end of the sequence.
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nAnalyzing Labouchere betting strategy...")
    
    # Simulate Labouchere strategy
    bankroll = 1000  # Initial bankroll
    base_unit = 10   # Base betting unit
    
    # Initial sequence (traditional Labouchere often starts with 1-2-3-4-5-6)
    # We'll scale it by the base unit
    initial_sequence = [1, 2, 3, 4, 5, 6]
    
    # Betting on red (18/38 chance of winning on American roulette)
    win_probability = 18/38
    payout_multiplier = 2  # Even money bet
    
    results = []
    win_count = 0
    loss_count = 0
    max_drawdown = 0
    peak_bankroll = bankroll
    
    # Run simulation
    for _ in range(validation_spins):
        # Reset sequence if empty or if we have a very long sequence (which can happen after many losses)
        if not initial_sequence or len(initial_sequence) > 20:
            initial_sequence = [1, 2, 3, 4, 5, 6]
        
        # Calculate bet amount (sum of first and last numbers in sequence)
        current_sequence = initial_sequence.copy()
        if len(current_sequence) == 1:
            bet_amount = current_sequence[0] * base_unit
        else:
            bet_amount = (current_sequence[0] + current_sequence[-1]) * base_unit
        
        # Ensure bet doesn't exceed bankroll
        bet_amount = min(bet_amount, bankroll)
        
        # Skip this round if bet would be zero
        if bet_amount <= 0:
            continue
        
        # Simulate bet outcome
        if random.random() < win_probability:
            # Win
            bankroll += bet_amount
            win_count += 1
            
            # Remove first and last numbers from sequence (Labouchere rule)
            if len(current_sequence) >= 2:
                initial_sequence = current_sequence[1:-1]
            else:
                initial_sequence = []
        else:
            # Loss
            bankroll -= bet_amount
            loss_count += 1
            
            # Add the bet amount (in units) to the end of the sequence
            bet_units = bet_amount // base_unit
            initial_sequence.append(bet_units)
        
        # Track results
        results.append(bankroll)
        
        # Update peak and drawdown
        peak_bankroll = max(peak_bankroll, bankroll)
        drawdown = peak_bankroll - bankroll
        max_drawdown = max(max_drawdown, drawdown)
        
        # Stop if bankrupt
        if bankroll <= 0:
            break
    
    # Calculate performance metrics
    final_bankroll = bankroll
    profit = final_bankroll - 1000
    profit_percentage = (profit / 1000) * 100
    win_rate = win_count / (win_count + loss_count) if (win_count + loss_count) > 0 else 0
    
    # Adjust performance by typical house edge for comparison
    typical_house_edge = -5.26  # American roulette house edge percentage
    relative_performance = profit_percentage - typical_house_edge
    
    print(f"Labouchere Strategy Results:")
    print(f"Final Bankroll: ${final_bankroll:.2f}")
    print(f"Profit/Loss: ${profit:+.2f} ({profit_percentage:+.2f}%)")
    print(f"Performance vs. Random: {relative_performance:+.2f}%")
    print(f"Win Rate: {win_rate:.2f}")
    print(f"Max Drawdown: ${max_drawdown:.2f}")
    
    return {
        'labouchere_final_bankroll': final_bankroll,
        'labouchere_profit': profit,
        'labouchere_profit_percentage': profit_percentage,
        'labouchere_performance': relative_performance,
        'labouchere_win_rate': win_rate,
        'labouchere_max_drawdown': max_drawdown
    } 