#!/usr/bin/env python3
"""
D'Alembert Strategy Analyzer

Implementation of the D'Alembert betting strategy for roulette,
a more conservative progression system than Martingale.
"""

import random
from src.utils.analysis import validate_numbers_performance

def analyze_dalembert_strategy(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze the D'Alembert betting strategy for roulette.
    
    The D'Alembert strategy increases bet by one unit after a loss 
    and decreases it by one unit after a win.
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nAnalyzing D'Alembert betting strategy...")
    
    # Simulate D'Alembert strategy
    bankroll = 1000  # Initial bankroll
    base_unit = 10   # Base betting unit
    current_bet = base_unit
    
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
        # Ensure bet doesn't exceed bankroll
        current_bet = min(current_bet, bankroll)
        
        # Simulate bet outcome
        if random.random() < win_probability:
            # Win
            bankroll += current_bet
            win_count += 1
            # Decrease bet by one unit, but not below base unit
            current_bet = max(base_unit, current_bet - base_unit)
        else:
            # Loss
            bankroll -= current_bet
            loss_count += 1
            # Increase bet by one unit
            current_bet += base_unit
        
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
    
    print(f"D'Alembert Strategy Results:")
    print(f"Final Bankroll: ${final_bankroll:.2f}")
    print(f"Profit/Loss: ${profit:+.2f} ({profit_percentage:+.2f}%)")
    print(f"Performance vs. Random: {relative_performance:+.2f}%")
    print(f"Win Rate: {win_rate:.2f}")
    print(f"Max Drawdown: ${max_drawdown:.2f}")
    
    return {
        'dalembert_final_bankroll': final_bankroll,
        'dalembert_profit': profit,
        'dalembert_profit_percentage': profit_percentage,
        'dalembert_performance': relative_performance,
        'dalembert_win_rate': win_rate,
        'dalembert_max_drawdown': max_drawdown
    } 