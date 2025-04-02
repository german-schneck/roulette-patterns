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
    def __init__(self, initial_bankroll: float, num_simulations: int, min_bet: float, strategies: List[Type[BaseStrategy]]):
        self.initial_bankroll = initial_bankroll
        self.num_simulations = num_simulations
        self.min_bet = min_bet
        self.strategies = strategies
        self.history = {}

    def print_progress_bar(self, current, total, prefix='', suffix='', length=50, fill='█'):
        """Print a progress bar to the console."""
        percent = ("{0:.1f}").format(100 * (current / float(total)))
        filled_length = int(length * current // total)
        bar = fill * filled_length + '-' * (length - filled_length)
        print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='')
        if current == total:
            print()

    def run_simulations(self) -> Dict[str, List[Dict]]:
        """Run multiple game sessions for each strategy."""
        results = {}
        
        for strategy_class in self.strategies:
            strategy_name = strategy_class.__name__
            print(f"\nSimulando {strategy_name}...")
            results[strategy_name] = []
            
            for i in range(self.num_simulations):
                strategy = strategy_class(self.initial_bankroll, self.min_bet)
                session = GameSession(strategy)
                session.play_until_bankruptcy()
                results[strategy_name].append(session.get_results())
                
                # Mostrar progreso
                self.print_progress_bar(i + 1, self.num_simulations, prefix=f'{strategy_name}:')
        
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

    def analyze_results(self, results: Dict[str, List[Dict]]) -> Dict[str, Dict]:
        """Analyze results for all strategies."""
        analysis = {}
        
        for strategy_name, sessions in results.items():
            successful_sessions = sum(1 for session in sessions if session['final_bankroll'] > self.initial_bankroll)
            total_wins = sum(session['wins'] for session in sessions)
            total_spins = sum(session['num_spins'] for session in sessions)
            
            # Analizar patrones de números exitosos
            all_spins = []
            for session in sessions:
                all_spins.extend(session['spins'])
            
            successful_patterns, successful_numbers = self.analyze_number_patterns(all_spins, strategy_name)
            
            analysis[strategy_name] = {
                'successful_sessions': successful_sessions,
                'total_wins': total_wins,
                'total_spins': total_spins,
                'win_rate': total_wins / total_spins if total_spins > 0 else 0,
                'successful_patterns': successful_patterns,
                'successful_numbers': successful_numbers
            }
        
        return analysis

    def get_most_successful_numbers(self, results: Dict[str, List[Dict]]) -> Dict[str, List[tuple]]:
        """Get the most successful numbers for each strategy."""
        number_analysis = {}
        
        for strategy_name, sessions in results.items():
            winning_numbers = []
            for session in sessions:
                for spin in session['spins']:
                    if spin['winnings'] > 0:
                        winning_numbers.append(spin['number'])
            
            # Contar frecuencia de números ganadores
            number_counts = Counter(winning_numbers)
            
            # Obtener los 5 números más exitosos
            most_successful = number_counts.most_common(5)
            number_analysis[strategy_name] = most_successful
        
        return number_analysis

    def plot_results(self, results: Dict[str, List[Dict]], output_path: str) -> None:
        """Generate plots comparing all strategies."""
        plt.figure(figsize=(15, 10))
        
        # Subplot 1: Evolución del bankroll
        plt.subplot(2, 2, 1)
        for strategy_name, sessions in results.items():
            # Encontrar la longitud mínima del historial
            min_length = min(len(session['bankroll_history']) for session in sessions)
            # Calcular el promedio solo hasta la longitud mínima
            avg_bankroll = [sum(session['bankroll_history'][i] for session in sessions) / len(sessions)
                          for i in range(min_length)]
            plt.plot(avg_bankroll, label=strategy_name)
        plt.title('Evolución Promedio del Bankroll')
        plt.xlabel('Número de Spins')
        plt.ylabel('Bankroll')
        plt.legend()
        
        # Subplot 2: Distribución de Win Rate
        plt.subplot(2, 2, 2)
        win_rates = {strategy_name: [session['win_rate'] for session in sessions]
                    for strategy_name, sessions in results.items()}
        plt.boxplot(win_rates.values(), labels=win_rates.keys())
        plt.title('Distribución de Win Rate')
        plt.xticks(rotation=45)
        plt.ylabel('Win Rate')
        
        # Subplot 3: Distribución de Profit/Loss
        plt.subplot(2, 2, 3)
        profits = {strategy_name: [session['final_bankroll'] - self.initial_bankroll for session in sessions]
                  for strategy_name, sessions in results.items()}
        plt.boxplot(profits.values(), labels=profits.keys())
        plt.title('Distribución de Profit/Loss')
        plt.xticks(rotation=45)
        plt.ylabel('Profit/Loss')
        
        # Subplot 4: Rango de Bankroll
        plt.subplot(2, 2, 4)
        bankroll_ranges = {strategy_name: [max(session['bankroll_history']) - min(session['bankroll_history'])
                                         for session in sessions]
                         for strategy_name, sessions in results.items()}
        plt.boxplot(bankroll_ranges.values(), labels=bankroll_ranges.keys())
        plt.title('Rango de Bankroll')
        plt.xticks(rotation=45)
        plt.ylabel('Rango')
        
        plt.tight_layout()
        plt.savefig(output_path)
        plt.close()

    def update_history(self, analysis: Dict, number_analysis: Dict) -> Dict[str, Tuple[bool, float]]:
        """Update history and return improvement status for each strategy."""
        improvements = {}
        
        for strategy_name in self.strategies:
            strategy_name = strategy_name.__name__
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