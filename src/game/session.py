from typing import Dict, List
from .roulette import Roulette
from ..strategy.base_strategy import BaseStrategy

class GameSession:
    def __init__(self, strategy: BaseStrategy):
        self.strategy = strategy
        self.roulette = Roulette()
        self.spins: List[Dict] = []
        self.bankroll_history: List[float] = [strategy.current_bankroll]
        self.wins = 0
        self.losses = 0
        self.total_spins = 0
        self.is_active = True

    def play_until_bankruptcy(self) -> Dict:
        """
        Play the game until the strategy goes bankrupt or reaches a target.
        Returns statistics about the game session.
        """
        while self.is_active and not self.strategy.is_bankrupt:
            # Calculate and place bets
            bets = self.strategy.calculate_bet()
            self.strategy.record_bet(bets)
            
            # Spin the wheel
            winning_number = self.roulette.spin()
            number_properties = self.roulette.get_number_properties(winning_number)
            
            # Calculate winnings
            winnings = self._calculate_winnings(bets, number_properties)
            
            # Update strategy state
            self.strategy.update_bankroll(winnings)
            self.strategy.record_spin(winning_number, winnings)
            
            # Record spin
            self.spins.append({
                'number': winning_number,
                'properties': number_properties,
                'bets': bets,
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
            
            # Check if we should stop
            if self.strategy.is_bankrupt:
                self.is_active = False
        
        return self.strategy.get_statistics()

    def _calculate_winnings(self, bets: Dict[str, float], number_properties: Dict) -> float:
        """Calculate winnings based on bets and winning number properties."""
        winnings = 0.0
        
        # Color bets
        if 'red' in bets and number_properties['color'] == 'red':
            winnings += bets['red'] * 2
        if 'black' in bets and number_properties['color'] == 'black':
            winnings += bets['black'] * 2
            
        # Zero bet
        if 'zero' in bets and number_properties['is_zero']:
            winnings += bets['zero'] * 36
            
        # Even/Odd bets
        if 'even' in bets and number_properties['is_even']:
            winnings += bets['even'] * 2
        if 'odd' in bets and number_properties['is_odd']:
            winnings += bets['odd'] * 2
            
        # Dozen bets
        if 'first_dozen' in bets and number_properties['dozen'] == 1:
            winnings += bets['first_dozen'] * 3
        if 'second_dozen' in bets and number_properties['dozen'] == 2:
            winnings += bets['second_dozen'] * 3
        if 'third_dozen' in bets and number_properties['dozen'] == 3:
            winnings += bets['third_dozen'] * 3
            
        # Column bets
        if 'first_column' in bets and number_properties['column'] == 1:
            winnings += bets['first_column'] * 3
        if 'second_column' in bets and number_properties['column'] == 2:
            winnings += bets['second_column'] * 3
        if 'third_column' in bets and number_properties['column'] == 3:
            winnings += bets['third_column'] * 3
            
        # Street bets
        for street_num, numbers in self.roulette.streets.items():
            bet_key = f'street_{street_num}'
            if bet_key in bets and number_properties['number'] in numbers:
                winnings += bets[bet_key] * 12
                
        # Corner bets
        for corner_nums, numbers in self.roulette.corners.items():
            bet_key = f'corner_{corner_nums}'
            if bet_key in bets and number_properties['number'] in numbers:
                winnings += bets[bet_key] * 9
        
        # Subtract total bet amount
        total_bet = sum(bets.values())
        return winnings - total_bet 

    def get_results(self) -> Dict:
        """Get the results of the game session."""
        return {
            'num_spins': self.total_spins,
            'wins': self.wins,
            'losses': self.losses,
            'win_rate': self.wins / self.total_spins if self.total_spins > 0 else 0,
            'final_bankroll': self.strategy.current_bankroll,
            'spins': self.spins,
            'bankroll_history': self.bankroll_history
        } 