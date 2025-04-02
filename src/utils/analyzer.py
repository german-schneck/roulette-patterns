#!/usr/bin/env python3
"""
Advanced Roulette Analyzer

Core class for analyzing roulette outcomes and generating statistics.
"""

import random
import numpy as np
from collections import defaultdict, Counter

class AdvancedRouletteAnalyzer:
    """
    Advanced analyzer for roulette outcomes.
    
    This class handles generating and analyzing roulette outcomes,
    providing statistics and patterns for strategy development.
    """
    
    def __init__(self, spins=1000, seed=None, history=None):
        """
        Initialize the analyzer with either a provided history or generate a random one.
        
        Args:
            spins (int): Number of spins to generate if no history is provided
            seed (int, optional): Random seed for reproducibility
            history (list, optional): Existing history of roulette outcomes
        """
        # American roulette wheel layout (0-36 plus 00)
        self.wheel_order = [
            '0', '28', '9', '26', '30', '11', '7', '20', '32', '17', '5', '22', '34', '15', 
            '3', '24', '36', '13', '1', '00', '27', '10', '25', '29', '12', '8', '19', '31', 
            '18', '6', '21', '33', '16', '4', '23', '35', '14', '2'
        ]
        
        # Number properties
        self.red_numbers = ['1', '3', '5', '7', '9', '12', '14', '16', '18', '19', '21', '23', '25', '27', '30', '32', '34', '36']
        self.black_numbers = ['2', '4', '6', '8', '10', '11', '13', '15', '17', '20', '22', '24', '26', '28', '29', '31', '33', '35']
        self.green_numbers = ['0', '00']
        
        # Initialize random generator with seed if provided
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        
        # Use provided history or generate random outcomes
        if history is not None:
            self.history = history
        else:
            self.generate_random_history(spins)
        
        # Initialize stats
        self.calculate_statistics()
    
    def generate_random_history(self, spins):
        """
        Generate a random history of roulette outcomes.
        
        Args:
            spins (int): Number of spins to generate
        """
        self.history = []
        for _ in range(spins):
            self.history.append(random.choice(self.wheel_order))
    
    def spin_batch(self, n_spins):
        """
        Generate a batch of random spins and return the results.
        
        Args:
            n_spins (int): Number of spins to generate
            
        Returns:
            list: Results of the batch of spins
        """
        results = []
        for _ in range(n_spins):
            results.append(random.choice(self.wheel_order))
        return results
    
    def calculate_statistics(self):
        """Calculate basic statistics from the history."""
        # Count occurrences of each number
        self.number_counts = Counter(self.history)
        
        # Calculate frequencies
        total_spins = len(self.history)
        self.frequencies = {num: count / total_spins for num, count in self.number_counts.items()}
        
        # Calculate standard deviation from expected frequency
        expected_freq = 1 / len(self.wheel_order)
        variances = [(freq - expected_freq) ** 2 for freq in self.frequencies.values()]
        self.frequency_std = np.sqrt(np.mean(variances)) if variances else 0
        
        # Analyze consecutive occurrences
        self.streak_lengths = self.calculate_streaks()
        
        # Analyze patterns in the sequence
        self.calculate_patterns()
    
    def calculate_streaks(self):
        """
        Calculate streak lengths (consecutive occurrences) for each number.
        
        Returns:
            dict: Maximum streak length for each number
        """
        streak_lengths = defaultdict(int)
        current_streaks = defaultdict(int)
        
        for num in self.history:
            # Reset all streaks except for the current number
            for key in current_streaks:
                if key != num:
                    current_streaks[key] = 0
            
            # Increment streak for current number
            current_streaks[num] += 1
            
            # Update max streak if current is longer
            if current_streaks[num] > streak_lengths[num]:
                streak_lengths[num] = current_streaks[num]
        
        return dict(streak_lengths)
    
    def calculate_patterns(self):
        """Calculate common patterns in the history."""
        self.patterns = {}
        
        # Calculate common pairs (consecutive numbers)
        pairs = []
        for i in range(len(self.history) - 1):
            pairs.append((self.history[i], self.history[i+1]))
        
        pair_counts = Counter(pairs)
        total_pairs = len(pairs)
        
        # Only keep pairs that occur more than expected by random chance
        expected_pair_freq = 1 / (len(self.wheel_order) ** 2)
        significant_threshold = expected_pair_freq * 1.5  # 50% more than expected
        
        self.significant_pairs = {pair: count / total_pairs 
                                 for pair, count in pair_counts.items() 
                                 if count / total_pairs > significant_threshold}
        
        # Calculate common triplets
        if len(self.history) >= 3:
            triplets = []
            for i in range(len(self.history) - 2):
                triplets.append((self.history[i], self.history[i+1], self.history[i+2]))
            
            triplet_counts = Counter(triplets)
            total_triplets = len(triplets)
            
            # Only keep triplets that occur more than expected by random chance
            expected_triplet_freq = 1 / (len(self.wheel_order) ** 3)
            significant_threshold = expected_triplet_freq * 2  # 100% more than expected
            
            self.significant_triplets = {triplet: count / total_triplets 
                                        for triplet, count in triplet_counts.items() 
                                        if count / total_triplets > significant_threshold}
        else:
            self.significant_triplets = {}
    
    def get_number_stats(self, number):
        """
        Get statistics for a specific number.
        
        Args:
            number (str): The roulette number to analyze
            
        Returns:
            dict: Statistics for the specified number
        """
        if number not in self.wheel_order:
            return {"error": f"Number {number} not found on the wheel"}
        
        # Find all occurrences of this number
        occurrences = [i for i, num in enumerate(self.history) if num == number]
        
        # Calculate gaps between occurrences
        gaps = []
        for i in range(1, len(occurrences)):
            gaps.append(occurrences[i] - occurrences[i-1])
        
        # Calculate average gap
        avg_gap = np.mean(gaps) if gaps else 0
        
        # Calculate following numbers (what tends to come after this number)
        following = []
        for i in range(len(self.history) - 1):
            if self.history[i] == number:
                following.append(self.history[i+1])
        
        following_counts = Counter(following)
        total_following = len(following)
        following_freqs = {num: count / total_following for num, count in following_counts.items()} if total_following else {}
        
        # Prepare stats
        stats = {
            "count": self.number_counts.get(number, 0),
            "frequency": self.frequencies.get(number, 0),
            "max_streak": self.streak_lengths.get(number, 0),
            "avg_gap": avg_gap,
            "following_numbers": dict(sorted(following_freqs.items(), key=lambda x: x[1], reverse=True)[:5])
        }
        
        return stats
    
    def find_hot_numbers(self, n=5):
        """
        Find the n most frequently occurring numbers.
        
        Args:
            n (int): Number of hot numbers to return
            
        Returns:
            list: The n most frequent numbers
        """
        sorted_counts = sorted(self.number_counts.items(), key=lambda x: x[1], reverse=True)
        return [num for num, _ in sorted_counts[:n]]
    
    def find_cold_numbers(self, n=5):
        """
        Find the n least frequently occurring numbers.
        
        Args:
            n (int): Number of cold numbers to return
            
        Returns:
            list: The n least frequent numbers
        """
        sorted_counts = sorted(self.number_counts.items(), key=lambda x: x[1])
        return [num for num, _ in sorted_counts[:n]]
    
    def find_due_numbers(self, n=5):
        """
        Find numbers that haven't appeared for the longest time.
        
        Args:
            n (int): Number of due numbers to return
            
        Returns:
            list: The n most overdue numbers
        """
        last_positions = {}
        for i, num in enumerate(self.history):
            last_positions[num] = i
        
        # Find all numbers on the wheel that aren't in last_positions
        missing = [num for num in self.wheel_order if num not in last_positions]
        
        # Add missing numbers with position -1 (never occurred)
        for num in missing:
            last_positions[num] = -1
        
        # Sort by position (smallest/earliest first)
        sorted_positions = sorted(last_positions.items(), key=lambda x: x[1])
        
        return [num for num, _ in sorted_positions[:n]]
    
    def analyze_sectors(self):
        """
        Analyze the distribution of outcomes across physical sectors of the wheel.
        
        Returns:
            dict: Statistics for each sector
        """
        # Define sectors (groups of physically adjacent numbers)
        sectors = {}
        
        # Divide wheel into 8 sectors of adjacent numbers
        sector_size = len(self.wheel_order) // 8
        for i in range(8):
            start = i * sector_size
            end = start + sector_size
            sector_numbers = self.wheel_order[start:end]
            sectors[f"Sector {i+1}"] = sector_numbers
        
        # Count occurrences in each sector
        sector_counts = {}
        for name, numbers in sectors.items():
            count = sum(self.number_counts.get(num, 0) for num in numbers)
            sector_counts[name] = count
        
        # Calculate frequencies
        total_spins = len(self.history)
        sector_freqs = {name: count / total_spins for name, count in sector_counts.items()}
        
        return {
            "counts": sector_counts,
            "frequencies": sector_freqs
        }
    
    def analyze_number_properties(self):
        """
        Analyze distribution across various number properties (red/black, odd/even, etc.).
        
        Returns:
            dict: Statistics for different number properties
        """
        # Initialize counters
        red_count = sum(self.number_counts.get(num, 0) for num in self.red_numbers)
        black_count = sum(self.number_counts.get(num, 0) for num in self.black_numbers)
        green_count = sum(self.number_counts.get(num, 0) for num in self.green_numbers)
        
        # Odd/Even
        odd_numbers = [str(n) for n in range(1, 37, 2)]
        even_numbers = [str(n) for n in range(2, 37, 2)]
        
        odd_count = sum(self.number_counts.get(num, 0) for num in odd_numbers)
        even_count = sum(self.number_counts.get(num, 0) for num in even_numbers)
        
        # Low/High
        low_numbers = [str(n) for n in range(1, 19)]
        high_numbers = [str(n) for n in range(19, 37)]
        
        low_count = sum(self.number_counts.get(num, 0) for num in low_numbers)
        high_count = sum(self.number_counts.get(num, 0) for num in high_numbers)
        
        # Dozens
        first_dozen = [str(n) for n in range(1, 13)]
        second_dozen = [str(n) for n in range(13, 25)]
        third_dozen = [str(n) for n in range(25, 37)]
        
        first_dozen_count = sum(self.number_counts.get(num, 0) for num in first_dozen)
        second_dozen_count = sum(self.number_counts.get(num, 0) for num in second_dozen)
        third_dozen_count = sum(self.number_counts.get(num, 0) for num in third_dozen)
        
        # Columns
        first_column = [str(n) for n in range(1, 37, 3)]
        second_column = [str(n) for n in range(2, 37, 3)]
        third_column = [str(n) for n in range(3, 37, 3)]
        
        first_column_count = sum(self.number_counts.get(num, 0) for num in first_column)
        second_column_count = sum(self.number_counts.get(num, 0) for num in second_column)
        third_column_count = sum(self.number_counts.get(num, 0) for num in third_column)
        
        # Calculate total (excluding 0 and 00 for some properties)
        total_non_green = len(self.history) - green_count
        
        # Return stats
        return {
            "color": {
                "red": red_count / len(self.history) if len(self.history) > 0 else 0,
                "black": black_count / len(self.history) if len(self.history) > 0 else 0,
                "green": green_count / len(self.history) if len(self.history) > 0 else 0
            },
            "parity": {
                "odd": odd_count / total_non_green if total_non_green > 0 else 0,
                "even": even_count / total_non_green if total_non_green > 0 else 0
            },
            "range": {
                "low": low_count / total_non_green if total_non_green > 0 else 0,
                "high": high_count / total_non_green if total_non_green > 0 else 0
            },
            "dozen": {
                "first": first_dozen_count / total_non_green if total_non_green > 0 else 0,
                "second": second_dozen_count / total_non_green if total_non_green > 0 else 0,
                "third": third_dozen_count / total_non_green if total_non_green > 0 else 0
            },
            "column": {
                "first": first_column_count / total_non_green if total_non_green > 0 else 0,
                "second": second_column_count / total_non_green if total_non_green > 0 else 0,
                "third": third_column_count / total_non_green if total_non_green > 0 else 0
            }
        }
    
    def analyze_number_combinations(self):
        """
        Analyze combinations of numbers to find potential patterns.
        
        Returns:
            dict: Information about number combinations
        """
        # Look for neighbors on the wheel that hit together
        neighbor_pairs = []
        for i in range(len(self.wheel_order)):
            # Get this number and its neighbors
            num = self.wheel_order[i]
            left_idx = (i - 1) % len(self.wheel_order)
            right_idx = (i + 1) % len(self.wheel_order)
            
            left_neighbor = self.wheel_order[left_idx]
            right_neighbor = self.wheel_order[right_idx]
            
            # Check if this number and either neighbor appear consecutively
            for j in range(len(self.history) - 1):
                if self.history[j] == num:
                    if self.history[j+1] == left_neighbor or self.history[j+1] == right_neighbor:
                        neighbor_pairs.append((self.history[j], self.history[j+1]))
        
        # Count number of times neighbor pairs occur
        neighbor_pair_counts = Counter(neighbor_pairs)
        
        # Check for mirror numbers (numbers on opposite sides of the wheel)
        mirror_pairs = []
        for i in range(len(self.wheel_order) // 2):
            opposite_idx = (i + len(self.wheel_order) // 2) % len(self.wheel_order)
            num = self.wheel_order[i]
            opposite = self.wheel_order[opposite_idx]
            
            # Check if number and its opposite appear close to each other
            for j in range(len(self.history) - 5):  # Within 5 spins
                window = self.history[j:j+5]
                if num in window and opposite in window:
                    idx1 = window.index(num)
                    idx2 = window.index(opposite)
                    mirror_pairs.append((num, opposite, abs(idx2 - idx1)))
        
        # Analyze splits (adjacent numbers on the layout)
        splits = [
            ('1', '2'), ('2', '3'), ('4', '5'), ('5', '6'), ('7', '8'), ('8', '9'),
            ('10', '11'), ('11', '12'), ('13', '14'), ('14', '15'), ('16', '17'), ('17', '18'),
            ('19', '20'), ('20', '21'), ('22', '23'), ('23', '24'), ('25', '26'), ('26', '27'),
            ('28', '29'), ('29', '30'), ('31', '32'), ('32', '33'), ('34', '35'), ('35', '36'),
            ('1', '4'), ('2', '5'), ('3', '6'), ('4', '7'), ('5', '8'), ('6', '9'),
            ('7', '10'), ('8', '11'), ('9', '12'), ('10', '13'), ('11', '14'), ('12', '15'),
            ('13', '16'), ('14', '17'), ('15', '18'), ('16', '19'), ('17', '20'), ('18', '21'),
            ('19', '22'), ('20', '23'), ('21', '24'), ('22', '25'), ('23', '26'), ('24', '27'),
            ('25', '28'), ('26', '29'), ('27', '30'), ('28', '31'), ('29', '32'), ('30', '33'),
            ('31', '34'), ('32', '35'), ('33', '36')
        ]
        
        split_hits = 0
        for i in range(len(self.history) - 1):
            current = self.history[i]
            next_num = self.history[i+1]
            
            # Check if current and next form a split
            if (current, next_num) in splits or (next_num, current) in splits:
                split_hits += 1
        
        split_frequency = split_hits / (len(self.history) - 1) if len(self.history) > 1 else 0
        
        return {
            "neighbor_pairs": dict(sorted(neighbor_pair_counts.items(), key=lambda x: x[1], reverse=True)[:10]),
            "mirror_pairs": sorted(mirror_pairs, key=lambda x: x[2])[:10],
            "split_hits": split_hits,
            "split_frequency": split_frequency
        }
    
    def generate_report(self):
        """
        Generate a comprehensive report of the analysis.
        
        Returns:
            dict: Complete analysis report
        """
        return {
            "total_spins": len(self.history),
            "hot_numbers": self.find_hot_numbers(10),
            "cold_numbers": self.find_cold_numbers(10),
            "due_numbers": self.find_due_numbers(10),
            "sector_analysis": self.analyze_sectors(),
            "property_analysis": self.analyze_number_properties(),
            "combination_analysis": self.analyze_number_combinations(),
            "significant_pairs": self.significant_pairs,
            "significant_triplets": self.significant_triplets
        }
    
    def recommend_numbers(self, n=8, method="frequency"):
        """
        Recommend n numbers to bet on based on specified method.
        
        Args:
            n (int): Number of recommendations to make
            method (str): Method to use ('frequency', 'streaks', 'due', 'combinations')
            
        Returns:
            list: Recommended numbers
        """
        if method == "frequency":
            # Recommend hot numbers
            return self.find_hot_numbers(n)
            
        elif method == "streaks":
            # Recommend numbers with long streaks
            sorted_streaks = sorted(self.streak_lengths.items(), key=lambda x: x[1], reverse=True)
            return [num for num, _ in sorted_streaks[:n]]
            
        elif method == "due":
            # Recommend overdue numbers
            return self.find_due_numbers(n)
            
        elif method == "combinations":
            # Recommend based on significant patterns
            candidates = []
            
            # Add second numbers from significant pairs
            for (first, second), _ in sorted(self.significant_pairs.items(), 
                                             key=lambda x: x[1], 
                                             reverse=True)[:n]:
                candidates.append(second)
            
            # If we need more recommendations, add from triplets
            if len(candidates) < n and self.significant_triplets:
                for (first, second, third), _ in sorted(self.significant_triplets.items(),
                                                       key=lambda x: x[1],
                                                       reverse=True)[:n - len(candidates)]:
                    candidates.append(third)
            
            # If still not enough, add hot numbers
            if len(candidates) < n:
                hot_numbers = self.find_hot_numbers(n - len(candidates))
                candidates.extend(hot_numbers)
            
            # Remove duplicates while preserving order
            seen = set()
            return [x for x in candidates if not (x in seen or seen.add(x))][:n]
            
        else:
            raise ValueError(f"Unknown recommendation method: {method}")

    def get_recent_history(self, n=20):
        """
        Get the most recent n outcomes from the history.
        
        Args:
            n (int): Number of recent outcomes to return
            
        Returns:
            list: Recent outcomes
        """
        return self.history[-n:] if len(self.history) >= n else self.history 