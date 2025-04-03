from typing import Dict
from .base_strategy import BaseStrategy

class GrandeMartingaleStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.current_bet = min_bet
        self.consecutive_losses = 0
        self.max_consecutive_losses = 10  # Límite para evitar ruina total
        self.extra_units = 2  # Unidades extra para hacer la estrategia más agresiva
        
        # Factor de escalado (mucho más agresivo que el Martingale normal)
        self.aggressive_mode = False  # Comienza en modo conservador
        self.profit_trigger = initial_bankroll * 0.1  # 10% de ganancia para activar modo agresivo
        self.session_profit = 0.0
        
        # Conteo de resultados para cambiar entre rojo/negro
        self.color_switch_count = 0
        self.current_color = 'red'  # Comienza apostando al rojo
        
    def toggle_color(self):
        """Cambiar de color para las apuestas."""
        self.current_color = 'black' if self.current_color == 'red' else 'red'

    def calculate_bet(self) -> Dict[str, float]:
        """Calcular la siguiente apuesta usando la estrategia Grande Martingale."""
        # En caso de pérdidas consecutivas, la apuesta es:
        # - Martingale normal: 2^n * base_bet
        # - Grande Martingale: 2^n * base_bet + n * extra_units
        if self.consecutive_losses > 0:
            factor = 2 ** self.consecutive_losses
            extra = self.consecutive_losses * self.extra_units * self.base_bet
            
            # En modo agresivo, añadir factor adicional
            if self.aggressive_mode:
                extra *= 1.5
                
            self.current_bet = (factor * self.base_bet) + extra
        else:
            self.current_bet = self.base_bet
        
        # Limitar la apuesta al bankroll disponible
        self.current_bet = min(self.current_bet, self.current_bankroll)
        
        # Si alcanzamos el máximo de pérdidas consecutivas, reiniciar
        if self.consecutive_losses >= self.max_consecutive_losses:
            self.current_bet = self.base_bet
            self.consecutive_losses = 0
            # Cambiar de color después de muchas pérdidas
            self.toggle_color()
        
        # Verificar si necesitamos cambiar de color
        self.color_switch_count += 1
        if self.color_switch_count >= 12:  # Cambiar color cada 12 apuestas
            self.toggle_color()
            self.color_switch_count = 0
        
        return {self.current_color: self.current_bet}

    def update_bankroll(self, winnings: float):
        """Actualizar el bankroll y el estado de la estrategia."""
        self.current_bankroll += winnings
        self.session_profit += winnings
        
        # Comprobar si activamos el modo agresivo
        if self.session_profit >= self.profit_trigger and not self.aggressive_mode:
            self.aggressive_mode = True
        elif self.session_profit <= 0 and self.aggressive_mode:
            self.aggressive_mode = False
        
        if winnings > 0:
            # Si ganamos, reiniciar la secuencia
            self.consecutive_losses = 0
            self.current_bet = self.base_bet
            
            # Después de una victoria, ocasionalmente cambiar de color
            if self.calculate_randomized_switch():
                self.toggle_color()
        else:
            # Si perdemos, incrementar el contador de pérdidas
            self.consecutive_losses += 1
    
    def calculate_randomized_switch(self) -> bool:
        """Determinar aleatoriamente si cambiar de color tras una victoria."""
        # Probabilidad 1/3 de cambiar tras victoria (para evitar patrones predecibles)
        import random
        return random.random() < 0.33

    def reset(self):
        """Resetear la estrategia a su estado inicial."""
        super().reset()
        self.consecutive_losses = 0
        self.current_bet = self.base_bet
        self.aggressive_mode = False
        self.session_profit = 0.0
        self.color_switch_count = 0
        self.current_color = 'red' 