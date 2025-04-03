from typing import Dict, List
from .base_strategy import BaseStrategy
import random

class TulumStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.hot_numbers = [17, 34, 6]  # Números iniciales "calientes"
        self.last_winning_numbers = []
        self.cycle_length = 5  # Cambiar números calientes cada 5 tiradas
        self.cycle_count = 0
        self.neighbors = {  # Vecinos físicos en la ruleta americana
            0: [0, 2, 28],
            1: [1, 20, 33],
            2: [2, 0, 14],
            3: [3, 26, 35],
            4: [4, 15, 23],
            5: [5, 10, 24],
            6: [6, 27, 13],
            7: [7, 18, 29],
            8: [8, 12, 19],
            9: [9, 31, 22],
            10: [10, 5, 8],
            11: [11, 30, 36],
            12: [12, 8, 29],
            13: [13, 6, 34],
            14: [14, 2, 35],
            15: [15, 4, 19],
            16: [16, 23, 33],
            17: [17, 25, 34],
            18: [18, 7, 22],
            19: [19, 15, 8],
            20: [20, 1, 14],
            21: [21, 28, 36],
            22: [22, 9, 18],
            23: [23, 4, 16],
            24: [24, 5, 33],
            25: [25, 17, 2],
            26: [26, 3, 0],
            27: [27, 6, 35],
            28: [28, 21, 0],
            29: [29, 7, 12],
            30: [30, 11, 26],
            31: [31, 9, 20],
            32: [32, 13, 35],
            33: [33, 1, 16],
            34: [34, 17, 13],
            35: [35, 3, 32],
            36: [36, 11, 21]
        }

    def update_hot_numbers(self, winning_number: int):
        """Update the list of hot numbers based on recent wins."""
        self.last_winning_numbers.append(winning_number)
        if len(self.last_winning_numbers) > 10:  # Mantener solo los últimos 10 números
            self.last_winning_numbers.pop(0)
        
        self.cycle_count += 1
        if self.cycle_count >= self.cycle_length:
            self.cycle_count = 0
            # Actualizar números calientes basado en los más frecuentes
            if self.last_winning_numbers:
                counts = {}
                for num in self.last_winning_numbers:
                    counts[num] = counts.get(num, 0) + 1
                sorted_nums = sorted(counts.items(), key=lambda x: x[1], reverse=True)
                self.hot_numbers = [num for num, _ in sorted_nums[:3]]
                if len(self.hot_numbers) < 3:  # Si no hay suficientes números diferentes
                    while len(self.hot_numbers) < 3:
                        new_num = random.randint(0, 36)
                        if new_num not in self.hot_numbers:
                            self.hot_numbers.append(new_num)

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet based on the Tulum strategy."""
        # Apostar a los números calientes y sus vecinos
        bet_numbers = set()
        for num in self.hot_numbers:
            bet_numbers.update(self.neighbors.get(num, [num]))
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_amount = min(self.base_bet, self.current_bankroll / len(bet_numbers))
        
        # Crear diccionario de apuestas
        return {str(num): bet_amount for num in bet_numbers}

    def update_bankroll(self, winnings: float):
        """Update the bankroll and strategy state based on winnings."""
        self.current_bankroll += winnings
        
        # Actualizar números calientes si sabemos qué número ganó
        if winnings > 0 and self.last_winning_numbers:
            self.update_hot_numbers(int(self.last_winning_numbers[-1]))
        
        # Ajustar apuesta según resultados
        if winnings > 0:
            # Si ganamos, reducir ligeramente la apuesta
            self.base_bet = max(self.min_bet, self.base_bet * 0.9)
        else:
            # Si perdemos, aumentar la apuesta
            self.base_bet = min(self.base_bet * 1.2, self.current_bankroll * 0.1)

    def reset(self):
        """Reset the strategy state."""
        super().reset()
        self.hot_numbers = [17, 34, 6]
        self.last_winning_numbers = []
        self.cycle_count = 0
        self.base_bet = self.min_bet 