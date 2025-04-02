#!/usr/bin/env python3
"""
Quantum pattern analyzer for roulette outcomes.
"""
import numpy as np
from collections import defaultdict
import math
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import linkage, fcluster

class QuantumPatternAnalyzer:
    """
    Advanced pattern detection system that combines 
    multiple analytical approaches to find hidden patterns in roulette outcomes.
    """
    
    def __init__(self, analyzer, history_length=10000):
        self.analyzer = analyzer
        self.history_length = history_length
        
        # Analysis components
        self.physical_bias = None
        self.markov_model = None
        self.correlations = None
        self.neural_weights = None

    def initialize(self):
        """Initialize all analytics components"""
        # Ensure we have sufficient history
        current_history_len = len(self.analyzer.history)
        if current_history_len < self.history_length:
            additional_needed = self.history_length - current_history_len
            self.analyzer.spin_batch(additional_needed)
            
        # Run all analysis components
        self._analyze_physical_bias()
        self._build_markov_model()
        self._analyze_correlations()
        self._initialize_neural_weights()
        
        print(f"Quantum Pattern Analyzer initialized with {len(self.analyzer.history)} data points")
        
    def _analyze_physical_bias(self):
        """
        Analyze for potential physical bias in the wheel
        based on outcomes distribution and adjacency patterns.
        """
        # Simple frequency analysis
        frequencies = defaultdict(int)
        for num in self.analyzer.history:
            frequencies[num] += 1
            
        # Calculate expected frequency
        total_spins = len(self.analyzer.history)
        expected_freq = total_spins / len(self.analyzer.numbers)
        
        # Calculate deviations and find biased numbers
        deviations = {}
        for num in self.analyzer.numbers:
            actual_freq = frequencies.get(num, 0)
            deviation = (actual_freq - expected_freq) / math.sqrt(expected_freq * (1 - 1/len(self.analyzer.numbers)))
            deviations[num] = deviation
            
        # Find numbers with significant bias (over 2 standard deviations)
        significant_bias = {n: dev for n, dev in deviations.items() if abs(dev) > 2.0}
        
        # Analyze wheel sectors for bias
        wheel_sectors = {}
        for i in range(0, len(self.analyzer.wheel_order), 5):
            sector = self.analyzer.wheel_order[i:i+5]
            if len(sector) < 3:
                continue
                
            sector_hits = sum(frequencies.get(num, 0) for num in sector)
            sector_expected = expected_freq * len(sector)
            sector_deviation = (sector_hits - sector_expected) / math.sqrt(sector_expected * (1 - len(sector)/len(self.analyzer.numbers)))
            
            if abs(sector_deviation) > 1.5:  # Lower threshold for sectors
                wheel_sectors[f"sector_{i}"] = {
                    "numbers": sector,
                    "deviation": sector_deviation,
                    "hit_rate": sector_hits / total_spins
                }
                
        # Analyze for sequential patterns (pairs of numbers)
        if len(self.analyzer.history) > 100:
            pairs = defaultdict(int)
            for i in range(len(self.analyzer.history) - 1):
                pair = (self.analyzer.history[i], self.analyzer.history[i+1])
                pairs[pair] += 1
                
            # Find significant pairs
            significant_pairs = {}
            for pair, count in pairs.items():
                expected_pair_count = total_spins / (len(self.analyzer.numbers) ** 2)
                deviation = (count - expected_pair_count) / math.sqrt(expected_pair_count)
                if abs(deviation) > 2.5:
                    significant_pairs[pair] = deviation
                    
            # Store results
            self.physical_bias = {
                "number_bias": significant_bias,
                "sector_bias": wheel_sectors,
                "sequential_bias": significant_pairs
            }
        
    def _build_markov_model(self):
        """
        Build a Markov chain model to capture sequential dependencies
        in roulette outcomes.
        """
        # Initialize transition matrix
        num_to_idx = {num: i for i, num in enumerate(self.analyzer.numbers)}
        n_states = len(self.analyzer.numbers)
        
        # Initialize with small pseudocounts
        transitions = np.ones((n_states, n_states)) * 0.1
        
        # Count transitions
        for i in range(len(self.analyzer.history) - 1):
            from_num = self.analyzer.history[i]
            to_num = self.analyzer.history[i+1]
            
            from_idx = num_to_idx[from_num]
            to_idx = num_to_idx[to_num]
            
            transitions[from_idx, to_idx] += 1
            
        # Normalize to get probabilities
        row_sums = transitions.sum(axis=1, keepdims=True)
        transition_probs = transitions / row_sums
        
        # Store the model
        self.markov_model = {
            "num_to_idx": num_to_idx,
            "idx_to_num": {i: num for num, i in num_to_idx.items()},
            "transitions": transition_probs
        }
    
    def _analyze_correlations(self):
        """
        Analyze correlations and patterns beyond sequential relationships.
        Look for long-distance correlations and cyclic patterns.
        """
        # Convert history to numeric representation
        numeric_history = np.array([int(n) if n.isdigit() else (0 if n == '0' else 37) 
                                   for n in self.analyzer.history])
        
        # Maximum lag to consider
        max_lag = 20
        
        # Calculate autocorrelations
        autocorr = []
        for lag in range(1, max_lag + 1):
            if lag >= len(numeric_history):
                break
                
            # Slice the arrays for lag calculation
            x1 = numeric_history[:-lag]
            x2 = numeric_history[lag:]
            
            # Calculate correlation coefficient
            correlation = np.corrcoef(x1, x2)[0, 1]
            autocorr.append((lag, correlation))
        
        # Find significant lags
        significant_lags = [(lag, corr) for lag, corr in autocorr 
                          if abs(corr) > 0.1]  # Threshold for significance
            
        # Detect cycles - lags with positive correlation
        cycles = [(lag, corr) for lag, corr in significant_lags if corr > 0]
            
        # Distance matrix for clustering
        if len(self.analyzer.history) > 1000:
            # Take a sample to make clustering more efficient
            sample_size = 1000
            sample_indices = np.random.choice(
                len(numeric_history) - 10, sample_size, replace=False)
            
            # Create feature vectors: each vector is a number and 5 subsequent numbers
            sequence_length = 6
            feature_vectors = np.array([
                numeric_history[i:i+sequence_length] 
                for i in sample_indices
            ])
            
            # Calculate distance matrix
            distances = pdist(feature_vectors, 'euclidean')
            dist_matrix = squareform(distances)
            
            # Hierarchical clustering
            linkage_matrix = linkage(distances, method='ward')
            
            # Identify clusters
            clusters = fcluster(linkage_matrix, t=5, criterion='distance')
            
            # Count members in each cluster
            cluster_counts = np.bincount(clusters)
            
            # Find significant clusters (more than random chance would predict)
            expected_cluster_size = sample_size / np.max(clusters)
            significant_clusters = [i for i, count in enumerate(cluster_counts) 
                                  if i > 0 and count > expected_cluster_size * 1.5]
            
            # Extract prototypes from significant clusters
            cluster_prototypes = []
            for cluster_id in significant_clusters:
                # Get all sequences in this cluster
                cluster_members = feature_vectors[clusters == cluster_id]
                
                # Find the centroid (average sequence)
                centroid = np.mean(cluster_members, axis=0)
                
                # Find the closest actual sequence to the centroid
                distances_to_centroid = np.linalg.norm(
                    cluster_members - centroid, axis=1)
                closest_idx = np.argmin(distances_to_centroid)
                prototype = cluster_members[closest_idx]
                
                # Convert numeric representation back to number strings
                prototype_numbers = [
                    self.analyzer.numbers[int(p)] if p < len(self.analyzer.numbers) else '00'
                    for p in prototype
                ]
                
                cluster_prototypes.append({
                    'pattern': prototype_numbers,
                    'size': int(cluster_counts[cluster_id]),
                    'percentage': cluster_counts[cluster_id] / sample_size * 100
                })
                
            # Store correlation analysis results
            self.correlations = {
                'autocorrelations': autocorr,
                'significant_lags': significant_lags,
                'cycles': cycles,
                'cluster_prototypes': cluster_prototypes if len(significant_clusters) > 0 else []
            }
        else:
            # Not enough data for clustering
            self.correlations = {
                'autocorrelations': autocorr,
                'significant_lags': significant_lags,
                'cycles': cycles,
                'cluster_prototypes': []
            }
            
    def _initialize_neural_weights(self):
        """
        Create a simple neural network weight matrix to capture
        more complex dependencies between numbers.
        """
        n_numbers = len(self.analyzer.numbers)
        
        # Initialize weight matrix with small values
        weights = np.random.randn(n_numbers, n_numbers) * 0.01
        
        # Convert history to indices
        num_to_idx = {num: i for i, num in enumerate(self.analyzer.numbers)}
        history_idx = [num_to_idx[num] for num in self.analyzer.history]
        
        # Learn weights based on co-occurrence within a window
        window_size = 5
        learning_rate = 0.01
        
        for i in range(len(history_idx) - window_size):
            window = history_idx[i:i+window_size]
            
            # Update weights for all pairs in window
            for j in range(len(window)):
                for k in range(j+1, len(window)):
                    distance = k - j
                    idx1, idx2 = window[j], window[k]
                    
                    # Inversely proportional to distance in window
                    weights[idx1, idx2] += learning_rate / distance
                    weights[idx2, idx1] += learning_rate / distance
        
        # Normalize weights
        row_sums = np.sum(np.abs(weights), axis=1, keepdims=True)
        normalized_weights = weights / row_sums
        
        self.neural_weights = {
            'weights': normalized_weights,
            'num_to_idx': num_to_idx,
            'idx_to_num': {i: num for num, i in num_to_idx.items()}
        }
        
    def predict_next_numbers(self, recent_history=None, top_n=10):
        """
        Predict most likely next numbers based on recent history
        using ensemble of prediction methods.
        """
        if not self.markov_model or not self.neural_weights:
            raise ValueError("Analyzer not initialized. Call initialize() first.")
            
        # Use provided history or the last 10 numbers from analyzer
        if recent_history is None:
            recent_history = self.analyzer.history[-10:]
            
        # Ensure we have at least some history
        if len(recent_history) == 0:
            # Return random selection if no history
            import random
            return {
                'predictions': random.sample(self.analyzer.numbers, top_n),
                'confidence': 0.0
            }
            
        # Get predictions from each model
        markov_preds = self._predict_with_markov(recent_history)
        correlation_preds = self._predict_with_correlations(recent_history)
        
        # Bias predictions - focus on numbers with physical bias
        biased_numbers = []
        if self.physical_bias and self.physical_bias['number_bias']:
            # Get top biased numbers (positive deviation = more frequent)
            biased_numbers = [
                num for num, dev in sorted(
                    self.physical_bias['number_bias'].items(), 
                    key=lambda x: x[1], 
                    reverse=True
                )[:5]
            ]
            
        # Helper function to normalize probabilities
        def normalize_probs(probs):
            total = sum(probs.values())
            if total == 0:
                # If all zeros, return uniform distribution
                return {k: 1.0/len(probs) for k in probs}
            return {k: v/total for k, v in probs.items()}
            
        # Combine predictions with weights
        ensemble_probs = defaultdict(float)
        
        # Assign weights to each model
        weights = {
            'markov': 0.4,
            'correlation': 0.4,
            'bias': 0.2
        }
        
        # Add Markov predictions
        markov_probs = normalize_probs(markov_preds['probabilities'])
        for num, prob in markov_probs.items():
            ensemble_probs[num] += weights['markov'] * prob
            
        # Add correlation predictions
        correlation_probs = normalize_probs(correlation_preds['probabilities'])
        for num, prob in correlation_probs.items():
            ensemble_probs[num] += weights['correlation'] * prob
            
        # Add bias component
        if biased_numbers:
            bias_weight = weights['bias'] / len(biased_numbers)
            for num in biased_numbers:
                ensemble_probs[num] += bias_weight
                
        # Sort and return top predictions
        top_predictions = sorted(
            ensemble_probs.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:top_n]
        
        # Calculate overall confidence (entropy-based)
        top_probs = [p for _, p in top_predictions]
        entropy = -sum(p * np.log2(p) if p > 0 else 0 for p in top_probs)
        max_entropy = np.log2(len(top_probs)) if top_probs else 1
        confidence = 1 - (entropy / max_entropy) if max_entropy > 0 else 0
        
        return {
            'predictions': [num for num, _ in top_predictions],
            'probabilities': {num: prob for num, prob in top_predictions},
            'confidence': confidence
        }
        
    def _predict_with_markov(self, recent_history):
        """Use Markov model to predict next numbers"""
        if len(recent_history) == 0:
            # Return uniform probabilities if no history
            return {
                'probabilities': {num: 1.0/len(self.analyzer.numbers) for num in self.analyzer.numbers}
            }
            
        # Get last number in history
        last_num = recent_history[-1]
        
        # Convert to index
        idx = self.markov_model['num_to_idx'].get(last_num)
        if idx is None:
            # Handle unknown number (shouldn't happen with proper initialization)
            return {
                'probabilities': {num: 1.0/len(self.analyzer.numbers) for num in self.analyzer.numbers}
            }
            
        # Get transition probabilities from this state
        trans_probs = self.markov_model['transitions'][idx]
        
        # Convert to dictionary
        probabilities = {
            self.markov_model['idx_to_num'][i]: prob 
            for i, prob in enumerate(trans_probs)
        }
        
        return {
            'probabilities': probabilities
        }
        
    def _predict_with_correlations(self, recent_history):
        """Use correlation analysis to predict next numbers"""
        # Default to uniform distribution
        uniform_probs = {num: 1.0/len(self.analyzer.numbers) for num in self.analyzer.numbers}
        
        if not self.correlations or len(recent_history) < 5:
            return {'probabilities': uniform_probs}
            
        # Check if we have significant cycles
        if not self.correlations['cycles']:
            return {'probabilities': uniform_probs}
            
        # Find best cycle lag
        best_lag = max(self.correlations['cycles'], key=lambda x: x[1])[0]
        
        # If history is shorter than lag, we can't use this method
        if len(recent_history) <= best_lag:
            return {'probabilities': uniform_probs}
            
        # Get number at best lag position
        cyclic_number = recent_history[-best_lag]
        
        # Initialize probabilities with a boost for this number
        probabilities = uniform_probs.copy()
        probabilities[cyclic_number] *= 3.0  # Boost the cyclic prediction
        
        # Check if we have cluster prototypes
        if self.correlations['cluster_prototypes']:
            # Find prototypes that match the recent history
            match_scores = []
            
            for prototype in self.correlations['cluster_prototypes']:
                pattern = prototype['pattern']
                if len(pattern) <= len(recent_history):
                    # Try to match the beginning of the pattern with the end of history
                    pattern_length = len(pattern)
                    history_tail = recent_history[-pattern_length:]
                    
                    # Calculate match score (percentage of matching elements)
                    matches = sum(1 for i, num in enumerate(history_tail) if num == pattern[i])
                    match_pct = matches / pattern_length
                    
                    if match_pct >= 0.5:  # At least 50% match
                        match_scores.append((prototype, match_pct))
            
            # If we have matching prototypes, use them to adjust probabilities
            if match_scores:
                # Sort by match percentage
                match_scores.sort(key=lambda x: x[1], reverse=True)
                
                # Get top match
                best_match, score = match_scores[0]
                
                # Find next number in the pattern after the matching segment
                history_len = len(recent_history)
                pattern = best_match['pattern']
                pattern_len = len(pattern)
                
                # Find the position where the pattern extends beyond history
                for offset in range(1, pattern_len):
                    if history_len >= offset:
                        # Compare pattern and history with this offset
                        match_len = min(pattern_len - offset, history_len)
                        pattern_segment = pattern[:match_len]
                        history_segment = recent_history[-match_len:]
                        
                        if pattern_segment == history_segment:
                            # We found a match, predict the next number from pattern
                            predicted = pattern[match_len] if match_len < pattern_len else None
                            if predicted:
                                # Boost this prediction significantly
                                probabilities[predicted] *= (2.0 + score * 3.0)
                                break
        
        return {'probabilities': probabilities}
    
    def get_optimum_betting_combination(self, num_numbers=8):
        """
        Generate an optimum combination of numbers to bet on
        based on all analytical components.
        """
        # Get predictions
        recent_history = self.analyzer.history[-20:]
        predictions = self.predict_next_numbers(recent_history, top_n=num_numbers)
        
        # Calculate wheel distance between two numbers
        def wheel_distance(num1, num2):
            if num1 not in self.analyzer.wheel_order or num2 not in self.analyzer.wheel_order:
                return len(self.analyzer.wheel_order) // 2  # Default to half way around
                
            idx1 = self.analyzer.wheel_order.index(num1)
            idx2 = self.analyzer.wheel_order.index(num2)
            
            # Distance in both directions around the wheel
            dist1 = abs(idx1 - idx2)
            dist2 = len(self.analyzer.wheel_order) - dist1
            
            return min(dist1, dist2)
        
        # Start with top predictions
        selected_numbers = predictions['predictions'][:num_numbers//2]
        
        # Add some numbers with physical bias if available
        if self.physical_bias and self.physical_bias['number_bias']:
            biased_nums = sorted(
                self.physical_bias['number_bias'].items(),
                key=lambda x: x[1],
                reverse=True
            )
            
            for num, _ in biased_nums:
                if len(selected_numbers) >= num_numbers:
                    break
                if num not in selected_numbers:
                    selected_numbers.append(num)
        
        # Add numbers that are nearby on the wheel to selected numbers
        # (to increase coverage of physical wheel sectors)
        if len(selected_numbers) < num_numbers:
            # For each selected number, find close neighbors on wheel
            for num in selected_numbers[:]:
                if len(selected_numbers) >= num_numbers:
                    break
                    
                # Find neighbors
                if num in self.analyzer.wheel_order:
                    idx = self.analyzer.wheel_order.index(num)
                    
                    # Try neighbors at different distances
                    for distance in [1, 2, -1, -2]:
                        neighbor_idx = (idx + distance) % len(self.analyzer.wheel_order)
                        neighbor = self.analyzer.wheel_order[neighbor_idx]
                        
                        if neighbor not in selected_numbers:
                            selected_numbers.append(neighbor)
                            if len(selected_numbers) >= num_numbers:
                                break
        
        # Fill remaining slots with random selections if needed
        while len(selected_numbers) < num_numbers:
            remaining = [n for n in self.analyzer.numbers if n not in selected_numbers]
            if not remaining:
                break
                
            import random
            selected_numbers.append(random.choice(remaining))
        
        # Calculate coverage percentage
        coverage = len(selected_numbers) / len(self.analyzer.numbers) * 100
        
        return {
            'numbers': selected_numbers[:num_numbers],
            'coverage': coverage,
            'confidence': predictions['confidence']
        } 