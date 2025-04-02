#!/usr/bin/env python3
"""
Kelly criterion optimizer for roulette betting strategies.
"""

class KellyOptimizer:
    """
    Kelly Criterion optimizer for betting size based on edge and variance.
    Uses advanced mathematics to determine optimal bet size for maximum growth.
    """
    def __init__(self, bankroll, edge=0.0, variance=1.0, risk_factor=0.5):
        self.bankroll = bankroll
        self.edge = edge  # Expected edge (positive for player advantage)
        self.variance = variance  # Variance of outcomes
        self.risk_factor = risk_factor  # Conservative adjustment (0-1)
        
    def calculate_optimal_bet(self):
        """
        Calculate the optimal bet size using the full Kelly formula:
        f* = p - q/b where:
        - p is probability of winning
        - q is probability of losing (1-p)
        - b is the odds received on the wager (payout ratio)
        
        For games like roulette with different odds:
        f* = sum(p_i * (b_i + 1) - 1) / b_i
        
        Adjusted by risk factor to be more conservative.
        """
        # For a simple bet with fixed odds (like color bet)
        if self.edge <= 0:
            # No edge or negative edge, bet minimum
            return 0.01 * self.bankroll
            
        # For a positive edge (usually doesn't exist in roulette unless biased)
        simple_kelly = self.edge / self.variance
        
        # Apply risk factor (conservative Kelly - avoid overbetting)
        conservative_kelly = simple_kelly * self.risk_factor
        
        # Limit to reasonable values (0.5%-5% of bankroll)
        return max(0.005 * self.bankroll, 
                  min(0.05 * self.bankroll, 
                      conservative_kelly * self.bankroll))
    
    def calculate_fractional_kelly(self, win_prob, loss_prob, payout):
        """
        More detailed Kelly calculation for specific bet types
        with corresponding payout structures.
        """
        if win_prob <= 0:
            return 0
            
        # Calculate Kelly fraction
        b = payout - 1  # convert from total payout to profit odds
        q = loss_prob
        p = win_prob
        
        # Regular Kelly: f* = (bp - q) / b
        f_star = (b*p - q) / b if b > 0 else 0
        
        # Apply risk factor and constraints
        conservative_f = f_star * self.risk_factor
        
        # Cap at reasonable levels
        return max(0.01, min(0.1, conservative_f)) 