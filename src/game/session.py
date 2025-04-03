from typing import Dict, List
from .roulette import Roulette
from ..strategy.base_strategy import BaseStrategy

class GameSession:
    def __init__(self, strategy: BaseStrategy, max_spins: int = 1000, profit_target_percentage: float = 50.0):
        self.strategy = strategy
        self.roulette = Roulette()
        self.spins: List[Dict] = []
        self.bankroll_history: List[float] = [strategy.current_bankroll]
        self.wins = 0
        self.losses = 0
        self.total_spins = 0
        self.is_active = True
        self.max_spins = max_spins
        self.profit_target = strategy.current_bankroll * (profit_target_percentage / 100.0)
        self.initial_bankroll = strategy.current_bankroll

    def play_until_bankruptcy(self) -> None:
        """Play until termination conditions are met:
           1. Player goes bankrupt (bankroll < min_bet)
           2. Max spins reached
           3. Profit target reached
        """
        while (self.strategy.current_bankroll >= self.strategy.min_bet and 
               self.total_spins < self.max_spins and 
               self.strategy.current_bankroll < (self.initial_bankroll + self.profit_target)):
            
            # Calculate bet
            bet = self.strategy.calculate_bet()
            
            # Spin the wheel
            number, winnings = self.roulette.spin(bet)
            
            # Update strategy and session state
            self.strategy.update_bankroll(winnings)
            
            # Record spin
            self.spins.append({
                'number': number,
                'bet': bet,
                'winnings': winnings,
                'bankroll': self.strategy.current_bankroll
            })
            
            # Update bankroll history
            self.bankroll_history.append(self.strategy.current_bankroll)
            
            # Update win/loss count
            if winnings > 0:
                self.wins += 1
            else:
                self.losses += 1
            
            self.total_spins += 1

    def get_results(self) -> Dict:
        """Get the results of the game session."""
        # Determine termination reason
        if self.strategy.current_bankroll < self.strategy.min_bet:
            termination_reason = "bankruptcy"
        elif self.total_spins >= self.max_spins:
            termination_reason = "max_spins_reached"
        elif self.strategy.current_bankroll >= (self.initial_bankroll + self.profit_target):
            termination_reason = "profit_target_reached"
        else:
            termination_reason = "unknown"
            
        return {
            'num_spins': self.total_spins,
            'wins': self.wins,
            'losses': self.losses,
            'win_rate': self.wins / self.total_spins if self.total_spins > 0 else 0,
            'final_bankroll': self.strategy.current_bankroll,
            'initial_bankroll': self.initial_bankroll,
            'spins': self.spins,
            'bankroll_history': self.bankroll_history,
            'termination_reason': termination_reason
        } 