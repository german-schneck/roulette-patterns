from typing import Dict, List
from .base_strategy import BaseStrategy

class LabouchereStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.target_profit = initial_bankroll * 0.1  # 10% del bankroll inicial
        self.sequence: List[float] = []
        self.initialize_sequence()

    def initialize_sequence(self):
        """Initialize the betting sequence to reach target profit."""
        remaining_profit = self.target_profit
        while remaining_profit > 0:
            bet = min(self.base_bet, remaining_profit)
            self.sequence.append(bet)
            remaining_profit -= bet

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet based on the Labouchere strategy."""
        if not self.sequence:
            self.initialize_sequence()
        
        # La suma de la primera y última apuesta
        bet_amount = self.sequence[0] + self.sequence[-1] if len(self.sequence) > 1 else self.sequence[0]
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_amount = min(bet_amount, self.current_bankroll)
        
        # Apostar a rojo (1:1)
        return {'red': bet_amount}

    def update_bankroll(self, winnings: float):
        """Update the bankroll and strategy state based on winnings."""
        self.current_bankroll += winnings
        
        if winnings > 0:
            # Si ganamos, eliminamos los números de la secuencia
            if len(self.sequence) > 1:
                self.sequence.pop(0)  # Eliminar primer número
                self.sequence.pop()   # Eliminar último número
            else:
                self.sequence.pop(0)  # Eliminar único número
                
            # Si la secuencia está vacía, reiniciamos
            if not self.sequence:
                self.initialize_sequence()
        else:
            # Si perdemos, agregamos la apuesta perdida al final
            self.sequence.append(self.sequence[0] + self.sequence[-1] if len(self.sequence) > 1 else self.sequence[0])

    def reset(self):
        """Reset the strategy state."""
        super().reset()
        self.sequence = []
        self.initialize_sequence() 