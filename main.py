import argparse
import time
from src.analysis.simulator import Simulator
from src.strategy.martingale import MartingaleStrategy
from src.strategy.fibonacci import FibonacciStrategy
from src.strategy.pattern import PatternStrategy
from src.strategy.paroli import ParoliStrategy
from src.strategy.dalembert import DAlembertStrategy
from src.strategy.oscar import OscarStrategy
from src.strategy.dragon_tiger import DragonTigerStrategy
from src.strategy.golden_eagle import GoldenEagleStrategy
from src.strategy.lucky_8 import Lucky8Strategy
from src.strategy.labouchere import LabouchereStrategy
from src.strategy.one_three_two_six import OneThreeTwoSixStrategy
# Estrategias Latinoamericanas
from src.strategy.tulum import TulumStrategy
from src.strategy.andina import AndinaStrategy
from src.strategy.caracas import CaracasStrategy
from src.strategy.tango import TangoStrategy
from src.strategy.carioca import CariocaStrategy
from src.strategy.valparaiso import ValparaisoStrategy
from src.strategy.montevideo import MontevideoStrategy
# Estrategias Vetadas de Casinos
from src.strategy.kesselgucken import KesselguckenStrategy
from src.strategy.grande_martingale import GrandeMartingaleStrategy
from src.strategy.thorp_system import ThorpSystemStrategy
from src.strategy.monaco_system import MonacoSystemStrategy
# Estrategias Científicas
from src.strategy.quantum_observer import QuantumObserverStrategy
from src.strategy.chaos_theory import ChaosTheoryStrategy
from src.strategy.statistical_mechanics import StatisticalMechanicsStrategy
# Nuevas estrategias reales
from src.strategy.james_bond import JamesBondStrategy
import matplotlib.pyplot as plt
from typing import List, Tuple

# Default configuration values
INITIAL_BANKROLL = 1000.0
NUM_SIMULATIONS = 100
MAX_SPINS = 1000
PROFIT_TARGET_PERCENTAGE = 50.0

