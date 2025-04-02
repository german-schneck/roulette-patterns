#!/usr/bin/env python3
"""
Parity and third-based analysis for roulette numbers.
"""
from src.utils.analysis import validate_numbers_performance

def analyze_parity_third(analyzer, validation_analyzer, validation_spins, number_hits, sorted_numbers):
    """
    Analyze performance of even/odd numbers and number thirds to create optimized combinations.
    
    Args:
        analyzer: Primary AdvancedRouletteAnalyzer instance
        validation_analyzer: Validation AdvancedRouletteAnalyzer instance
        validation_spins: Number of spins to use for validation
        number_hits: Dictionary mapping numbers to their hit counts
        sorted_numbers: List of numbers sorted by performance
        
    Returns:
        dict: Results with parity-third optimization data
    """
    print("\nGenerando combinación de paridad y tercio optimizada...")
    # Analizar rendimiento de números pares/impares y por tercios
    even_numbers = [num for num in analyzer.numbers if num not in ['0', '00'] and int(num) % 2 == 0]
    odd_numbers = [num for num in analyzer.numbers if num not in ['0', '00'] and int(num) % 2 == 1]
    first_third = [str(i) for i in range(1, 13)]
    second_third = [str(i) for i in range(13, 25)]
    third_third = [str(i) for i in range(25, 37)]
    
    # Evaluar cada grupo
    even_win_rate = validate_numbers_performance(validation_analyzer, even_numbers, validation_spins // 2)
    odd_win_rate = validate_numbers_performance(validation_analyzer, odd_numbers, validation_spins // 2)
    first_win_rate = validate_numbers_performance(validation_analyzer, first_third, validation_spins // 2)
    second_win_rate = validate_numbers_performance(validation_analyzer, second_third, validation_spins // 2)
    third_win_rate = validate_numbers_performance(validation_analyzer, third_third, validation_spins // 2)
    
    # Determinar mejor paridad y mejor tercio
    best_parity = "even" if even_win_rate > odd_win_rate else "odd"
    best_parity_numbers = even_numbers if best_parity == "even" else odd_numbers
    
    third_rates = [
        ("first", first_win_rate, first_third),
        ("second", second_win_rate, second_third),
        ("third", third_win_rate, third_third)
    ]
    best_third = max(third_rates, key=lambda x: x[1])
    
    # Crear combinación híbrida de paridad-tercio
    # Tomar 4 mejores números de la mejor paridad y 4 del mejor tercio
    parity_third_numbers = []
    
    # Filtrar números de la mejor paridad por su rendimiento individual
    parity_performance = [(num, number_hits.get(num, 0)) for num in best_parity_numbers]
    top_parity = sorted(parity_performance, key=lambda x: x[1], reverse=True)[:4]
    parity_third_numbers.extend([num for num, _ in top_parity])
    
    # Filtrar números del mejor tercio por su rendimiento individual
    third_performance = [(num, number_hits.get(num, 0)) for num in best_third[2]]
    top_third = sorted(third_performance, key=lambda x: x[1], reverse=True)[:4]
    
    # Añadir números del tercio que no estén ya incluidos
    for num, _ in top_third:
        if num not in parity_third_numbers:
            parity_third_numbers.append(num)
            if len(parity_third_numbers) >= 8:
                break
    
    # Si no tenemos 8 números, completar con los mejores números individuales
    while len(parity_third_numbers) < 8:
        for num in sorted_numbers:
            if num not in parity_third_numbers:
                parity_third_numbers.append(num)
                if len(parity_third_numbers) >= 8:
                    break
    
    # Validar la combinación paridad-tercio
    parity_third_win_rate = validate_numbers_performance(
        validation_analyzer, parity_third_numbers, validation_spins)
    parity_third_coverage = len(parity_third_numbers) / 38 * 100
    parity_third_performance = (parity_third_win_rate / parity_third_coverage - 1) * 100
    
    print(f"Combinación paridad ({best_parity})-tercio ({best_third[0]}): {parity_third_numbers}")
    print(f"Tasa de victoria: {parity_third_win_rate:.2f}%")
    print(f"Rendimiento: {parity_third_performance:+.2f}%")
    
    return {
        'parity_third_numbers': parity_third_numbers,
        'parity_third_win_rate': parity_third_win_rate,
        'parity_third_coverage': parity_third_coverage,
        'parity_third_performance': parity_third_performance,
        'best_parity': best_parity,
        'best_third': best_third[0]
    } 