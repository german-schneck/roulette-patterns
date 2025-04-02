from typing import Dict
import random
from .base_strategy import BaseStrategy

class DragonTigerStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.current_bet = min_bet
        self.consecutive_losses = 0
        self.max_consecutive_losses = 5
        self.lucky_numbers = [8, 18, 28]  # Números considerados de suerte en la cultura asiática
        self.last_bet_type = None

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet using Dragon Tiger strategy."""
        # Si tenemos pérdidas consecutivas, aumentamos la apuesta
        if self.consecutive_losses > 0:
            self.current_bet = self.base_bet * (1.5 ** self.consecutive_losses)
        else:
            self.current_bet = self.base_bet

        # Asegurar que no apostamos más que nuestro bankroll
        if self.current_bet > self.current_bankroll:
            self.current_bet = self.current_bankroll

        # Determinar tipo de apuesta
        if self.last_bet_type is None or self.consecutive_losses >= 2:
            # Alternar entre lucky numbers y color
            self.last_bet_type = 'lucky' if self.last_bet_type != 'lucky' else 'color'
        
        # Colocar apuesta según el tipo
        if self.last_bet_type == 'lucky':
            lucky_number = random.choice(self.lucky_numbers)
            return {str(lucky_number): self.current_bet}
        else:
            return {'red': self.current_bet}

    def update_bankroll(self, winnings: float) -> None:
        """Update the bankroll and strategy state."""
        super().update_bankroll(winnings)
        
        # Actualizar contador de pérdidas consecutivas
        if winnings < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

    def reset(self) -> None:
        """Reset the strategy to its initial state."""
        super().reset()
        self.consecutive_losses = 0
        self.last_bet_type = None
        self.current_bet = self.base_bet 