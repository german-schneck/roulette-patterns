#!/usr/bin/env python3
"""
Temporal cycles analysis for roulette numbers.
"""
import numpy as np
from collections import defaultdict, Counter
from src.utils.analysis import validate_numbers_performance

def analyze_temporal_cycles(analyzer, validation_analyzer, validation_spins, number_hits):
    """
    Identify cyclical patterns in historical results.
    
    Args:
        analyzer: Primary AdvancedRouletteAnalyzer instance
        validation_analyzer: Validation AdvancedRouletteAnalyzer instance
        validation_spins: Number of spins to use for validation
        number_hits: Dictionary mapping numbers to their hit counts
        
    Returns:
        dict: Results with temporal cycles data
    """
    print("\nGenerando combinación basada en ciclos temporales...")
    
    # Variables para los resultados
    cycle_numbers = []
    cycle_win_rate = 0
    cycle_coverage = 0
    cycle_performance = 0
    
    # Analizar el historial para buscar patrones cíclicos
    history = validation_analyzer.history
    if len(history) > 1000:
        # Buscar ciclos entre 5 y 50 tiradas
        potential_cycles = range(5, min(51, len(history) // 10))
        cycle_scores = {}
        
        for cycle_length in potential_cycles:
            # Analizar apariciones de números en cada posición del ciclo
            cycle_positions = defaultdict(lambda: defaultdict(int))
            
            for i in range(len(history) - cycle_length):
                position = i % cycle_length
                number = history[i]
                cycle_positions[position][number] += 1
            
            # Calcular números con mayor tendencia en cada posición del ciclo
            position_winners = {}
            for position, counts in cycle_positions.items():
                if counts:
                    # Normalizar por total de apariciones
                    total = sum(counts.values())
                    normalized = {num: count/total for num, count in counts.items()}
                    position_winners[position] = max(normalized.items(), key=lambda x: x[1])
            
            # Evaluar la fuerza del ciclo basada en la desviación de la distribución uniforme
            expected_prob = 1.0 / len(analyzer.numbers)
            avg_deviation = np.mean([abs(prob - expected_prob) for _, prob in position_winners.values()])
            
            # Puntuar el ciclo
            cycle_scores[cycle_length] = avg_deviation * 100  # Porcentaje de desviación
        
        # Seleccionar el mejor ciclo
        if cycle_scores:
            best_cycle_length = max(cycle_scores.items(), key=lambda x: x[1])[0]
            
            # Analizar el ciclo actual para predecir los próximos números
            current_position = len(history) % best_cycle_length
            
            # Construir histograma de números que han aparecido en las siguientes posiciones
            upcoming_positions = [(current_position + i) % best_cycle_length for i in range(1, 9)]
            
            # Contar apariciones en posiciones futuras del ciclo
            future_counts = defaultdict(int)
            
            for i in range(0, len(history) - best_cycle_length, best_cycle_length):
                for pos_offset, future_pos in enumerate(upcoming_positions):
                    actual_pos = i + future_pos
                    if actual_pos < len(history):
                        num = history[actual_pos]
                        # Dar más peso a las posiciones más cercanas
                        weight = 1.0 / (pos_offset + 1)
                        future_counts[num] += weight
            
            # Combinar con el rendimiento general de los números
            cycle_candidates = {}
            for num, cycle_count in future_counts.items():
                # Normalizar puntuación cíclica
                cycle_score = cycle_count / max(future_counts.values()) if future_counts else 0
                
                # Obtener rendimiento histórico
                hit_score = number_hits.get(num, 0) / max(number_hits.values()) if number_hits else 0
                
                # Combinar puntuaciones
                cycle_candidates[num] = (cycle_score * 0.7) + (hit_score * 0.3)
            
            # Seleccionar los 8 mejores números basados en la puntuación combinada
            cycle_numbers = [num for num, _ in sorted(
                cycle_candidates.items(), key=lambda x: x[1], reverse=True)[:8]]
            
            # Validar la combinación de ciclos temporales
            cycle_win_rate = validate_numbers_performance(
                validation_analyzer, cycle_numbers, validation_spins)
            cycle_coverage = len(cycle_numbers) / 38 * 100
            cycle_performance = (cycle_win_rate / cycle_coverage - 1) * 100
            
            print(f"Mejor longitud de ciclo: {best_cycle_length} tiradas")
            print(f"Combinación de ciclos temporales: {cycle_numbers}")
            print(f"Tasa de victoria: {cycle_win_rate:.2f}%")
            print(f"Rendimiento: {cycle_performance:+.2f}%")
        else:
            print("No se encontraron patrones cíclicos significativos")
    else:
        print("Datos históricos insuficientes para análisis de ciclos temporales")
    
    return {
        'cycle_numbers': cycle_numbers,
        'cycle_win_rate': cycle_win_rate,
        'cycle_coverage': cycle_coverage,
        'cycle_performance': cycle_performance,
    } 