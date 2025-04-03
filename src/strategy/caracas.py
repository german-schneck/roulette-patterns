from typing import Dict, List
from .base_strategy import BaseStrategy

class CaracasStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        
        # Fases del método Caracas
        self.phases = ["conservadora", "agresiva", "recuperación"]
        self.current_phase = 0
        
        # Números clave para cada fase (inspirados en fechas históricas venezolanas)
        self.key_numbers = {
            "conservadora": [19, 5, 24, 30, 3],  # Fechas históricas (5 julio 1811, 24 julio 1783, etc.)
            "agresiva": [8, 13, 31, 17, 12],     # Números de suerte tradicional venezolana
            "recuperación": [24, 12, 36, 5, 0]   # Combinación estratégica
        }
        
        # Progresión de apuestas para cada fase
        self.bet_progression = {
            "conservadora": [1.0, 1.5, 2.0, 2.5],
            "agresiva": [1.0, 2.0, 3.0, 5.0],
            "recuperación": [1.0, 2.0, 4.0, 8.0]
        }
        
        self.current_progression_index = 0
        self.consecutive_losses = 0
        self.phase_threshold = 3  # Cambio de fase después de 3 pérdidas/ganancias consecutivas
        self.consecutive_phase_losses = 0
        
    def get_current_phase(self) -> str:
        """Get the current betting phase."""
        return self.phases[self.current_phase]
        
    def get_current_numbers(self) -> List[int]:
        """Get the numbers for the current phase."""
        phase = self.get_current_phase()
        return self.key_numbers[phase]
        
    def get_current_progression(self) -> float:
        """Get the current bet multiplier from the progression."""
        phase = self.get_current_phase()
        progression = self.bet_progression[phase]
        return progression[min(self.current_progression_index, len(progression) - 1)]

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet based on the Caracas method."""
        # Obtener números y multiplicador de apuesta actuales
        numbers = self.get_current_numbers()
        multiplier = self.get_current_progression()
        
        # Calcular apuesta base multiplicada
        bet_amount = self.base_bet * multiplier
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_per_number = min(bet_amount, self.current_bankroll / len(numbers))
        
        # Crear apuestas para cada número
        return {str(num): bet_per_number for num in numbers}

    def update_bankroll(self, winnings: float):
        """Update the bankroll and strategy state based on winnings."""
        self.current_bankroll += winnings
        
        if winnings > 0:
            # Si ganamos, mejoramos la progresión
            self.consecutive_losses = 0
            self.current_progression_index = max(0, self.current_progression_index - 1)
            
            # Contamos victorias consecutivas para posible cambio de fase
            if self.current_phase != 0:  # Si no estamos en fase conservadora
                self.consecutive_phase_losses -= 1
                if self.consecutive_phase_losses <= -self.phase_threshold:
                    # Volver a fase conservadora después de varias victorias
                    self.current_phase = 0
                    self.consecutive_phase_losses = 0
                    self.current_progression_index = 0
        else:
            # Si perdemos, avanzamos en la progresión y contamos
            self.consecutive_losses += 1
            self.current_progression_index = min(self.current_progression_index + 1, 
                                               len(self.bet_progression[self.get_current_phase()]) - 1)
            self.consecutive_phase_losses += 1
            
            # Si tenemos muchas pérdidas consecutivas, cambiamos de fase
            if self.consecutive_phase_losses >= self.phase_threshold:
                next_phase = min(self.current_phase + 1, len(self.phases) - 1)
                if next_phase != self.current_phase:
                    self.current_phase = next_phase
                    self.consecutive_phase_losses = 0
                    self.current_progression_index = 0

    def reset(self):
        """Reset the strategy state."""
        super().reset()
        self.current_phase = 0
        self.current_progression_index = 0
        self.consecutive_losses = 0
        self.consecutive_phase_losses = 0
        self.base_bet = self.min_bet 