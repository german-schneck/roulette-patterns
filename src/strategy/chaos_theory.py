from typing import Dict, List, Tuple
from .base_strategy import BaseStrategy
import random
import math

class ChaosTheoryStrategy(BaseStrategy):
    """
    Estrategia basada en la teoría del caos:
    - Efecto mariposa (sensibilidad a condiciones iniciales)
    - Atractores extraños
    - Bifurcaciones y patrones emergentes
    - Fractales y auto-similitud en secuencias
    """
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        
        # Parámetros del sistema caótico (ecuación logística)
        self.r_value = 3.7  # Valor de bifurcación (3.57-4.0 para comportamiento caótico)
        self.x_current = random.random()  # Valor inicial aleatorio entre 0 y 1
        
        # Mapa de Lorenz (atractor extraño)
        self.sigma = 10.0
        self.rho = 28.0
        self.beta = 8.0/3.0
        self.lorenz_state = [random.uniform(-10, 10) for _ in range(3)]  # [x, y, z]
        self.dt = 0.01  # Delta t para la integración
        
        # Historial de números y resultados para análisis
        self.number_history = []
        self.result_history = []  # 1 para victoria, 0 para derrota
        self.lyapunov_exponent = 0.1  # Exponente de Lyapunov inicial
        
        # Atractores (patrones que atraen la dinámica del sistema)
        self.attractors = self._initialize_attractors()
        self.current_attractor = random.choice(list(self.attractors.keys()))
        
        # Estado de la estrategia
        self.iteration_count = 0
        self.phase = 'exploration'  # 'exploration', 'exploitation', 'transition'
        self.transition_threshold = 20  # Cambiar de fase cada N iteraciones
        self.sensitivity = 0.05  # Sensibilidad a perturbaciones
        
        # Gestión adaptativa de bankroll
        self.fractal_dimension = 1.5  # Dimensión fractal para escalado de apuestas
        self.max_bet_fraction = 0.08  # Máximo 8% del bankroll en una tirada
        
    def _initialize_attractors(self) -> Dict[str, List[int]]:
        """Inicializar atractores basados en la disposición de la ruleta."""
        # Los atractores son configuraciones estables hacia las que tiende el sistema
        return {
            'zero_neighbor': [0, 26, 3, 35],  # Vecinos de 0
            'fibonacci': [1, 2, 3, 5, 8, 13, 21, 34],  # Números Fibonacci
            'prime': [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31],  # Números primos
            'triangular': [1, 3, 6, 10, 15, 21, 28, 36],  # Números triangulares
            'power_two': [1, 2, 4, 8, 16, 32],  # Potencias de 2 o vecinos
            'golden_ratio': [1, 2, 3, 5, 8, 13, 21, 34]  # Secuencia relacionada con proporción áurea
        }
    
    def iterate_logistic_map(self, iterations: int = 1) -> float:
        """Iterar el mapa logístico (ecuación caótica simple)."""
        x = self.x_current
        for _ in range(iterations):
            x = self.r_value * x * (1 - x)
        self.x_current = x
        return x
    
    def lorenz_step(self) -> Tuple[float, float, float]:
        """Calcular un paso en el sistema de Lorenz."""
        x, y, z = self.lorenz_state
        
        # Sistema de ecuaciones de Lorenz
        dx = self.sigma * (y - x)
        dy = x * (self.rho - z) - y
        dz = x * y - self.beta * z
        
        # Integración numérica usando método de Euler
        x += dx * self.dt
        y += dy * self.dt
        z += dz * self.dt
        
        self.lorenz_state = [x, y, z]
        return x, y, z
    
    def calculate_lyapunov_exponent(self):
        """Calcular una aproximación al exponente de Lyapunov."""
        if len(self.result_history) < 10:
            return
        
        # Calcular distancias entre resultados consecutivos
        distances = []
        for i in range(1, len(self.result_history)):
            dist = abs(self.result_history[i] - self.result_history[i-1])
            distances.append(dist)
        
        # Aproximación del exponente (simplificado)
        if sum(distances) > 0:
            self.lyapunov_exponent = sum(distances) / len(distances)
        
        # Ajustar sensibilidad basada en el exponente
        self.sensitivity = min(0.2, max(0.01, self.lyapunov_exponent))
    
    def get_next_numbers(self, count: int = 6) -> List[int]:
        """Obtener próximos números basados en el estado actual del sistema."""
        # Usar el sistema de Lorenz para generar números (caóticos pero deterministas)
        lorenz_numbers = []
        for _ in range(count):
            x, _, _ = self.lorenz_step()
            # Mapear el valor x a un número de ruleta (0-36)
            num = int(abs(x) % 37)
            lorenz_numbers.append(num)
        
        # Combinar con atractores actuales para dar estabilidad
        attractor_numbers = self.attractors[self.current_attractor]
        
        # Mezclar ambos conjuntos con probabilidad basada en fase
        if self.phase == 'exploration':
            # Más peso a números caóticos en exploración
            combined = lorenz_numbers + random.sample(attractor_numbers, min(2, len(attractor_numbers)))
        elif self.phase == 'exploitation':
            # Más peso a atractores en explotación
            combined = attractor_numbers + random.sample(lorenz_numbers, min(2, len(lorenz_numbers)))
        else:  # Transition
            # Mezcla equilibrada
            combined = random.sample(lorenz_numbers, count//2) + random.sample(attractor_numbers, count//2)
        
        # Eliminar duplicados
        result = list(set(combined))
        # Limitar a count números
        return result[:count]
    
    def detect_patterns(self) -> bool:
        """Detectar patrones emergentes en el historial de números."""
        if len(self.number_history) < 10:
            return False
        
        # Analizar últimos números para detectar patrones
        recent_numbers = self.number_history[-10:]
        
        # Buscar secuencias que se repiten (patrón)
        for attractor_name, attractor_numbers in self.attractors.items():
            matches = sum(1 for num in recent_numbers if num in attractor_numbers)
            # Si más de 40% de números coinciden con un atractor
            if matches >= 4:  # 40% de 10
                self.current_attractor = attractor_name
                return True
        
        return False
    
    def update_phase(self):
        """Actualizar la fase de la estrategia."""
        self.iteration_count += 1
        
        # Comprobar si detectamos patrones claros
        pattern_detected = self.detect_patterns()
        
        # Actualizar fase basada en iteraciones y patrones
        if self.iteration_count % self.transition_threshold == 0:
            if self.phase == 'exploration':
                self.phase = 'exploitation' if pattern_detected else 'transition'
            elif self.phase == 'exploitation':
                # Si seguimos detectando patrones, mantener explotación
                if not pattern_detected:
                    self.phase = 'transition'
            else:  # transition
                self.phase = 'exploration'
            
            # Ajustar r_value para cambiar el comportamiento caótico
            # Valores cercanos a 4.0 son más caóticos
            if self.phase == 'exploration':
                self.r_value = min(3.99, 3.7 + random.random() * 0.29)
            elif self.phase == 'exploitation':
                self.r_value = 3.5 + random.random() * 0.2  # Menos caótico
            else:
                self.r_value = 3.7  # Valor intermedio
    
    def calculate_fractal_bet(self) -> float:
        """Calcular apuesta usando principios fractales."""
        # Usar el valor actual del mapa logístico para escalar la apuesta
        x = self.iterate_logistic_map(3)  # Iterar varias veces
        
        # Escalar apuesta basada en dimensión fractal y estado del sistema
        scale_factor = math.pow(x, 1/self.fractal_dimension)
        
        # Ajustar por fase y lyapunov
        if self.phase == 'exploitation':
            # Apuestas más grandes cuando encontramos patrones
            base_multiplier = 1.5 + self.lyapunov_exponent
        elif self.phase == 'exploration':
            # Apuestas más pequeñas durante exploración
            base_multiplier = 1.0
        else:  # transition
            base_multiplier = 1.2
        
        bet = self.base_bet * base_multiplier * (1 + scale_factor)
        
        # Limitar a un porcentaje máximo del bankroll
        max_bet = self.current_bankroll * self.max_bet_fraction
        return min(bet, max_bet)

    def calculate_bet(self) -> Dict[str, float]:
        """Calcular apuestas usando la estrategia de teoría del caos."""
        # Actualizar el exponente de Lyapunov y la fase
        self.calculate_lyapunov_exponent()
        self.update_phase()
        
        # Obtener números para apostar según el estado caótico actual
        if self.phase == 'exploitation':
            # En fase de explotación, apostar a menos números con más confianza
            bet_count = 4
        elif self.phase == 'exploration':
            # En exploración, apostar a más números
            bet_count = 8
        else:  # transition
            bet_count = 6
            
        bet_numbers = self.get_next_numbers(bet_count)
        
        # Calcular apuesta total
        total_bet = self.calculate_fractal_bet()
        
        # Distribuir entre los números seleccionados
        bet_per_number = total_bet / len(bet_numbers)
        
        # Asegurar que no apostamos más que nuestro bankroll
        bet_per_number = min(bet_per_number, self.current_bankroll / len(bet_numbers))
        
        return {str(num): bet_per_number for num in bet_numbers}

    def update_bankroll(self, winnings: float):
        """Actualizar bankroll y estado de la estrategia."""
        self.current_bankroll += winnings
        
        # Registrar resultado (victoria/derrota)
        self.result_history.append(1 if winnings > 0 else 0)
        if len(self.result_history) > 30:
            self.result_history.pop(0)
        
        # Si ganamos, puede ser señal de que estamos en un patrón
        if winnings > 0:
            # Reducir ligeramente el valor r para estabilizar
            self.r_value = max(3.6, self.r_value - 0.05)
            
            # Si estamos en fase de transición, considerar cambiar a explotación
            if self.phase == 'transition' and random.random() < 0.7:
                self.phase = 'exploitation'
                
            # Perturbación mínima al sistema (estabilidad)
            self.x_current += random.uniform(-0.01, 0.01)
            self.x_current = max(0.01, min(0.99, self.x_current))  # Mantener en rango válido
        else:
            # Si perdemos, puede ser señal de que necesitamos más caos
            # Incrementar valor r para más caos
            self.r_value = min(3.99, self.r_value + 0.03)
            
            # Perturbar el sistema más significativamente
            self.x_current += random.uniform(-0.1, 0.1) * self.sensitivity
            self.x_current = max(0.01, min(0.99, self.x_current))
            
            # Considerar cambiar de atractor
            if random.random() < 0.3:
                new_attractor = random.choice(list(self.attractors.keys()))
                if new_attractor != self.current_attractor:
                    self.current_attractor = new_attractor
        
        # Normalizar los estados del sistema
        # Lorenz puede volverse inestable, reiniciar si valores son extremos
        if any(abs(x) > 50 for x in self.lorenz_state):
            self.lorenz_state = [random.uniform(-10, 10) for _ in range(3)]
    
    def record_number(self, number: int):
        """Registrar un número para análisis posterior."""
        self.number_history.append(number)
        if len(self.number_history) > 50:
            self.number_history.pop(0)

    def reset(self):
        """Resetear la estrategia a su estado inicial."""
        super().reset()
        self.x_current = random.random()
        self.lorenz_state = [random.uniform(-10, 10) for _ in range(3)]
        self.r_value = 3.7
        self.number_history = []
        self.result_history = []
        self.iteration_count = 0
        self.phase = 'exploration'
        self.current_attractor = random.choice(list(self.attractors.keys()))
        self.lyapunov_exponent = 0.1 