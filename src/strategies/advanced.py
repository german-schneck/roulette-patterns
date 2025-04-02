#!/usr/bin/env python3
"""
Advanced betting strategy implementation for roulette.
"""
from ..optimizers.kelly import KellyOptimizer
from ..analyzers.bayesian import BayesianPredictor

class AdvancedBettingStrategy:
    """
    Implements advanced mathematical betting strategies
    based on statistical analysis and risk management.
    """
    def __init__(self, bankroll=100):
        self.bankroll = bankroll
        self.starting_bankroll = bankroll
        self.kelly = KellyOptimizer(bankroll)
        self.bayes = BayesianPredictor()
        
        # Risk management parameters
        self.max_drawdown = 0.25  # Maximum allowed drawdown
        self.target_profit = 0.5  # Target profit (50% of bankroll)
        
        # Track performance
        self.peak_bankroll = bankroll
        self.max_drawdown_seen = 0
        self.win_streak = 0
        self.loss_streak = 0
        
        # Strategy state
        self.strategy_type = 'flat'  # flat, progressive, or defensive
        self.bet_size = 1  # Default bet size
        
    def update_kelly_parameters(self, edge, variance, risk_factor=None):
        """Update Kelly optimizer parameters"""
        self.kelly.edge = edge
        self.kelly.variance = variance
        if risk_factor is not None:
            self.kelly.risk_factor = risk_factor
    
    def calculate_bet_size(self, win_prob, payout, strategy=None):
        """
        Calculate optimal bet size based on:
        - Current bankroll
        - Estimated edge
        - Current strategy phase
        - Risk management rules
        """
        # Update Kelly calculator with current bankroll
        self.kelly.bankroll = self.bankroll
        
        # Base calculation on win probability and payout
        loss_prob = 1 - win_prob
        
        # Adjust risk factor based on win/loss streaks
        risk_factor = 0.5  # default
        if self.win_streak > 3:
            risk_factor = 0.7  # More aggressive during win streaks
        elif self.loss_streak > 2:
            risk_factor = 0.3  # More conservative during loss streaks
            
        # Calculate using fractional Kelly
        kelly_fraction = self.kelly.calculate_fractional_kelly(
            win_prob, loss_prob, payout)
            
        # Apply strategy adjustments
        if strategy == 'progressive' and self.win_streak > 1:
            # Increase bet size during winning streaks
            kelly_fraction *= 1.2
        elif strategy == 'defensive' or self.bankroll < 0.8 * self.starting_bankroll:
            # Reduce bet size when losing or in defensive mode
            kelly_fraction *= 0.7
            
        # Calculate actual bet size
        bet_size = kelly_fraction * self.bankroll
        
        # Risk management limits
        min_bet = 1  # Minimum bet
        max_bet = 0.1 * self.bankroll  # Maximum 10% of bankroll
        
        # Ensure bet is within bounds
        return max(min_bet, min(max_bet, bet_size))
        
    def select_best_bet(self, analyzer, recent_results):
        """
        Select the most promising bet based on recent results
        and statistical analysis.
        """
        # Update Bayesian model with recent results
        for result in recent_results:
            color = analyzer.get_color(result)
            self.bayes.update(result, color)
            
        # Analyze sectors performance
        sector_analysis = analyzer.analyze_sectors()
        
        # Find sectors with significant deviation from expected values
        promising_sectors = []
        for sector_name, stats in sector_analysis.items():
            # Look for sectors performing significantly better than expected
            if stats['variance_percent'] > 15:  # 15% better than expected
                promising_sectors.append((sector_name, stats))
        
        if promising_sectors:
            # Sort by highest variance from expected
            promising_sectors.sort(key=lambda x: x[1]['variance_percent'], reverse=True)
            best_sector = promising_sectors[0]
            
            # Calculate win probability and payout
            sector_name = best_sector[0]
            stats = best_sector[1]
            win_prob = stats['actual_rate']
            
            # Calculate payout based on sector type
            if sector_name in ['red', 'black', 'even', 'odd', 'high', 'low']:
                payout = 2.0  # Even money bets
            elif sector_name in ['first_dozen', 'second_dozen', 'third_dozen',
                               'first_column', 'second_column', 'third_column']:
                payout = 3.0  # 2-to-1 bets
            else:
                # For custom sectors, approximate payout based on coverage
                coverage = len(analyzer.sectors[sector_name]) / len(analyzer.numbers)
                payout = 1 / coverage if coverage > 0 else 36
                
            # Calculate bet size
            bet_size = self.calculate_bet_size(win_prob, payout, self.strategy_type)
            
            return {
                'type': 'sector',
                'sector': sector_name,
                'numbers': analyzer.sectors[sector_name],
                'bet_size': bet_size,
                'win_prob': win_prob,
                'payout': payout,
                'expected_value': (win_prob * payout) - 1  # EV calculation
            }
            
        else:
            # Default to simple strategy if no promising sectors
            # Use Bayesian prediction for next color
            predicted_color = self.bayes.predict_next_color()
            
            if predicted_color in ['red', 'black']:
                win_prob = 18/38  # Standard probability for red/black bets
                payout = 2.0
                bet_size = self.calculate_bet_size(win_prob, payout, 'defensive')
                
                return {
                    'type': 'color',
                    'sector': predicted_color,
                    'numbers': analyzer.sectors[predicted_color],
                    'bet_size': bet_size,
                    'win_prob': win_prob,
                    'payout': payout,
                    'expected_value': (win_prob * payout) - 1
                }
            else:
                # If green predicted (very unlikely), bet on a split of 0 and 00
                win_prob = 2/38
                payout = 18.0
                bet_size = self.calculate_bet_size(win_prob, payout, 'aggressive')
                
                return {
                    'type': 'split',
                    'sector': 'green_split',
                    'numbers': ['0', '00'],
                    'bet_size': bet_size,
                    'win_prob': win_prob,
                    'payout': payout,
                    'expected_value': (win_prob * payout) - 1
                }
    
    def execute_strategy(self, analyzer, max_spins=1000):
        """
        Execute the complete betting strategy over multiple spins,
        applying advanced risk management and adaptation.
        
        Returns list of (bankroll, win/loss) tuples for each bet placed.
        """
        results = []
        spins_played = 0
        
        # Initial bankroll and record-keeping
        self.bankroll = self.starting_bankroll
        self.peak_bankroll = self.starting_bankroll
        self.max_drawdown_seen = 0
        self.win_streak = 0
        self.loss_streak = 0
        
        # Generate initial history if needed
        if len(analyzer.history) < 100:
            analyzer.spin_batch(100)
            
        # Start simulation
        while spins_played < max_spins:
            # Check stop conditions
            if self.bankroll <= 0:
                break  # Bankrupt
                
            if self.bankroll >= self.starting_bankroll * (1 + self.target_profit):
                break  # Reached profit target
                
            current_drawdown = 1 - (self.bankroll / self.peak_bankroll)
            if current_drawdown > self.max_drawdown:
                break  # Hit maximum drawdown limit
            
            # Select best bet based on recent history
            recent_results = analyzer.history[-20:] if len(analyzer.history) >= 20 else analyzer.history
            bet = self.select_best_bet(analyzer, recent_results)
            
            # Adjust bet size if near bankroll limits
            if self.bankroll < 0.2 * self.starting_bankroll:
                # Very defensive when low on funds
                bet['bet_size'] = min(bet['bet_size'], 0.05 * self.bankroll)
                self.strategy_type = 'defensive'
            elif self.bankroll > 1.5 * self.starting_bankroll:
                # More aggressive when doing well
                self.strategy_type = 'progressive'
            else:
                # Normal balanced approach
                self.strategy_type = 'flat'
                
            # Place bet and spin the wheel
            result, color = analyzer.spin()
            spins_played += 1
            
            # Check if bet won
            won = result in bet['numbers']
            
            # Update bankroll
            if won:
                # Win - add winnings
                winnings = bet['bet_size'] * (bet['payout'] - 1)
                self.bankroll += winnings
                self.win_streak += 1
                self.loss_streak = 0
            else:
                # Loss - deduct bet amount
                self.bankroll -= bet['bet_size']
                self.win_streak = 0
                self.loss_streak += 1
                
            # Update peak bankroll and drawdown stats
            if self.bankroll > self.peak_bankroll:
                self.peak_bankroll = self.bankroll
            
            current_drawdown = 1 - (self.bankroll / self.peak_bankroll)
            if current_drawdown > self.max_drawdown_seen:
                self.max_drawdown_seen = current_drawdown
                
            # Record result
            results.append((self.bankroll, won))
            
        return results 