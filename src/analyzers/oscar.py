#!/usr/bin/env python3
"""
Oscar's Grind Strategy Analyzer

Implementation of the Oscar's Grind (also known as Hoyle's Press) betting strategy for roulette,
a conservative system designed to recover losses gradually.
"""

import random
from src.utils.analysis import validate_numbers_performance

def analyze_oscar_grind_strategy(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze the Oscar's Grind betting strategy for roulette.
    
    The Oscar's Grind strategy increases bets by one unit after each win
    but keeps the bet the same after a loss. The goal is to win exactly one unit
    in each cycle.
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nAnalyzing Oscar's Grind betting strategy...")
    
    # Simulate Oscar's Grind strategy
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
    
    # Oscar's Grind cycle tracking
    cycle_profit = 0
    
    # Run simulation
    for _ in range(validation_spins):
        # Ensure bet doesn't exceed bankroll
        current_bet = min(current_bet, bankroll)
        
        # Oscar's Grind rule: never bet more than what would make the cycle profit equal to 1 unit
        if cycle_profit + current_bet > base_unit:
            current_bet = base_unit - cycle_profit
        
        # Simulate bet outcome
        if random.random() < win_probability:
            # Win
            win_amount = current_bet
            bankroll += win_amount
            win_count += 1
            cycle_profit += win_amount
            
            # Oscar's Grind rule: increase bet by one unit after a win, unless we completed a cycle
            if cycle_profit >= base_unit:
                # Cycle complete - reset
                cycle_profit = 0
                current_bet = base_unit
            else:
                # Increase bet by one unit, but never more than the base unit
                current_bet = min(current_bet + base_unit, 4 * base_unit)
        else:
            # Loss
            bankroll -= current_bet
            loss_count += 1
            cycle_profit -= current_bet
            
            # Oscar's Grind rule: keep the same bet after a loss
            # Do nothing to current_bet
        
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
    
    print(f"Oscar's Grind Strategy Results:")
    print(f"Final Bankroll: ${final_bankroll:.2f}")
    print(f"Profit/Loss: ${profit:+.2f} ({profit_percentage:+.2f}%)")
    print(f"Performance vs. Random: {relative_performance:+.2f}%")
    print(f"Win Rate: {win_rate:.2f}")
    print(f"Max Drawdown: ${max_drawdown:.2f}")
    
    return {
        'oscar_final_bankroll': final_bankroll,
        'oscar_profit': profit,
        'oscar_profit_percentage': profit_percentage,
        'oscar_performance': relative_performance,
        'oscar_win_rate': win_rate,
        'oscar_max_drawdown': max_drawdown
    } 