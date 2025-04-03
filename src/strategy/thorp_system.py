from typing import Dict, List, Tuple
from .base_strategy import BaseStrategy
import math
import random

class ThorpSystemStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        
        # Thorp utilizaba análisis matemático para identificar sesgos
        # Sectores para análisis de varianza estadística
        self.number_sectors = {
            'third_1': list(range(1, 13)),
            'third_2': list(range(13, 25)),
            'third_3': list(range(25, 37))
        }
        
        # Vecinos físicos de números (simplificación del análisis de Thorp)
        self.physical_neighbors = {
            i: [(i+j) % 37 for j in [-2, -1, 1, 2, 3]] for i in range(37)
        }
        
        # Configuración de análisis
        self.winning_history = []
        self.sector_hit_count = {sector: 0 for sector in self.number_sectors.keys()}
        self.number_hit_count = {i: 0 for i in range(37)}
        self.sample_size = 50  # Tamaño de muestra para análisis
        self.chi_squared_threshold = 12.0  # Umbral para detección de sesgo
        
        # Estado de la estrategia
        self.current_betting_numbers = []
        self.phase = "observation"  # Fases: "observation", "betting"
        self.observation_count = 0
        self.min_observations = 30  # Mínimo de observaciones antes de apostar
        
        # Kelly criterion para gestión de bankroll
        self.kelly_fraction = 0.05  # Factor conservador para Kelly
        self.expected_edge = 0.0  # Ventaja esperada (actualizado con análisis)
        
        # Contadores para cambiar estrategia
        self.strategy_change_threshold = 15  # Cambiar tras N spins sin éxito
        self.spins_since_last_win = 0
        
    def record_number(self, number: int):
        """Registrar un número para análisis."""
        self.winning_history.append(number)
        
        # Mantener solo los últimos sample_size números
        if len(self.winning_history) > self.sample_size:
            old_number = self.winning_history.pop(0)
            # Actualizar contadores para el número eliminado
            self.number_hit_count[old_number] -= 1
            for sector, numbers in self.number_sectors.items():
                if old_number in numbers:
                    self.sector_hit_count[sector] -= 1
        
        # Actualizar contadores para el nuevo número
        self.number_hit_count[number] += 1
        for sector, numbers in self.number_sectors.items():
            if number in numbers:
                self.sector_hit_count[sector] += 1
                
        # En fase de observación, incrementar contador
        if self.phase == "observation":
            self.observation_count += 1
            # Cambiar a fase de apuestas si tenemos suficientes observaciones
            if self.observation_count >= self.min_observations:
                self.phase = "betting"
                self.analyze_bias()
    
    def analyze_bias(self) -> Tuple[bool, List[int]]:
        """Analizar los datos para detectar sesgos en la ruleta."""
        # No suficientes datos para análisis
        if len(self.winning_history) < self.min_observations:
            return False, []
        
        # 1. Análisis de sectores - Chi cuadrado
        expected_hits_per_sector = len(self.winning_history) / len(self.number_sectors)
        chi_squared = sum(
            ((hits - expected_hits_per_sector) ** 2) / expected_hits_per_sector
            for hits in self.sector_hit_count.values()
        )
        
        sector_bias = chi_squared > self.chi_squared_threshold
        
        # 2. Análisis de números individuales
        expected_hits_per_number = len(self.winning_history) / 37
        biased_numbers = []
        
        for num, hits in self.number_hit_count.items():
            # Un número se considera sesgado si su frecuencia es significativamente mayor
            if hits > expected_hits_per_number * 1.75:  # 75% más que lo esperado
                biased_numbers.append(num)
                
                # Incluir vecinos físicos si el sesgo es fuerte
                if hits > expected_hits_per_number * 2.5:
                    biased_numbers.extend(self.physical_neighbors[num])
        
        # Eliminar duplicados y limitar a 8 números máximo
        biased_numbers = list(set(biased_numbers))[:8]
        
        # Calcular la ventaja esperada (edge)
        if biased_numbers:
            # Probabilidad de victoria con números sesgados
            p_win = sum(self.number_hit_count[n] for n in biased_numbers) / len(self.winning_history)
            # Pago esperado (35:1 para números individuales)
            payout = 36  # Ganancia + apuesta original
            # Ventaja esperada según fórmula de Thorp
            self.expected_edge = p_win * payout - 1
        else:
            self.expected_edge = 0.0
        
        return sector_bias or bool(biased_numbers), biased_numbers
    
    def calculate_kelly_bet(self, numbers: List[int]) -> float:
        """Calcular tamaño de apuesta óptimo según criterio de Kelly."""
        if not numbers or self.expected_edge <= 0:
            return self.base_bet
        
        # Probabilidad de ganar
        p_win = len(numbers) / 37
        # Odds contra (cuánto se gana por unidad apostada)
        b = 36 / len(numbers) - 1
        
        # Fórmula de Kelly: f* = (bp - q)/b donde q = 1-p
        f_star = (b * p_win - (1 - p_win)) / b
        
        # Aplicar fracción conservadora y asegurar que es positivo
        kelly_bet = max(0, f_star * self.kelly_fraction * self.current_bankroll)
        
        # Limitar a un rango razonable
        return max(self.base_bet, min(kelly_bet, self.current_bankroll * 0.1))

    def calculate_bet(self) -> Dict[str, float]:
        """Calcular apuestas usando el sistema Thorp."""
        # Durante la fase de observación, no apostamos
        if self.phase == "observation" or len(self.winning_history) < self.min_observations:
            # Apuesta mínima en un solo número para seguir recolectando datos
            random_number = random.randint(0, 36)
            return {str(random_number): self.min_bet}
        
        # Analizar datos para detectar sesgos
        bias_detected, biased_numbers = self.analyze_bias()
        
        if bias_detected and biased_numbers:
            # Usar números con sesgo detectado
            self.current_betting_numbers = biased_numbers
        else:
            # Si no hay sesgo claro, usar una estrategia alternativa
            # Thorp sugería apostar en números que no han salido recientemente
            least_frequent = sorted(self.number_hit_count.items(), key=lambda x: x[1])
            self.current_betting_numbers = [num for num, _ in least_frequent[:6]]
        
        # Calcular el tamaño óptimo de apuesta usando Kelly
        total_bet = self.calculate_kelly_bet(self.current_betting_numbers)
        
        # Distribuir la apuesta entre los números seleccionados
        bet_per_number = total_bet / len(self.current_betting_numbers)
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_per_number = min(bet_per_number, self.current_bankroll / len(self.current_betting_numbers))
        
        return {str(num): bet_per_number for num in self.current_betting_numbers}

    def update_bankroll(self, winnings: float):
        """Actualizar bankroll y estado de la estrategia."""
        self.current_bankroll += winnings
        
        # Registrar el número ganador para análisis
        # Asumimos que el ultimo número en la historia es el ganador
        if self.winning_history:
            last_number = self.winning_history[-1]
            
            # Actualizar contadores de éxito/fracaso
            if winnings > 0:
                self.spins_since_last_win = 0
            else:
                self.spins_since_last_win += 1
            
            # Cambiar estrategia si llevamos muchos spins sin ganar
            if self.spins_since_last_win >= self.strategy_change_threshold:
                self.spins_since_last_win = 0
                # Reanalizar los datos con un enfoque diferente
                self.analyze_bias()
    
    def reset(self):
        """Resetear la estrategia a su estado inicial."""
        super().reset()
        self.winning_history = []
        self.sector_hit_count = {sector: 0 for sector in self.number_sectors.keys()}
        self.number_hit_count = {i: 0 for i in range(37)}
        self.current_betting_numbers = []
        self.phase = "observation"
        self.observation_count = 0
        self.expected_edge = 0.0
        self.spins_since_last_win = 0 