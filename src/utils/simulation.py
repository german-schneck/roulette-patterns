#!/usr/bin/env python3
"""
Roulette Simulator

This module provides simulation capabilities for roulette strategies.
"""

import random
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

class RouletteSimulator:
    """
    Simulator for roulette strategies and bankroll evolution.
    
    This class provides methods to simulate various betting strategies, 
    track bankroll changes, and analyze performance metrics.
    """
    
    def __init__(self, wheel_type="american"):
        """
        Initialize the simulator.
        
        Args:
            wheel_type (str): Type of roulette wheel ('american' or 'european')
        """
        # Set up wheel configuration
        if wheel_type == "american":
            self.wheel = list(range(1, 37)) + [0, 00]
            self.zero_count = 2
        elif wheel_type == "european":
            self.wheel = list(range(1, 37)) + [0]
            self.zero_count = 1
        else:
            raise ValueError(f"Unknown wheel type: {wheel_type}")
        
        # Basic wheel properties
        self.wheel_size = len(self.wheel)
        self.number_odds = self.wheel_size - 1  # Payout odds for single number bet
        
        # Default bet types and their payouts
        self.bet_types = {
            "straight": {"payout": 35, "coverage": 1},  # Single number
            "split": {"payout": 17, "coverage": 2},     # Two adjacent numbers
            "street": {"payout": 11, "coverage": 3},    # Three numbers in a row
            "corner": {"payout": 8, "coverage": 4},     # Four numbers in a square
            "five": {"payout": 6, "coverage": 5},       # 0, 00, 1, 2, 3 (American roulette)
            "six_line": {"payout": 5, "coverage": 6},   # Six numbers (two rows)
            "dozen": {"payout": 2, "coverage": 12},     # 12 numbers (1-12, 13-24, 25-36)
            "column": {"payout": 2, "coverage": 12},    # 12 numbers (vertical columns)
            "red_black": {"payout": 1, "coverage": 18}, # 18 numbers (red/black)
            "odd_even": {"payout": 1, "coverage": 18},  # 18 numbers (odd/even)
            "high_low": {"payout": 1, "coverage": 18}   # 18 numbers (1-18/19-36)
        }
    
    def simulate_spin(self):
        """
        Simulate a single roulette spin.
        
        Returns:
            int or str: The winning number (0, 00, or 1-36)
        """
        return random.choice(self.wheel)
    
    def check_win(self, bet_numbers, winning_number):
        """
        Check if a bet wins based on the winning number.
        
        Args:
            bet_numbers (list): Numbers covered by the bet
            winning_number: The number that came up in the spin
            
        Returns:
            bool: True if bet wins, False otherwise
        """
        return winning_number in bet_numbers
    
    def calculate_bet_return(self, bet_amount, bet_type, is_win):
        """
        Calculate the return from a bet.
        
        Args:
            bet_amount (float): Amount bet
            bet_type (str): Type of bet placed
            is_win (bool): Whether the bet won
            
        Returns:
            float: Net return (positive for wins, negative for losses)
        """
        if is_win:
            return bet_amount * self.bet_types[bet_type]["payout"]
        else:
            return -bet_amount
    
    def simulate_session(self, strategy, starting_bankroll=1000, bet_amount=10, max_spins=1000):
        """
        Simulate a complete betting session using the specified strategy.
        
        Args:
            strategy (callable): Function that returns bet numbers for each spin
            starting_bankroll (float): Initial bankroll
            bet_amount (float): Amount to bet on each spin
            max_spins (int): Maximum number of spins to simulate
            
        Returns:
            dict: Session results including bankroll history and statistics
        """
        bankroll = starting_bankroll
        bankroll_history = [bankroll]
        bet_history = []
        
        spin_count = 0
        win_count = 0
        
        while bankroll >= bet_amount and spin_count < max_spins:
            # Get bet numbers from strategy
            bet_numbers = strategy(spin_count, bet_history)
            
            # Simulate spin
            winning_number = self.simulate_spin()
            
            # Check if bet wins
            is_win = self.check_win(bet_numbers, winning_number)
            
            # Calculate bet coverage
            coverage = len(bet_numbers)
            
            # Find appropriate bet type based on coverage
            bet_type = None
            for btype, props in self.bet_types.items():
                if props["coverage"] == coverage:
                    bet_type = btype
                    break
            
            # If no matching bet type, use straight bet with proportional coverage
            if bet_type is None:
                # Custom bet with coverage not matching standard bet types
                # Use proportional payout based on coverage
                net_return = -bet_amount  # Default to loss
                if is_win:
                    payout = (self.wheel_size / coverage - 1)
                    net_return = bet_amount * payout
            else:
                # Standard bet type
                net_return = self.calculate_bet_return(bet_amount, bet_type, is_win)
            
            # Update bankroll
            bankroll += net_return
            
            # Update histories and counts
            bankroll_history.append(bankroll)
            bet_history.append({
                "spin": spin_count,
                "bet_numbers": bet_numbers.copy(),
                "winning_number": winning_number,
                "is_win": is_win,
                "net_return": net_return
            })
            
            spin_count += 1
            if is_win:
                win_count += 1
        
        # Calculate session statistics
        win_rate = win_count / spin_count if spin_count > 0 else 0
        profit = bankroll - starting_bankroll
        profit_percentage = (profit / starting_bankroll) * 100
        
        return {
            "bankroll_history": bankroll_history,
            "bet_history": bet_history,
            "final_bankroll": bankroll,
            "spins": spin_count,
            "wins": win_count,
            "win_rate": win_rate,
            "profit": profit,
            "profit_percentage": profit_percentage
        }
    
    def simulate_fixed_strategy(self, bet_numbers, starting_bankroll=1000, bet_amount=10, max_spins=1000):
        """
        Simulate a session with a fixed set of bet numbers.
        
        Args:
            bet_numbers (list): Fixed set of numbers to bet on each spin
            starting_bankroll (float): Initial bankroll
            bet_amount (float): Amount to bet on each spin
            max_spins (int): Maximum number of spins to simulate
            
        Returns:
            dict: Session results
        """
        # Create a strategy function that always returns the same numbers
        fixed_strategy = lambda spin, history: bet_numbers
        
        return self.simulate_session(fixed_strategy, starting_bankroll, bet_amount, max_spins)
    
    def simulate_martingale(self, bet_type="red_black", starting_bankroll=1000, base_bet=10, max_spins=1000, max_bet=None):
        """
        Simulate a Martingale betting strategy.
        
        Args:
            bet_type (str): Type of bet to place
            starting_bankroll (float): Initial bankroll
            base_bet (float): Initial bet amount
            max_spins (int): Maximum number of spins to simulate
            max_bet (float, optional): Maximum allowed bet
            
        Returns:
            dict: Session results
        """
        bankroll = starting_bankroll
        bankroll_history = [bankroll]
        
        spin_count = 0
        win_count = 0
        current_bet = base_bet
        consecutive_losses = 0
        
        while bankroll >= current_bet and spin_count < max_spins:
            # Get covered numbers based on bet type
            if bet_type == "red_black":
                # Red numbers
                bet_numbers = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
            elif bet_type == "odd_even":
                # Odd numbers
                bet_numbers = list(range(1, 37, 2))
            elif bet_type == "high_low":
                # Low numbers (1-18)
                bet_numbers = list(range(1, 19))
            else:
                raise ValueError(f"Unsupported bet type for Martingale: {bet_type}")
            
            # Simulate spin
            winning_number = self.simulate_spin()
            
            # Check if bet wins
            is_win = self.check_win(bet_numbers, winning_number)
            
            # Calculate net return
            if is_win:
                net_return = current_bet
                consecutive_losses = 0
                current_bet = base_bet
                win_count += 1
            else:
                net_return = -current_bet
                consecutive_losses += 1
                # Double bet for next spin (Martingale progression)
                current_bet *= 2
                # Cap bet if max_bet is specified
                if max_bet is not None and current_bet > max_bet:
                    current_bet = max_bet
            
            # Update bankroll
            bankroll += net_return
            
            # Update history
            bankroll_history.append(bankroll)
            
            spin_count += 1
        
        # Calculate session statistics
        win_rate = win_count / spin_count if spin_count > 0 else 0
        profit = bankroll - starting_bankroll
        profit_percentage = (profit / starting_bankroll) * 100
        
        return {
            "bankroll_history": bankroll_history,
            "final_bankroll": bankroll,
            "spins": spin_count,
            "wins": win_count,
            "win_rate": win_rate,
            "profit": profit,
            "profit_percentage": profit_percentage,
            "max_consecutive_losses": consecutive_losses
        }
    
    def simulate_returns(self, win_probability, trials=1000, bets_per_trial=100, starting_bankroll=100, bet_size_percent=0.01):
        """
        Simulate returns based on a given win probability.
        
        Args:
            win_probability (float): Probability of winning each bet
            trials (int): Number of trials to run
            bets_per_trial (int): Number of bets per trial
            starting_bankroll (float): Initial bankroll for each trial
            bet_size_percent (float): Bet size as percentage of current bankroll
            
        Returns:
            list: Bankroll history for each trial
        """
        # Payoff for a win assuming straight bet
        payout = (1 / win_probability) - 1
        
        all_trial_results = []
        
        for _ in range(trials):
            bankroll = starting_bankroll
            bankroll_history = [bankroll]
            
            for _ in range(bets_per_trial):
                # Calculate bet size (percentage of current bankroll)
                bet_amount = bankroll * bet_size_percent
                
                # Simulate bet outcome
                if random.random() < win_probability:
                    # Win
                    bankroll += bet_amount * payout
                else:
                    # Loss
                    bankroll -= bet_amount
                
                bankroll_history.append(bankroll)
                
                # Break if bankrupt
                if bankroll <= 0:
                    break
            
            all_trial_results.append(bankroll_history)
        
        return all_trial_results
    
    def calculate_survival_probability(self, win_probability, trials=1000, max_bets=500, starting_bankroll=100, bet_size=1):
        """
        Calculate probability of bankroll survival over time.
        
        Args:
            win_probability (float): Probability of winning each bet
            trials (int): Number of trials to run
            max_bets (int): Maximum number of bets per trial
            starting_bankroll (float): Initial bankroll for each trial
            bet_size (float): Fixed bet size
            
        Returns:
            dict: Survival probability at different points
        """
        survivors = [trials]  # Start with all trials surviving
        
        for bet_num in range(1, max_bets + 1):
            active_trials = 0
            
            for _ in range(trials):
                bankroll = starting_bankroll
                
                # Simulate bets up to current bet number
                for _ in range(bet_num):
                    if random.random() < win_probability:
                        # Win
                        bankroll += bet_size
                    else:
                        # Loss
                        bankroll -= bet_size
                    
                    # Check if bankrupt
                    if bankroll <= 0:
                        break
                
                # Count as survivor if not bankrupt
                if bankroll > 0:
                    active_trials += 1
            
            # Record number of survivors after this many bets
            survivors.append(active_trials)
        
        # Calculate survival probabilities
        bet_numbers = list(range(0, max_bets + 1))
        survival_probs = [s / trials for s in survivors]
        
        return {
            "bet_numbers": bet_numbers,
            "survival_probabilities": survival_probs
        }
    
    def compare_strategies(self, strategies, trials=100, starting_bankroll=1000, max_spins=500):
        """
        Compare multiple betting strategies.
        
        Args:
            strategies (dict): Dictionary mapping strategy names to strategy functions
            trials (int): Number of trials to run for each strategy
            starting_bankroll (float): Initial bankroll for each trial
            max_spins (int): Maximum number of spins per trial
            
        Returns:
            dict: Comparison results for each strategy
        """
        results = {}
        
        for name, strategy in strategies.items():
            strategy_results = []
            
            for _ in range(trials):
                trial_result = self.simulate_session(
                    strategy, 
                    starting_bankroll=starting_bankroll, 
                    max_spins=max_spins
                )
                strategy_results.append(trial_result)
            
            # Calculate aggregate statistics
            avg_profit = np.mean([r["profit"] for r in strategy_results])
            avg_win_rate = np.mean([r["win_rate"] for r in strategy_results])
            avg_spins = np.mean([r["spins"] for r in strategy_results])
            
            # Calculate bankroll trajectory (average across all trials)
            max_length = max([len(r["bankroll_history"]) for r in strategy_results])
            avg_bankroll = np.zeros(max_length)
            count_per_spin = np.zeros(max_length)
            
            for r in strategy_results:
                for i, bal in enumerate(r["bankroll_history"]):
                    avg_bankroll[i] += bal
                    count_per_spin[i] += 1
            
            # Avoid division by zero
            count_per_spin[count_per_spin == 0] = 1
            avg_bankroll = avg_bankroll / count_per_spin
            
            results[name] = {
                "avg_profit": avg_profit,
                "avg_win_rate": avg_win_rate,
                "avg_spins": avg_spins,
                "avg_bankroll": avg_bankroll.tolist()
            }
        
        return results 