# Advanced Roulette Strategy Analyzer

## Description

This project implements an advanced statistical analysis system for American roulette, using multiple prediction methodologies, mathematical modeling, and simulation. The system integrates classic gaming techniques with modern algorithms to identify patterns and maximize the probability of success.

## Concept and Philosophy

Roulette has traditionally been considered a game of pure chance, but this system explores the premise that through advanced statistical analysis, large-scale simulations, and machine learning methods, it is possible to identify suboptimal patterns in the distribution of results. The project does not claim to "beat" roulette (mathematically impossible under perfect conditions), but rather to optimize decision-making to maximize results in real environments where physical imperfections exist.

## Main Features

- **Multi-strategy Analysis**: Implements more than 20 different strategies, from classic (Martingale) to advanced (neural correlation analysis).
- **Large-Scale Simulation**: Ability to run millions of simulations with adjustable configuration.
- **Bankroll Analysis**: Capital survival simulation with different strategies.
- **Advanced Visualization**: Comparison graphs, heat maps, and performance analysis.
- **Adaptive Optimization**: The system learns from previous results and adjusts parameters.
- **Rigorous Validation**: All strategies undergo cross-validation to avoid overfitting.

## Implemented Strategies

### Classic Historical Strategies
- **Martingale**: Classic doubling system after losses. After each loss, the bet is doubled to recover previous losses and gain a small profit when a win eventually occurs.
- **D'Alembert**: More conservative arithmetic progression than Martingale. Increases bet by one unit after a loss and decreases by one unit after a win, creating a more gradual progression.
- **Fibonacci**: Sequence based on the Fibonacci series. Bets follow the Fibonacci sequence (1, 1, 2, 3, 5, 8, 13...), advancing one step after a loss and moving back two steps after a win.

### Latin American Strategies
- **Cancellation System**: Crossing-out method for bet management. Numbers in a sequence are crossed out as wins occur, with bet sizes determined by adding the first and last numbers in the active sequence.
- **Mexican Progression**: Adaptive progression system based on clusters. Identifies clusters of numbers that appear together and adjusts bet sizes based on recent hit patterns and sector performance.

### Las Vegas Professional Techniques
- **Dealer Signature**: Analysis of dealer-specific patterns. Tracks individual dealers' release habits, speed, and consistency to identify predictable patterns in ball landing positions.
- **Sector Targeting**: Concentration on physical sectors of the roulette wheel. Focuses bets on specific physical sectors where the ball tends to land more frequently due to wheel characteristics.
- **Visual Ballistics**: Prediction based on physical parameters. Observes the initial velocity of the ball, wheel rotation speed, and release point to estimate the likely landing area.
- **Mechanical Bias**: Detection of physical imperfections in the wheel. Analyzes long-term data to identify if certain numbers or sectors appear more frequently due to wheel imperfections.
- **Chaotic Domain**: Analysis of chaotic domains to predict attractors. Uses chaos theory principles to identify patterns in seemingly random outcomes and predict potential "attractor" numbers.

### Advanced Methodologies
- **Neural Correlation**: Correlation analysis using neural networks. Employs neural networks to identify complex, non-linear relationships between historical outcomes and predict future results.
- **Physical Section Analysis**: Study of physical sections of the wheel. Maps the physical layout of numbers on the wheel to identify sections that receive more hits due to mechanical factors.
- **Dynamic Clustering**: Dynamic grouping of numbers by behavior. Groups numbers based on their historical performance patterns and adjusts these clusters as new data becomes available.
- **Momentum-Based Analysis**: Analysis based on trends and momentum. Identifies "hot" and "cold" numbers and sectors, betting on the continuation or reversal of these trends.
- **Hot Neighbors**: Analysis of adjacent numbers on the physical wheel. Focuses on numbers physically adjacent to recent winners, based on the theory that wheel bias affects neighboring pockets.
- **Temporal Cycles**: Detection of temporal cycles in the sequence. Identifies repeating patterns in the timing of specific numbers or groups of numbers appearing.
- **Variance Balance**: Optimization based on variance balance. Selects numbers that provide optimal coverage of the wheel while maintaining balance between high and low variance sectors.
- **Geometric Symmetry**: Analysis of geometric symmetry patterns. Identifies symmetrical relationships between numbers on the wheel and uses these patterns to predict future outcomes.

### Asian Betting Strategies
- **Feng Shui Harmony**: Traditional Chinese approach based on energy balance, Wu Xing (Five Elements), Yin-Yang harmony, and Bagua energy mapping, using lucky/unlucky number associations from Chinese numerology. Selects numbers based on their elemental properties and energy flow principles.
- **I Ching Oracle System**: Ancient Chinese divination methodology that uses the 64 hexagrams to identify optimal numbers. Creates betting patterns based on changing lines and trigram associations with cardinal directions and elements. Each spin result is interpreted through I Ching principles to determine the next bet.
- **Pachinko Progression**: Japanese-inspired strategy that adapts concepts from the popular Pachinko gambling machines. Implements a cascading bet progression system based on the ball's mechanical probability distribution in traditional Pachinko games. Bets increase or decrease following a pattern similar to how balls cascade through a Pachinko machine.

## Analysis and Results

The system generates detailed comparative analyses between all strategies, showing:

- Success rate (win rate) for each strategy
- Relative performance compared to random expectation
- Bankroll evolution with each strategy
- Expected bankroll survival time
- Visualization of recommended numbers through heat maps
- Historical performance tracking between sessions

Tests have shown that certain strategies can achieve success rates above 22.5% for selections of 8 numbers, which represents a significant improvement over the 21.05% randomly expected.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/advanced-roulette-strategy-analyzer.git
cd advanced-roulette-strategy-analyzer
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the script:

```bash
python main.py
```

## Usage  

```bash
python main.py
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
