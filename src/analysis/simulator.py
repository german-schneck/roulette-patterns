from typing import List, Dict, Type, Tuple
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from collections import Counter, defaultdict
import os
from ..game.session import GameSession
from ..strategy.base_strategy import BaseStrategy
from .history import History

class Simulator:
    def __init__(self, strategies: List[BaseStrategy], max_spins: int = 1000, profit_target_percentage: float = 50.0):
        self.strategies = strategies
        self.max_spins = max_spins
        self.profit_target_percentage = profit_target_percentage
        self.history = {}

    def print_progress_bar(self, current, total, prefix='', suffix='', length=50, fill='█'):
        """Print a progress bar to the console."""
        percent = ("{0:.1f}").format(100 * (current / float(total)))
        filled_length = int(length * current // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='')
        if current == total:
            print()

    def run_simulations(self, num_simulations: int = 100) -> Dict:
        """Run multiple simulations for each strategy."""
        results = {}
        
        for strategy in self.strategies:
            strategy_name = strategy.__class__.__name__
            print(f"\nSimulando {strategy_name}...")
            results[strategy_name] = []
            
            for i in range(num_simulations):
                # Crear una nueva instancia de la estrategia para cada simulación
                strategy_instance = strategy.__class__(strategy.initial_bankroll, strategy.min_bet)
                session = GameSession(strategy_instance, max_spins=self.max_spins, 
                                     profit_target_percentage=self.profit_target_percentage)
                session.play_until_bankruptcy()
                results[strategy_name].append(session.get_results())
                
                # Mostrar progreso
                self.print_progress_bar(i + 1, num_simulations, prefix=f'{strategy_name}:')
            
        return results

    def analyze_number_patterns(self, spins: List[Dict], strategy_name: str) -> Tuple[List[Tuple[List[int], int]], List[Tuple[int, int]]]:
        """Analyze winning number patterns in the spins."""
        # Definir patrones de la ruleta americana
        patterns = {
            'red': [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36],
            'black': [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35],
            'even': [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36],
            'odd': [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35],
            'high': [19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36],
            'low': [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18],
            'dozens': {
                'first': [1,2,3,4,5,6,7,8,9,10,11,12],
                'second': [13,14,15,16,17,18,19,20,21,22,23,24],
                'third': [25,26,27,28,29,30,31,32,33,34,35,36]
            },
            'columns': {
                'first': [1,4,7,10,13,16,19,22,25,28,31,34],
                'second': [2,5,8,11,14,17,20,23,26,29,32,35],
                'third': [3,6,9,12,15,18,21,24,27,30,33,36]
            }
        }

        # Analizar números ganadores
        winning_numbers = [spin['number'] for spin in spins if spin['winnings'] > 0]
        winning_patterns = defaultdict(int)
        number_counts = Counter(winning_numbers)

        # Filtrar números según la estrategia
        if 'Martingale' in strategy_name:
            # Martingale tiende a apostar a números con mejor probabilidad
            filtered_numbers = {num: count for num, count in number_counts.items() 
                              if num in patterns['red'] or num in patterns['black']}
        elif 'Fibonacci' in strategy_name:
            # Fibonacci tiende a apostar a números bajos
            filtered_numbers = {num: count for num, count in number_counts.items() 
                              if num in patterns['low']}
        elif 'Pattern' in strategy_name:
            # Pattern tiende a seguir secuencias
            filtered_numbers = number_counts
        elif 'Paroli' in strategy_name:
            # Paroli tiende a apostar a números con mejor probabilidad
            filtered_numbers = {num: count for num, count in number_counts.items() 
                              if num in patterns['even'] or num in patterns['odd']}
        elif 'DAlembert' in strategy_name:
            # D'Alembert tiende a apostar a números medios
            filtered_numbers = {num: count for num, count in number_counts.items() 
                              if 10 <= num <= 27}
        elif 'Oscar' in strategy_name:
            # Oscar tiende a apostar a números altos
            filtered_numbers = {num: count for num, count in number_counts.items() 
                              if num in patterns['high']}
        elif 'DragonTiger' in strategy_name:
            # Dragon Tiger tiende a apostar a números específicos
            filtered_numbers = {num: count for num, count in number_counts.items() 
                              if num in [1, 6, 3, 7, 9]}
        elif 'GoldenEagle' in strategy_name:
            # Golden Eagle tiende a apostar a números dorados
            filtered_numbers = {num: count for num, count in number_counts.items() 
                              if num in [2, 5, 8]}
        elif 'Lucky8' in strategy_name:
            # Lucky 8 tiende a apostar a números con 8
            filtered_numbers = {num: count for num, count in number_counts.items() 
                              if num in [8, 18, 28, 38]}
        else:
            filtered_numbers = number_counts

        # Analizar patrones de 2-3 números consecutivos
        for i in range(len(winning_numbers)-1):
            # Patrón de 2 números
            pair = tuple(sorted([winning_numbers[i], winning_numbers[i+1]]))
            winning_patterns[pair] += 1

            # Patrón de 3 números
            if i < len(winning_numbers)-2:
                triplet = tuple(sorted([winning_numbers[i], winning_numbers[i+1], winning_numbers[i+2]]))
                winning_patterns[triplet] += 1

        # Analizar patrones de la ruleta
        for number in winning_numbers:
            # Patrones de color
            if number in patterns['red']:
                winning_patterns[('red',)] += 1
            if number in patterns['black']:
                winning_patterns[('black',)] += 1
            
            # Patrones de paridad
            if number in patterns['even']:
                winning_patterns[('even',)] += 1
            if number in patterns['odd']:
                winning_patterns[('odd',)] += 1
            
            # Patrones de docenas
            for dozen_name, dozen_numbers in patterns['dozens'].items():
                if number in dozen_numbers:
                    winning_patterns[(dozen_name,)] += 1
            
            # Patrones de columnas
            for column_name, column_numbers in patterns['columns'].items():
                if number in column_numbers:
                    winning_patterns[(column_name,)] += 1

        # Ordenar patrones por frecuencia
        sorted_patterns = sorted(winning_patterns.items(), key=lambda x: x[1], reverse=True)
        sorted_numbers = sorted(filtered_numbers.items(), key=lambda x: x[1], reverse=True)
        
        # Convertir patrones a formato legible
        result_patterns = []
        for pattern, count in sorted_patterns[:5]:  # Top 5 patrones
            if isinstance(pattern[0], str):  # Patrón de la ruleta
                result_patterns.append(([pattern[0]], count))
            else:  # Patrón de números
                result_patterns.append((list(pattern), count))
        
        return result_patterns, sorted_numbers

    def analyze_results(self, results: Dict) -> Dict:
        """Analyze the results of all simulations."""
        analysis = {}
        
        for strategy_name, sessions in results.items():
            # Calcular métricas básicas
            num_sessions = len(sessions)
            
            # Contar razones de terminación
            termination_counts = Counter(s['termination_reason'] for s in sessions)
            bankruptcy_count = termination_counts['bankruptcy']
            max_spins_count = termination_counts['max_spins_reached']
            profit_target_count = termination_counts['profit_target_reached']
            
            # Una sesión es exitosa si termina por alcanzar el objetivo de ganancia o por alcanzar el máximo de tiradas con un bankroll mayor al inicial
            successful_sessions = profit_target_count + sum(1 for s in sessions 
                                if s['termination_reason'] == 'max_spins_reached' and 
                                s['final_bankroll'] > s['initial_bankroll'])
            
            success_rate = successful_sessions / num_sessions
            
            # Calcular métricas de rendimiento
            win_rates = [s['wins'] / s['num_spins'] for s in sessions]
            avg_win_rate = sum(win_rates) / num_sessions
            
            profits = [s['final_bankroll'] - s['initial_bankroll'] for s in sessions]
            avg_profit = sum(profits) / num_sessions
            max_profit = max(profits)
            max_loss = min(profits)
            
            avg_spins = sum(s['num_spins'] for s in sessions) / num_sessions
            
            analysis[strategy_name] = {
                'success_rate': success_rate,
                'win_rate': avg_win_rate,
                'avg_profit_loss': avg_profit,
                'max_profit': max_profit,
                'max_loss': max_loss,
                'avg_spins': avg_spins,
                'bankruptcy_count': bankruptcy_count,
                'max_spins_count': max_spins_count,
                'profit_target_count': profit_target_count
            }
        
        return analysis

    def get_best_betting_patterns(self, results: Dict) -> Dict[str, List[Tuple[str, int]]]:
        """Analyze the most successful betting patterns for each strategy."""
        patterns = {}
        
        for strategy_name, sessions in results.items():
            # Recolectar números ganadores
            winning_numbers = []
            for session in sessions:
                for spin in session['spins']:
                    if spin['winnings'] > 0:
                        winning_numbers.append(spin['number'])
            
            # Contar ocurrencias
            number_counts = Counter(winning_numbers)
            
            # Obtener los 5 números más comunes
            patterns[strategy_name] = number_counts.most_common(5)
        
        return patterns

    def plot_results(self, results: Dict, output_file: str = 'output/roulette_simulation.png'):
        """Plot the results of all simulations."""
        plt.figure(figsize=(15, 10))
        
        # Subplot 1: Evolución del bankroll
        plt.subplot(2, 2, 1)
        for strategy_name, sessions in results.items():
            for session in sessions:
                if session['termination_reason'] == 'profit_target_reached':
                    plt.plot(session['bankroll_history'], color='green', alpha=0.3)
                elif session['termination_reason'] == 'max_spins_reached':
                    plt.plot(session['bankroll_history'], color='blue', alpha=0.3)
                else:
                    plt.plot(session['bankroll_history'], color='red', alpha=0.1)
        plt.title('Evolución del Bankroll')
        plt.xlabel('Número de Tiradas')
        plt.ylabel('Bankroll')
        
        # Subplot 2: Distribución de tasas de victoria
        plt.subplot(2, 2, 2)
        win_rates = []
        labels = []
        for strategy_name, sessions in results.items():
            rates = [s['wins'] / s['num_spins'] for s in sessions]
            win_rates.append(rates)
            labels.extend([strategy_name] * len(rates))
        plt.boxplot(win_rates, labels=list(results.keys()))
        plt.title('Distribución de Tasas de Victoria')
        plt.xticks(rotation=45)
        plt.ylabel('Tasa de Victoria')
        
        # Subplot 3: Distribución de beneficio/pérdida
        plt.subplot(2, 2, 3)
        profits = []
        labels = []
        for strategy_name, sessions in results.items():
            session_profits = [s['final_bankroll'] - s['initial_bankroll'] for s in sessions]
            profits.append(session_profits)
            labels.extend([strategy_name] * len(session_profits))
        plt.boxplot(profits, labels=list(results.keys()))
        plt.title('Distribución de Beneficio/Pérdida')
        plt.xticks(rotation=45)
        plt.ylabel('Beneficio/Pérdida')
        
        # Subplot 4: Razones de terminación
        plt.subplot(2, 2, 4)
        strategy_names = list(results.keys())
        bankruptcy_counts = []
        max_spins_counts = []
        profit_target_counts = []
        
        for strategy_name, sessions in results.items():
            termination_counts = Counter(s['termination_reason'] for s in sessions)
            bankruptcy_counts.append(termination_counts['bankruptcy'])
            max_spins_counts.append(termination_counts['max_spins_reached'])
            profit_target_counts.append(termination_counts['profit_target_reached'])
        
        width = 0.25
        x = range(len(strategy_names))
        
        plt.bar([i - width for i in x], bankruptcy_counts, width=width, label='Bancarrota')
        plt.bar(x, max_spins_counts, width=width, label='Máx. Tiradas')
        plt.bar([i + width for i in x], profit_target_counts, width=width, label='Objetivo Ganancia')
        
        plt.xticks(x, strategy_names, rotation=45)
        plt.title('Razones de Terminación')
        plt.ylabel('Número de Sesiones')
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(output_file)
        plt.close()

    def update_history(self, analysis: Dict, number_analysis: Dict) -> Dict[str, Tuple[bool, float]]:
        """Update history and return improvement status for each strategy."""
        improvements = {}
        
        for strategy_name in self.strategies:
            strategy_name = strategy_name.__class__.__name__
            stats = analysis[strategy_name]
            numbers = number_analysis[strategy_name]
            
            # Get best numbers and their win count
            best_numbers = [num for num, _ in numbers]
            wins_count = len(numbers)
            
            # Update history and get improvement status
            improved, improvement = self.history.update_strategy_history(
                strategy_name,
                stats['average_profit'],
                best_numbers,
                wins_count
            )
            
            improvements[strategy_name] = (improved, improvement)
        
        return improvements 