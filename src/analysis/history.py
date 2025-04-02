import json
import os
from datetime import datetime
from typing import Dict, List, Tuple

class History:
    def __init__(self, history_file: str = "output/history.json"):
        self.history_file = history_file
        self.history = self._load_history()

    def _load_history(self) -> Dict:
        """Load history from JSON file or create new if doesn't exist."""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r') as f:
                return json.load(f)
        return {}

    def save_history(self) -> None:
        """Save history to JSON file."""
        os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
        with open(self.history_file, 'w') as f:
            json.dump(self.history, f, indent=4)

    def get_strategy_history(self, strategy_name: str) -> Dict:
        """Get history for a specific strategy."""
        return self.history.get(strategy_name, {})

    def update_strategy_history(self, strategy_name: str, win_rate: float, 
                              best_numbers: List[int], wins_count: int) -> Tuple[bool, float]:
        """Update strategy history and return if it improved and by how much."""
        current_time = datetime.now().isoformat()
        strategy_history = self.get_strategy_history(strategy_name)
        
        # Get previous best win rate
        previous_best = strategy_history.get('best_win_rate', 0.0)
        
        # Check if current performance is better
        improved = win_rate > previous_best
        improvement = win_rate - previous_best if improved else 0.0
        
        # Update history
        self.history[strategy_name] = {
            'best_win_rate': win_rate,
            'best_numbers': best_numbers,
            'wins_count': wins_count,
            'last_update': current_time,
            'previous_best': previous_best
        }
        
        # Save to file
        self.save_history()
        
        return improved, improvement 