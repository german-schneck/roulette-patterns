from typing import Dict
from .base_strategy import BaseStrategy

class OscarStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.current_bet = min_bet
        self.consecutive_losses = 0
        self.session_profit = 0
        self.max_consecutive_losses = 5  # Máximo de pérdidas consecutivas antes de reiniciar
        self.target_profit = initial_bankroll * 0.05  # 5% del bankroll inicial como objetivo

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet using Oscar's Grind strategy."""
        # Si estamos en pérdida en la sesión, aumentamos la apuesta
        if self.session_profit < 0:
            self.current_bet = self.base_bet * (1 + abs(self.session_profit) / self.base_bet)
        else:
            self.current_bet = self.base_bet

        # Asegurar que no apostamos más que nuestro bankroll
        if self.current_bet > self.current_bankroll:
            self.current_bet = self.current_bankroll

        # Si alcanzamos el máximo de pérdidas consecutivas, reiniciamos
        if self.consecutive_losses >= self.max_consecutive_losses:
            self.consecutive_losses = 0
            self.current_bet = self.base_bet

        # Si alcanzamos el objetivo de ganancia, reiniciamos
        if self.session_profit >= self.target_profit:
            self.session_profit = 0
            self.current_bet = self.base_bet

        return {'red': self.current_bet}

    def update_bankroll(self, winnings: float) -> None:
        """Update the bankroll and strategy state."""
        super().update_bankroll(winnings)
        
        # Actualizar contador de pérdidas consecutivas y ganancias de la sesión
        if winnings < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
            # Si ganamos, mantenemos la misma apuesta
            self.current_bet = self.current_bet

        self.session_profit += winnings

    def reset(self) -> None:
        """Reset the strategy to its initial state."""
        super().reset()
        self.consecutive_losses = 0
        self.session_profit = 0
        self.current_bet = self.base_bet 