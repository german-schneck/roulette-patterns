#!/usr/bin/env python3
"""
Dynamic clustering analysis for roulette numbers.
"""
import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist
from src.utils.analysis import validate_numbers_performance

def analyze_dynamic_clustering(analyzer, validation_analyzer, validation_spins, number_hits):
    """
    Analyze roulette numbers using dynamic clustering based on co-occurrence patterns.
    
    Args:
        analyzer: Primary AdvancedRouletteAnalyzer instance
        validation_analyzer: Validation AdvancedRouletteAnalyzer instance
        validation_spins: Number of spins to use for validation
        number_hits: Dictionary mapping numbers to their hit counts
        
    Returns:
        dict: Results with dynamic clustering data
    """
    print("\nGenerando combinación con clustering dinámico...")
    
    # Inicializar variables para resultados
    top_cluster_numbers = []
    cluster_win_rate = 0
    cluster_coverage = 0
    cluster_performance = 0
    
    # Tomar una muestra de resultados para análisis de cluster
    sample_size = min(2000, len(validation_analyzer.history))
    if sample_size > 100:
        sample = validation_analyzer.history[-sample_size:]
        
        # Crear matriz de coocurrencia para todos los números
        cooccurrence = np.zeros((len(analyzer.numbers), len(analyzer.numbers)))
        
        for i in range(len(sample) - 1):
            current_num = sample[i]
            next_num = sample[i + 1]
            
            if current_num in analyzer.numbers and next_num in analyzer.numbers:
                current_idx = analyzer.numbers.index(current_num)
                next_idx = analyzer.numbers.index(next_num)
                cooccurrence[current_idx, next_idx] += 1
        
        # Normalizar matriz
        row_sums = cooccurrence.sum(axis=1, keepdims=True)
        # Evitar división por cero
        row_sums[row_sums == 0] = 1
        cooccurrence_norm = cooccurrence / row_sums
        
        # Usar distancia euclidiana para clustering
        distances = pdist(cooccurrence_norm)
        linkage_matrix = linkage(distances, method='ward')
        
        # Dividir en 4 clusters
        clusters = fcluster(linkage_matrix, 4, criterion='maxclust')
        
        # Evaluar rendimiento de cada cluster
        cluster_performances = []
        for cluster_id in range(1, 5):  # Los clusters están numerados desde 1
            cluster_members = [analyzer.numbers[i] for i, c in enumerate(clusters) if c == cluster_id]
            if len(cluster_members) > 0:
                cluster_win_rate = validate_numbers_performance(
                    validation_analyzer, cluster_members, validation_spins // 2)
                cluster_coverage = len(cluster_members) / 38 * 100
                
                cluster_performances.append({
                    'cluster_id': cluster_id,
                    'members': cluster_members,
                    'win_rate': cluster_win_rate,
                    'coverage': cluster_coverage,
                    'performance': (cluster_win_rate / cluster_coverage - 1) * 100
                })
        
        # Seleccionar el mejor cluster por rendimiento
        if cluster_performances:
            best_cluster = max(cluster_performances, key=lambda x: x['performance'])
            
            # Seleccionar top 8 números del mejor cluster por rendimiento individual
            top_cluster_numbers = []
            
            cluster_members_perf = [(num, number_hits.get(num, 0)) 
                                   for num in best_cluster['members']]
            sorted_cluster = sorted(cluster_members_perf, key=lambda x: x[1], reverse=True)
            
            top_cluster_numbers = [num for num, _ in sorted_cluster[:8]]
            
            # Completar hasta 8 números si es necesario
            while len(top_cluster_numbers) < 8 and len(top_cluster_numbers) < len(best_cluster['members']):
                top_cluster_numbers.append(sorted_cluster[len(top_cluster_numbers)][0])
            
            # Validar la combinación de cluster
            cluster_win_rate = validate_numbers_performance(
                validation_analyzer, top_cluster_numbers, validation_spins)
            cluster_coverage = len(top_cluster_numbers) / 38 * 100
            cluster_performance = (cluster_win_rate / cluster_coverage - 1) * 100
            
            print(f"Combinación de cluster dinámico: {top_cluster_numbers}")
            print(f"Tasa de victoria: {cluster_win_rate:.2f}%")
            print(f"Rendimiento: {cluster_performance:+.2f}%")
        else:
            print("No se pudo generar combinación de cluster válida")
    else:
        print("Datos insuficientes para análisis de cluster dinámico")
    
    return {
        'top_cluster_numbers': top_cluster_numbers,
        'cluster_win_rate': cluster_win_rate,
        'cluster_coverage': cluster_coverage,
        'cluster_performance': cluster_performance
    } 