from typing import Dict
from .base_strategy import BaseStrategy

class Lucky8Strategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.consecutive_losses = 0
        self.session_profit = 0.0
        self.target_profit = initial_bankroll * 0.1  # 10% del bankroll inicial
        self.lucky_numbers = [8, 18, 28]  # Números asociados con 8
        self.combinations = [
            [8, 18], [8, 28], [18, 28],  # Combinaciones de números 8
            [8, 17, 26], [8, 19, 27],    # Combinaciones de 3 números
            [8, 17, 26, 35]              # Combinación de 4 números
        ]
        self.current_combination_index = 0

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet based on the Lucky 8 strategy."""
        if self.consecutive_losses >= 3:
            # Después de 3 pérdidas consecutivas, apostar solo a números individuales
            bet_amount = self.base_bet * (self.consecutive_losses - 2)
            return {str(num): bet_amount for num in self.lucky_numbers}
        
        # Alternar entre números individuales y combinaciones
        if self.consecutive_losses % 2 == 0:
            # Apostar a números individuales
            bet_amount = self.base_bet
            return {str(num): bet_amount for num in self.lucky_numbers}
        else:
            # Apostar a combinaciones
            combination = self.combinations[self.current_combination_index]
            bet_amount = self.base_bet / len(combination)
            self.current_combination_index = (self.current_combination_index + 1) % len(self.combinations)
            return {str(num): bet_amount for num in combination}

    def update_bankroll(self, winnings: float):
        """Update the bankroll and strategy state based on winnings."""
        self.current_bankroll += winnings
        self.session_profit += winnings
        
        if winnings > 0:
            self.consecutive_losses = 0
            if self.session_profit >= self.target_profit:
                self.session_profit = 0.0
        else:
            self.consecutive_losses += 1

    def reset(self):
        """Reset the strategy state."""
        super().reset()
        self.consecutive_losses = 0
        self.session_profit = 0.0
        self.current_combination_index = 0 