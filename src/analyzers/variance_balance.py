#!/usr/bin/env python3
"""
Variance balance analysis for roulette wheel coverage.
"""
import numpy as np
import itertools
from src.utils.analysis import validate_numbers_performance

def analyze_variance_balance(analyzer, validation_analyzer, validation_spins, sorted_numbers):
    """
    Optimize number selection for maximum spatial dispersion on the wheel.
    
    Args:
        analyzer: Primary AdvancedRouletteAnalyzer instance
        validation_analyzer: Validation AdvancedRouletteAnalyzer instance
        validation_spins: Number of spins to use for validation
        sorted_numbers: List of numbers sorted by performance
        
    Returns:
        dict: Results with variance balance data
    """
    print("\nGenerando combinación con equilibrio de varianza...")
    
    # Variables para los resultados
    variance_numbers = []
    variance_win_rate = 0
    variance_coverage = 0
    variance_performance = 0
    
    # Ordenar números por rendimiento
    candidates = sorted_numbers[:20]  # Considerar solo los 20 mejores números
    
    # Verificar que hay suficientes candidatos
    if len(candidates) >= 8:
        # Función para calcular la dispersión espacial de una combinación en la rueda
        def calculate_dispersion(numbers):
            # Obtener posiciones en la rueda
            positions = []
            for num in numbers:
                if num in analyzer.wheel_order:
                    idx = analyzer.wheel_order.index(num)
                    positions.append(idx)
            
            if len(positions) < 2:
                return 0
            
            # Ordenar posiciones
            positions.sort()
            
            # Calcular distancias entre números consecutivos (considerando que la rueda es circular)
            wheel_size = len(analyzer.wheel_order)
            distances = []
            
            for i in range(len(positions)):
                next_pos = positions[(i + 1) % len(positions)]
                curr_pos = positions[i]
                
                # Distancia circular
                distance = min(
                    (next_pos - curr_pos) % wheel_size,
                    (curr_pos - next_pos) % wheel_size
                )
                distances.append(distance)
            
            # La varianza ideal sería cuando los números están perfectamente espaciados
            # La desviación estándar de las distancias debería ser cercana a cero
            if distances:
                return -np.std(distances)  # Negativo porque queremos maximizar este valor
            return -float('inf')
        
        # Calcular la puntuación de cada candidato basada en su rendimiento
        performance_scores = {}
        for i, num in enumerate(candidates):
            # Dar más peso a los números con mejor rendimiento
            performance_scores[num] = 1.0 - (i / len(candidates))
        
        # Estrategia: seleccionar primero los mejores rendimientos, luego optimizar la dispersión
        # Empezar con los 3 mejores números
        variance_numbers = candidates[:3]
        
        # Agregar los números restantes optimizando la dispersión
        remaining_candidates = candidates[3:]
        
        while len(variance_numbers) < 8 and remaining_candidates:
            best_addition = None
            best_score = -float('inf')
            
            for candidate in remaining_candidates:
                # Evaluar la dispersión si agregamos este número
                temp_combination = variance_numbers + [candidate]
                dispersion = calculate_dispersion(temp_combination)
                
                # Combinar dispersión con rendimiento
                performance_weight = performance_scores.get(candidate, 0)
                combined_score = (dispersion * 0.7) + (performance_weight * 0.3)
                
                if combined_score > best_score:
                    best_score = combined_score
                    best_addition = candidate
            
            if best_addition:
                variance_numbers.append(best_addition)
                remaining_candidates.remove(best_addition)
            else:
                break
        
        # Validar la combinación de equilibrio de varianza
        variance_win_rate = validate_numbers_performance(
            validation_analyzer, variance_numbers, validation_spins)
        variance_coverage = len(variance_numbers) / 38 * 100
        variance_performance = (variance_win_rate / variance_coverage - 1) * 100
        
        print(f"Combinación de equilibrio de varianza: {variance_numbers}")
        print(f"Tasa de victoria: {variance_win_rate:.2f}%")
        print(f"Rendimiento: {variance_performance:+.2f}%")
    else:
        print("Datos insuficientes para analizar equilibrio de varianza")
    
    return {
        'variance_numbers': variance_numbers,
        'variance_win_rate': variance_win_rate,
        'variance_coverage': variance_coverage,
        'variance_performance': variance_performance
    } 