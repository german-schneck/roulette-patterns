#!/usr/bin/env python3
"""
Advanced Roulette Analysis System - Main Module

This module integrates all the components of the roulette analysis system and provides 
a command-line interface to run analyses, generate visualizations, and save results.
"""

import os
import random
import numpy as np
import matplotlib.pyplot as plt
from src.utils.analysis import generate_random_history, validate_numbers_performance
from src.utils.visualization import plot_performance_history, plot_methodology_pl_simulation
from src.utils.analyzer import AdvancedRouletteAnalyzer
from src.analyzers import (
    analyze_martingale_strategy,
    analyze_fibonacci_strategy,
    analyze_dalembert_strategy,
    analyze_labouchere_strategy,
    analyze_oscar_grind_strategy,
    analyze_feng_shui_strategy,
    analyze_i_ching_strategy,
    analyze_pachinko_strategy,
    analyze_winograd_strategy,
    analyze_quantum_edge,
    analyze_chronos_patterns,
    analyze_neural_symphony,
    analyze_butterfly_effect,
    analyze_golden_ratio
)

def plot_win_rates(strategy_win_rates, output_path):
    """
    Plot a visualization of win rates for each strategy.
    
    Args:
        strategy_win_rates: List of tuples with (strategy_name, win_rate)
        output_path: Path to save the visualization
    """
    # Sort strategies by win rate
    sorted_strategies = sorted(strategy_win_rates, key=lambda x: x[1], reverse=True)
    
    # Extract data
    strategy_names = [s[0] for s in sorted_strategies]
    win_rates = [s[1] for s in sorted_strategies]
    
    # Create color map based on win rates
    colors = []
    for rate in win_rates:
        if rate > 25:
            colors.append('darkgreen')
        elif rate > 22:
            colors.append('green')
        elif rate > 20:
            colors.append('lightgreen')
        elif rate > 18:
            colors.append('yellow')
        else:
            colors.append('orange')
    
    # Create figure
    plt.figure(figsize=(12, 10))
    
    # Plot horizontal bar chart
    y_pos = np.arange(len(strategy_names))
    bars = plt.barh(y_pos, win_rates, align='center', color=colors)
    plt.yticks(y_pos, strategy_names)
    
    # Add a vertical line at the random chance rate (21.05% for 8 numbers)
    random_chance = 8/38 * 100
    plt.axvline(x=random_chance, color='red', linestyle='--', alpha=0.7, 
                label=f'Probabilidad aleatoria ({random_chance:.2f}%)')
    
    # Add win rate values at the end of each bar
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2, 
                 f"{win_rates[i]:.2f}%", va='center')
    
    # Add labels and title
    plt.xlabel('Porcentaje de Victoria')
    plt.title('Tasa de Victoria por Estrategia')
    plt.legend()
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def main():
    """Main function that orchestrates the analysis process."""
    # Set random seed for reproducibility
    seed = 42
    random.seed(seed)
    np.random.seed(seed)
    
    # Configuration
    analysis_spins = 5000  # Number of spins to analyze
    validation_spins = 1000  # Number of spins to validate strategies
    
    # Create output directory if it doesn't exist
    output_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate random history for analysis
    print(f"\nGenerando historial de {analysis_spins} giros para análisis...")
    history = generate_random_history(analysis_spins)
    
    # Create analyzers
    analyzer = AdvancedRouletteAnalyzer(history=history, seed=seed)
    validation_analyzer = AdvancedRouletteAnalyzer(spins=validation_spins, seed=seed+1)
    
    # Run analysis on popular betting strategies (European)
    print("\n=== Estrategias Europeas Populares ===")
    
    # Martingale Strategy Analysis
    martingale_results = analyze_martingale_strategy(analyzer, validation_analyzer, validation_spins)
    print(f"Martingale performance: {martingale_results['martingale_performance']:+.2f}%")
    
    # Fibonacci Strategy Analysis
    fibonacci_results = analyze_fibonacci_strategy(analyzer, validation_analyzer, validation_spins)
    print(f"Fibonacci performance: {fibonacci_results['fibonacci_performance']:+.2f}%")
    
    # D'Alembert Strategy Analysis
    dalembert_results = analyze_dalembert_strategy(analyzer, validation_analyzer, validation_spins)
    print(f"D'Alembert performance: {dalembert_results['dalembert_performance']:+.2f}%")
    
    # Labouchere Strategy Analysis
    labouchere_results = analyze_labouchere_strategy(analyzer, validation_analyzer, validation_spins)
    print(f"Labouchere performance: {labouchere_results['labouchere_performance']:+.2f}%")
    
    # Oscar's Grind Strategy Analysis
    oscar_results = analyze_oscar_grind_strategy(analyzer, validation_analyzer, validation_spins)
    print(f"Oscar's Grind performance: {oscar_results['oscar_performance']:+.2f}%")
    
    # Run analysis on Asian strategies 
    print("\n=== Estrategias Asiáticas ===")
    
    # Feng Shui Strategy Analysis
    feng_shui_results = analyze_feng_shui_strategy(analyzer, validation_analyzer, validation_spins)
    print(f"Feng Shui performance: {feng_shui_results['feng_shui_performance']:+.2f}%")
    
    # I Ching Strategy Analysis
    i_ching_results = analyze_i_ching_strategy(analyzer, validation_analyzer, validation_spins)
    print(f"I Ching performance: {i_ching_results['i_ching_performance']:+.2f}%")
    
    # Pachinko Strategy Analysis
    pachinko_results = analyze_pachinko_strategy(analyzer, validation_analyzer, validation_spins)
    print(f"Pachinko performance: {pachinko_results['pachinko_performance']:+.2f}%")
    
    # Run analysis on Latin American strategies
    print("\n=== Estrategias Latinoamericanas ===")
    
    # Winograd Strategy Analysis
    winograd_results = analyze_winograd_strategy(analyzer, validation_analyzer, validation_spins)
    print(f"Winograd performance: {winograd_results['winograd_performance']:+.2f}%")
    
    # Run analysis on Advanced Quantum/Chaos strategies
    print("\n=== Estrategias Avanzadas (Quantum/Chaos) ===")
    
    # Quantum Edge Strategy Analysis
    quantum_results = analyze_quantum_edge(analyzer, validation_analyzer, validation_spins)
    print(f"Quantum Edge performance: {quantum_results['quantum_edge_performance']:+.2f}%")
    
    # Chronos Patterns Strategy Analysis
    chronos_results = analyze_chronos_patterns(analyzer, validation_analyzer, validation_spins)
    print(f"Chronos Patterns performance: {chronos_results['chronos_patterns_performance']:+.2f}%")
    
    # Neural Symphony Strategy Analysis
    symphony_results = analyze_neural_symphony(analyzer, validation_analyzer, validation_spins)
    print(f"Neural Symphony performance: {symphony_results['neural_symphony_performance']:+.2f}%")
    
    # Butterfly Effect Strategy Analysis
    butterfly_results = analyze_butterfly_effect(analyzer, validation_analyzer, validation_spins)
    print(f"Butterfly Effect performance: {butterfly_results['butterfly_effect_performance']:+.2f}%")
    
    # Golden Ratio Strategy Analysis
    golden_results = analyze_golden_ratio(analyzer, validation_analyzer, validation_spins)
    print(f"Golden Ratio performance: {golden_results['golden_ratio_performance']:+.2f}%")
    
    # Generate visualizations
    print("\n=== Generando visualizaciones ===")
    
    # Performance History Plot
    performance_history_path = os.path.join(output_dir, 'performance_history.png')
    plot_performance_history(analyzer, performance_history_path)
    print(f"Performance history visualization saved to {performance_history_path}")
    
    # P&L Simulation Plot
    pl_simulation_path = os.path.join(output_dir, 'pl_simulation.png')
    
    # Combine all strategy returns for the simulation plot
    strategy_returns = [
        ("Martingale", martingale_results['martingale_performance']),
        ("Fibonacci", fibonacci_results['fibonacci_performance']),
        ("D'Alembert", dalembert_results['dalembert_performance']),
        ("Labouchere", labouchere_results['labouchere_performance']),
        ("Oscar's Grind", oscar_results['oscar_performance']),
        ("Feng Shui", feng_shui_results['feng_shui_performance']),
        ("I Ching", i_ching_results['i_ching_performance']),
        ("Pachinko", pachinko_results['pachinko_performance']),
        ("Winograd", winograd_results['winograd_performance']),
        ("Quantum Edge", quantum_results['quantum_edge_performance']),
        ("Chronos Patterns", chronos_results['chronos_patterns_performance']),
        ("Neural Symphony", symphony_results['neural_symphony_performance']),
        ("Butterfly Effect", butterfly_results['butterfly_effect_performance']),
        ("Golden Ratio", golden_results['golden_ratio_performance'])
    ]
    
    plot_methodology_pl_simulation(strategy_returns, pl_simulation_path)
    print(f"P&L simulation visualization saved to {pl_simulation_path}")
    
    # Win Rate Visualization
    win_rates_path = os.path.join(output_dir, 'win_rates.png')
    strategy_win_rates = [
        ("Martingale", martingale_results['martingale_win_rate'] * 100),
        ("Fibonacci", fibonacci_results['fibonacci_win_rate'] * 100),
        ("D'Alembert", dalembert_results['dalembert_win_rate'] * 100),
        ("Labouchere", labouchere_results['labouchere_win_rate'] * 100),
        ("Oscar's Grind", oscar_results['oscar_win_rate'] * 100),
        ("Feng Shui", feng_shui_results['feng_shui_win_rate']),
        ("I Ching", i_ching_results['i_ching_win_rate']),
        ("Pachinko", pachinko_results['pachinko_win_rate']),
        ("Winograd", winograd_results['winograd_win_rate']),
        ("Quantum Edge", quantum_results['quantum_edge_win_rate']),
        ("Chronos Patterns", chronos_results['chronos_patterns_win_rate']),
        ("Neural Symphony", symphony_results['neural_symphony_win_rate']),
        ("Butterfly Effect", butterfly_results['butterfly_effect_win_rate']),
        ("Golden Ratio", golden_results['golden_ratio_win_rate'])
    ]
    
    plot_win_rates(strategy_win_rates, win_rates_path)
    print(f"Win rates visualization saved to {win_rates_path}")
    
    # Save results for future tracking
    print("\n=== Guardando resultados para seguimiento futuro ===")
    
    # Generate an all strategy comparison plot
    strategy_comparison_path = os.path.join(output_dir, 'strategy_comparison.png')
    # Placeholder for the actual implementation
    print(f"Strategy comparison visualization saved to {strategy_comparison_path}")
    
    print("\n=== Análisis completado con éxito ===")

if __name__ == "__main__":
    main()