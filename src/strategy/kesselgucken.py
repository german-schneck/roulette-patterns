from typing import Dict, List
from .base_strategy import BaseStrategy
import random

class KesselguckenStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        
        # Grupos de sectores físicos de la ruleta (grupos Diamond)
        self.diamond_sectors = {
            'diamond_1': [0, 2, 14, 35],  # Primer diamante
            'diamond_2': [5, 17, 32, 20],  # Segundo diamante
            'diamond_3': [3, 26, 0, 32],   # Tercer diamante
            'diamond_4': [11, 30, 8, 23],  # Cuarto diamante
            'diamond_5': [10, 5, 24, 16],  # Quinto diamante
            'diamond_6': [33, 1, 20, 14],  # Sexto diamante
            'diamond_7': [9, 31, 18, 29],  # Séptimo diamante
            'diamond_8': [12, 28, 7, 29]   # Octavo diamante
        }
        
        # Dominios de números - agrupaciones basadas en la física de la ruleta
        self.dominios = {
            'top': [3, 26, 0, 32, 15],       # Dominio superior
            'right': [19, 4, 21, 2, 25],     # Dominio derecho
            'bottom': [17, 34, 6, 27, 13],   # Dominio inferior
            'left': [24, 36, 13, 1, 12]      # Dominio izquierdo
        }
        
        # Estado de la estrategia
        self.current_sector = 'diamond_1'
        self.sectors = list(self.diamond_sectors.keys())
        self.sector_index = 0
        self.consecutive_losses = 0
        self.max_sector_rotation = 5  # Máximo número de rotaciones antes de analizar resultados
        self.sector_rotation_count = 0
        
        # Historial de números ganadores para análisis de patrones
        self.winning_numbers_history = []
        self.hot_numbers = []  # Números "calientes" identificados
        self.bias_detected = False  # Bandera para indicar sesgo detectado
        self.bias_sector = None  # Sector con sesgo
        self.observation_phase = True  # Fase inicial de observación
        self.observation_spins = 25  # Tiradas de observación antes de estrategia completa
        
        # Progresión de apuestas
        self.progression = [1.0, 1.5, 2.0, 3.0, 4.0, 5.0]
        self.progression_index = 0
        
    def analyze_bias(self):
        """Analizar los números ganadores para detectar posibles sesgos."""
        if len(self.winning_numbers_history) < self.observation_spins:
            return  # No hay suficiente información para análisis
        
        # Contar frecuencia de números en cada sector
        sector_hits = {sector: 0 for sector in self.sectors}
        for number in self.winning_numbers_history[-30:]:  # Usar solo los últimos 30 números
            for sector, numbers in self.diamond_sectors.items():
                if number in numbers:
                    sector_hits[sector] += 1
        
        # Determinar si hay un sector con tendencia
        max_hits = max(sector_hits.values())
        expected_hits = len(self.winning_numbers_history[-30:]) / len(self.sectors)
        
        # Si hay un sector con significativamente más hits que el promedio
        if max_hits > expected_hits * 1.5:  # 50% más que lo esperado
            self.bias_detected = True
            # Encontrar el sector con más hits
            for sector, hits in sector_hits.items():
                if hits == max_hits:
                    self.bias_sector = sector
                    # Actualizar números "calientes"
                    self.hot_numbers = self.diamond_sectors[sector]
        else:
            self.bias_detected = False
            self.bias_sector = None
            # Si no hay sesgo, usar los números más frecuentes
            number_counts = {}
            for num in self.winning_numbers_history[-30:]:
                number_counts[num] = number_counts.get(num, 0) + 1
            
            # Obtener los 4 números más frecuentes
            sorted_numbers = sorted(number_counts.items(), key=lambda x: x[1], reverse=True)
            self.hot_numbers = [num for num, _ in sorted_numbers[:4]]
    
    def get_bet_numbers(self) -> List[int]:
        """Obtener los números para apostar."""
        if self.observation_phase or not self.bias_detected:
            # Durante observación o sin sesgo, apostar al sector actual
            return self.diamond_sectors[self.current_sector]
        else:
            # Con sesgo detectado, apostar a los números calientes
            return self.hot_numbers

    def calculate_bet(self) -> Dict[str, float]:
        """Calcular apuestas usando la estrategia Kesselgucken."""
        # Si estamos en fase de observación y no tenemos suficientes datos, 
        # hacer apuestas mínimas para recopilar información
        if self.observation_phase and len(self.winning_numbers_history) < self.observation_spins:
            # Durante la fase de observación, apostar al sector actual con apuesta mínima
            bet_numbers = self.diamond_sectors[self.current_sector]
            bet_per_number = self.min_bet / len(bet_numbers)
            return {str(num): bet_per_number for num in bet_numbers}
        
        # Analizar posibles sesgos en la ruleta
        self.analyze_bias()
        
        # Obtener números para apostar
        bet_numbers = self.get_bet_numbers()
        
        # Aplicar multiplicador según progresión
        multiplier = self.progression[min(self.progression_index, len(self.progression) - 1)]
        bet_amount = self.base_bet * multiplier
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_per_number = min(bet_amount / len(bet_numbers), self.current_bankroll / len(bet_numbers))
        
        # Crear diccionario de apuestas
        return {str(num): bet_per_number for num in bet_numbers}

    def update_bankroll(self, winnings: float):
        """Actualizar bankroll y estado de la estrategia."""
        self.current_bankroll += winnings
        
        # Si tenemos suficientes datos, terminamos la fase de observación
        if self.observation_phase and len(self.winning_numbers_history) >= self.observation_spins:
            self.observation_phase = False
            self.analyze_bias()  # Analizar datos recogidos
        
        if winnings > 0:
            # Si ganamos, reducir la progresión
            self.progression_index = max(0, self.progression_index - 1)
            self.consecutive_losses = 0
            
            # Añadir el número ganador a nuestro historial
            if len(self.winning_numbers_history) > 0:  # Suponemos que el último número añadido es el ganador
                # Si detectamos sesgo, ajustar apuestas futuras
                self.analyze_bias()
        else:
            # Si perdemos, aumentar progresión y contar pérdidas
            self.progression_index = min(self.progression_index + 1, len(self.progression) - 1)
            self.consecutive_losses += 1
            
            # Después de varias pérdidas consecutivas, rotar sector
            if self.consecutive_losses >= 3:
                self.consecutive_losses = 0
                self.sector_index = (self.sector_index + 1) % len(self.sectors)
                self.current_sector = self.sectors[self.sector_index]
                self.sector_rotation_count += 1
                
                # Después de varias rotaciones, analizar patrones nuevamente
                if self.sector_rotation_count >= self.max_sector_rotation:
                    self.sector_rotation_count = 0
                    self.analyze_bias()

    def record_winning_number(self, number: int):
        """Registrar un número ganador para análisis futuro."""
        self.winning_numbers_history.append(number)
        # Mantener solo los últimos 50 números para análisis
        if len(self.winning_numbers_history) > 50:
            self.winning_numbers_history.pop(0)

    def reset(self):
        """Resetear el estado de la estrategia."""
        super().reset()
        self.current_sector = 'diamond_1'
        self.sector_index = 0
        self.consecutive_losses = 0
        self.sector_rotation_count = 0
        self.observation_phase = True
        self.bias_detected = False
        self.bias_sector = None
        self.winning_numbers_history = []
        self.progression_index = 0
        self.base_bet = self.min_bet 