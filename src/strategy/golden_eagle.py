from typing import Dict
import random
from .base_strategy import BaseStrategy

class GoldenEagleStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.current_bet = min_bet
        self.consecutive_losses = 0
        self.max_consecutive_losses = 4
        self.golden_numbers = [7, 17, 27]  # Números dorados en la cultura asiática
        self.last_bet_type = None
        self.session_profit = 0
        self.target_profit = initial_bankroll * 0.08  # 8% del bankroll inicial como objetivo

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet using Golden Eagle strategy."""
        # Ajustar apuesta basada en pérdidas consecutivas y ganancias de la sesión
        if self.consecutive_losses > 0:
            self.current_bet = self.base_bet * (1.3 ** self.consecutive_losses)
        elif self.session_profit < 0:
            self.current_bet = self.base_bet * 1.2
        else:
            self.current_bet = self.base_bet

        # Asegurar que no apostamos más que nuestro bankroll
        if self.current_bet > self.current_bankroll:
            self.current_bet = self.current_bankroll

        # Determinar tipo de apuesta
        if self.last_bet_type is None or self.consecutive_losses >= 2:
            # Alternar entre golden numbers y docena
            self.last_bet_type = 'golden' if self.last_bet_type != 'golden' else 'dozen'
        
        # Colocar apuesta según el tipo
        if self.last_bet_type == 'golden':
            golden_number = random.choice(self.golden_numbers)
            return {str(golden_number): self.current_bet}
        else:
            # Apostar a la primera docena (1-12)
            return {'first_dozen': self.current_bet}

    def update_bankroll(self, winnings: float) -> None:
        """Update the bankroll and strategy state."""
        super().update_bankroll(winnings)
        
        # Actualizar contador de pérdidas consecutivas y ganancias de la sesión
        if winnings < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

        self.session_profit += winnings

        # Si alcanzamos el objetivo de ganancia, reiniciamos
        if self.session_profit >= self.target_profit:
            self.session_profit = 0
            self.current_bet = self.base_bet

    def reset(self) -> None:
        """Reset the strategy to its initial state."""
        super().reset()
        self.consecutive_losses = 0
        self.session_profit = 0
        self.last_bet_type = None
        self.current_bet = self.base_bet 