#!/usr/bin/env python3
"""
Advanced American Roulette Strategy Analyzer
Main entry point for the modular roulette analyzer package.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import time
from datetime import datetime
import traceback

# Import modules from package
from src.analyzers.advanced import AdvancedRouletteAnalyzer
from src.analyzers.quantum import QuantumPatternAnalyzer
from src.analyzers.bayesian import BayesianPredictor
# Import new analyzers
from src.analyzers.physical_section import analyze_physical_sections
from src.analyzers.fibonacci import analyze_fibonacci_patterns
from src.analyzers.parity_third import analyze_parity_third
from src.analyzers.clustering import analyze_dynamic_clustering
from src.analyzers.momentum import analyze_momentum
# Import additional new analyzers
from src.analyzers.hot_neighbors import analyze_hot_neighbors
from src.analyzers.temporal_cycles import analyze_temporal_cycles
from src.analyzers.variance_balance import analyze_variance_balance
from src.analyzers.geometric_symmetry import analyze_geometric_symmetry
# Import Las Vegas professional techniques
from src.analyzers.dealer_signature import analyze_dealer_signature
from src.analyzers.mechanical_bias import analyze_mechanical_bias
from src.analyzers.visual_ballistics import analyze_visual_ballistics
from src.analyzers.sector_targeting import analyze_sector_targeting
from src.analyzers.chaotic_domain import analyze_chaotic_domain
# Import Latin American strategies
from src.analyzers.latin_cancellation import analyze_latin_cancellation
from src.analyzers.mexican_progression import analyze_mexican_progression
# Import historical strategies
from src.analyzers.martingale import analyze_martingale_strategy
# Import Asian strategies
from src.analyzers.feng_shui import analyze_feng_shui_strategy
from src.analyzers.i_ching import analyze_i_ching_oracle
from src.analyzers.pachinko import analyze_pachinko_progression

from src.strategies.advanced import AdvancedBettingStrategy
from src.optimizers.kelly import KellyOptimizer

# Import utility functions
from src.utils.analysis import (
    validate_numbers_performance,
    analyze_number_patterns,
    load_previous_results,
    save_current_results,
    generate_performance_report,
    plot_roulette_heatmap,
    plot_performance_history
)
from src.utils.visualization import (
    plot_methodology_performance,
    plot_methodology_pl_simulation,
    plot_individual_methodology_performance,
    plot_bankroll_survival
)
from src.utils.gpu import setup_gpu_environment

# Simplified configuration
SPINS = 100        # Simulations per strategy
BANKROLL = 5000     # Initial bankroll in dollars
MAX_BANKROLL_SPINS = 1000  # Number of spins for bankroll simulation

# Configuration log
print(f"Configuration: SPINS={SPINS}, BANKROLL=${BANKROLL}")

# Function to display previous results
def display_previous_results(previous_results):
    """
    Displays previous results in a formatted way.
    
    Args:
        previous_results: Dictionary with data from previous runs
    """
    last_run = previous_results.get("last_run")
    best_historical = {
        "rate": previous_results.get("best_rate", 0),
        "formula": previous_results.get("best_formula", "None"),
        "numbers": previous_results.get("best_numbers", [])
    }
    
    # Show previous execution information if available
    if last_run:
        print("\n=========================================================")
        print("PREVIOUS RESULTS")
        print("=========================================================")
        print(f"Last execution: {last_run.get('date', 'Unknown')}")
        print(f"Win rate: {last_run.get('win_rate', 0):.2f}%")
        print(f"Formula: {last_run.get('formula', 'Unknown')}")
        print(f"Numbers: {', '.join(last_run.get('numbers', []))}")
        
        print(f"\nBest historical result: {best_historical['rate']:.2f}%")
        print(f"Formula: {best_historical['formula']}")
        print(f"Numbers: {', '.join(best_historical['numbers'])}")
        print("=========================================================")

def generate_optimum_number_recommendations(analyzer, num_simulations=None):
    """Generate optimum number recommendations based on statistical analysis."""
    # Use SPINS as default value
    if num_simulations is None:
        num_simulations = SPINS
    
    print(f"Analyzing patterns across {num_simulations} simulations...")
    pattern_analysis = analyze_number_patterns(analyzer, num_simulations)
    
    # Extract number scores from analysis
    number_stats = {}
    for num, z_score in pattern_analysis['number_zscores'].items():
        number_stats[num] = {
            'z_score': z_score,
            'ensemble_score': z_score  # Initialize with z-score, will be updated
        }
    
    # Integrate pair analysis to enhance scores
    if pattern_analysis['pair_significance']:
        for pair_info in pattern_analysis['pair_significance']:
            pair = pair_info['pair']
            z_score = pair_info['z_score']
            
            # Boost scores of numbers that appear in significant pairs
            for num in pair:
                if num in number_stats:
                    # Add a portion of the pair significance to the number's score
                    number_stats[num]['ensemble_score'] += z_score * 0.2
    
    # Integrate wheel sector analysis
    if pattern_analysis['top_sectors']:
        for sector_name, sector_info in pattern_analysis['top_sectors']:
            # Boost scores of numbers in high-variance sectors
            for num in sector_info['numbers']:
                if num in number_stats:
                    boost = abs(sector_info['variance']) * 0.02
                    number_stats[num]['ensemble_score'] += boost
    
    # Create optimized groups of numbers
    # Group 1: Top 8 numbers overall
    sorted_numbers = sorted(
        [(num, stats['ensemble_score']) for num, stats in number_stats.items()],
        key=lambda x: x[1],
        reverse=True
    )
    
    # Get just the number strings
    recommended_numbers = [num for num, _ in sorted_numbers]
    
    # Create different optimized groups
    optimized_groups = [
        recommended_numbers[:8],  # Top 8 numbers
        recommended_numbers[8:16],  # Next 8 numbers
        recommended_numbers[:4] + recommended_numbers[8:12],  # Mixed group
    ]
    
    # Add a group based on physical adjacency
    wheel_order = analyzer.wheel_order
    physical_group = []
    
    # Find a sequence of adjacent numbers on the wheel with good scores
    for start_idx in range(len(wheel_order)):
        group = []
        for offset in range(12):  # Look at 12 positions
            idx = (start_idx + offset) % len(wheel_order)
            num = wheel_order[idx]
            if num in recommended_numbers[:20]:  # One of the top 20 numbers
                group.append(num)
                if len(group) >= 8:
                    break
        
        if len(group) >= 6:  # Found a good cluster
            physical_group = group[:8]  # Take at most 8
            break
    
    if physical_group:
        optimized_groups.append(physical_group)
    
    # Return comprehensive results
    return {
        'recommended_numbers': recommended_numbers,
        'number_stats': number_stats,
        'optimized_groups': optimized_groups
    }

def main():
    try:
        print("Advanced American Roulette Strategy Analyzer")
        print("-------------------------------------------\n")
        
        print("Configuring execution environment...")
        # Configure GPU/CPU environment directly
        setup_gpu_environment()
        
        # Create output directories if they don't exist
        os.makedirs("output", exist_ok=True)
        os.makedirs("output/graphs", exist_ok=True)
        
        # Load previous analysis if it exists
        analyzer = AdvancedRouletteAnalyzer()
        previous_results = load_previous_results()
        
        # Display previous results
        display_previous_results(previous_results)
        
        print("\n=========================================================")
        print("DEEP PATTERN ANALYSIS")
        print("=========================================================")
        
        # Run analysis with simplified configuration
        print(f"Running analysis with {SPINS} simulations...")
        
        # Generate optimal number recommendations
        print("This process may take several minutes. Optimizing number patterns...")
        
        # Generate initial data
        analyzer.spin_batch(50000)  # Generate initial history
        
        number_recommendations = generate_optimum_number_recommendations(analyzer)
        
        # Show only top 10 numbers for clarity
        print("\nTOP 10 RECOMMENDED OPTIMAL NUMBERS:")
        top_nums = number_recommendations['recommended_numbers'][:10]
        for i, num in enumerate(top_nums, 1):
            if num in number_recommendations['number_stats']:
                stats = number_recommendations['number_stats'][num]
                print(f"{i}. Number {num} | Z-score: {stats['z_score']} | Ensemble: {stats['ensemble_score']}")
        
        # Evaluate each optimized group with extended simulation
        print(f"\nValidating with {SPINS} independent simulations...")
        validation_spins = SPINS
        
        # Create new analyzer for independent validation
        validation_analyzer = AdvancedRouletteAnalyzer()
        validation_analyzer.spin_batch(50000)  # Large database for validations
        
        # Matrix to record results per number
        number_hits = {num: 0 for num in number_recommendations['recommended_numbers']}
        total_spins = 0
        
        # Simulate and evaluate with optimized method
        print("Validating individual number performance...")
        batch_size = min(100000, validation_spins)
        remaining_spins = validation_spins
        
        while remaining_spins > 0:
            current_batch = min(batch_size, remaining_spins)
            results = validation_analyzer.spin_batch(current_batch)
            total_spins += current_batch
            
            # Count hits for each number
            for result in results:
                if result in number_hits:
                    number_hits[result] += 1
            
            remaining_spins -= current_batch
            if remaining_spins > 0:
                print(f"Progress: {(validation_spins - remaining_spins):,}/{validation_spins:,} simulations completed")
        
        # Evaluate each optimized group with accelerated method
        print("\nAnalyzing number pattern performance...")
        
        # Validate each group
        group_info = []
        for i, group in enumerate(number_recommendations['optimized_groups']):
            print(f"Validating Group {i+1}...")
            win_rate = validate_numbers_performance(
                validation_analyzer, group, validation_spins)
            
            coverage = len(group) / 38 * 100
            performance = (win_rate / coverage - 1) * 100
            wins = int(win_rate * validation_spins / 100)
            
            group_info.append({
                'group': i+1,
                'win_rate': win_rate,
                'coverage': coverage,
                'performance': performance,
                'wins': wins,
                'numbers': group
            })
        
        # Sort individual numbers by hit rate
        sorted_numbers = sorted(
            [(num, hits, hits/total_spins*100) for num, hits in number_hits.items()],
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Compile top 6 individual numbers with best performance
        best_individual_numbers = [num for num, _, _ in sorted_numbers[:6]]
        print("\nBest individual numbers identified.")
        
        # Find the group with highest win rate and best performance
        best_group = max(group_info, key=lambda x: x['win_rate'])
        best_performance = max(group_info, key=lambda x: x['performance'])
        
        # Create a hybrid combination of the best individual numbers and the best group
        hybrid_combination = list(set(best_individual_numbers + best_group['numbers']))[:8]
        
        # Validate the hybrid combination
        print("\nValidating hybrid combination...")
        hybrid_win_rate = validate_numbers_performance(
            validation_analyzer, hybrid_combination, validation_spins)
        
        hybrid_coverage = len(hybrid_combination) / 38 * 100
        hybrid_performance = (hybrid_win_rate / hybrid_coverage - 1) * 100
        
        # Apply advanced quantum pattern analysis
        print("\n=========================================================")
        print("ADVANCED NEURAL CORRELATION ANALYSIS")
        print("=========================================================")
        
        # Initialize quantum analyzer
        quantum_analyzer = QuantumPatternAnalyzer(analyzer)
        quantum_analyzer.initialize()
        
        # Get optimal combination based on advanced correlation analysis
        quantum_combination = quantum_analyzer.get_optimum_betting_combination(num_numbers=8)
        
        # Validate the quantum combination
        print("\nValidating neural correlation combination...")
        quantum_win_rate = validate_numbers_performance(
            validation_analyzer, quantum_combination['numbers'], validation_spins)
        
        quantum_performance = (quantum_win_rate / quantum_combination['coverage'] - 1) * 100

        # Run new methodologies
        print("\n=========================================================")
        print("ADVANCED METHODOLOGY ANALYSIS")
        print("=========================================================")
        
        # 1. Physical Wheel Section Analysis
        print("\nRunning Physical Wheel Section Analysis...")
        physical_results = analyze_physical_sections(analyzer, validation_analyzer, validation_spins)
        physical_section_numbers = physical_results.get('physical_sections', [])
        physical_win_rate = physical_results.get('physical_section_win_rate', 0)
        physical_performance = physical_results.get('physical_section_performance', 0)
        
        # 2. Fibonacci Sequence Analysis
        print("\nRunning Fibonacci Sequence Analysis...")
        sorted_numbers_only = [num for num, _, _ in sorted_numbers]
        fibonacci_results = analyze_fibonacci_patterns(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        fibonacci_numbers = fibonacci_results.get('fibonacci_numbers', [])
        fibonacci_win_rate = fibonacci_results.get('fibonacci_win_rate', 0)
        fibonacci_performance = fibonacci_results.get('fibonacci_performance', 0)
        
        # 3. Parity and Third Distribution Analysis
        print("\nRunning Parity and Third Distribution Analysis...")
        parity_third_results = analyze_parity_third(
            analyzer, validation_analyzer, validation_spins, number_hits, sorted_numbers_only)
        parity_third_numbers = parity_third_results.get('parity_third_numbers', [])
        parity_third_win_rate = parity_third_results.get('parity_third_win_rate', 0)
        parity_third_performance = parity_third_results.get('parity_third_performance', 0)
        
        # 4. Dynamic Clustering System
        print("\nRunning Dynamic Clustering System...")
        clustering_results = analyze_dynamic_clustering(analyzer, validation_analyzer, validation_spins, number_hits)
        cluster_numbers = clustering_results.get('top_cluster_numbers', [])
        cluster_win_rate = clustering_results.get('cluster_win_rate', 0)
        cluster_performance = clustering_results.get('cluster_performance', 0)
        
        # 5. Momentum-Based Analysis
        print("\nRunning Momentum-Based Analysis...")
        momentum_results = analyze_momentum(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        momentum_numbers = momentum_results.get('momentum_numbers', [])
        momentum_win_rate = momentum_results.get('momentum_win_rate', 0)
        momentum_performance = momentum_results.get('momentum_performance', 0)
        
        # 6. Hot Neighbors Analysis
        print("\nRunning Hot Neighbors Analysis...")
        hot_neighbors_results = analyze_hot_neighbors(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        hot_neighbor_numbers = hot_neighbors_results.get('hot_neighbor_numbers', [])
        hot_neighbor_win_rate = hot_neighbors_results.get('hot_neighbor_win_rate', 0)
        hot_neighbor_performance = hot_neighbors_results.get('hot_neighbor_performance', 0)
        
        # 7. Temporal Cycles Analysis
        print("\nRunning Temporal Cycles Analysis...")
        temporal_cycles_results = analyze_temporal_cycles(analyzer, validation_analyzer, validation_spins, number_hits)
        cycle_numbers = temporal_cycles_results.get('cycle_numbers', [])
        cycle_win_rate = temporal_cycles_results.get('cycle_win_rate', 0)
        cycle_performance = temporal_cycles_results.get('cycle_performance', 0)
        
        # 8. Variance Balance Analysis
        print("\nRunning Variance Balance Analysis...")
        variance_balance_results = analyze_variance_balance(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        variance_numbers = variance_balance_results.get('variance_numbers', [])
        variance_win_rate = variance_balance_results.get('variance_win_rate', 0)
        variance_performance = variance_balance_results.get('variance_performance', 0)
        
        # 9. Geometric Symmetry Analysis
        print("\nRunning Geometric Symmetry Analysis...")
        geometric_symmetry_results = analyze_geometric_symmetry(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        symmetry_numbers = geometric_symmetry_results.get('symmetry_numbers', [])
        symmetry_win_rate = geometric_symmetry_results.get('symmetry_win_rate', 0)
        symmetry_performance = geometric_symmetry_results.get('symmetry_performance', 0)
        
        # 10. Dealer Signature Analysis (Las Vegas technique)
        print("\n=========================================================")
        print("LAS VEGAS PROFESSIONAL TECHNIQUES")
        print("=========================================================")
        
        print("\nRunning Dealer Signature Analysis...")
        dealer_signature_results = analyze_dealer_signature(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        signature_numbers = dealer_signature_results.get('signature_numbers', [])
        signature_win_rate = dealer_signature_results.get('signature_win_rate', 0)
        signature_performance = dealer_signature_results.get('signature_performance', 0)
        
        # 11. Mechanical Bias Detection
        print("\nRunning Mechanical Bias Analysis...")
        mechanical_bias_results = analyze_mechanical_bias(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        bias_numbers = mechanical_bias_results.get('bias_numbers', [])
        bias_win_rate = mechanical_bias_results.get('bias_win_rate', 0)
        bias_performance = mechanical_bias_results.get('bias_performance', 0)
        
        # 12. Visual Ballistics Prediction
        print("\nRunning Visual Ballistics Analysis...")
        visual_ballistics_results = analyze_visual_ballistics(analyzer, validation_analyzer, validation_spins, number_hits)
        ballistic_numbers = visual_ballistics_results.get('ballistic_numbers', [])
        ballistic_win_rate = visual_ballistics_results.get('ballistic_win_rate', 0)
        ballistic_performance = visual_ballistics_results.get('ballistic_performance', 0)
        
        # 13. Sector Targeting Strategy
        print("\nRunning Sector Targeting Strategy...")
        sector_targeting_results = analyze_sector_targeting(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        sector_numbers = sector_targeting_results.get('sector_numbers', [])
        sector_win_rate = sector_targeting_results.get('sector_win_rate', 0)
        sector_performance = sector_targeting_results.get('sector_performance', 0)
        
        # 14. Chaotic Domain Analysis
        print("\nRunning Chaotic Domain Analysis...")
        chaotic_domain_results = analyze_chaotic_domain(analyzer, validation_analyzer, validation_spins, number_hits)
        chaotic_numbers = chaotic_domain_results.get('chaotic_numbers', [])
        chaotic_win_rate = chaotic_domain_results.get('chaotic_win_rate', 0)
        chaotic_performance = chaotic_domain_results.get('chaotic_performance', 0)
        
        # 15-18. Latin American Strategies
        print("\n=========================================================")
        print("LATIN AMERICAN STRATEGIES")
        print("=========================================================")
        
        # 15. Latin Cancellation System
        print("\nRunning Latin Cancellation Analysis...")
        latin_cancellation_results = analyze_latin_cancellation(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        cancellation_numbers = latin_cancellation_results.get('cancellation_numbers', [])
        cancellation_win_rate = latin_cancellation_results.get('cancellation_win_rate', 0)
        cancellation_performance = latin_cancellation_results.get('cancellation_performance', 0)
        
        # 16. Mexican Progression
        print("\nRunning Mexican Progression Analysis...")
        mexican_progression_results = analyze_mexican_progression(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        progression_numbers = mexican_progression_results.get('progression_numbers', [])
        progression_win_rate = mexican_progression_results.get('progression_win_rate', 0)
        progression_performance = mexican_progression_results.get('progression_performance', 0)
        
        # 17. Martingale Strategy (Historical classic)
        print("\n=========================================================")
        print("HISTORICAL CLASSIC STRATEGIES")
        print("=========================================================")
        
        print("\nRunning Martingale Strategy Analysis...")
        martingale_results = analyze_martingale_strategy(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        martingale_numbers = martingale_results.get('martingale_numbers', [])
        martingale_win_rate = martingale_results.get('martingale_win_rate', 0)
        martingale_performance = martingale_results.get('martingale_performance', 0)
        martingale_approach = martingale_results.get('best_approach', '')
        
        # 18. Feng Shui Strategy (Asian strategy)
        print("\n=========================================================")
        print("ASIAN BETTING STRATEGIES")
        print("=========================================================")
        
        print("\nRunning Feng Shui Harmony Analysis...")
        feng_shui_results = analyze_feng_shui_strategy(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        feng_shui_numbers = feng_shui_results.get('feng_shui_numbers', [])
        feng_shui_win_rate = feng_shui_results.get('feng_shui_win_rate', 0)
        feng_shui_performance = feng_shui_results.get('feng_shui_performance', 0)
        feng_shui_type = feng_shui_results.get('best_combination_type', '')
        
        # 19. I Ching Oracle System
        print("\nRunning I Ching Oracle Analysis...")
        i_ching_results = analyze_i_ching_oracle(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        i_ching_numbers = i_ching_results.get('i_ching_numbers', [])
        i_ching_win_rate = i_ching_results.get('i_ching_win_rate', 0)
        i_ching_performance = i_ching_results.get('i_ching_performance', 0)
        i_ching_type = i_ching_results.get('best_combination_type', '')
        
        # 20. Pachinko Progression
        print("\nRunning Pachinko Progression Analysis...")
        pachinko_results = analyze_pachinko_progression(analyzer, validation_analyzer, validation_spins, sorted_numbers_only)
        pachinko_numbers = pachinko_results.get('pachinko_numbers', [])
        pachinko_win_rate = pachinko_results.get('pachinko_win_rate', 0)
        pachinko_performance = pachinko_results.get('pachinko_performance', 0)
        pachinko_type = pachinko_results.get('best_combination_type', '')
        
        # Add strategies to final combinations
        final_combinations = [
            {"name": "Best Original Group", "numbers": best_group['numbers'], "rate": best_group['win_rate']},
            {"name": "Top Individual Numbers", "numbers": best_individual_numbers, "rate": sum(hits/total_spins*100 for _, hits, _ in sorted_numbers[:6])},
            {"name": "Optimized Hybrid Combination", "numbers": hybrid_combination, "rate": hybrid_win_rate},
            {"name": "Advanced Neural Correlation", "numbers": quantum_combination['numbers'], "rate": quantum_win_rate},
            {"name": "Physical Wheel Section", "numbers": physical_section_numbers, "rate": physical_win_rate},
            {"name": "Fibonacci Sequence", "numbers": fibonacci_numbers, "rate": fibonacci_win_rate},
            {"name": "Parity-Third Optimization", "numbers": parity_third_numbers, "rate": parity_third_win_rate},
            {"name": "Dynamic Clustering", "numbers": cluster_numbers, "rate": cluster_win_rate},
            {"name": "Momentum-Based", "numbers": momentum_numbers, "rate": momentum_win_rate},
            {"name": "Hot Neighbors", "numbers": hot_neighbor_numbers, "rate": hot_neighbor_win_rate},
            {"name": "Temporal Cycles", "numbers": cycle_numbers, "rate": cycle_win_rate},
            {"name": "Variance Balance", "numbers": variance_numbers, "rate": variance_win_rate},
            {"name": "Geometric Symmetry", "numbers": symmetry_numbers, "rate": symmetry_win_rate},
            {"name": "Dealer Signature", "numbers": signature_numbers, "rate": signature_win_rate},
            {"name": "Mechanical Bias", "numbers": bias_numbers, "rate": bias_win_rate},
            {"name": "Visual Ballistics", "numbers": ballistic_numbers, "rate": ballistic_win_rate},
            {"name": "Sector Targeting", "numbers": sector_numbers, "rate": sector_win_rate},
            {"name": "Chaotic Domain", "numbers": chaotic_numbers, "rate": chaotic_win_rate},
            {"name": "Latin Cancellation", "numbers": cancellation_numbers, "rate": cancellation_win_rate},
            {"name": "Mexican Progression", "numbers": progression_numbers, "rate": progression_win_rate},
            {"name": "Classic Martingale", "numbers": martingale_numbers, "rate": martingale_win_rate},
            {"name": "Feng Shui Harmony", "numbers": feng_shui_numbers, "rate": feng_shui_win_rate},
            {"name": "I Ching Oracle", "numbers": i_ching_numbers, "rate": i_ching_win_rate},
            {"name": "Pachinko Progression", "numbers": pachinko_numbers, "rate": pachinko_win_rate},
        ]
        
        ultimate_best = max(final_combinations, key=lambda x: x['rate'])
        
        print("\n=========================================================")
        print("FINAL RESULT: OPTIMAL COMBINATION")
        print("=========================================================")
        
        print(f"\n🥇 COMBINATION WITH HIGHEST SUCCESS PROBABILITY:")
        print(f"   Name: {ultimate_best['name']}")
        print(f"   Win rate: {ultimate_best['rate']:.2f}%")
        print(f"   Numbers: {', '.join(ultimate_best['numbers'])}")
        
        # Ultra-brief analysis of the winning combination
        formula_name = ""
        if ultimate_best['name'] == "Advanced Neural Correlation":
            formula_name = "Advanced analysis of non-linear correlations and physical bias"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {quantum_performance:+.2f}%")
        elif ultimate_best['name'] == "Optimized Hybrid Combination":
            formula_name = "Hybrid combination of best performing individual numbers"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {hybrid_performance:+.2f}%")
        elif ultimate_best['name'] == "Best Original Group":
            formula_name = "Consistently optimized group"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {best_group['performance']:+.2f}%")
        elif ultimate_best['name'] == "Physical Wheel Section":
            formula_name = "Analysis of physical wheel sectors performance"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {physical_performance:+.2f}%")
        elif ultimate_best['name'] == "Fibonacci Sequence":
            formula_name = "Strategic positions using Fibonacci number patterns"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {fibonacci_performance:+.2f}%")
        elif ultimate_best['name'] == "Parity-Third Optimization":
            formula_name = "Optimized distribution based on parity and wheel thirds"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {parity_third_performance:+.2f}%")
        elif ultimate_best['name'] == "Dynamic Clustering":
            formula_name = "Co-occurrence based dynamic clustering system"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {cluster_performance:+.2f}%")
        elif ultimate_best['name'] == "Momentum-Based":
            formula_name = "Trend and momentum analysis with historical weighting"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {momentum_performance:+.2f}%")
        elif ultimate_best['name'] == "Hot Neighbors":
            formula_name = "Sequential analysis of numbers following high performers"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {hot_neighbor_performance:+.2f}%")
        elif ultimate_best['name'] == "Temporal Cycles":
            formula_name = "Cyclical pattern detection in historical results"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {cycle_performance:+.2f}%")
        elif ultimate_best['name'] == "Variance Balance":
            formula_name = "Optimized spatial dispersion for maximum wheel coverage"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {variance_performance:+.2f}%")
        elif ultimate_best['name'] == "Geometric Symmetry":
            formula_name = "Symmetric geometric patterns exploiting wheel biases"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {symmetry_performance:+.2f}%")
        elif ultimate_best['name'] == "Dealer Signature":
            formula_name = "Analysis of croupier behavior patterns and tendencies"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {signature_performance:+.2f}%")
        elif ultimate_best['name'] == "Mechanical Bias":
            formula_name = "Detection of physical imperfections in the roulette wheel"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {bias_performance:+.2f}%")
        elif ultimate_best['name'] == "Visual Ballistics":
            formula_name = "Trajectory prediction based on initial conditions"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {ballistic_performance:+.2f}%")
        elif ultimate_best['name'] == "Sector Targeting":
            formula_name = "Strategic focus on high-probability wheel sections"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {sector_performance:+.2f}%")
        elif ultimate_best['name'] == "Chaotic Domain":
            formula_name = "Identification of strange attractors in chaotic systems"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {chaotic_performance:+.2f}%")
        elif ultimate_best['name'] == "Latin Cancellation":
            formula_name = "Pattern-based sequence analysis from Latin American casinos"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {cancellation_performance:+.2f}%")
        elif ultimate_best['name'] == "Mexican Progression":
            formula_name = "Modified Martingale system focusing on repeating clusters"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {progression_performance:+.2f}%")
        elif ultimate_best['name'] == "Classic Martingale":
            formula_name = f"Classic doubling progression on {martingale_approach}"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {martingale_performance:+.2f}%")
        elif ultimate_best['name'] == "Feng Shui Harmony":
            formula_name = f"Chinese Feng Shui {feng_shui_type} approach"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {feng_shui_performance:+.2f}%")
        elif ultimate_best['name'] == "I Ching Oracle":
            formula_name = f"Ancient Chinese I Ching {i_ching_type} divination"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {i_ching_performance:+.2f}%")
        elif ultimate_best['name'] == "Pachinko Progression":
            formula_name = f"Japanese Pachinko {pachinko_type} system"
            print(f"\nFORMULA: {formula_name}")
            print(f"Performance vs expected: {pachinko_performance:+.2f}%")
        else:
            formula_name = "Selection of individual numbers with best hit-rate"
            print(f"\nFORMULA: {formula_name}")
        
        # Rate comparison
        print("\nSTRATEGY COMPARISON:")
        for combo in sorted(final_combinations, key=lambda x: x['rate'], reverse=True):
            print(f"• {combo['name']}: {combo['rate']:.2f}%")
        
        # Bankroll simulations for all methodologies
        print("\n=========================================================")
        print("GENERATING VISUALIZATIONS")
        print("=========================================================")
        
        # Comparison of all methodologies
        plot_methodology_performance(final_combinations)
        print(f"Comparison chart saved: output/graphs/methodology_comparison.png")
        
        # P/L simulation for all methodologies with bankroll
        plot_methodology_pl_simulation(final_combinations, initial_bankroll=BANKROLL)
        print(f"Bankroll simulation chart saved: output/graphs/bankroll_simulation.png")
        
        # Bankroll survival analysis
        plot_bankroll_survival(final_combinations, initial_bankroll=BANKROLL)
        print(f"Bankroll survival chart saved: output/graphs/bankroll_survival.png")
        
        # Individual analysis for each methodology
        for combo in final_combinations:
            plot_individual_methodology_performance(combo, validation_analyzer, validation_spins, initial_bankroll=BANKROLL)
        
        # Generate roulette heatmap
        plot_roulette_heatmap(final_combinations)
        
        # Generate comparative performance report
        improvements = generate_performance_report(
            ultimate_best['rate'], 
            formula_name, 
            ultimate_best['numbers']
        )

        # Save current results
        save_success = save_current_results(
            ultimate_best['rate'], 
            formula_name, 
            ultimate_best['numbers'],
            improvements
        )

        # Generate and save performance history chart
        plot_success = plot_performance_history()

        # Get the last_run info from previous_results for the report
        last_run = previous_results.get("last_run", {})

        # Show performance report
        print("\n=========================================================")
        print("PERFORMANCE IMPROVEMENT REPORT")
        print("=========================================================")
        
        # Compare with target rate of 21.16%
        baseline_imp = improvements.get("baseline", {})
        print(f"\nComparison with target rate (21.16%):")
        print(f"• Absolute difference: {baseline_imp.get('improvement', 0):+.2f}%")
        print(f"• Relative improvement: {baseline_imp.get('percentage', 0):+.2f}%")
        
        # Compare with last execution if it exists
        if "last_run" in improvements:
            last_imp = improvements["last_run"]
            print(f"\nComparison with last execution ({last_imp.get('previous_rate', 0):.2f}%):")
            print(f"• Absolute difference: {last_imp.get('improvement', 0):+.2f}%")
            print(f"• Relative improvement: {last_imp.get('percentage', 0):+.2f}%")
            print(f"• Last execution date: {last_run.get('date', 'Unknown')}")
        
        # Compare with historical best if it exists and is different
        if "historical" in improvements:
            hist_imp = improvements["historical"]
            print(f"\nComparison with historical best ({hist_imp.get('previous_rate', 0):.2f}%):")
            print(f"• Absolute difference: {hist_imp.get('improvement', 0):+.2f}%")
            print(f"• Relative improvement: {hist_imp.get('percentage', 0):+.2f}%")
        
        # Information about saved results
        if save_success:
            print("\nResults successfully saved for future tracking.")
        else:
            print("\nCould not save results. Check write permissions.")
            
        if plot_success:
            print("Evolution chart generated: output/graphs/performance_history.png")
        
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main() 