#!/usr/bin/env python3
"""
Bayesian statistics predictor for roulette outcomes.
"""

class BayesianPredictor:
    """
    Uses Bayesian statistics to update probabilities
    based on observed outcomes.
    """
    def __init__(self):
        # Prior probabilities (start with uniform)
        self.priors = {'red': 18/38, 'black': 18/38, 'green': 2/38}
        self.number_priors = {str(i): 1/38 for i in range(1, 37)}
        self.number_priors['0'] = 1/38
        self.number_priors['00'] = 1/38
        
        # Evidence counters
        self.observations = {'red': 0, 'black': 0, 'green': 0}
        self.number_observations = {str(i): 0 for i in range(1, 37)}
        self.number_observations['0'] = 0
        self.number_observations['00'] = 0
        
        # Total observations
        self.total_observations = 0
        
    def update(self, result, color):
        """Update Bayesian model with new observation"""
        # Update counters
        self.observations[color] += 1
        self.number_observations[result] += 1
        self.total_observations += 1
        
        # Apply Bayesian update formula (simple count-based approach)
        # P(A|B) = P(B|A) * P(A) / P(B)
        # For simple count-based systems, we just use frequencies
        
    def predict_next_color(self):
        """Predict the most likely next color using Bayesian inference"""
        if self.total_observations < 10:
            return 'black'  # Default before enough data
            
        # Get posterior probabilities (with smoothing)
        alpha = 0.5  # Smoothing parameter
        posteriors = {}
        for color in ['red', 'black', 'green']:
            posteriors[color] = (self.observations[color] + alpha) / (self.total_observations + 3*alpha)
        
        # Find the color with the lowest posterior (contrarian strategy)
        min_color = min(posteriors.items(), key=lambda x: x[1])[0]
        
        return min_color
        
    def predict_most_likely_numbers(self, n=5):
        """Predict n most likely numbers based on observations"""
        if self.total_observations < 20:
            return [str(i) for i in range(1, 6)]  # Default before enough data
            
        # Calculate probability for each number (with smoothing)
        alpha = 0.1  # Smoothing parameter
        posteriors = {}
        for num in self.number_observations:
            posteriors[num] = (self.number_observations[num] + alpha) / (self.total_observations + 38*alpha)
            
        # Find numbers with lowest posterior (contrarian approach)
        sorted_nums = sorted(posteriors.items(), key=lambda x: x[1])
        
        return [num for num, _ in sorted_nums[:n]] 