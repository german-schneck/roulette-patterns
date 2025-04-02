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
import matplotlib.pyplot as plt
from typing import List, Tuple

# Default configuration values
INITIAL_BANKROLL = 1000.0
NUM_SIMULATIONS = 10

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
    parser.add_argument('--initial-bankroll', type=float, default=1000.0,
                      help='Bankroll inicial para cada simulación')
    parser.add_argument('--num-simulations', type=int, default=100,
                      help='Número de simulaciones a ejecutar')
    parser.add_argument('--min-bet', type=float, default=1.0,
                      help='Apuesta mínima permitida')
    parser.add_argument('--output-plot', type=str, default='results.png',
                      help='Ruta del archivo de gráfico de resultados')
    args = parser.parse_args()

    print("\n=== Configuración de Simulación ===")
    print(f"Bankroll inicial: ${args.initial_bankroll:,.2f}")
    print(f"Simulaciones por estrategia: {args.num_simulations}")
    print(f"Apuesta mínima: ${args.min_bet:,.2f}")
    print("-" * 40)

    # Definir las estrategias a probar
    strategies = [
        MartingaleStrategy,
        FibonacciStrategy,
        PatternStrategy,
        ParoliStrategy,
        DAlembertStrategy,
        OscarStrategy,
        DragonTigerStrategy,
        GoldenEagleStrategy,
        Lucky8Strategy
    ]

    # Crear y ejecutar el simulador
    simulator = Simulator(
        initial_bankroll=args.initial_bankroll,
        num_simulations=args.num_simulations,
        min_bet=args.min_bet,
        strategies=strategies
    )

    # Ejecutar simulaciones
    results = simulator.run_simulations()

    # Analizar resultados
    analysis = simulator.analyze_results(results)

    # Imprimir resumen conciso
    print("\n=== Resumen de Estrategias ===")
    for strategy_name, metrics in analysis.items():
        win_rate = metrics['win_rate'] * 100
        patterns = [f"{format_pattern(pattern)} ({count})" 
                   for pattern, count in metrics['successful_patterns']]
        patterns_str = " | ".join(patterns)
        numbers_str = format_numbers(metrics['successful_numbers'])
        print(f"\n{strategy_name}:")
        print(f"  Patrones: {patterns_str}")
        print(f"  Números: {numbers_str}")
        print(f"  Rate: {win_rate:.2f}%")

    # Generar gráficos
    simulator.plot_results(results, args.output_plot)
    print(f"\nGráficos guardados en: {args.output_plot}")

if __name__ == "__main__":
    main() 