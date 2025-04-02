#!/usr/bin/env python3
"""
Momentum-based analysis for roulette numbers.
"""
import numpy as np
from src.utils.analysis import validate_numbers_performance

def analyze_momentum(analyzer, validation_analyzer, validation_spins, sorted_numbers):
    """
    Identify numbers with positive momentum based on recent trends.
    
    Args:
        analyzer: Primary AdvancedRouletteAnalyzer instance
        validation_analyzer: Validation AdvancedRouletteAnalyzer instance
        validation_spins: Number of spins to use for validation
        sorted_numbers: List of numbers sorted by performance
        
    Returns:
        dict: Results with momentum-based data
    """
    print("\nGenerando combinación basada en momentum...")
    
    # Inicializar variables para resultados
    momentum_numbers = []
    momentum_win_rate = 0
    momentum_coverage = 0
    momentum_performance = 0
    
    # Dividir la historia en segmentos para analizar tendencias
    history = validation_analyzer.history
    if len(history) >= 500:
        # Analizar los últimos 500 resultados
        recent_segment = history[-500:]
        
        # Dividir en bloques de 100 para análisis de tendencia
        segments = [
            recent_segment[-100:],
            recent_segment[-200:-100],
            recent_segment[-300:-200],
            recent_segment[-400:-300],
            recent_segment[-500:-400]
        ]
        
        # Calcular frecuencias en cada segmento
        frequency_by_segment = []
        
        for segment in segments:
            frequencies = {}
            for num in analyzer.numbers:
                frequencies[num] = segment.count(num) / len(segment) * 100
            frequency_by_segment.append(frequencies)
        
        # Calcular momentum (cambio en frecuencia a través de segmentos)
        momentum_scores = {}
        for num in analyzer.numbers:
            # Dar más peso a segmentos más recientes
            momentum = (
                frequency_by_segment[0][num] * 1.0 +
                frequency_by_segment[1][num] * 0.8 +
                frequency_by_segment[2][num] * 0.6 +
                frequency_by_segment[3][num] * 0.4 +
                frequency_by_segment[4][num] * 0.2
            )
            
            # Evaluar tendencia: incremento en frecuencia más reciente
            trend = frequency_by_segment[0][num] - frequency_by_segment[1][num]
            
            # Ajustar el momentum según la tendencia
            if trend > 0:
                momentum *= 1.2  # Bonificación por tendencia positiva
            
            momentum_scores[num] = momentum
        
        # Seleccionar números con el momentum más alto
        momentum_items = sorted(momentum_scores.items(), key=lambda x: x[1], reverse=True)
        candidate_numbers = [num for num, _ in momentum_items[:12]]
        
        # Verificar el top 20 de números con mejor rendimiento general
        top_performers = set(sorted_numbers[:20])
        
        # Seleccionar números que tienen alto momentum y también buen rendimiento general
        momentum_numbers = []
        for num in candidate_numbers:
            if num in top_performers:
                momentum_numbers.append(num)
            if len(momentum_numbers) >= 8:
                break
        
        # Si no tenemos 8 números, añadir más números con alto momentum
        if len(momentum_numbers) < 8:
            for num, _ in momentum_items:
                if num not in momentum_numbers:
                    momentum_numbers.append(num)
                if len(momentum_numbers) >= 8:
                    break
        
        # Validar la combinación de momentum
        momentum_win_rate = validate_numbers_performance(
            validation_analyzer, momentum_numbers, validation_spins)
        momentum_coverage = len(momentum_numbers) / 38 * 100
        momentum_performance = (momentum_win_rate / momentum_coverage - 1) * 100
        
        print(f"Combinación basada en momentum: {momentum_numbers}")
        print(f"Tasa de victoria: {momentum_win_rate:.2f}%")
        print(f"Rendimiento: {momentum_performance:+.2f}%")
    else:
        print("Datos históricos insuficientes para análisis de momentum")
    
    return {
        'momentum_numbers': momentum_numbers,
        'momentum_win_rate': momentum_win_rate,
        'momentum_coverage': momentum_coverage,
        'momentum_performance': momentum_performance
    } 