from typing import Dict, List
from .base_strategy import BaseStrategy

class MontevideoStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        
        # Números basados en la historia uruguaya y cultura
        self.independence_numbers = [18, 25, 30]  # Fechas de independencia (25/08/1830)
        self.mate_numbers = [5, 10, 15, 20, 25, 30, 35]  # Números separados por 5 (tiempo de cebar mate)
        self.tango_numbers = [2, 4, 8, 11, 22]  # Inspirados en el tango y milonga
        
        # Secuencias especiales
        self.candombe_sequence = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]  # Ritmo de candombe
        self.portuario_sequence = [1, 7, 13, 19, 23, 31]  # Barrio portuario
        
        # Sistema "Barrios" - diferentes sectores de apuesta
        self.barrios = {
            'ciudad_vieja': self.independence_numbers,
            'prado': self.mate_numbers,
            'pocitos': self.tango_numbers,
            'palermo': self.candombe_sequence,
            'puerto': self.portuario_sequence
        }
        
        # Estado de la estrategia
        self.current_barrio = 'ciudad_vieja'
        self.barrio_rotation = ['ciudad_vieja', 'prado', 'pocitos', 'palermo', 'puerto']
        self.barrio_index = 0
        
        # Sistema de progresión "Río de la Plata"
        self.river_levels = {
            'bajo': 1.0,      # Nivel bajo del río
            'normal': 1.5,    # Nivel normal
            'crecido': 2.0,   # Nivel crecido
            'inundacion': 3.0 # Nivel de inundación
        }
        self.current_river_level = 'bajo'
        self.river_states = ['bajo', 'normal', 'crecido', 'inundacion']
        self.river_index = 0
        
        self.win_counter = 0
        self.loss_counter = 0
        self.persistence_factor = 3  # Cambios en el nivel del río
    
    def get_current_numbers(self) -> List[int]:
        """Get numbers for the current neighborhood (barrio)."""
        return self.barrios[self.current_barrio]
    
    def get_river_multiplier(self) -> float:
        """Get the current river level multiplier."""
        return self.river_levels[self.current_river_level]

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate bets using the Montevideo strategy."""
        # Obtener números del barrio actual
        numbers = self.get_current_numbers()
        
        # Aplicar multiplicador según nivel del río
        multiplier = self.get_river_multiplier()
        bet_amount = self.base_bet * multiplier
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_per_number = min(bet_amount / len(numbers), self.current_bankroll / len(numbers))
        
        # Crear diccionario de apuestas
        return {str(num): bet_per_number for num in numbers}

    def raise_river_level(self):
        """Raise the river level."""
        self.river_index = min(self.river_index + 1, len(self.river_states) - 1)
        self.current_river_level = self.river_states[self.river_index]
    
    def lower_river_level(self):
        """Lower the river level."""
        self.river_index = max(self.river_index - 1, 0)
        self.current_river_level = self.river_states[self.river_index]
    
    def change_barrio(self, forward: bool = True):
        """Change the current neighborhood."""
        if forward:
            self.barrio_index = (self.barrio_index + 1) % len(self.barrio_rotation)
        else:
            self.barrio_index = (self.barrio_index - 1) % len(self.barrio_rotation)
        self.current_barrio = self.barrio_rotation[self.barrio_index]

    def update_bankroll(self, winnings: float):
        """Update bankroll and strategy state."""
        self.current_bankroll += winnings
        
        if winnings > 0:
            # Victoria
            self.win_counter += 1
            self.loss_counter = 0
            
            # Después de varias victorias consecutivas
            if self.win_counter >= self.persistence_factor:
                self.win_counter = 0
                
                # Reducir el nivel del río (menos agresivo)
                self.lower_river_level()
                
                # Cambiar de barrio (hacia adelante)
                self.change_barrio(forward=True)
            
            # Ajustar base bet en ganancias
            if self.win_counter >= 2:
                # Aumentar ligeramente la apuesta base con ganancias
                self.base_bet = min(self.base_bet * 1.1, self.current_bankroll * 0.01)
        else:
            # Derrota
            self.loss_counter += 1
            self.win_counter = 0
            
            # Después de varias derrotas consecutivas
            if self.loss_counter >= self.persistence_factor:
                self.loss_counter = 0
                
                # Aumentar el nivel del río (más agresivo)
                self.raise_river_level()
                
                # Cambiar de barrio (hacia atrás)
                self.change_barrio(forward=False)
            
            # Ajustar base bet en pérdidas
            if self.loss_counter >= 2:
                # Reducir la apuesta base con pérdidas
                self.base_bet = max(self.min_bet, self.base_bet * 0.9)

    def reset(self):
        """Reset the strategy to its initial state."""
        super().reset()
        self.current_barrio = 'ciudad_vieja'
        self.barrio_index = 0
        self.current_river_level = 'bajo'
        self.river_index = 0
        self.win_counter = 0
        self.loss_counter = 0
        self.base_bet = self.min_bet 