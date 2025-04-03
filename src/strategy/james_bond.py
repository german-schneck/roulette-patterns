from typing import Dict
from .base_strategy import BaseStrategy

class JamesBondStrategy(BaseStrategy):
    """
    Estrategia James Bond - Un sistema de cobertura fijo para ruleta europea.
    
    Esta estrategia, mencionada en las novelas de Ian Fleming, implica una cobertura de 
    25 de los 37 números en la ruleta. La distribución clásica de la apuesta es:
    - 14 unidades en los números altos (19-36)
    - 5 unidades en la sexta línea (13-18)
    - 1 unidad en el 0
    
    Con cada apuesta se cubren 25 números con diferentes pagos.
    """
    
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        # La unidad de apuesta base debe ser al menos el mínimo
        self.unit_size = max(min_bet, 1.0)
        
        # Tracking de resultados
        self.consecutive_losses = 0
        self.total_spins = 0
        self.profit_this_session = 0.0
        self.max_consecutive_losses = 0
        
        # Sistema de progresión
        self.progression_level = 1
        self.max_progression = 4  # Límite para evitar apuestas excesivas
        
        # Control de objetivos
        self.target_profit = 20.0 * self.unit_size  # Objetivo: 20 unidades de ganancia
        self.stop_loss = -40.0 * self.unit_size     # Parar si se pierden 40 unidades
    
    def calculate_bet(self) -> Dict[str, float]:
        """
        Calcula las apuestas según la estrategia James Bond.
        
        Retorna un diccionario con las apuestas a realizar:
        - 14 unidades en números altos (19-36) - paga 1:1
        - 5 unidades en sexta línea (13-18) - paga 5:1
        - 1 unidad en el 0 - paga 35:1
        """
        # Calcular el tamaño de la unidad actual según el nivel de progresión
        current_unit = self.unit_size * self.progression_level
        
        # Total de la apuesta: 20 unidades
        total_bet = current_unit * 20
        
        # Verificar si tenemos suficiente bankroll
        if total_bet > self.current_bankroll:
            # Si no hay suficiente bankroll, usar lo que queda
            current_unit = self.current_bankroll / 20
        
        bets = {}
        
        # Apuesta en los números altos (19-36) - 14 unidades
        high_bet = current_unit * 14
        for i in range(19, 37):
            bets[str(i)] = high_bet / 18  # Distribuir entre 18 números
        
        # Apuesta en la sexta línea (13-18) - 5 unidades
        line_bet = current_unit * 5
        for i in range(13, 19):
            bets[str(i)] = line_bet / 6  # Distribuir entre 6 números
        
        # Apuesta en el 0 - 1 unidad
        bets["0"] = current_unit
        
        return bets
    
    def update_bankroll(self, winnings: float):
        """
        Actualiza el bankroll y ajusta la estrategia según el resultado.
        
        Args:
            winnings: La cantidad ganada (o perdida si es negativa) en la apuesta.
        """
        self.current_bankroll += winnings
        self.total_spins += 1
        self.profit_this_session += winnings
        
        # Determinar si fue una victoria o pérdida
        current_unit = self.unit_size * self.progression_level
        total_bet = current_unit * 20
        
        if winnings >= 0:  # Victoria
            self.consecutive_losses = 0
            # Si alcanzamos el objetivo de ganancia, resetear la progresión
            if self.profit_this_session >= self.target_profit:
                self.progression_level = 1
                self.profit_this_session = 0.0
            # Después de una victoria, reducir un nivel la progresión (si es posible)
            elif self.progression_level > 1:
                self.progression_level -= 1
        else:  # Pérdida
            self.consecutive_losses += 1
            if self.consecutive_losses > self.max_consecutive_losses:
                self.max_consecutive_losses = self.consecutive_losses
            
            # Aumentar la progresión tras pérdida, pero limitada al máximo
            if self.consecutive_losses >= 2:
                self.progression_level = min(self.progression_level + 1, self.max_progression)
            
            # Si alcanzamos el límite de pérdida, resetear la progresión
            if self.profit_this_session <= self.stop_loss:
                self.progression_level = 1
                self.profit_this_session = 0.0
    
    def reset(self):
        """Resetea la estrategia a su estado inicial."""
        super().reset()
        self.consecutive_losses = 0
        self.total_spins = 0
        self.profit_this_session = 0.0
        self.max_consecutive_losses = 0
        self.progression_level = 1 