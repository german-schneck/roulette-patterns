from typing import Dict, List
from .base_strategy import BaseStrategy

class ValparaisoStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        
        # Cerros (colinas) de Valparaíso - grupos de números por sector
        self.cerros = {
            'alegre': [1, 3, 5, 7, 9],  # Cerro Alegre (números impares < 10)
            'concepcion': [12, 14, 16, 18, 20],  # Cerro Concepción (pares 12-20)
            'playa_ancha': [21, 23, 25, 27, 29],  # Playa Ancha (impares 21-29)
            'cordillera': [30, 31, 32, 33, 34, 35, 36],  # Cordillera (números altos)
            'puerto': [0, 2, 4, 6, 8, 10]  # Puerto (0 y pares < 12)
        }
        
        # Secuencia de visita a los cerros (inspirada en recorrido turístico)
        self.sequence = ['puerto', 'alegre', 'concepcion', 'playa_ancha', 'cordillera']
        self.current_cerro_index = 0
        
        # Sistema de gestión de bankroll inspirado en mareas
        self.marea_alta = False  # Bandera para modo "marea alta" (apuestas altas)
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.win_threshold = 3  # Umbral para activar marea alta
        self.loss_threshold = 4  # Umbral para desactivar marea alta
        
        # Multiplicadores para cada estado de marea
        self.marea_baja_multipliers = [1.0, 1.2, 1.5, 1.8]  # Multiplicadores en marea baja
        self.marea_alta_multipliers = [2.0, 2.5, 3.0, 4.0]  # Multiplicadores en marea alta
        self.current_multiplier_index = 0

    def get_current_cerro(self) -> List[int]:
        """Get the current hill (cerro) numbers."""
        cerro_name = self.sequence[self.current_cerro_index]
        return self.cerros[cerro_name]

    def get_current_multiplier(self) -> float:
        """Get the current bet multiplier based on tide state."""
        if self.marea_alta:
            multipliers = self.marea_alta_multipliers
        else:
            multipliers = self.marea_baja_multipliers
            
        return multipliers[min(self.current_multiplier_index, len(multipliers) - 1)]

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate bets using the Valparaiso strategy."""
        # Obtener números del cerro actual
        numbers = self.get_current_cerro()
        
        # Aplicar multiplicador actual
        multiplier = self.get_current_multiplier()
        bet_amount = self.base_bet * multiplier
        
        # Distribuir la apuesta entre los números
        bet_per_number = min(bet_amount / len(numbers), self.current_bankroll / len(numbers))
        
        # Crear diccionario de apuestas
        return {str(num): bet_per_number for num in numbers}

    def update_bankroll(self, winnings: float):
        """Update bankroll and strategy state."""
        self.current_bankroll += winnings
        
        if winnings > 0:
            # Victoria
            self.consecutive_wins += 1
            self.consecutive_losses = 0
            
            # Reducir multiplier si estamos ganando
            if self.current_multiplier_index > 0:
                self.current_multiplier_index -= 1
                
            # Comprobar cambio de marea
            if self.consecutive_wins >= self.win_threshold and not self.marea_alta:
                self.marea_alta = True
                self.current_multiplier_index = 0  # Resetear índice al cambiar
                
            # Cambiar de cerro después de dos victorias consecutivas
            if self.consecutive_wins % 2 == 0:
                self.current_cerro_index = (self.current_cerro_index + 1) % len(self.sequence)
        else:
            # Derrota
            self.consecutive_losses += 1
            self.consecutive_wins = 0
            
            # Aumentar multiplier si estamos perdiendo
            multipliers = self.marea_alta_multipliers if self.marea_alta else self.marea_baja_multipliers
            if self.current_multiplier_index < len(multipliers) - 1:
                self.current_multiplier_index += 1
                
            # Comprobar cambio de marea
            if self.consecutive_losses >= self.loss_threshold and self.marea_alta:
                self.marea_alta = False
                self.current_multiplier_index = 0  # Resetear índice al cambiar
                
            # Cambiar de cerro después de tres derrotas consecutivas
            if self.consecutive_losses % 3 == 0:
                # Moverse dos cerros hacia adelante para un cambio más drástico
                self.current_cerro_index = (self.current_cerro_index + 2) % len(self.sequence)

    def reset(self):
        """Reset the strategy to its initial state."""
        super().reset()
        self.current_cerro_index = 0
        self.marea_alta = False
        self.consecutive_wins = 0
        self.consecutive_losses = 0
        self.current_multiplier_index = 0
        self.base_bet = self.min_bet 