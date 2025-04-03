from typing import Dict
from .base_strategy import BaseStrategy

class OneThreeTwoSixStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.consecutive_wins = 0
        self.bet_multipliers = [1, 3, 2, 6]  # Secuencia de multiplicadores
        self.current_position = 0
        self.session_profit = 0.0
        self.target_profit = initial_bankroll * 0.1  # 10% del bankroll inicial

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet based on the 1-3-2-6 strategy."""
        if self.consecutive_wins == 0:
            # Si no hay ganancias consecutivas, volver al inicio
            self.current_position = 0
            bet_amount = self.base_bet
        else:
            # Usar el multiplicador correspondiente a la posición actual
            multiplier = self.bet_multipliers[self.current_position]
            bet_amount = self.base_bet * multiplier
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_amount = min(bet_amount, self.current_bankroll)
        
        # Apostar a rojo (1:1)
        return {'red': bet_amount}

    def update_bankroll(self, winnings: float):
        """Update the bankroll and strategy state based on winnings."""
        self.current_bankroll += winnings
        self.session_profit += winnings
        
        if winnings > 0:
            self.consecutive_wins += 1
            # Avanzar en la secuencia si hay suficientes ganancias consecutivas
            if self.consecutive_wins <= len(self.bet_multipliers):
                self.current_position = self.consecutive_wins - 1
            
            # Si alcanzamos el objetivo de ganancia, reiniciamos
            if self.session_profit >= self.target_profit:
                self.session_profit = 0.0
                self.consecutive_wins = 0
                self.current_position = 0
        else:
            # Si perdemos, volvemos al inicio
            self.consecutive_wins = 0
            self.current_position = 0

    def reset(self):
        """Reset the strategy state."""
        super().reset()
        self.consecutive_wins = 0
        self.current_position = 0
        self.session_profit = 0.0 