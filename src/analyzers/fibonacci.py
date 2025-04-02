#!/usr/bin/env python3
"""
Fibonacci sequence analysis for roulette wheel positions.
"""
from src.utils.analysis import validate_numbers_performance

def analyze_fibonacci_patterns(analyzer, validation_analyzer, validation_spins, sorted_numbers):
    """
    Analyze patterns using Fibonacci sequence to select positions on the wheel.
    
    Args:
        analyzer: Primary AdvancedRouletteAnalyzer instance
        validation_analyzer: Validation AdvancedRouletteAnalyzer instance
        validation_spins: Number of spins to use for validation
        sorted_numbers: List of numbers sorted by performance
        
    Returns:
        dict: Results with best Fibonacci sequence data
    """
    print("\nGenerando combinación con secuencia Fibonacci...")
    # Usar números Fibonacci para seleccionar posiciones en la rueda
    fib_sequence = [1, 2, 3, 5, 8, 13, 21, 34]
    fibonacci_numbers = []
    
    # Seleccionar punto de partida con mejor Z-score
    start_positions = sorted_numbers[:5]
    best_fib_rate = 0
    best_fib_combination = []
    
    for start_num in start_positions:
        if start_num in analyzer.wheel_order:
            start_idx = analyzer.wheel_order.index(start_num)
            fib_nums = []
            for offset in fib_sequence:
                idx = (start_idx + offset) % len(analyzer.wheel_order)
                fib_nums.append(analyzer.wheel_order[idx])
            
            # Validar esta combinación
            fib_win_rate = validate_numbers_performance(
                validation_analyzer, fib_nums, validation_spins // 2)
            
            if fib_win_rate > best_fib_rate:
                best_fib_rate = fib_win_rate
                best_fib_combination = fib_nums
    
    fibonacci_numbers = best_fib_combination
    fibonacci_win_rate = best_fib_rate
    fibonacci_coverage = len(fibonacci_numbers) / 38 * 100
    fibonacci_performance = (fibonacci_win_rate / fibonacci_coverage - 1) * 100
    
    print(f"Combinación Fibonacci: {fibonacci_numbers}")
    print(f"Tasa de victoria: {fibonacci_win_rate:.2f}%")
    print(f"Rendimiento: {fibonacci_performance:+.2f}%")
    
    return {
        'fibonacci_numbers': fibonacci_numbers,
        'fibonacci_win_rate': fibonacci_win_rate,
        'fibonacci_coverage': fibonacci_coverage,
        'fibonacci_performance': fibonacci_performance
    }

def analyze_fibonacci_strategy(analyzer, validation_analyzer, validation_spins, sorted_numbers=None):
    """
    Analyze the Fibonacci betting strategy for roulette.
    
    The Fibonacci strategy uses the Fibonacci sequence for bet size progression
    after losses, and returns to the beginning of the sequence after wins.
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
        sorted_numbers: Optional pre-sorted list of numbers
        
    Returns:
        dict: Analysis results
    """
    print("\nAnalyzing Fibonacci betting strategy...")
    
    # Define Fibonacci sequence for bet progression
    fibonacci_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610]
    
    # Simulate Fibonacci strategy
    bankroll = 1000  # Initial bankroll
    initial_bet = 10  # Starting bet
    base_bet = initial_bet
    
    # Betting on red (18/38 chance of winning on American roulette)
    win_probability = 18/38
    payout_multiplier = 2  # Even money bet
    
    results = []
    win_count = 0
    loss_count = 0
    max_drawdown = 0
    peak_bankroll = bankroll
    
    # Sequence position tracker
    position = 0
    
    # Run simulation
    for _ in range(validation_spins):
        # Calculate bet amount based on position in Fibonacci sequence
        bet_amount = base_bet * fibonacci_sequence[position]
        
        # Ensure bet doesn't exceed bankroll
        bet_amount = min(bet_amount, bankroll)
        
        # Simulate bet outcome
        if random.random() < win_probability:
            # Win
            bankroll += bet_amount
            win_count += 1
            position = 0  # Reset to beginning of sequence
        else:
            # Loss
            bankroll -= bet_amount
            loss_count += 1
            position = min(position + 1, len(fibonacci_sequence) - 1)  # Move to next position, but don't exceed sequence
        
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
    
    print(f"Fibonacci Strategy Results:")
    print(f"Final Bankroll: ${final_bankroll:.2f}")
    print(f"Profit/Loss: ${profit:+.2f} ({profit_percentage:+.2f}%)")
    print(f"Performance vs. Random: {relative_performance:+.2f}%")
    print(f"Win Rate: {win_rate:.2f}")
    print(f"Max Drawdown: ${max_drawdown:.2f}")
    
    return {
        'fibonacci_final_bankroll': final_bankroll,
        'fibonacci_profit': profit,
        'fibonacci_profit_percentage': profit_percentage,
        'fibonacci_performance': relative_performance,
        'fibonacci_win_rate': win_rate,
        'fibonacci_max_drawdown': max_drawdown
    }

# Make sure we import random for the strategy simulation
import random 