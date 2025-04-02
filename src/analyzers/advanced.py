#!/usr/bin/env python3
"""
Advanced roulette analyzer with multiple statistical approaches.
"""
import random
import numpy as np
from collections import defaultdict, Counter

class AdvancedRouletteAnalyzer:
    """
    Advanced analyzer for roulette patterns and statistics.
    Includes multiple methods for statistical analysis of roulette outcomes.
    """
    def __init__(self):
        # American roulette has numbers 0, 00, and 1-36
        self.numbers = ['0', '00'] + [str(i) for i in range(1, 37)]
        self.wheel_order = self._initialize_wheel_order()
        
        # Mappings and lookups for colors and sectors
        self._initialize_color_mappings()
        self.sectors = self._generate_sector_mappings()
        
        # History tracking
        self.history = []
        self.color_history = []
        
        # Performance tracking
        self.spins_count = 0
        self.hit_rates = {}
        self.pattern_frequencies = {}
        
    def _initialize_wheel_order(self):
        """Initialize American roulette wheel order"""
        # Physical order of numbers on an American roulette wheel
        return ['0', '28', '9', '26', '30', '11', '7', '20', '32', '17',
                '5', '22', '34', '15', '3', '24', '36', '13', '1', '00',
                '27', '10', '25', '29', '12', '8', '19', '31', '18', '6',
                '21', '33', '16', '4', '23', '35', '14', '2']
    
    def _initialize_color_mappings(self):
        """Setup color mappings for each number"""
        # Red numbers in American roulette
        red_numbers = ['1', '3', '5', '7', '9', '12', '14', '16', '18',
                      '19', '21', '23', '25', '27', '30', '32', '34', '36']
        
        # Black numbers in American roulette
        black_numbers = ['2', '4', '6', '8', '10', '11', '13', '15', '17',
                        '20', '22', '24', '26', '28', '29', '31', '33', '35']
        
        # Green numbers (0 and 00)
        green_numbers = ['0', '00']
        
        # Create mapping dict
        self.colors = {}
        for num in red_numbers:
            self.colors[num] = 'red'
        for num in black_numbers:
            self.colors[num] = 'black'
        for num in green_numbers:
            self.colors[num] = 'green'
        
    def _generate_sector_mappings(self):
        """Generate mappings for different sectors and betting areas"""
        # Standard betting areas
        sectors = {
            'first_dozen': [str(i) for i in range(1, 13)],
            'second_dozen': [str(i) for i in range(13, 25)],
            'third_dozen': [str(i) for i in range(25, 37)],
            'first_column': [str(i) for i in range(1, 37, 3)],
            'second_column': [str(i) for i in range(2, 37, 3)],
            'third_column': [str(i) for i in range(3, 37, 3)],
            'low': [str(i) for i in range(1, 19)],
            'high': [str(i) for i in range(19, 37)],
            'even': [str(i) for i in range(2, 37, 2)],
            'odd': [str(i) for i in range(1, 37, 2)],
            'red': [k for k, v in self.colors.items() if v == 'red'],
            'black': [k for k, v in self.colors.items() if v == 'black'],
            'green': ['0', '00']
        }
        
        # Add physical sectors (groups of adjacent numbers on the wheel)
        for i in range(0, len(self.wheel_order), 5):
            section = self.wheel_order[i:i+5]
            if len(section) >= 3:  # Only create sectors with at least 3 numbers
                sectors[f'wheel_sector_{i}'] = section
                
        return sectors
    
    def spin(self):
        """Simulate a single roulette spin"""
        result = random.choice(self.numbers)
        color = self.get_color(result)
        
        # Track history
        self.history.append(result)
        self.color_history.append(color)
        self.spins_count += 1
        
        return result, color
    
    def spin_batch(self, n_spins, store_history=True):
        """Simulate multiple spins efficiently"""
        results = []
        
        for _ in range(n_spins):
            result = random.choice(self.numbers)
            if store_history:
                self.history.append(result)
                self.color_history.append(self.get_color(result))
            results.append(result)
            
        self.spins_count += n_spins
        return results
    
    def get_color(self, number):
        """Get the color of a given number"""
        return self.colors.get(number, 'unknown')
        
    def calculate_shannon_entropy(self, sequence):
        """
        Calculate Shannon entropy of a sequence.
        Higher entropy indicates more randomness/unpredictability.
        """
        if not sequence:
            return 0
            
        # Count frequencies
        counts = Counter(sequence)
        total = sum(counts.values())
        
        # Calculate entropy: -sum(p_i * log2(p_i))
        entropy = 0
        for count in counts.values():
            probability = count / total
            entropy -= probability * np.log2(probability)
            
        return entropy
    
    def detect_bias(self, num_simulations=1000, confidence_level=0.95):
        """
        Analyze the wheel for potential bias using statistical methods.
        Uses chi-square test for goodness of fit against expected uniform distribution.
        """
        # If history is too short, simulate more spins
        if len(self.history) < 500:
            self.spin_batch(1000)
            
        # Count occurrences of each number
        counts = Counter(self.history)
        
        # Expected count for each number under fair conditions
        expected_count = len(self.history) / len(self.numbers)
        
        # Calculate chi-square statistic
        chi_square = sum((counts[num] - expected_count)**2 / expected_count 
                         for num in self.numbers)
        
        # Degrees of freedom = number of categories - 1
        df = len(self.numbers) - 1
        
        # Critical value for chi-square at given confidence level
        from scipy import stats
        critical_value = stats.chi2.ppf(confidence_level, df)
        
        # Identify potentially biased numbers
        p_value = 1 - stats.chi2.cdf(chi_square, df)
        
        # Get top 5 most frequent numbers
        most_frequent = counts.most_common(5)
        
        # Get bottom 5 least frequent numbers
        least_frequent = counts.most_common()[:-6:-1]
        
        return {
            'chi_square': chi_square,
            'critical_value': critical_value,
            'p_value': p_value,
            'bias_detected': chi_square > critical_value,
            'most_frequent': most_frequent,
            'least_frequent': least_frequent,
            'confidence_level': confidence_level
        }
    
    def analyze_sectors(self):
        """
        Analyze which sectors have been performing above or below expectation.
        Good for identifying temporary patterns or streaks.
        """
        if len(self.history) < 50:
            self.spin_batch(100)
            
        results = {}
        
        for sector_name, numbers in self.sectors.items():
            # Calculate expected hit rate
            expected_rate = len(numbers) / len(self.numbers)
            
            # Calculate actual hit rate from history
            hits = sum(1 for num in self.history if num in numbers)
            actual_rate = hits / len(self.history)
            
            # Calculate variance from expectation
            variance = actual_rate - expected_rate
            variance_percent = (variance / expected_rate) * 100
            
            results[sector_name] = {
                'expected_rate': expected_rate,
                'actual_rate': actual_rate,
                'variance': variance,
                'variance_percent': variance_percent,
                'hit_count': hits,
                'total_spins': len(self.history)
            }
            
        return results