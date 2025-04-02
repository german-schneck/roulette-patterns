#!/usr/bin/env python3
"""
Geometric symmetry analysis for roulette wheel patterns.
"""
import numpy as np
import math
from src.utils.analysis import validate_numbers_performance

def analyze_geometric_symmetry(analyzer, validation_analyzer, validation_spins, sorted_numbers):
    """
    Select numbers based on geometric symmetric patterns on the wheel.
    
    Args:
        analyzer: Primary AdvancedRouletteAnalyzer instance
        validation_analyzer: Validation AdvancedRouletteAnalyzer instance
        validation_spins: Number of spins to use for validation
        sorted_numbers: List of numbers sorted by performance
        
    Returns:
        dict: Results with geometric symmetry data
    """
    print("\nGenerando combinación con simetría geométrica...")
    
    # Variables para los resultados
    symmetry_numbers = []
    symmetry_win_rate = 0
    symmetry_coverage = 0
    symmetry_performance = 0
    
    # Verificar que tenemos acceso al orden de la rueda
    if hasattr(analyzer, 'wheel_order') and len(analyzer.wheel_order) > 0:
        wheel_order = analyzer.wheel_order
        
        # Definir patrones geométricos para evaluar
        patterns = [
            {"name": "Diamante", "angles": [0, 90, 180, 270]},
            {"name": "Estrella", "angles": [0, 72, 144, 216, 288]},
            {"name": "Hexágono", "angles": [0, 60, 120, 180, 240, 300]},
            {"name": "Octágono", "angles": [0, 45, 90, 135, 180, 225, 270, 315]},
            {"name": "Cruz", "angles": [0, 90, 180, 270], "offset": 45}
        ]
        
        # Filtrar los mejores números para considerar
        top_candidates = sorted_numbers[:25]
        
        # Función para encontrar números que estén cerca de una posición angular específica
        def find_number_at_angle(angle, center, exclude=[]):
            # Convertir ángulo a posición en rueda
            wheel_size = len(wheel_order)
            target_position = (center + round((angle / 360) * wheel_size)) % wheel_size
            
            # Buscar número más cercano que esté en los candidatos y no en excluidos
            best_num = None
            min_distance = wheel_size
            
            for i in range(wheel_size):
                # Calcular distancia circular
                dist = min(
                    abs(i - target_position),
                    wheel_size - abs(i - target_position)
                )
                
                if dist < min_distance:
                    num = wheel_order[i]
                    if num in top_candidates and num not in exclude:
                        min_distance = dist
                        best_num = num
            
            return best_num
        
        # Evaluar cada patrón geométrico
        best_pattern = {"numbers": [], "win_rate": 0}
        
        for pattern in patterns:
            # Probar con diferentes puntos centrales
            for center_idx in range(0, len(wheel_order), len(wheel_order) // 10):
                pattern_numbers = []
                
                # Agregar número central si existe
                center_num = wheel_order[center_idx]
                if center_num in top_candidates:
                    pattern_numbers.append(center_num)
                
                # Agregar números en ángulos específicos
                offset = pattern.get("offset", 0)
                for angle in pattern["angles"]:
                    num = find_number_at_angle(angle + offset, center_idx, pattern_numbers)
                    if num:
                        pattern_numbers.append(num)
                
                # Completar hasta 8 números con los mejores candidatos
                remaining = [num for num in top_candidates if num not in pattern_numbers]
                pattern_numbers.extend(remaining[:max(0, 8 - len(pattern_numbers))])
                
                # Limitar a 8 números
                pattern_numbers = pattern_numbers[:8]
                
                # Validar combinación
                if len(pattern_numbers) == 8:
                    win_rate = validate_numbers_performance(
                        validation_analyzer, pattern_numbers, validation_spins // 3)
                    
                    if win_rate > best_pattern["win_rate"]:
                        best_pattern["numbers"] = pattern_numbers
                        best_pattern["win_rate"] = win_rate
                        best_pattern["name"] = pattern["name"]
                        best_pattern["center"] = center_idx
        
        # Validar la mejor combinación encontrada
        if best_pattern["numbers"]:
            symmetry_numbers = best_pattern["numbers"]
            symmetry_win_rate = validate_numbers_performance(
                validation_analyzer, symmetry_numbers, validation_spins)
            symmetry_coverage = len(symmetry_numbers) / 38 * 100
            symmetry_performance = (symmetry_win_rate / symmetry_coverage - 1) * 100
            
            print(f"Mejor patrón: {best_pattern['name']}")
            print(f"Combinación de simetría geométrica: {symmetry_numbers}")
            print(f"Tasa de victoria: {symmetry_win_rate:.2f}%")
            print(f"Rendimiento: {symmetry_performance:+.2f}%")
        else:
            print("No se pudo encontrar un patrón geométrico adecuado")
    else:
        print("No se puede acceder al orden de la rueda para análisis geométrico")
    
    return {
        'symmetry_numbers': symmetry_numbers,
        'symmetry_win_rate': symmetry_win_rate,
        'symmetry_coverage': symmetry_coverage,
        'symmetry_performance': symmetry_performance
    } 