from typing import Dict, List
import random
from .base_strategy import BaseStrategy

class PatternStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.current_bet = min_bet
        self.recent_numbers: List[int] = []
        self.max_history = 10  # Mantener historial de últimos 10 números
        self.consecutive_losses = 0
        self.last_bet_type = None
        self.pattern_weights = {
            'color': 0.4,
            'parity': 0.3,
            'dozen': 0.2,
            'column': 0.1
        }

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet using pattern analysis."""
        if len(self.recent_numbers) < 3:
            # Si no hay suficientes números para analizar, usar apuesta base
            self.current_bet = self.base_bet
            return self._place_basic_bet()

        # Analizar patrones
        patterns = self._analyze_patterns()
        
        # Calcular apuesta basada en pérdidas consecutivas
        if self.consecutive_losses > 0:
            self.current_bet = self.base_bet * (1.5 ** self.consecutive_losses)
        else:
            self.current_bet = self.base_bet

        # Asegurar que no apostamos más que nuestro bankroll
        if self.current_bet > self.current_bankroll:
            self.current_bet = self.current_bankroll

        # Determinar tipo de apuesta basado en patrones
        bet_type = self._determine_bet_type(patterns)
        self.last_bet_type = bet_type

        # Colocar apuesta según el tipo determinado
        return self._place_bet_by_type(bet_type)

    def _analyze_patterns(self) -> Dict:
        """Analizar patrones en los números recientes."""
        patterns = {
            'color': {'red': 0, 'black': 0},
            'parity': {'even': 0, 'odd': 0},
            'dozen': {'first': 0, 'second': 0, 'third': 0},
            'column': {'first': 0, 'second': 0, 'third': 0}
        }

        for num in self.recent_numbers[-5:]:  # Analizar últimos 5 números
            # Color
            if num in [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]:
                patterns['color']['red'] += 1
            elif num in [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]:
                patterns['color']['black'] += 1

            # Paridad
            if num % 2 == 0:
                patterns['parity']['even'] += 1
            else:
                patterns['parity']['odd'] += 1

            # Docena
            if 1 <= num <= 12:
                patterns['dozen']['first'] += 1
            elif 13 <= num <= 24:
                patterns['dozen']['second'] += 1
            else:
                patterns['dozen']['third'] += 1

            # Columna
            if num % 3 == 1:
                patterns['column']['first'] += 1
            elif num % 3 == 2:
                patterns['column']['second'] += 1
            else:
                patterns['column']['third'] += 1

        return patterns

    def _determine_bet_type(self, patterns: Dict) -> str:
        """Determinar el tipo de apuesta basado en patrones."""
        # Calcular tendencias
        color_trend = patterns['color']['red'] - patterns['color']['black']
        parity_trend = patterns['parity']['even'] - patterns['parity']['odd']
        dozen_trend = max(patterns['dozen'].items(), key=lambda x: x[1])[0]
        column_trend = max(patterns['column'].items(), key=lambda x: x[1])[0]

        # Si hay una tendencia clara en color, usar color
        if abs(color_trend) >= 3:
            return 'color'
        
        # Si hay una tendencia clara en paridad, usar paridad
        if abs(parity_trend) >= 3:
            return 'parity'
        
        # Si hay una tendencia en docena, usar docena
        if patterns['dozen'][dozen_trend] >= 3:
            return 'dozen'
        
        # Si hay una tendencia en columna, usar columna
        if patterns['column'][column_trend] >= 3:
            return 'column'
        
        # Si no hay tendencia clara, usar apuesta básica
        return 'basic'

    def _place_bet_by_type(self, bet_type: str) -> Dict[str, float]:
        """Colocar apuesta según el tipo determinado."""
        if bet_type == 'color':
            return {'red': self.current_bet} if random.random() < 0.5 else {'black': self.current_bet}
        elif bet_type == 'parity':
            return {'even': self.current_bet} if random.random() < 0.5 else {'odd': self.current_bet}
        elif bet_type == 'dozen':
            return {'first_dozen': self.current_bet}
        elif bet_type == 'column':
            return {'first_column': self.current_bet}
        else:
            return self._place_basic_bet()

    def _place_basic_bet(self) -> Dict[str, float]:
        """Colocar una apuesta básica."""
        return {'red': self.current_bet}

    def update_bankroll(self, winnings: float) -> None:
        """Update the bankroll and strategy state."""
        super().update_bankroll(winnings)
        
        # Actualizar contador de pérdidas consecutivas
        if winnings < 0:
            self.consecutive_losses += 1
        else:
            self.consecutive_losses = 0

    def record_spin(self, number: int, winnings: float) -> None:
        """Record a spin result and update recent numbers history."""
        super().record_spin(number, winnings)
        
        # Actualizar historial de números recientes
        self.recent_numbers.append(number)
        if len(self.recent_numbers) > self.max_history:
            self.recent_numbers.pop(0)

    def reset(self) -> None:
        """Reset the strategy to its initial state."""
        super().reset()
        self.recent_numbers = []
        self.consecutive_losses = 0
        self.last_bet_type = None 