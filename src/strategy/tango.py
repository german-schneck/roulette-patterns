from typing import Dict, List
from .base_strategy import BaseStrategy

class TangoStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        
        # Compases de tango (2/4, 4/4) y fechas importantes para Argentina
        self.tango_numbers = {
            'base': [2, 4, 8, 16, 24],  # Compases básicos
            'milonga': [9, 18, 25, 27, 36],  # Números asociados a milongas famosas
            'gardel': [11, 22, 33]  # En honor a Carlos Gardel
        }
        
        self.patterns = ['base', 'milonga', 'gardel']
        self.current_pattern = 0
        self.consecutive_losses = 0
        self.pattern_change_threshold = 3
        self.progression = [1.0, 1.5, 2.0, 3.0, 4.5]  # Progresión de apuestas
        self.progression_index = 0
        
        # Sistema de "paradas" (stops) - puntos de ganancia objetivo y límites de pérdida
        self.session_profit = 0.0
        self.target_profit = initial_bankroll * 0.25  # 25% de ganancia objetivo
        self.stop_loss = initial_bankroll * 0.2  # 20% como límite de pérdida
        
    def get_current_numbers(self) -> List[int]:
        """Get the current set of numbers to bet on."""
        pattern = self.patterns[self.current_pattern]
        return self.tango_numbers[pattern]
    
    def calculate_bet(self) -> Dict[str, float]:
        """Calculate bets using the Tango strategy."""
        # Obtener conjunto actual de números
        numbers = self.get_current_numbers()
        
        # Determinar multiplicador de apuesta según progresión
        multiplier = self.progression[min(self.progression_index, len(self.progression) - 1)]
        bet_amount = self.base_bet * multiplier
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_per_number = min(bet_amount, self.current_bankroll / len(numbers))
        
        # Si la apuesta total excede el bankroll, redimensionar
        if bet_per_number * len(numbers) > self.current_bankroll:
            bet_per_number = self.current_bankroll / len(numbers)
            
        # Crear diccionario de apuestas
        return {str(num): bet_per_number for num in numbers}

    def update_bankroll(self, winnings: float):
        """Update bankroll and strategy state."""
        self.current_bankroll += winnings
        self.session_profit += winnings
        
        # Verificar si alcanzamos ganancia objetivo o límite de pérdida
        if self.session_profit >= self.target_profit:
            # Reiniciar si alcanzamos el objetivo
            self.session_profit = 0
            self.progression_index = 0
            self.current_pattern = 0
            self.consecutive_losses = 0
            return
            
        if self.session_profit <= -self.stop_loss:
            # Cambiar a patrón más conservador si alcanzamos límite de pérdida
            self.session_profit = 0
            self.current_pattern = 0  # Volver al patrón base
            self.progression_index = 0
            return
        
        if winnings > 0:
            # Si ganamos, reducir la progresión
            self.progression_index = max(0, self.progression_index - 1)
            self.consecutive_losses = 0
        else:
            # Si perdemos, aumentar progresión y contar pérdidas
            self.progression_index = min(self.progression_index + 1, len(self.progression) - 1)
            self.consecutive_losses += 1
            
            # Cambiar patrón después de varias pérdidas consecutivas
            if self.consecutive_losses >= self.pattern_change_threshold:
                self.current_pattern = (self.current_pattern + 1) % len(self.patterns)
                self.consecutive_losses = 0

    def reset(self):
        """Reset the strategy to its initial state."""
        super().reset()
        self.current_pattern = 0
        self.consecutive_losses = 0
        self.progression_index = 0
        self.session_profit = 0.0
        self.base_bet = self.min_bet 