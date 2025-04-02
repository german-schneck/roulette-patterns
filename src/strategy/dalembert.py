from typing import Dict
from .base_strategy import BaseStrategy

class DAlembertStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.current_bet = min_bet
        self.consecutive_losses = 0
        self.max_consecutive_losses = 5  # Máximo de pérdidas consecutivas antes de reiniciar
        self.bet_increment = min_bet  # Incremento de apuesta después de cada pérdida

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet using D'Alembert strategy."""
        # Ajustar la apuesta basada en pérdidas consecutivas
        if self.consecutive_losses > 0:
            self.current_bet = self.base_bet + (self.bet_increment * self.consecutive_losses)
        else:
            self.current_bet = self.base_bet

        # Asegurar que no apostamos más que nuestro bankroll
        if self.current_bet > self.current_bankroll:
            self.current_bet = self.current_bankroll

        # Si alcanzamos el máximo de pérdidas consecutivas, reiniciamos
        if self.consecutive_losses >= self.max_consecutive_losses:
            self.consecutive_losses = 0
            self.current_bet = self.base_bet

        return {'red': self.current_bet}

    def update_bankroll(self, winnings: float) -> None:
        """Update the bankroll and strategy state."""
        super().update_bankroll(winnings)
        
        # Actualizar contador de pérdidas consecutivas
        if winnings < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
            # Si ganamos, reducimos la apuesta al siguiente giro
            self.current_bet = max(self.base_bet, self.current_bet - self.bet_increment)

    def reset(self) -> None:
        """Reset the strategy to its initial state."""
        super().reset()
        self.consecutive_losses = 0
        self.current_bet = self.base_bet 