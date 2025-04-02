from typing import Dict
from .base_strategy import BaseStrategy

class FibonacciStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.fibonacci_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        self.current_index = 0
        self.consecutive_losses = 0

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet using the Fibonacci strategy."""
        # Fibonacci strategy: use Fibonacci sequence for bet amounts after losses
        if self.consecutive_losses > 0:
            # Use Fibonacci sequence, but don't exceed sequence length
            sequence_index = min(self.consecutive_losses - 1, len(self.fibonacci_sequence) - 1)
            self.current_bet = self.base_bet * self.fibonacci_sequence[sequence_index]
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
        self.current_index = 0
        self.consecutive_losses = 0 