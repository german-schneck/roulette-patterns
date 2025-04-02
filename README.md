# Roulette Strategy Simulator

This project simulates American Roulette games with different betting strategies to analyze their performance and effectiveness.

## Features

- Simulates American Roulette games with realistic wheel properties
- Supports multiple betting strategies (currently includes Martingale)
- Analyzes performance metrics including:
  - Win rate
  - Profit/Loss
  - Bankroll evolution
  - Best betting patterns
- Generates visualizations of results
- Configurable simulation parameters

## Project Structure

```
src/
├── game/
│   ├── roulette.py      # Roulette wheel implementation
│   └── session.py       # Game session management
├── strategy/
│   ├── base_strategy.py # Base strategy class
│   └── martingale.py    # Martingale strategy implementation
├── analysis/
│   └── simulator.py     # Simulation and analysis tools
└── utils/              # Utility functions (to be added)
```

## Installation

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the simulator with default parameters:
```bash
python main.py
```

Or specify custom parameters:
```bash
python main.py --initial-bankroll 2000 --num-simulations 200 --min-bet 5 --output-plot my_results.png
```

### Command Line Arguments

- `--initial-bankroll`: Starting bankroll for each simulation (default: 1000.0)
- `--num-simulations`: Number of simulations to run (default: 100)
- `--min-bet`: Minimum bet amount (default: 1.0)
- `--output-plot`: Path to save the results plot (default: results.png)

## Adding New Strategies

To add a new betting strategy:

1. Create a new file in `src/strategy/` (e.g., `fibonacci.py`)
2. Inherit from `BaseStrategy` class
3. Implement the required methods:
   - `calculate_bet()`
   - `update_bankroll()`
   - `reset()`

Example:
```python
from .base_strategy import BaseStrategy

class FibonacciStrategy(BaseStrategy):
    def __init__(self, initial_bankroll: float, min_bet: float = 1.0):
        super().__init__(initial_bankroll, min_bet)
        self.base_bet = min_bet
        self.fibonacci_sequence = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55]
        self.current_index = 0

    def calculate_bet(self) -> Dict[str, float]:
        # Implement your strategy here
        pass
```

## Output

The simulator generates:
1. Console output with statistics about the simulations
2. A plot file showing:
   - Bankroll evolution of the best session
   - Win rate distribution
   - Profit/Loss distribution
   - Bankroll range statistics

## Contributing

Feel free to submit issues and enhancement requests! 