def print_progress_bar(current, total, prefix='', suffix='', length=50, fill='█'):
    """Print a progress bar to the console."""
    percent = ("{0:.1f}").format(100 * (current / float(total)))
    filled_length = int(length * current // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='')
    if current == total:
        print()

def format_number_list(numbers):
    """Format a list of numbers as a string."""
    if not numbers:
        return "Sin números exitosos"
    return f"({', '.join(str(num) for num, _ in numbers)})"

def format_improvement(improved: bool, improvement: float) -> str:
    """Format improvement information."""
    if improved:
        return f"↑ Mejoró {improvement:.2%}"
    return "→ Sin cambios"

def format_pattern(pattern: List) -> str:
    """Format a pattern for display."""
    if isinstance(pattern[0], str):
        return pattern[0]
    return '-'.join(str(num) for num in pattern)

def format_numbers(numbers: List[Tuple[int, int]]) -> str:
    """Format a list of numbers and their counts."""
    return ', '.join(f"{num}({count})" for num, count in numbers)

def main():
    parser = argparse.ArgumentParser(description='Simulador de Ruleta Americana')
    parser.add_argument('--initial-bankroll', type=float, default=INITIAL_BANKROLL,
                       help='Bankroll inicial para cada simulación')
    parser.add_argument('--num-simulations', type=int, default=NUM_SIMULATIONS,
                       help='Número de simulaciones a ejecutar')
    parser.add_argument('--min-bet', type=float, default=1.0,
                       help='Apuesta mínima permitida')
    parser.add_argument('--max-spins', type=int, default=MAX_SPINS,
                       help='Número máximo de tiradas por sesión')
    parser.add_argument('--profit-target', type=float, default=PROFIT_TARGET_PERCENTAGE,
                       help='Objetivo de ganancia como porcentaje del bankroll inicial')
    parser.add_argument('--output-plot', type=str, default='results.png',
                       help='Ruta del archivo de gráfico de resultados')
    args = parser.parse_args()

    print("\n=== Configuración de Simulación ===")
    print(f"Bankroll inicial: ${args.initial_bankroll:,.2f}")
    print(f"Simulaciones por estrategia: {args.num_simulations}")
    print(f"Apuesta mínima: ${args.min_bet:,.2f}")
    print(f"Máximo de tiradas: {args.max_spins}")
    print(f"Objetivo de ganancia: {args.profit_target}% del bankroll inicial")
    print("-" * 40)

    # Definir las estrategias a probar
    strategies = [
        # Estrategias clásicas
        MartingaleStrategy(args.initial_bankroll, args.min_bet),
        FibonacciStrategy(args.initial_bankroll, args.min_bet),
        PatternStrategy(args.initial_bankroll, args.min_bet),
        ParoliStrategy(args.initial_bankroll, args.min_bet),
        DAlembertStrategy(args.initial_bankroll, args.min_bet),
        OscarStrategy(args.initial_bankroll, args.min_bet),
        
        # Estrategias asiáticas
        DragonTigerStrategy(args.initial_bankroll, args.min_bet),
        GoldenEagleStrategy(args.initial_bankroll, args.min_bet),
        Lucky8Strategy(args.initial_bankroll, args.min_bet),
        
        # Estrategias profesionales de Las Vegas
        LabouchereStrategy(args.initial_bankroll, args.min_bet),
        OneThreeTwoSixStrategy(args.initial_bankroll, args.min_bet),
        JamesBondStrategy(args.initial_bankroll, args.min_bet),  # Nueva estrategia
        
        # Estrategias latinoamericanas
        TulumStrategy(args.initial_bankroll, args.min_bet),        # México
        AndinaStrategy(args.initial_bankroll, args.min_bet),       # Región Andina
        CaracasStrategy(args.initial_bankroll, args.min_bet),      # Venezuela
        TangoStrategy(args.initial_bankroll, args.min_bet),        # Argentina
        CariocaStrategy(args.initial_bankroll, args.min_bet),      # Brasil
        ValparaisoStrategy(args.initial_bankroll, args.min_bet),   # Chile
        MontevideoStrategy(args.initial_bankroll, args.min_bet),   # Uruguay
        
        # Estrategias Vetadas de Casinos
        KesselguckenStrategy(args.initial_bankroll, args.min_bet),   # Monte Carlo/Alemania
        GrandeMartingaleStrategy(args.initial_bankroll, args.min_bet), # Las Vegas/Europa
        ThorpSystemStrategy(args.initial_bankroll, args.min_bet),    # Desarrollado por E. Thorp
        MonacoSystemStrategy(args.initial_bankroll, args.min_bet),   # Casino de Monte Carlo
        
        # Estrategias basadas en Ciencia y Física
        QuantumObserverStrategy(args.initial_bankroll, args.min_bet),    # Física cuántica
        ChaosTheoryStrategy(args.initial_bankroll, args.min_bet),        # Teoría del caos
        StatisticalMechanicsStrategy(args.initial_bankroll, args.min_bet) # Mecánica estadística
    ]
    
    # Crear y ejecutar el simulador
    simulator = Simulator(strategies, max_spins=args.max_spins, profit_target_percentage=args.profit_target)
    
    # Ejecutar simulaciones
    results = simulator.run_simulations(args.num_simulations)
    
    # Analizar resultados
    analysis = simulator.analyze_results(results)
    
    # Obtener patrones más exitosos
    patterns = simulator.get_best_betting_patterns(results)
    
    # Imprimir resumen conciso
    print("\n=== Resumen de Estrategias ===")
    
    # Agrupar estrategias por categoría
    strategy_categories = {
        "Estrategias Clásicas": ["MartingaleStrategy", "FibonacciStrategy", "PatternStrategy", 
                                "ParoliStrategy", "DAlembertStrategy", "OscarStrategy"],
        "Estrategias Asiáticas": ["DragonTigerStrategy", "GoldenEagleStrategy", "Lucky8Strategy"],
        "Estrategias de Las Vegas": ["LabouchereStrategy", "OneThreeTwoSixStrategy", "JamesBondStrategy"],
        "Estrategias Latinoamericanas": [
            "TulumStrategy", "AndinaStrategy", "CaracasStrategy",
            "TangoStrategy", "CariocaStrategy", "ValparaisoStrategy", "MontevideoStrategy"
        ],
        "Estrategias Vetadas de Casinos": [
            "KesselguckenStrategy", "GrandeMartingaleStrategy", 
            "ThorpSystemStrategy", "MonacoSystemStrategy"
        ],
        "Estrategias basadas en Ciencia y Física": [
            "QuantumObserverStrategy", "ChaosTheoryStrategy", "StatisticalMechanicsStrategy"
        ]
    }
    
    for category, strategy_names in strategy_categories.items():
        print(f"\n== {category} ==")
        for strategy_name in strategy_names:
            if strategy_name in analysis:
                metrics = analysis[strategy_name]
                win_rate = metrics['win_rate'] * 100
                success_rate = metrics['success_rate'] * 100
                avg_profit = metrics['avg_profit_loss']
                
                print(f"\n{strategy_name}:")
                print(f"  Probabilidad de éxito: {success_rate:.2f}%")
                print(f"  Tasa de victoria: {win_rate:.2f}%")
                print(f"  Beneficio/Pérdida promedio: ${avg_profit:.2f}")
                
                # Mostrar estadísticas de terminación
                bankruptcy = metrics['bankruptcy_count']
                max_spins = metrics['max_spins_count']
                profit_target = metrics['profit_target_count']
                print(f"  Terminación por bancarrota: {bankruptcy} ({bankruptcy/args.num_simulations:.1%})")
                print(f"  Terminación por máx. tiradas: {max_spins} ({max_spins/args.num_simulations:.1%})")
                print(f"  Terminación por objetivo: {profit_target} ({profit_target/args.num_simulations:.1%})")
                
                # Mostrar patrones más exitosos
                if strategy_name in patterns:
                    strategy_patterns = patterns[strategy_name]
                    if strategy_patterns:
                        patterns_str = ", ".join([f"{num}({count})" for num, count in strategy_patterns[:5]])
                        print(f"  Números más efectivos: {patterns_str}")
    
    # Generar gráficos
    simulator.plot_results(results, args.output_plot)
    print(f"\nGráficos guardados en: {args.output_plot}")

if __name__ == "__main__":
    main() 