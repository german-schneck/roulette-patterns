from typing import Dict, List
from .base_strategy import BaseStrategy
import random

class CariocaStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        
        # Grupos de números inspirados en las escuelas de samba
        self.portela = [10, 20, 30]  # Portela (azul y blanco)
        self.mangueira = [1, 11, 21, 31]  # Mangueira (verde y rosa)
        self.salgueiro = [3, 13, 23, 33]  # Salgueiro (rojo y blanco)
        self.unidos = [7, 17, 27]  # Unidos da Tijuca (azul y amarillo)
        self.imperatriz = [5, 14, 25, 34]  # Imperatriz (verde y blanco)
        
        # Colores del carnaval
        self.carnival_colors = {
            'verde': [0, 10, 20, 30, 8, 26, 28],
            'amarillo': [1, 9, 13, 24, 27, 36],
            'azul': [2, 5, 15, 18, 22, 29, 32],
            'rojo': [3, 12, 16, 19, 23, 25, 34]
        }
        
        # Estado de la estrategia
        self.current_escola = 0  # Índice de la escuela actual
        self.current_color = 'verde'  # Color actual
        self.escolas = [self.portela, self.mangueira, self.salgueiro, self.unidos, self.imperatriz]
        self.escola_names = ['Portela', 'Mangueira', 'Salgueiro', 'Unidos', 'Imperatriz']
        self.colors = list(self.carnival_colors.keys())
        
        # Sistema de progresión "Samba"
        self.samba_steps = [1, 2, 1, 3, 1, 2, 4]  # Ritmo de samba en progresión de apuestas
        self.current_step = 0
        self.mode = 'escola'  # Alternamos entre 'escola' y 'color'
        self.win_streak = 0
        self.loss_streak = 0
        
    def get_current_bet_numbers(self) -> List[int]:
        """Get the current set of numbers to bet on based on mode."""
        if self.mode == 'escola':
            return self.escolas[self.current_escola]
        else:  # mode == 'color'
            return self.carnival_colors[self.current_color]
    
    def calculate_bet(self) -> Dict[str, float]:
        """Calculate bets using the Carioca strategy."""
        # Obtener números actuales
        bet_numbers = self.get_current_bet_numbers()
        
        # Aplicar multiplicador según paso de samba
        multiplier = self.samba_steps[self.current_step]
        bet_amount = self.base_bet * multiplier
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_per_number = min(bet_amount, self.current_bankroll / len(bet_numbers))
        
        # Crear diccionario de apuestas
        return {str(num): bet_per_number for num in bet_numbers}

    def update_bankroll(self, winnings: float):
        """Update bankroll and strategy state."""
        self.current_bankroll += winnings
        
        if winnings > 0:
            # Si ganamos, mejoramos
            self.win_streak += 1
            self.loss_streak = 0
            
            # Avanzar en los pasos de samba (hacia atrás)
            self.current_step = max(0, self.current_step - 1)
            
            # Cambiar de escuela/color después de varias victorias
            if self.win_streak >= 3:
                self.win_streak = 0
                if self.mode == 'escola':
                    # Cambiar a modo color
                    self.mode = 'color'
                    self.current_color = random.choice(self.colors)
                else:
                    # Cambiar a modo escola
                    self.mode = 'escola'
                    self.current_escola = (self.current_escola + 1) % len(self.escolas)
        else:
            # Si perdemos, retrocedemos
            self.loss_streak += 1
            self.win_streak = 0
            
            # Avanzar en los pasos de samba (hacia adelante)
            self.current_step = min(self.current_step + 1, len(self.samba_steps) - 1)
            
            # Después de muchas pérdidas consecutivas, cambiar drásticamente
            if self.loss_streak >= 5:
                self.loss_streak = 0
                
                # Cambiar modo y selección
                if self.mode == 'escola':
                    self.mode = 'color'
                    self.current_color = random.choice(self.colors)
                else:
                    self.mode = 'escola'
                    # Saltamos dos escuelas para cambio más radical
                    self.current_escola = (self.current_escola + 2) % len(self.escolas)

    def reset(self):
        """Reset the strategy to its initial state."""
        super().reset()
        self.current_escola = 0
        self.current_color = 'verde'
        self.mode = 'escola'
        self.current_step = 0
        self.win_streak = 0
        self.loss_streak = 0
        self.base_bet = self.min_bet 