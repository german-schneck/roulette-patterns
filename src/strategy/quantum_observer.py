from typing import Dict, List, Tuple
from .base_strategy import BaseStrategy
import random
import math

class QuantumObserverStrategy(BaseStrategy):
    """
    Estrategia basada en los principios de la física cuántica:
    - Principio de incertidumbre de Heisenberg
    - Efecto del observador
    - Superposición cuántica
    - Entrelazamiento entre números
    """
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        
        # Definir estados cuánticos (representando la probabilidad de cada número)
        self.quantum_states = {i: 1/37 for i in range(37)}  # Distribución uniforme inicial
        
        # Estado de la estrategia
        self.observation_phase = True
        self.min_observations = 20
        self.observation_count = 0
        self.winning_history = []
        self.entangled_pairs = []  # Pares de números con correlación
        self.superposition_sectors = []  # Sectores actualmente en superposición
        
        # Parámetros cuánticos
        self.collapse_threshold = 0.15  # Umbral para "colapso" de función de onda
        self.uncertainty_factor = 0.08  # Factor de incertidumbre de Heisenberg
        self.interference_matrix = self._initialize_interference()
        self.coherence = 1.0  # Coherencia cuántica (se reduce con cada medición)
        
        # Ciclos de estrategia cuántica
        self.cycle_phase = 'superposition'  # 'superposition', 'entanglement', 'collapse'
        self.cycle_count = 0
        self.phase_duration = 5  # Tiradas por fase
        
        # Gestión de bankroll
        self.max_bet_percentage = 0.05  # Máximo 5% del bankroll por tirada
        self.wavefunction_collapse = False  # Indicador de colapso de la función de onda
        
        # Inicializar sectores en superposición
        self._initialize_superposition()
    
    def _initialize_interference(self) -> Dict[int, Dict[int, float]]:
        """Inicializar matriz de interferencia entre números."""
        interference = {}
        # Crear matriz de interferencia basada en distancia física en la rueda
        roulette_order = [0, 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 
                           11, 30, 8, 23, 10, 5, 24, 16, 33, 1, 20, 14, 31, 
                           9, 22, 18, 29, 7, 28, 12, 35, 3, 26]
        
        for i in range(37):
            interference[i] = {}
            i_pos = roulette_order.index(i)
            for j in range(37):
                j_pos = roulette_order.index(j)
                # Calcular distancia mínima en el círculo
                dist = min(abs(i_pos - j_pos), 37 - abs(i_pos - j_pos))
                # Convertir distancia a factor de interferencia
                interference[i][j] = math.exp(-0.3 * dist)
        
        return interference
    
    def _initialize_superposition(self):
        """Inicializar sectores en superposición."""
        # Definir sectores físicos de la ruleta en superposición
        self.superposition_sectors = [
            [0, 32, 15, 19, 4, 21],  # Primer sector
            [21, 2, 25, 17, 34, 6],  # Segundo sector
            [6, 27, 13, 36, 11, 30],  # Tercer sector
            [30, 8, 23, 10, 5, 24],   # Cuarto sector
            [24, 16, 33, 1, 20, 14],  # Quinto sector
            [14, 31, 9, 22, 18, 29],  # Sexto sector
            [29, 7, 28, 12, 35, 3, 26]  # Séptimo sector
        ]
        
        # Seleccionar dos sectores para estar en superposición inicial
        self.current_sectors = random.sample(self.superposition_sectors, 2)
    
    def update_quantum_states(self, winning_number: int):
        """Actualizar los estados cuánticos basados en el número ganador."""
        # Aplicar el principio de observación cuántica
        # Cuando medimos un número, afectamos su probabilidad y la de sus vecinos
        
        # Factor de normalización
        normalization = 0.0
        
        for i in range(37):
            # La observación afecta a todos los números, pero más a los cercanos
            if i == winning_number:
                # El número observado gana probabilidad
                self.quantum_states[i] *= (1 + self.collapse_threshold)
            else:
                # Otros números se ven afectados por la interferencia con el número ganador
                interference = self.interference_matrix[winning_number][i]
                # Aplicar interferencia constructiva o destructiva
                if interference > 0.5:  # Interferencia constructiva
                    self.quantum_states[i] *= (1 + interference * self.uncertainty_factor)
                else:  # Interferencia destructiva
                    self.quantum_states[i] *= (1 - (1-interference) * self.uncertainty_factor)
            
            normalization += self.quantum_states[i]
        
        # Normalizar para mantener la suma de probabilidades = 1
        for i in range(37):
            self.quantum_states[i] /= normalization
        
        # Reducir coherencia con cada observación
        self.coherence *= 0.95
        if self.coherence < 0.2:
            # Restablecer coherencia y cambiar fase
            self.wavefunction_collapse = True
            self.coherence = 1.0
    
    def identify_entangled_pairs(self):
        """Identificar pares de números entrelazados basados en historias correlacionadas."""
        if len(self.winning_history) < 10:
            return
        
        # Buscar correlaciones en el historial
        pairs = []
        for i in range(37):
            for j in range(i+1, 37):
                # Contar cuántas veces i está seguido por j o viceversa
                correlation = 0
                for k in range(1, len(self.winning_history)):
                    if (self.winning_history[k-1] == i and self.winning_history[k] == j) or \
                       (self.winning_history[k-1] == j and self.winning_history[k] == i):
                        correlation += 1
                
                # Si la correlación es significativa
                if correlation >= 2:  # Al menos 2 ocurrencias
                    pairs.append((i, j, correlation))
        
        # Ordenar por correlación y tomar los 3 pares más correlacionados
        pairs.sort(key=lambda x: x[2], reverse=True)
        self.entangled_pairs = pairs[:3]
    
    def update_cycle_phase(self):
        """Actualizar la fase del ciclo cuántico."""
        self.cycle_count += 1
        if self.cycle_count >= self.phase_duration:
            self.cycle_count = 0
            # Rotar fases: superposición -> entrelazamiento -> colapso
            if self.cycle_phase == 'superposition':
                self.cycle_phase = 'entanglement'
                # Identificar pares entrelazados
                self.identify_entangled_pairs()
            elif self.cycle_phase == 'entanglement':
                self.cycle_phase = 'collapse'
                # Prepararse para el colapso
                self.wavefunction_collapse = True
            else:  # collapse
                self.cycle_phase = 'superposition'
                # Resetear y seleccionar nuevos sectores
                self._initialize_superposition()
                self.wavefunction_collapse = False
    
    def get_most_probable_numbers(self, count: int = 6) -> List[Tuple[int, float]]:
        """Obtener los números más probables según los estados cuánticos."""
        numbers_with_probs = [(i, self.quantum_states[i]) for i in range(37)]
        numbers_with_probs.sort(key=lambda x: x[1], reverse=True)
        return numbers_with_probs[:count]
    
    def get_entangled_numbers(self) -> List[int]:
        """Obtener números de pares entrelazados."""
        if not self.entangled_pairs:
            return []
        
        numbers = []
        for i, j, _ in self.entangled_pairs:
            if i not in numbers:
                numbers.append(i)
            if j not in numbers:
                numbers.append(j)
        
        return numbers[:8]  # Limitar a 8 números

    def calculate_bet(self) -> Dict[str, float]:
        """Calcular apuestas usando la estrategia de observador cuántico."""
        # Durante la fase de observación, no apostamos o hacemos apuestas mínimas
        if self.observation_phase:
            if self.observation_count < self.min_observations:
                # Apuesta mínima en un solo número para seguir recolectando datos
                random_number = random.randint(0, 36)
                return {str(random_number): self.min_bet}
            else:
                # Terminar fase de observación
                self.observation_phase = False
        
        # Números a apostar según la fase actual
        bet_numbers = []
        
        if self.cycle_phase == 'superposition':
            # Apostar a números en superposición (combinación de sectores actuales)
            for sector in self.current_sectors:
                bet_numbers.extend(sector)
            # Eliminar duplicados
            bet_numbers = list(set(bet_numbers))
            
        elif self.cycle_phase == 'entanglement':
            # Apostar a números entrelazados
            bet_numbers = self.get_entangled_numbers()
            if not bet_numbers:  # Si no hay suficientes pares entrelazados
                # Usar los más probables
                most_probable = self.get_most_probable_numbers(6)
                bet_numbers = [num for num, _ in most_probable]
                
        else:  # Fase de colapso
            # Apostar fuertemente a los números más probables
            most_probable = self.get_most_probable_numbers(4)
            bet_numbers = [num for num, _ in most_probable]
        
        # Si no tenemos suficientes números, añadir algunos al azar
        while len(bet_numbers) < 4:
            num = random.randint(0, 36)
            if num not in bet_numbers:
                bet_numbers.append(num)
        
        # Calcular apuesta total
        if self.wavefunction_collapse:
            # Durante el colapso, aplicamos apuesta mayor
            total_bet = self.current_bankroll * self.max_bet_percentage
        else:
            # Apuesta estándar
            total_bet = self.base_bet * (1 + self.coherence)
        
        # Limitar la apuesta total
        total_bet = min(total_bet, self.current_bankroll)
        
        # Distribuir la apuesta
        bet_per_number = total_bet / len(bet_numbers)
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_per_number = min(bet_per_number, self.current_bankroll / len(bet_numbers))
        
        return {str(num): bet_per_number for num in bet_numbers}

    def update_bankroll(self, winnings: float):
        """Actualizar bankroll y estado de la estrategia."""
        self.current_bankroll += winnings
        
        # Si estamos en fase de observación
        if self.observation_phase:
            self.observation_count += 1
        
        # Actualizar fase del ciclo
        self.update_cycle_phase()
        
        # Si la función de onda colapsó, resetear
        if self.wavefunction_collapse:
            # Resetear algunos parámetros después del colapso
            self.wavefunction_collapse = False
            # Redistribuir probabilidades
            normalization = 0.0
            for i in range(37):
                self.quantum_states[i] = random.uniform(0.8, 1.2) * (1/37)
                normalization += self.quantum_states[i]
            
            # Normalizar
            for i in range(37):
                self.quantum_states[i] /= normalization
    
    def record_winning_number(self, number: int):
        """Registrar un número ganador para análisis futuro."""
        self.winning_history.append(number)
        # Mantener solo los últimos 50 números para análisis
        if len(self.winning_history) > 50:
            self.winning_history.pop(0)
        
        # Actualizar estados cuánticos basados en esta observación
        self.update_quantum_states(number)

    def reset(self):
        """Resetear la estrategia a su estado inicial."""
        super().reset()
        self.quantum_states = {i: 1/37 for i in range(37)}
        self.observation_phase = True
        self.observation_count = 0
        self.winning_history = []
        self.cycle_phase = 'superposition'
        self.cycle_count = 0
        self.wavefunction_collapse = False
        self.coherence = 1.0
        self.entangled_pairs = []
        self._initialize_superposition() 