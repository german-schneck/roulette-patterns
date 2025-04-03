from typing import Dict, List
from .base_strategy import BaseStrategy
import random

class MonacoSystemStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        
        # Configuración de sectores del sistema Monaco
        # Basado en el diseño de la ruleta del Casino de Monte Carlo
        self.tiers_du_cylindre = [33, 16, 24, 5, 10, 23, 8, 30, 11, 36, 13, 27]  # Tiers du Cylindre
        self.voisins_du_zero = [22, 18, 29, 7, 28, 12, 35, 3, 26, 0, 32, 15, 19, 4, 21, 2, 25]  # Voisins du Zero
        self.orphelins = [1, 20, 14, 31, 9, 17, 34, 6]  # Orphelins
        
        # Dividir la ruleta en tercios (por posición física)
        self.pockets = {
            'first_third': [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13],
            'second_third': [36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14],
            'last_third': [31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        }
        
        # Estado de la estrategia
        self.current_sector = 'tiers_du_cylindre'
        self.sector_options = ['tiers_du_cylindre', 'voisins_du_zero', 'orphelins']
        self.sector_index = 0
        self.progression_level = 0
        self.session_profit = 0.0
        
        # Matriz de progresión de apuestas (Monaco system tiene progresión específica)
        self.progression = [1.0, 2.0, 3.0, 4.0, 6.0, 9.0, 12.0, 18.0]
        
        # Sistema de switching (cambio basado en resultados)
        self.consecutive_losses = 0
        self.max_consecutive_losses = 4
        self.results_history = []  # Historial de resultados para análisis
        self.sector_success_count = {sector: 0 for sector in self.sector_options}
        
        # Gestión de bankroll Monaco
        self.profit_target = initial_bankroll * 0.15  # 15% de ganancia como objetivo
        self.stop_loss = initial_bankroll * 0.25  # 25% de pérdida como límite
    
    def get_current_sector_numbers(self) -> List[int]:
        """Obtener los números del sector actual."""
        if self.current_sector == 'tiers_du_cylindre':
            return self.tiers_du_cylindre
        elif self.current_sector == 'voisins_du_zero':
            return self.voisins_du_zero
        elif self.current_sector == 'orphelins':
            return self.orphelins
        
        # Fallback a un sector aleatorio si hay algún error
        return random.choice([self.tiers_du_cylindre, self.voisins_du_zero, self.orphelins])
    
    def determine_best_sector(self) -> str:
        """Determinar el mejor sector basado en resultados previos."""
        if not self.results_history:
            return 'tiers_du_cylindre'  # Sector por defecto
        
        # Analizar los últimos 20 resultados
        recent_results = self.results_history[-20:]
        sector_hits = {sector: 0 for sector in self.sector_options}
        
        for result in recent_results:
            if result in self.tiers_du_cylindre:
                sector_hits['tiers_du_cylindre'] += 1
            elif result in self.voisins_du_zero:
                sector_hits['voisins_du_zero'] += 1
            elif result in self.orphelins:
                sector_hits['orphelins'] += 1
        
        # Retornar el sector con más hits
        return max(sector_hits.items(), key=lambda x: x[1])[0]
    
    def switch_sector(self, forced=False):
        """Cambiar el sector de apuesta."""
        if forced or random.random() < 0.7:  # 70% de probabilidad de cambio inteligente
            # Elegir sector basado en análisis
            self.current_sector = self.determine_best_sector()
        else:
            # Cambio aleatorio/cíclico
            self.sector_index = (self.sector_index + 1) % len(self.sector_options)
            self.current_sector = self.sector_options[self.sector_index]

    def calculate_bet(self) -> Dict[str, float]:
        """Calcular apuestas usando el sistema Monaco."""
        # Obtener números del sector actual
        numbers = self.get_current_sector_numbers()
        
        # Multiplicador según nivel de progresión
        multiplier = self.progression[min(self.progression_level, len(self.progression) - 1)]
        bet_amount = self.base_bet * multiplier
        
        # Calcular apuesta por número (limitada por bankroll)
        bet_per_number = min(bet_amount / len(numbers), self.current_bankroll / len(numbers))
        
        # Verificar límites de bankroll
        if bet_per_number * len(numbers) > self.current_bankroll:
            bet_per_number = self.current_bankroll / len(numbers)
        
        # Crear diccionario de apuestas
        return {str(num): bet_per_number for num in numbers}

    def update_bankroll(self, winnings: float):
        """Actualizar bankroll y estado de la estrategia."""
        self.current_bankroll += winnings
        self.session_profit += winnings
        
        # Registrar resultado para análisis
        if self.results_history and winnings > 0:
            # Asumimos que el último número en la historia es el ganador
            winning_number = self.results_history[-1]
            
            # Incrementar contador de éxito para el sector
            for sector_name in self.sector_options:
                sector_numbers = getattr(self, sector_name)
                if winning_number in sector_numbers:
                    self.sector_success_count[sector_name] += 1
        
        # Verificar objetivos de ganancia y límites de pérdida
        if self.session_profit >= self.profit_target:
            # Si alcanzamos el objetivo, reiniciar
            self.progression_level = 0
            self.switch_sector(forced=True)
            self.session_profit = 0
            return
        
        if self.session_profit <= -self.stop_loss:
            # Si alcanzamos el límite de pérdida, reiniciar a estrategia conservadora
            self.progression_level = 0
            self.current_sector = 'tiers_du_cylindre'  # El sector más equilibrado
            return
        
        if winnings > 0:
            # Si ganamos, reducir el nivel de progresión
            self.progression_level = max(0, self.progression_level - 1)
            self.consecutive_losses = 0
            
            # Ocasionalmente cambiar de sector tras una victoria
            if random.random() < 0.25:  # 25% de probabilidad
                self.switch_sector()
        else:
            # Si perdemos, aumentar nivel de progresión y contar pérdidas
            self.progression_level = min(self.progression_level + 1, len(self.progression) - 1)
            self.consecutive_losses += 1
            
            # Después de varias pérdidas consecutivas, cambiar de sector
            if self.consecutive_losses >= self.max_consecutive_losses:
                self.consecutive_losses = 0
                self.switch_sector(forced=True)
    
    def record_result(self, number: int):
        """Registrar un resultado para análisis futuro."""
        self.results_history.append(number)
        # Mantener solo los últimos 50 resultados
        if len(self.results_history) > 50:
            self.results_history.pop(0)

    def reset(self):
        """Resetear la estrategia a su estado inicial."""
        super().reset()
        self.current_sector = 'tiers_du_cylindre'
        self.sector_index = 0
        self.progression_level = 0
        self.session_profit = 0.0
        self.consecutive_losses = 0
        self.results_history = []
        self.sector_success_count = {sector: 0 for sector in self.sector_options} 