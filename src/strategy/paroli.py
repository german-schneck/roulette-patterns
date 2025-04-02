from typing import Dict
from .base_strategy import BaseStrategy

class ParoliStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.current_bet = min_bet
        self.consecutive_wins = 0
        self.max_consecutive_wins = 3  # Máximo de victorias consecutivas antes de reiniciar
        self.target_profit = initial_bankroll * 0.1  # 10% del bankroll inicial como objetivo

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet using Paroli strategy."""
        # Si tenemos ganancias consecutivas, doblamos la apuesta
        if self.consecutive_wins > 0:
            self.current_bet = self.base_bet * (2 ** self.consecutive_wins)
        else:
            self.current_bet = self.base_bet

        # Asegurar que no apostamos más que nuestro bankroll
        if self.current_bet > self.current_bankroll:
            self.current_bet = self.current_bankroll

        # Si alcanzamos el objetivo de ganancia, reiniciamos
        if self.current_bankroll >= self.initial_bankroll + self.target_profit:
            self.consecutive_wins = 0
            self.current_bet = self.base_bet

        return {'red': self.current_bet}

    def update_bankroll(self, winnings: float) -> None:
        """Update the bankroll and strategy state."""
        super().update_bankroll(winnings)
        
        # Actualizar contador de victorias consecutivas
        if winnings > 0:
            self.consecutive_wins += 1
            # Si alcanzamos el máximo de victorias consecutivas, reiniciamos
            if self.consecutive_wins >= self.max_consecutive_wins:
                self.consecutive_wins = 0
                self.current_bet = self.base_bet
        else:
            self.consecutive_wins = 0
            self.current_bet = self.base_bet

    def reset(self) -> None:
        """Reset the strategy to its initial state."""
        super().reset()
        self.consecutive_wins = 0
        self.current_bet = self.base_bet 