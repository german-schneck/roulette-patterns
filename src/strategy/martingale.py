from typing import Dict
from .base_strategy import BaseStrategy

class MartingaleStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.current_bet = min_bet
        self.consecutive_losses = 0

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet using the Martingale strategy."""
        # Martingale strategy: double bet after each loss, reset to base bet after win
        if self.consecutive_losses > 0:
            self.current_bet = self.base_bet * (2 ** self.consecutive_losses)
        else:
            self.current_bet = self.base_bet

        # Ensure we don't bet more than our current bankroll
        if self.current_bet > self.current_bankroll:
            self.current_bet = self.current_bankroll

        # Place bet on red (could be modified to bet on other options)
        return {'red': self.current_bet}

    def update_bankroll(self, winnings: float) -> None:
        """Update the bankroll and strategy state."""
        super().update_bankroll(winnings)
        
        # Update consecutive losses counter
        if winnings < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

    def reset(self) -> None:
        """Reset the strategy to its initial state."""
        super().reset()
        self.current_bet = self.base_bet
        self.consecutive_losses = 0 