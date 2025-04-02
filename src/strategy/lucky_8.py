from typing import Dict
import random
from .base_strategy import BaseStrategy

class Lucky8Strategy(BaseStrategy):
    def __init__(self, initial_bankroll: float, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.current_bet = min_bet
        self.consecutive_losses = 0
        self.max_consecutive_losses = 6
        self.lucky_8_numbers = [8, 18, 28, 38]  # Números que contienen 8
        self.lucky_8_combinations = [
            [8, 18], [8, 28], [8, 38],
            [18, 28], [18, 38], [28, 38]
        ]
        self.last_bet_type = None
        self.session_profit = 0
        self.target_profit = initial_bankroll * 0.06  # 6% del bankroll inicial como objetivo

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet using Lucky 8 strategy."""
        # Ajustar apuesta basada en pérdidas consecutivas
        if self.consecutive_losses > 0:
            self.current_bet = self.base_bet * (1.2 ** self.consecutive_losses)
        else:
            self.current_bet = self.base_bet

        # Asegurar que no apostamos más que nuestro bankroll
        if self.current_bet > self.current_bankroll:
            self.current_bet = self.current_bankroll

        # Determinar tipo de apuesta
        if self.last_bet_type is None or self.consecutive_losses >= 3:
            # Alternar entre lucky 8 numbers y combinaciones
            self.last_bet_type = 'single' if self.last_bet_type != 'single' else 'combination'
        
        # Colocar apuesta según el tipo
        if self.last_bet_type == 'single':
            lucky_number = random.choice(self.lucky_8_numbers)
            return {str(lucky_number): self.current_bet}
        else:
            # Elegir una combinación aleatoria de dos números
            combination = random.choice(self.lucky_8_combinations)
            bet_per_number = self.current_bet / 2
            return {str(num): bet_per_number for num in combination}

    def update_bankroll(self, winnings: float) -> None:
        """Update the bankroll and strategy state."""
        super().update_bankroll(winnings)
        
        # Actualizar contador de pérdidas consecutivas y ganancias de la sesión
        if winnings < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0
            self.session_profit += winnings

        # Si alcanzamos el objetivo de ganancia, reiniciamos
        if self.session_profit >= self.target_profit:
            self.session_profit = 0
            self.current_bet = self.base_bet

    def reset(self) -> None:
        """Reset the strategy to its initial state."""
        super().reset()
        self.consecutive_losses = 0
        self.session_profit = 0
        self.last_bet_type = None
        self.current_bet = self.base_bet 