#!/usr/bin/env python3
"""
Martingale Strategy Analyzer

Implementation of the classic Martingale betting strategy for roulette,
one of the oldest and most well-known progression systems.
"""

import random
from src.utils.analysis import validate_numbers_performance

def analyze_martingale_strategy(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze the Martingale betting strategy for roulette.
    
    The Martingale strategy doubles the bet after each loss,
    with the goal of recovering all past losses plus a profit equal to the original bet.
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nAnalyzing Martingale betting strategy...")
    
    # Simulate Martingale strategy
    bankroll = 1000  # Initial bankroll
    base_bet = 10    # Starting bet
    current_bet = base_bet
    
    # Betting on red (18/38 chance of winning on American roulette)
    win_probability = 18/38
    payout_multiplier = 2  # Even money bet
    
    results = []
    win_count = 0
    loss_count = 0
    max_drawdown = 0
    peak_bankroll = bankroll
    consecutive_losses = 0
    max_consecutive_losses = 0
    
    # Run simulation
    for _ in range(validation_spins):
        # Ensure bet doesn't exceed bankroll
        current_bet = min(current_bet, bankroll)
        
        # Simulate bet outcome
        if random.random() < win_probability:
            # Win
            bankroll += current_bet
            win_count += 1
            consecutive_losses = 0
            current_bet = base_bet  # Reset to base bet after a win
        else:
            # Loss
            bankroll -= current_bet
            loss_count += 1
            consecutive_losses += 1
            if consecutive_losses > max_consecutive_losses:
                max_consecutive_losses = consecutive_losses
            current_bet *= 2  # Double bet after a loss (Martingale rule)
        
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
    
    print(f"Martingale Strategy Results:")
    print(f"Final Bankroll: ${final_bankroll:.2f}")
    print(f"Profit/Loss: ${profit:+.2f} ({profit_percentage:+.2f}%)")
    print(f"Performance vs. Random: {relative_performance:+.2f}%")
    print(f"Win Rate: {win_rate:.2f}")
    print(f"Max Drawdown: ${max_drawdown:.2f}")
    print(f"Max Consecutive Losses: {max_consecutive_losses}")
    
    return {
        'martingale_final_bankroll': final_bankroll,
        'martingale_profit': profit,
        'martingale_profit_percentage': profit_percentage,
        'martingale_performance': relative_performance,
        'martingale_win_rate': win_rate,
        'martingale_max_drawdown': max_drawdown,
        'martingale_max_consecutive_losses': max_consecutive_losses
    } 