#!/usr/bin/env python3
"""
Utility functions for roulette analysis.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import json
import os
from datetime import datetime
from collections import defaultdict

def validate_numbers_performance(analyzer, numbers, n_spins):
    """
    Validate the performance of a set of numbers through simulation.
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        numbers: List of number strings to bet on
        n_spins: Number of spins to simulate
        
    Returns:
        float: Win rate percentage
    """
    # Convert string numbers to ensure consistency
    numeric_targets = [str(num) for num in numbers]
    
    # Perform spins
    results = analyzer.spin_batch(n_spins)
    
    # Count hits
    hits = sum(1 for result in results if result in numeric_targets)
    
    # Calculate win rate
    win_rate = (hits / n_spins) * 100
    
    print(f"Validation completed: {hits} hits from {n_spins} spins ({win_rate:.2f}%)")
    
    return win_rate

def analyze_number_patterns(analyzer, num_simulations=5000, top_count=25):
    """
    Analyze patterns in roulette numbers to identify potential betting opportunities.
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        num_simulations: Number of simulations to run
        top_count: Number of top patterns to return
        
    Returns:
        dict: Analysis results
    """
    # Ensure we have enough data
    if len(analyzer.history) < num_simulations * 0.5:
        print(f"Generating additional data for pattern analysis...")
        analyzer.spin_batch(num_simulations)
    
    # Frequency analysis
    number_frequencies = {num: 0 for num in analyzer.numbers}
    for result in analyzer.history:
        number_frequencies[result] += 1
    
    total_spins = len(analyzer.history)
    
    # Calculate z-scores for each number
    expected_freq = total_spins / len(analyzer.numbers)
    number_zscores = {}
    
    for num, freq in number_frequencies.items():
        # Calculate standardized z-score
        std_dev = np.sqrt(expected_freq * (1 - 1/len(analyzer.numbers)))
        z_score = (freq - expected_freq) / std_dev
        number_zscores[num] = z_score
    
    # Pair frequency analysis
    if len(analyzer.history) >= 2:
        pairs = {}
        for i in range(len(analyzer.history) - 1):
            pair = (analyzer.history[i], analyzer.history[i+1])
            pairs[pair] = pairs.get(pair, 0) + 1
        
        # Find top pairs
        sorted_pairs = sorted(pairs.items(), key=lambda x: x[1], reverse=True)
        top_pairs = sorted_pairs[:top_count]
        
        # Calculate significance
        expected_pair_freq = total_spins / (len(analyzer.numbers) ** 2)
        pair_significance = []
        
        for pair, freq in top_pairs:
            std_dev = np.sqrt(expected_pair_freq * (1 - 1/(len(analyzer.numbers)**2)))
            z_score = (freq - expected_pair_freq) / std_dev
            significance = {
                'pair': pair,
                'frequency': freq,
                'z_score': z_score
            }
            pair_significance.append(significance)
    else:
        pair_significance = []
    
    # Analyze physical adjacency patterns
    wheel_sector_analysis = {}
    for i in range(0, len(analyzer.wheel_order), 3):
        sector = analyzer.wheel_order[i:i+5]
        if len(sector) < 3:
            continue
            
        hits = sum(1 for spin in analyzer.history if spin in sector)
        hit_rate = hits / total_spins * 100
        expected_rate = len(sector) / len(analyzer.numbers) * 100
        
        wheel_sector_analysis[f"sector_{i}"] = {
            'numbers': sector,
            'hit_rate': hit_rate,
            'expected_rate': expected_rate,
            'variance': hit_rate - expected_rate
        }
    
    # Sort wheel sectors by variance
    sorted_sectors = sorted(
        wheel_sector_analysis.items(), 
        key=lambda x: abs(x[1]['variance']), 
        reverse=True
    )
    top_sectors = sorted_sectors[:5]
    
    # Return full analysis
    return {
        'number_frequencies': number_frequencies,
        'number_zscores': number_zscores,
        'pair_significance': pair_significance,
        'top_sectors': top_sectors
    }

def load_previous_results():
    """
    Load previous analysis results from file.
    
    Returns:
        dict: Previous results data or empty dict if file doesn't exist
    """
    results_file = "output/strategy_performance.json"
    
    try:
        if os.path.exists(results_file):
            with open(results_file, 'r') as f:
                return json.load(f)
        else:
            return {}
    except Exception as e:
        print(f"Error loading previous results: {e}")
        return {}

def save_current_results(win_rate, formula_name, numbers, improvements=None):
    """
    Save current analysis results to file.
    
    Args:
        win_rate: Win rate percentage
        formula_name: Name of the formula/strategy
        numbers: List of recommended numbers
        improvements: Dict of improvement metrics
        
    Returns:
        bool: True if save was successful
    """
    results_file = "output/strategy_performance.json"
    
    try:
        # Create output directory if it doesn't exist
        os.makedirs("output", exist_ok=True)
        
        # Load existing data if available
        previous_data = load_previous_results()
        
        # Get current best rate
        current_best_rate = previous_data.get("best_rate", 0)
        
        # Update data
        current_data = {
            "last_run": {
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "win_rate": win_rate,
                "formula": formula_name,
                "numbers": numbers,
                "improvements": improvements or {}
            }
        }
        
        # Check if this is a new best result
        if win_rate > current_best_rate:
            current_data["best_rate"] = win_rate
            current_data["best_formula"] = formula_name
            current_data["best_numbers"] = numbers
            print("🚨 New best result achieved!")
        else:
            # Keep previous best
            current_data["best_rate"] = current_best_rate
            current_data["best_formula"] = previous_data.get("best_formula")
            current_data["best_numbers"] = previous_data.get("best_numbers")
        
        # Add historical runs if they exist
        if "history" in previous_data:
            current_data["history"] = previous_data["history"]
        else:
            current_data["history"] = []
        
        # Add current run to history
        history_entry = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "win_rate": win_rate,
            "formula": formula_name
        }
        current_data["history"].append(history_entry)
        
        # Keep history limited to last 20 runs
        if len(current_data["history"]) > 20:
            current_data["history"] = current_data["history"][-20:]
        
        # Save to file
        with open(results_file, 'w') as f:
            json.dump(current_data, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Error saving results: {e}")
        return False

def generate_performance_report(win_rate, formula_name, numbers):
    """
    Generate a report comparing the current performance with baselines.
    
    Args:
        win_rate: Current win rate percentage
        formula_name: Name of the formula/strategy
        numbers: List of recommended numbers
        
    Returns:
        dict: Performance comparison metrics
    """
    # Load previous results for comparison
    previous_data = load_previous_results()
    
    # Get the last_run info from previous_results for the report
    last_run = previous_data.get("last_run", {})
    
    # Define target baseline rate
    baseline_rate = 21.16  # Target percentage
    
    # Calculate improvements
    improvements = {}
    
    # Compare with baseline
    baseline_improvement = win_rate - baseline_rate
    baseline_percentage = (baseline_improvement / baseline_rate) * 100
    
    improvements["baseline"] = {
        "previous_rate": baseline_rate,
        "improvement": baseline_improvement,
        "percentage": baseline_percentage
    }
    
    # Compare with last run if it exists
    if "last_run" in previous_data:
        last_run = previous_data["last_run"]
        last_rate = last_run.get("win_rate", 0)
        
        last_improvement = win_rate - last_rate
        last_percentage = (last_improvement / last_rate) * 100 if last_rate > 0 else 0
        
        improvements["last_run"] = {
            "previous_rate": last_rate,
            "improvement": last_improvement,
            "percentage": last_percentage,
            "date": last_run.get("date", "Unknown")
        }
    
    # Compare with historical best if it exists and is different from current
    historical_best_rate = previous_data.get("best_rate", 0)
    if historical_best_rate > 0 and abs(historical_best_rate - win_rate) > 0.01:
        hist_improvement = win_rate - historical_best_rate
        hist_percentage = (hist_improvement / historical_best_rate) * 100
        
        improvements["historical"] = {
            "previous_rate": historical_best_rate,
            "improvement": hist_improvement,
            "percentage": hist_percentage,
            "formula": previous_data.get("best_formula", "Unknown")
        }
    
    return improvements

def plot_methodology_performance(final_combinations):
    """
    Generate a comparative visualization of the performance of all methodologies.
    
    Args:
        final_combinations: List of dictionaries with combinations from all methods
    """
    print("Generating comparative methodology chart...")
    
    # Sort by success rate (highest to lowest)
    sorted_combinations = sorted(final_combinations, key=lambda x: x['rate'], reverse=True)
    
    # Extract names and rates
    names = [combo['name'] for combo in sorted_combinations]
    rates = [combo['rate'] for combo in sorted_combinations]
    
    # Determine colors based on rate (best = green, worst = red)
    max_rate = max(rates)
    min_rate = min(rates)
    colors = []
    
    for rate in rates:
        # Normalize the rate between 0 and 1
        if max_rate > min_rate:
            normalized = (rate - min_rate) / (max_rate - min_rate)
        else:
            normalized = 0.5
            
        # Green for high rates, red for low
        colors.append((1-normalized, normalized, 0))
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Create horizontal bar chart
    bars = plt.barh(names, rates, color=colors)
    
    # Add value labels
    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2, 
                f"{rates[i]:.2f}%", va='center')
    
    # Customize chart
    plt.xlabel('Success Rate (%)')
    plt.title('Performance Comparison by Methodology')
    plt.grid(axis='x', linestyle='--', alpha=0.6)
    plt.tight_layout()
    
    # Save chart
    output_path = "output/graphs/methodology_comparison.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Comparative chart saved at: {output_path}")

def plot_methodology_pl_simulation(final_combinations):
    """
    Simulates and visualizes the profit/loss evolution for each methodology.
    
    Args:
        final_combinations: List of dictionaries with combinations from all methods
    """
    print("Generating profit/loss simulation...")
    
    # Simulation parameters
    n_spins = 100  # Number of spins to simulate
    bet_amount = 1  # Bet unit
    payout_multiplier = 35  # Roulette payout (35 to 1)
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Simulate for each methodology
    for combo in sorted(final_combinations, key=lambda x: x['rate'], reverse=True)[:8]:  # Top 8
        # Calculate probability per spin
        win_probability = combo['rate'] / 100
        
        # Simulate betting sequence
        cumulative_pl = [0]  # Start with 0
        
        for _ in range(n_spins):
            # Determine if we win on this spin
            if np.random.random() < win_probability:
                # Win: (payout - bets on numbers)
                win_amount = bet_amount * payout_multiplier - bet_amount * len(combo['numbers'])
                cumulative_pl.append(cumulative_pl[-1] + win_amount)
            else:
                # Lose: all bets
                cumulative_pl.append(cumulative_pl[-1] - bet_amount * len(combo['numbers']))
        
        # Plot this methodology
        plt.plot(range(n_spins+1), cumulative_pl, label=f"{combo['name']} ({combo['rate']:.2f}%)")
    
    # Equilibrium line (0)
    plt.axhline(y=0, color='black', linestyle='-', alpha=0.3)
    
    # Customize chart
    plt.xlabel('Number of Spins')
    plt.ylabel('Cumulative Profit/Loss (units)')
    plt.title('Profit/Loss Simulation by Methodology')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend(loc='best')
    plt.tight_layout()
    
    # Save chart
    output_path = "output/graphs/pl_simulation.png"
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Profit/loss simulation saved at: {output_path}")

def plot_individual_methodology_performance(combo, validation_analyzer, validation_spins):
    """
    Generates a detailed performance analysis for a specific methodology.
    
    Args:
        combo: Dictionary with methodology information
        validation_analyzer: Analyzer for validation
        validation_spins: Number of spins for validation
    """
    # Create safe filename
    safe_name = combo['name'].lower().replace(' ', '_')
    output_path = f"output/graphs/methodology_{safe_name}.png"
    
    # Extract information
    numbers = combo['numbers']
    win_rate = combo['rate']
    
    # Calculate coverage and performance
    coverage = len(numbers) / 38 * 100
    performance = (win_rate / coverage - 1) * 100
    
    # Simulate results for this set of numbers
    hits = []
    results = validation_analyzer.spin_batch(validation_spins)
    
    for result in results:
        if result in numbers:
            hits.append(1)  # Hit
        else:
            hits.append(0)  # Miss
    
    # Calculate cumulative frequency
    cumulative_hit_rate = []
    hit_count = 0
    
    for i, hit in enumerate(hits):
        hit_count += hit
        cumulative_hit_rate.append(hit_count / (i+1) * 100)
    
    # Create figure with two subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [2, 1]})
    
    # Chart 1: Cumulative hit rate
    ax1.plot(range(1, len(cumulative_hit_rate)+1), cumulative_hit_rate, 'b-')
    ax1.axhline(y=win_rate, color='r', linestyle='--', label=f'Final Rate: {win_rate:.2f}%')
    ax1.axhline(y=coverage, color='g', linestyle=':', label=f'Coverage: {coverage:.2f}%')
    
    # Customize chart 1
    ax1.set_xlabel('Number of Spins')
    ax1.set_ylabel('Hit Rate (%)')
    ax1.set_title(f'Performance Analysis: {combo["name"]}')
    ax1.grid(True, linestyle='--', alpha=0.6)
    ax1.legend(loc='best')
    
    # Chart 2: Streak distribution
    streak_lengths = []
    current_streak = 0
    streak_type = None
    
    for hit in hits:
        if streak_type is None:
            streak_type = hit
            current_streak = 1
        elif hit == streak_type:
            current_streak += 1
        else:
            streak_lengths.append((streak_type, current_streak))
            streak_type = hit
            current_streak = 1
    
    # Add the last streak
    if streak_type is not None:
        streak_lengths.append((streak_type, current_streak))
    
    # Filter win and loss streaks
    win_streaks = [length for streak_type, length in streak_lengths if streak_type == 1]
    loss_streaks = [length for streak_type, length in streak_lengths if streak_type == 0]
    
    # Streak histogram
    if win_streaks:
        ax2.hist(win_streaks, bins=range(1, max(win_streaks) + 2), alpha=0.6, 
                color='green', label='Win Streaks')
    if loss_streaks:
        ax2.hist(loss_streaks, bins=range(1, max(loss_streaks) + 2), alpha=0.6, 
                color='red', label='Loss Streaks')
    
    # Customize chart 2
    ax2.set_xlabel('Streak Length')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Streak Distribution')
    ax2.legend(loc='best')
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    # Add additional information
    info_text = (f"Numbers: {', '.join(numbers)}\n"
                f"Hit Rate: {win_rate:.2f}%\n"
                f"Coverage: {coverage:.2f}%\n"
                f"Performance vs Random: {performance:+.2f}%")
    
    fig.text(0.5, 0.01, info_text, ha='center', va='bottom', bbox=dict(facecolor='white', alpha=0.5))
    
    # Adjust layout and save
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_performance_history():
    """
    Generates a chart showing performance evolution over time.
    
    Returns:
        bool: True if the operation was successful
    """
    try:
        # Load historical data
        data = load_previous_results()
        history = data.get("history", [])
        
        if not history:
            print("No historical data available for charting.")
            return False
        
        # Extract dates and rates
        dates = [datetime.strptime(entry["date"], "%Y-%m-%d %H:%M:%S") for entry in history]
        rates = [entry["win_rate"] for entry in history]
        formulas = [entry["formula"] for entry in history]
        
        # Create figure
        plt.figure(figsize=(12, 8))
        
        # Plot evolution
        plt.plot(dates, rates, 'o-', color='blue')
        
        # Add labels for key points
        best_idx = rates.index(max(rates))
        plt.annotate(f"Best: {rates[best_idx]:.2f}%", 
                    xy=(dates[best_idx], rates[best_idx]),
                    xytext=(10, 10), textcoords='offset points',
                    bbox=dict(boxstyle="round,pad=0.3", fc="yellow", alpha=0.5))
        
        # Adjust date format on X axis
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates)//10)))
        
        # Customize chart
        plt.xlabel('Date')
        plt.ylabel('Success Rate (%)')
        plt.title('Performance Evolution')
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Save chart
        output_path = "output/graphs/performance_history.png"
        plt.savefig(output_path, dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Evolution chart saved at: {output_path}")
        return True
        
    except Exception as e:
        print(f"Error plotting performance history: {e}")
        return False

def plot_roulette_heatmap(final_combinations, target_directory="output/graphs"):
    """
    Generate a heatmap visualization of roulette numbers based on their frequency 
    in analysis results across all methodologies.
    
    Args:
        final_combinations: List of dictionaries with methodology data and recommended numbers
        target_directory: Directory to save the plot
        
    Returns:
        bool: True if plotting was successful
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(target_directory, exist_ok=True)
        
        # Get frequency of each number across all methods
        number_frequency = defaultdict(int)
        total_methods = len(final_combinations)
        
        # Count appearances of each number
        for combo in final_combinations:
            for number in combo["numbers"]:
                number_frequency[number] += 1
        
        # Normalize frequencies (0 to 1)
        max_freq = max(number_frequency.values()) if number_frequency else 1
        normalized_freq = {num: freq/max_freq for num, freq in number_frequency.items()}
        
        # Define American roulette wheel number order
        wheel_numbers = [
            '0', '28', '9', '26', '30', '11', '7', '20', '32', '17', 
            '5', '22', '34', '15', '3', '24', '36', '13', '1', '00', 
            '27', '10', '25', '29', '12', '8', '19', '31', '18', '6', 
            '21', '33', '16', '4', '23', '35', '14', '2'
        ]
        
        # Create a circular plot (polar projection)
        fig, ax = plt.subplots(figsize=(12, 12), subplot_kw={'projection': 'polar'})
        
        # Calculate angles for each number (distribute evenly in a circle)
        theta = np.linspace(0, 2*np.pi, len(wheel_numbers), endpoint=False)
        
        # Width of each segment
        width = 2*np.pi / len(wheel_numbers)
        
        # Define colors for the wheel positions
        colors = {
            '0': 'green',
            '00': 'green',
            '1': 'red', '3': 'red', '5': 'red', '7': 'red', '9': 'red',
            '12': 'red', '14': 'red', '16': 'red', '18': 'red', '19': 'red',
            '21': 'red', '23': 'red', '25': 'red', '27': 'red', '30': 'red',
            '32': 'red', '34': 'red', '36': 'red',
            '2': 'black', '4': 'black', '6': 'black', '8': 'black', '10': 'black',
            '11': 'black', '13': 'black', '15': 'black', '17': 'black', '20': 'black',
            '22': 'black', '24': 'black', '26': 'black', '28': 'black', '29': 'black',
            '31': 'black', '33': 'black', '35': 'black'
        }
        
        # Draw segments for each number
        for i, num in enumerate(wheel_numbers):
            # Get frequency (0 if not in results)
            freq = normalized_freq.get(num, 0)
            
            # Determine color based on roulette wheel
            base_color = colors.get(num, 'gray')
            
            # Create a color with alpha based on frequency
            # High frequency numbers will be more opaque
            segment_color = base_color
            
            # Plot the segment
            ax.bar(
                theta[i], 
                1, 
                width=width, 
                bottom=0.6,  # Inner radius
                alpha=0.3 + 0.7 * freq,  # Vary opacity based on frequency
                color=segment_color,
                edgecolor='white',
                linewidth=2
            )
            
            # Add the number text
            ax.text(
                theta[i], 
                1.05,  # Radius for text
                num,
                horizontalalignment='center',
                verticalalignment='center',
                fontsize=12,
                fontweight='bold',
                color=base_color
            )
        
        # Add title and remove radial ticks/labels
        ax.set_title('Roulette Number Heatmap - Analysis Frequency', fontsize=16)
        ax.set_yticklabels([])
        ax.set_xticklabels([])
        
        # Add a color bar to indicate frequency
        sm = plt.cm.ScalarMappable(
            cmap=plt.cm.Reds,
            norm=plt.Normalize(0, max_freq)
        )
        sm.set_array([])
        cbar = plt.colorbar(sm, ax=ax, shrink=0.7)
        cbar.set_label('Frequency in Analysis Results', fontsize=12)
        
        # Save plot
        plt.savefig(f"{target_directory}/roulette_heatmap.png", dpi=300, bbox_inches='tight')
        plt.close()
        
        print(f"Roulette heatmap saved: {target_directory}/roulette_heatmap.png")
        return True
        
    except Exception as e:
        print(f"Error generating roulette heatmap: {e}")
        return False 
    except Exception as e:
        print(f"Error generating roulette heatmap: {e}")
        return False 