from typing import Dict
from .base_strategy import BaseStrategy

class AndinaStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float = 1000.0, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.losses_counter = 0
        
        # Sectores andinos basados en "altitudes" numéricas
        self.alto_sector = [29, 7, 28, 12, 35, 3, 26]  # Sector alto (montañas)
        self.medio_sector = [0, 32, 15, 19, 4, 21, 2]  # Sector medio (valles)
        self.bajo_sector = [25, 17, 34, 6, 27, 13, 36]  # Sector bajo (costas)
        
        # Estados cíclicos
        self.sectors = [self.alto_sector, self.medio_sector, self.bajo_sector]
        self.current_sector_index = 0
        self.consecutive_wins = 0
        self.sector_switch_threshold = 3  # Cambiar sector después de 3 pérdidas consecutivas
        
    def get_current_sector(self):
        """Get the current betting sector."""
        return self.sectors[self.current_sector_index]

    def calculate_bet(self) -> Dict[str, float]:
        """Calculate the next bet based on the Andina strategy."""
        # Obtener sector actual
        current_sector = self.get_current_sector()
        
        # Calcular cantidad de apuesta por número
        bet_per_number = min(
            self.base_bet * (1.0 + (self.losses_counter * 0.2)), 
            self.current_bankroll / len(current_sector)
        )
        
        # Asegurar que no apostamos más que nuestro bankroll
        if bet_per_number * len(current_sector) > self.current_bankroll:
            bet_per_number = self.current_bankroll / len(current_sector)
        
        # Crear apuestas para todos los números del sector actual
        bets = {str(num): bet_per_number for num in current_sector}
        
        return bets
        
    def update_bankroll(self, winnings: float):
        """Update the bankroll and strategy state based on winnings."""
        self.current_bankroll += winnings
        
        if winnings > 0:
            # Si ganamos, reducimos la apuesta base y contamos victoria
            self.base_bet = max(self.min_bet, self.base_bet * 0.8)
            self.consecutive_wins += 1
            self.losses_counter = 0
            
            # Si tenemos varias victorias consecutivas, avanzamos al siguiente sector
            if self.consecutive_wins >= 2:
                self.consecutive_wins = 0
                self.current_sector_index = (self.current_sector_index + 1) % len(self.sectors)
        else:
            # Si perdemos, aumentamos la apuesta base
            self.base_bet = min(self.base_bet * 1.3, self.current_bankroll * 0.15)
            self.consecutive_wins = 0
            self.losses_counter += 1
            
            # Si tenemos muchas pérdidas consecutivas, cambiamos de sector
            if self.losses_counter >= self.sector_switch_threshold:
                self.losses_counter = 0
                self.current_sector_index = (self.current_sector_index + 2) % len(self.sectors)

    def reset(self):
        """Reset the strategy state."""
        super().reset()
        self.current_sector_index = 0
        self.consecutive_wins = 0
        self.losses_counter = 0
        self.base_bet = self.min_bet 