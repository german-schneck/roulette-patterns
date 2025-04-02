#!/usr/bin/env python3
"""
Hot neighbors analysis for roulette numbers.
"""
import numpy as np
from collections import defaultdict
from src.utils.analysis import validate_numbers_performance

def analyze_hot_neighbors(analyzer, validation_analyzer, validation_spins, sorted_numbers):
    """
    Identify numbers that tend to appear near high-performing numbers in sequence.
    
    Args:
        analyzer: Primary AdvancedRouletteAnalyzer instance
        validation_analyzer: Validation AdvancedRouletteAnalyzer instance
        validation_spins: Number of spins to use for validation
        sorted_numbers: List of numbers sorted by performance
        
    Returns:
        dict: Results with hot neighbors data
    """
    print("\nGenerando combinación basada en vecinos calientes...")
    
    # Variables para los resultados
    hot_neighbor_numbers = []
    hot_neighbor_win_rate = 0
    hot_neighbor_coverage = 0
    hot_neighbor_performance = 0
    
    # Identificar los "números calientes" (top 10)
    hot_numbers = sorted_numbers[:10]
    
    # Analizar el historial para encontrar los vecinos de números calientes
    history = validation_analyzer.history
    if len(history) > 500:
        # Crear un mapa de vecinos para cada número
        neighbor_map = defaultdict(list)
        for i in range(1, len(history)-1):
            current = history[i]
            after = history[i+1]
            
            # Registrar los números que siguen a cada número
            neighbor_map[current].append(after)
        
        # Calcular la frecuencia de vecinos para números calientes
        neighbor_frequencies = defaultdict(int)
        neighbor_counts = defaultdict(int)
        
        for hot_num in hot_numbers:
            if hot_num in neighbor_map:
                for neighbor in neighbor_map[hot_num]:
                    neighbor_frequencies[neighbor] += 1
                    neighbor_counts[neighbor] += 1
        
        # Calcular las puntuaciones de vecinos calientes
        neighbor_scores = {}
        total_appearances = sum(neighbor_counts.values()) or 1  # Evitar división por cero
        
        for num, count in neighbor_counts.items():
            # Calcular score basado en frecuencia como vecino y proximidad a números calientes
            frequency_score = count / total_appearances
            proximity_to_hot = sum(1 for hot_num in hot_numbers if hot_num in analyzer.wheel_order)
            
            if proximity_to_hot > 0:  # Evitar división por cero
                hot_wheel_order = analyzer.wheel_order
                
                # Calcular distancia física promedio a números calientes en la rueda
                avg_distance = 0
                count_valid = 0
                
                if num in hot_wheel_order:
                    num_idx = hot_wheel_order.index(num)
                    for hot_num in hot_numbers:
                        if hot_num in hot_wheel_order:
                            hot_idx = hot_wheel_order.index(hot_num)
                            # Distancia circular en la rueda
                            distance = min(
                                abs(hot_idx - num_idx),
                                len(hot_wheel_order) - abs(hot_idx - num_idx)
                            )
                            avg_distance += distance
                            count_valid += 1
                
                if count_valid > 0:
                    avg_distance /= count_valid
                    proximity_score = 1 - (avg_distance / (len(hot_wheel_order) / 2))
                else:
                    proximity_score = 0
                
                # Combinar puntuaciones
                neighbor_scores[num] = (frequency_score * 0.7) + (proximity_score * 0.3)
            else:
                neighbor_scores[num] = frequency_score
        
        # Seleccionar los vecinos con mejor puntuación
        top_neighbors = sorted(neighbor_scores.items(), key=lambda x: x[1], reverse=True)
        candidate_neighbors = [num for num, _ in top_neighbors[:12]]
        
        # Filtrar para quedarnos con los 8 mejores que no sean ya números calientes
        hot_neighbor_numbers = []
        for num in candidate_neighbors:
            if len(hot_neighbor_numbers) >= 8:
                break
            hot_neighbor_numbers.append(num)
        
        # Validar la combinación de vecinos calientes
        hot_neighbor_win_rate = validate_numbers_performance(
            validation_analyzer, hot_neighbor_numbers, validation_spins)
        hot_neighbor_coverage = len(hot_neighbor_numbers) / 38 * 100
        hot_neighbor_performance = (hot_neighbor_win_rate / hot_neighbor_coverage - 1) * 100
        
        print(f"Combinación de vecinos calientes: {hot_neighbor_numbers}")
        print(f"Tasa de victoria: {hot_neighbor_win_rate:.2f}%")
        print(f"Rendimiento: {hot_neighbor_performance:+.2f}%")
    else:
        print("Datos históricos insuficientes para análisis de vecinos calientes")
    
    return {
        'hot_neighbor_numbers': hot_neighbor_numbers,
        'hot_neighbor_win_rate': hot_neighbor_win_rate,
        'hot_neighbor_coverage': hot_neighbor_coverage,
        'hot_neighbor_performance': hot_neighbor_performance
    } 