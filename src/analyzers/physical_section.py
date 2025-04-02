#!/usr/bin/env python3
"""
Physical section analysis for roulette wheel.
"""
from src.utils.analysis import validate_numbers_performance

def analyze_physical_sections(analyzer, validation_analyzer, validation_spins):
    """
    Analyze physical sections of the roulette wheel to find the best performing section.
    
    Args:
        analyzer: Primary AdvancedRouletteAnalyzer instance
        validation_analyzer: Validation AdvancedRouletteAnalyzer instance
        validation_spins: Number of spins to use for validation
        
    Returns:
        dict: Results with best physical section data
    """
    print("\nGenerando combinación por secciones físicas de la rueda...")
    physical_sections = []
    wheel_order = analyzer.wheel_order
    
    # Identificar secciones de la rueda con mejor rendimiento (8 números cada una)
    section_performance = []
    for start_idx in range(0, len(wheel_order), 8):
        if start_idx + 8 <= len(wheel_order):
            section = wheel_order[start_idx:start_idx+8]
            section_win_rate = validate_numbers_performance(
                validation_analyzer, section, validation_spins // 2)
            section_coverage = len(section) / 38 * 100
            section_performance.append({
                'start_idx': start_idx,
                'section': section,
                'win_rate': section_win_rate,
                'coverage': section_coverage,
                'performance': (section_win_rate / section_coverage - 1) * 100
            })
    
    # Seleccionar la mejor sección
    results = {
        'physical_sections': [],
        'physical_section_win_rate': 0,
        'physical_section_performance': 0
    }
    
    if section_performance:
        best_physical_section = max(section_performance, key=lambda x: x['performance'])
        physical_sections = best_physical_section['section']
        physical_section_win_rate = best_physical_section['win_rate']
        physical_section_performance = best_physical_section['performance']
        
        print(f"Mejor sección física: {physical_sections}")
        print(f"Tasa de victoria: {physical_section_win_rate:.2f}%")
        print(f"Rendimiento: {physical_section_performance:+.2f}%")
        
        results = {
            'physical_sections': physical_sections,
            'physical_section_win_rate': physical_section_win_rate,
            'physical_section_performance': physical_section_performance
        }
    
    return results 