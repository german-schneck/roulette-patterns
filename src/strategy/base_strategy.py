from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

class BaseStrategy(ABC):
    def __init__(self, initial_bankroll: float, min_bet: float = 1.0):
        self.initial_bankroll = initial_bankroll
        self.current_bankroll = initial_bankroll
        self.min_bet = min_bet
        self.bet_history: List[Dict] = []
        self.spins_history: List[Dict] = []
        self.is_bankrupt = False

    @abstractmethod
    def calculate_bet(self) -> Dict[str, float]:
        """
        Calculate the next bet based on the strategy.
        Returns a dictionary with bet types and amounts.
        Example: {'red': 10.0, 'black': 0.0, 'zero': 0.0}
        """
        pass

    def update_bankroll(self, winnings: float) -> None:
        """Update the current bankroll with winnings or losses."""
        self.current_bankroll += winnings
        if self.current_bankroll < self.min_bet:
            self.is_bankrupt = True

    def record_bet(self, bet: Dict[str, float]) -> None:
        """Record a bet in the history."""
        self.bet_history.append({
            'bet': bet,
            'bankroll': self.current_bankroll
        })

    def record_spin(self, number: int, winnings: float) -> None:
        """Record a spin result in the history."""
        self.spins_history.append({
            'number': number,
            'winnings': winnings,
            'bankroll': self.current_bankroll
        })

    def get_statistics(self) -> Dict:
        """Get statistics about the strategy's performance."""
        total_spins = len(self.spins_history)
        if total_spins == 0:
            return {
                'total_spins': 0,
                'win_rate': 0,
                'profit_loss': 0,
                'max_bankroll': self.initial_bankroll,
                'min_bankroll': self.initial_bankroll,
                'final_bankroll': self.current_bankroll
            }

        winning_spins = sum(1 for spin in self.spins_history if spin['winnings'] > 0)
        total_profit_loss = self.current_bankroll - self.initial_bankroll
        max_bankroll = max(spin['bankroll'] for spin in self.spins_history)
        min_bankroll = min(spin['bankroll'] for spin in self.spins_history)

        return {
            'total_spins': total_spins,
            'win_rate': winning_spins / total_spins,
            'profit_loss': total_profit_loss,
            'max_bankroll': max_bankroll,
            'min_bankroll': min_bankroll,
            'final_bankroll': self.current_bankroll
        }

    def reset(self) -> None:
        """Reset the strategy to its initial state."""
        self.current_bankroll = self.initial_bankroll
        self.bet_history = []
        self.spins_history = []
        self.is_bankrupt = False 