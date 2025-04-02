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