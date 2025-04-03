from typing import Dict, List, Tuple
from .base_strategy import BaseStrategy
import random
import math
import numpy as np

class StatisticalMechanicsStrategy(BaseStrategy):
    """
    Estrategia basada en principios de mecánica estadística:
    - Entropía y teoría de la información
    - Distribuciones de Maxwell-Boltzmann
    - Equilibrio termodinámico y fluctuaciones
    - Transiciones de fase en sistemas complejos
    """
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        
        # Parámetros termodinámicos
        self.temperature = 1.0  # Temperatura del sistema (controla aleatoriedad)
        self.energy_states = {i: 1.0 for i in range(37)}  # Energía de cada número
        self.entropy = math.log(37)  # Entropía inicial (máxima)
        self.beta = 1.0  # Factor de Boltzmann (1/kT)
        
        # Historial y estadísticas
        self.number_history = []
        self.frequency_distribution = {i: 0 for i in range(37)}
        self.energy_history = []  # Historial de energía del sistema
        
        # Fases del sistema
        self.phase = 'disordered'  # 'disordered', 'ordered', 'critical'
        self.phase_transition_point = 0.5  # Punto de transición de fase
        self.relaxation_time = 15  # Tiempo de relajación del sistema
        self.time_since_transition = 0
        
        # Configuración de microestados
        self.microstates = self._initialize_microstates()
        self.current_microstate = 'uniform'
        
        # Parámetros de apuesta
        self.bet_temperature_factor = 2.0  # Factor para escalar apuestas con temperatura
        self.max_bet_fraction = 0.06  # Máximo 6% del bankroll
        self.min_numbers = 3  # Mínimo de números a apostar
        self.max_numbers = 10  # Máximo de números a apostar
        
    def _initialize_microstates(self) -> Dict[str, Dict[int, float]]:
        """Inicializar configuraciones de microestados del sistema."""
        microstates = {
            'uniform': {i: 1.0 for i in range(37)},  # Distribución uniforme
            'thirds': {},  # Tercio de la ruleta con energía más baja
            'odd_even': {},  # Alternancia entre pares e impares
            'neighbors': {},  # Vecinos físicos con correlación
            'hot_cold': {}  # Números "calientes" y "fríos"
        }
        
        # Configuración para 'thirds' (dividir la ruleta en tercios)
        for i in range(37):
            if i <= 12:
                microstates['thirds'][i] = 3.0
            elif i <= 24:
                microstates['thirds'][i] = 1.0
            else:
                microstates['thirds'][i] = 0.5
                
        # Configuración para 'odd_even'
        for i in range(37):
            if i == 0:
                microstates['odd_even'][i] = 1.0
            elif i % 2 == 0:  # Par
                microstates['odd_even'][i] = 2.0
            else:  # Impar
                microstates['odd_even'][i] = 0.5
                
        # Configuración para 'neighbors' (vecinos físicos)
        roulette_order = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 
                          11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 
                          9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        
        focus_point = random.choice(roulette_order)
        for i in range(37):
            # Calcular distancia en la rueda
            i_pos = roulette_order.index(i)
            focus_pos = roulette_order.index(focus_point)
            dist = min(abs(i_pos - focus_pos), 37 - abs(i_pos - focus_pos))
            # Mayor energía para vecinos cercanos
            microstates['neighbors'][i] = math.exp(-0.3 * dist)
            
        # Inicializar 'hot_cold' (se actualizará con datos reales)
        for i in range(37):
            microstates['hot_cold'][i] = 1.0
            
        return microstates
    
    def update_temperature(self, winning_number: int):
        """Actualizar temperatura del sistema basado en el historial."""
        self.time_since_transition += 1
        
        # Registrar número y actualizar distribución
        self.frequency_distribution[winning_number] += 1
        
        # Calcular la entropía actual del sistema
        total_spins = sum(self.frequency_distribution.values())
        if total_spins > 0:
            entropy = 0
            for count in self.frequency_distribution.values():
                if count > 0:
                    p = count / total_spins
                    entropy -= p * math.log(p)
                    
            self.entropy = entropy
            
            # Calcular "temperatura" basada en la entropía
            # Menor entropía = sistema más "frío" (más ordenado)
            max_entropy = math.log(37)  # Entropía máxima (distribución uniforme)
            self.temperature = max(0.1, min(5.0, entropy / max_entropy * 3.0))
            
            # Actualizar beta (inverso de la temperatura)
            self.beta = 1.0 / self.temperature
    
    def update_energy_states(self):
        """Actualizar estados de energía basados en la distribución actual."""
        total_spins = sum(self.frequency_distribution.values())
        if total_spins < 10:
            return  # No hay suficientes datos
        
        # Actualizar microestado 'hot_cold' basado en frecuencias
        max_freq = max(self.frequency_distribution.values())
        min_freq = min(self.frequency_distribution.values())
        range_freq = max(1, max_freq - min_freq)
        
        for i in range(37):
            # Normalizar frecuencia a un valor entre 0 y 1
            norm_freq = (self.frequency_distribution[i] - min_freq) / range_freq
            # Convertir a energía (mayor frecuencia = menor energía)
            self.microstates['hot_cold'][i] = 1.0 - norm_freq
            
        # Recalcular estados de energía basados en el microestado actual
        for i in range(37):
            self.energy_states[i] = self.microstates[self.current_microstate][i]
    
    def determine_phase(self):
        """Determinar la fase actual del sistema basado en la entropía."""
        # Normalizar entropía entre 0 y 1
        norm_entropy = self.entropy / math.log(37)
        
        # Transición de fase basada en entropía
        old_phase = self.phase
        
        if norm_entropy > 0.8:
            # Alta entropía = sistema desordenado
            self.phase = 'disordered'
        elif norm_entropy < 0.4:
            # Baja entropía = sistema ordenado
            self.phase = 'ordered'
        else:
            # Entropía intermedia = punto crítico
            self.phase = 'critical'
            
        # Si cambiamos de fase, resetear contador
        if old_phase != self.phase:
            self.time_since_transition = 0
            
            # En transición de fase, actualizar microestado
            if self.phase == 'ordered':
                # Cuando el sistema se ordena, apostar a los "patrones" detectados
                self.current_microstate = 'hot_cold'
            elif self.phase == 'disordered':
                # Cuando está desordenado, apostar uniforme o a tercios
                self.current_microstate = random.choice(['uniform', 'thirds'])
            else:  # critical
                # En punto crítico, usar vecinos o alternancia
                self.current_microstate = random.choice(['neighbors', 'odd_even'])
    
    def calculate_boltzmann_probabilities(self) -> Dict[int, float]:
        """Calcular probabilidades según distribución de Boltzmann."""
        # Probabilidades basadas en e^(-βE)
        probabilities = {}
        denominator = 0
        
        for i in range(37):
            # Menor energía = mayor probabilidad
            energy = self.energy_states[i]
            p = math.exp(-self.beta * energy)
            probabilities[i] = p
            denominator += p
            
        # Normalizar
        for i in range(37):
            probabilities[i] /= denominator
            
        return probabilities
    
    def select_numbers_by_probability(self, probabilities: Dict[int, float], count: int) -> List[int]:
        """Seleccionar números basados en sus probabilidades."""
        # Convertir a formato para np.random.choice
        numbers = list(range(37))
        probs = [probabilities[i] for i in range(37)]
        
        # Normalizar probabilidades
        probs = np.array(probs) / sum(probs)
        
        # Seleccionar sin reemplazo
        try:
            selected = np.random.choice(numbers, size=count, replace=False, p=probs)
            return selected.tolist()
        except:
            # Fallback en caso de error
            return sorted(probabilities.items(), key=lambda x: x[1], reverse=True)[:count]
    
    def calculate_optimal_bet_count(self) -> int:
        """Calcular el número óptimo de números para apostar según la fase."""
        if self.phase == 'ordered':
            # En sistema ordenado, apostar a menos números
            count = self.min_numbers + int(self.temperature)
        elif self.phase == 'disordered':
            # En sistema desordenado, apostar a más números
            count = self.min_numbers + int(self.temperature * 2)
        else:  # critical
            # En punto crítico, balance
            count = self.min_numbers + int(self.temperature * 1.5)
            
        return max(self.min_numbers, min(self.max_numbers, count))
    
    def calculate_bet_amount(self) -> float:
        """Calcular monto de apuesta basado en termodinámica del sistema."""
        # Factor basado en la fase
        if self.phase == 'ordered':
            # Sistema ordenado = apuestas más grandes
            factor = 2.0
        elif self.phase == 'disordered':
            # Sistema desordenado = apuestas más pequeñas
            factor = 1.0
        else:  # critical
            # Punto crítico = depende del tiempo desde transición
            # Usar fluctuaciones cerca del punto crítico
            critical_factor = 1.5 + 0.5 * math.sin(0.5 * self.time_since_transition)
            factor = critical_factor
            
        # Ajustar por temperatura (menor temperatura = mayor confianza)
        temperature_modifier = self.bet_temperature_factor / (0.5 + self.temperature)
        
        bet = self.base_bet * factor * temperature_modifier
        
        # Limitar a un porcentaje máximo del bankroll
        max_bet = self.current_bankroll * self.max_bet_fraction
        return min(bet, max_bet)

    def calculate_bet(self) -> Dict[str, float]:
        """Calcular apuestas usando principios de mecánica estadística."""
        # Actualizar estados de energía
        self.update_energy_states()
        
        # Determinar fase del sistema
        self.determine_phase()
        
        # Calcular probabilidades según Boltzmann
        probabilities = self.calculate_boltzmann_probabilities()
        
        # Determinar cuántos números apostar
        bet_count = self.calculate_optimal_bet_count()
        
        # Seleccionar números basados en probabilidades
        bet_numbers = self.select_numbers_by_probability(probabilities, bet_count)
        
        # Calcular monto total a apostar
        total_bet = self.calculate_bet_amount()
        
        # Distribuir entre los números seleccionados
        bet_per_number = total_bet / len(bet_numbers)
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_per_number = min(bet_per_number, self.current_bankroll / len(bet_numbers))
        
        return {str(num): bet_per_number for num in bet_numbers}

    def update_bankroll(self, winnings: float):
        """Actualizar bankroll y estado de la estrategia."""
        self.current_bankroll += winnings
        
        # Fluctuaciones en temperatura basadas en resultados
        if winnings > 0:
            # Victoria = sistema más "frío" (más ordenado)
            self.temperature = max(0.2, self.temperature * 0.9)
            
            # Victoria en fase crítica puede llevar a ordenación
            if self.phase == 'critical' and random.random() < 0.7:
                self.phase = 'ordered'
                self.time_since_transition = 0
                
        else:
            # Derrota = sistema más "caliente" (más desordenado)
            self.temperature = min(5.0, self.temperature * 1.1)
            
            # Múltiples derrotas pueden llevar a fase desordenada
            if self.time_since_transition > self.relaxation_time and random.random() < 0.3:
                self.phase = 'disordered'
                self.time_since_transition = 0
                
        # Actualizar beta
        self.beta = 1.0 / self.temperature
        
        # Registrar energía del sistema
        current_energy = sum(self.energy_states.values())
        self.energy_history.append(current_energy)
        if len(self.energy_history) > 50:
            self.energy_history.pop(0)
    
    def record_number(self, number: int):
        """Registrar un número para análisis."""
        self.number_history.append(number)
        if len(self.number_history) > 100:
            self.number_history.pop(0)
            
        # Actualizar temperatura y distribución
        self.update_temperature(number)

    def reset(self):
        """Resetear la estrategia a su estado inicial."""
        super().reset()
        self.temperature = 1.0
        self.entropy = math.log(37)
        self.beta = 1.0
        self.number_history = []
        self.frequency_distribution = {i: 0 for i in range(37)}
        self.energy_history = []
        self.phase = 'disordered'
        self.time_since_transition = 0
        self.current_microstate = 'uniform'
        
        # Reinicializar microestados
        self.microstates = self._initialize_microstates()
        # Reinicializar estados de energía
        self.energy_states = {i: 1.0 for i in range(37)} 