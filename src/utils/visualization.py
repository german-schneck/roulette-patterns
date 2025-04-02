#!/usr/bin/env python3
"""
Visualization utilities for roulette analysis methodologies.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def plot_methodology_performance(final_combinations, target_directory="output/graphs"):
    """
    Generate a comparative bar chart of all methodology win rates.
    
    Args:
        final_combinations: List of dictionaries with methodology data
        target_directory: Directory to save the plot
        
    Returns:
        bool: True if plotting was successful
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(target_directory, exist_ok=True)
        
        # Extract data for plotting
        methodologies = [combo["name"] for combo in final_combinations]
        win_rates = [combo["rate"] for combo in final_combinations]
        
        # Sort by win rate descending
        sorted_indices = np.argsort(win_rates)[::-1]
        methodologies = [methodologies[i] for i in sorted_indices]
        win_rates = [win_rates[i] for i in sorted_indices]
        
        # Create plot
        plt.figure(figsize=(12, 8))
        bars = plt.bar(methodologies, win_rates, color='steelblue')
        
        # Add data labels on top of bars
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height + 0.1,
                    f'{height:.2f}%', ha='center', va='bottom')
        
        # Set title and labels
        plt.title("Comparativa de Rendimiento por Metodología", fontsize=15)
        plt.xlabel("Metodología")
        plt.ylabel("Tasa de Victoria (%)")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        
        # Add horizontal line for baseline (expected rate with random selection)
        avg_coverage = sum(len(combo["numbers"]) for combo in final_combinations) / len(final_combinations)
        baseline = avg_coverage / 38 * 100
        plt.axhline(y=baseline, color='r', linestyle='--', label=f'Línea Base ({baseline:.2f}%)')
        plt.legend()
        
        # Save plot
        plt.savefig(f"{target_directory}/methodology_comparison.png", dpi=300)
        plt.close()
        
        print(f"Gráfica de comparación guardada: {target_directory}/methodology_comparison.png")
        return True
        
    except Exception as e:
        print(f"Error al generar gráfica de metodologías: {e}")
        return False

def plot_methodology_pl_simulation(strategy_returns, output_path):
    """
    Plot a simulation of P&L for different methodologies.
    
    Args:
        strategy_returns: List of tuples with (strategy_name, performance_percentage)
        output_path: Path to save the visualization
    """
    # Create figure and axes
    plt.figure(figsize=(12, 8))
    
    # Sort strategies by performance
    sorted_strategies = sorted(strategy_returns, key=lambda x: x[1], reverse=True)
    
    # Calculate statistics
    strategy_names = [s[0] for s in sorted_strategies]
    performances = [s[1] for s in sorted_strategies]
    
    # Create color map based on performance
    colors = []
    for perf in performances:
        if perf > 5:
            colors.append('green')
        elif perf > 0:
            colors.append('lightgreen')
        elif perf > -10:
            colors.append('orange')
        else:
            colors.append('red')
    
    # Plot horizontal bar chart of performances
    y_pos = np.arange(len(strategy_names))
    plt.barh(y_pos, performances, align='center', color=colors)
    plt.yticks(y_pos, strategy_names)
    
    # Add a vertical line at 0 for reference
    plt.axvline(x=0, color='black', linestyle='-', alpha=0.3)
    
    # Add labels
    plt.xlabel('Performance vs. Random (%)')
    plt.title('Strategy Performance Comparison')
    
    # Add performance values at the end of each bar
    for i, v in enumerate(performances):
        plt.text(v + 0.5, i, f"{v:+.1f}%", va='center')
    
    # Adjust layout and save
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()

def plot_individual_methodology_performance(methodology, analyzer, validation_spins, target_directory="output/graphs", initial_bankroll=1000):
    """
    Generate a detailed analysis plot for a single methodology.
    
    Args:
        methodology: Dictionary with methodology data
        analyzer: AdvancedRouletteAnalyzer instance
        validation_spins: Number of spins to use for validation
        target_directory: Directory to save the plot
        initial_bankroll: Initial bankroll in dollars
        
    Returns:
        bool: True if plotting was successful
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(target_directory, exist_ok=True)
        
        method_name = methodology["name"]
        safe_name = method_name.lower().replace(" ", "_")
        numbers = methodology["numbers"]
        win_rate = methodology["rate"]
        
        # Create a figure with 2x2 subplots
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 14))
        
        # Plot 1: Roulette wheel with selected numbers highlighted
        ax1.set_title(f"Números Seleccionados - {method_name}")
        
        # Create a wheel representation
        wheel_numbers = [str(i) for i in range(37)] + ['00']
        theta = np.linspace(0, 2*np.pi, len(wheel_numbers), endpoint=False)
        
        # Plot wheel as a circle
        circle = plt.Circle((0, 0), 1, fill=False, color='black')
        ax1.add_patch(circle)
        
        # Add numbers around the wheel
        radius = 1.0
        for t, num in zip(theta, wheel_numbers):
            x = radius * np.cos(t)
            y = radius * np.sin(t)
            
            # Highlight selected numbers
            if num in numbers:
                ax1.text(x*1.1, y*1.1, num, ha='center', va='center', fontsize=12, 
                        fontweight='bold', color='red')
                # Add a marker for the selected number
                ax1.plot(x, y, 'ro', markersize=8)
            else:
                ax1.text(x*1.1, y*1.1, num, ha='center', va='center', fontsize=10)
        
        # Set equal aspect ratio
        ax1.set_aspect('equal')
        ax1.set_xlim(-1.5, 1.5)
        ax1.set_ylim(-1.5, 1.5)
        ax1.axis('off')
        
        # Plot 2: Performance metrics
        ax2.set_title(f"Métricas de Rendimiento - {method_name}")
        
        # Metrics to display
        coverage = len(numbers) / 38 * 100
        expected_rate = coverage
        performance = (win_rate / expected_rate - 1) * 100
        edge = 100 - (36 * (win_rate / 100)) / (coverage / 100)
        
        metrics = ['Tasa de Victoria', 'Cobertura', 'Rendimiento', 'Ventaja']
        values = [win_rate, coverage, performance, edge]
        colors = ['green', 'blue', 'purple', 'orange']
        
        # Create horizontal bar chart
        bars = ax2.barh(metrics, values, color=colors, alpha=0.7)
        
        # Add data labels
        for bar, val in zip(bars, values):
            width = bar.get_width()
            label_x_pos = width if width >= 0 else 0
            ax2.text(label_x_pos + 1, bar.get_y() + bar.get_height()/2, f'{val:.2f}%',
                    va='center')
        
        # Add a vertical line at the 0% mark for performance
        ax2.axvline(x=0, color='gray', linestyle='--', alpha=0.7)
        
        # Set x-axis label
        ax2.set_xlabel('Porcentaje (%)')
        
        # Plot 3: Bankroll Simulation
        ax3.set_title(f"Simulación de Bankroll - {method_name}")
        
        # Simulation parameters
        max_spins = 5000
        bet_size = 10
        
        # Run multiple simulations
        num_sims = 5
        sim_results = []
        bankruptcy_spins = []
        
        for sim in range(num_sims):
            balance_curve = []
            balance = initial_bankroll
            win_prob = win_rate / 100
            
            np.random.seed(42 + sim)  # Different seed for each sim
            
            for spin in range(max_spins):
                if balance <= 0:
                    bankruptcy_spins.append(spin)
                    break
                
                current_bet = min(bet_size, balance)
                
                # Simulate the bet
                if np.random.random() < win_prob:  # Win
                    balance += current_bet * (36 / len(numbers) - 1)
                else:  # Loss
                    balance -= current_bet
                
                balance_curve.append(balance)
            
            if balance > 0:  # If didn't go bankrupt
                bankruptcy_spins.append(max_spins)
                
            sim_results.append(balance_curve)
        
        # Plot each simulation
        for i, result in enumerate(sim_results):
            ax3.plot(range(len(result)), result, alpha=0.7, 
                    label=f"Sim {i+1}" if i < 3 else "_nolegend_")
        
        # Add horizontal line at 0 and initial bankroll
        ax3.axhline(y=0, color='r', linestyle='-', alpha=0.3)
        ax3.axhline(y=initial_bankroll, color='g', linestyle='--', alpha=0.3)
        
        # Format y-axis with dollar symbol
        formatter = ticker.FormatStrFormatter('$%1.0f')
        ax3.yaxis.set_major_formatter(formatter)
        
        # Add labels
        ax3.set_xlabel("Número de Apuestas")
        ax3.set_ylabel("Bankroll ($)")
        ax3.grid(True, linestyle='--', alpha=0.7)
        ax3.legend(loc='upper right')
        
        # Plot 4: Bankruptcy Distribution
        ax4.set_title(f"Distribución de Supervivencia - {method_name}")
        
        # Run more simulations for distribution
        more_sims = 50
        more_bankruptcies = bankruptcy_spins.copy()
        
        for sim in range(num_sims, more_sims):
            balance = initial_bankroll
            win_prob = win_rate / 100
            
            np.random.seed(42 + sim)
            
            for spin in range(max_spins):
                if balance <= 0:
                    more_bankruptcies.append(spin)
                    break
                
                current_bet = min(bet_size, balance)
                
                # Simulate the bet
                if np.random.random() < win_prob:  # Win
                    balance += current_bet * (36 / len(numbers) - 1)
                else:  # Loss
                    balance -= current_bet
            
            if balance > 0:  # If didn't go bankrupt
                more_bankruptcies.append(max_spins)
        
        # Create a histogram
        histogram = ax4.hist(more_bankruptcies, bins=20, color='skyblue', edgecolor='black', alpha=0.7)
        
        # Add mean survival line
        mean_survival = np.mean(more_bankruptcies)
        ax4.axvline(x=mean_survival, color='red', linestyle='--')
        ax4.text(mean_survival, max(histogram[0]) * 0.9, 
                f'Media: {mean_survival:.0f} apuestas', 
                rotation=90, ha='right', va='top')
        
        # Add labels
        ax4.set_xlabel("Apuestas hasta bancarrota")
        ax4.set_ylabel("Frecuencia")
        ax4.grid(True, linestyle='--', alpha=0.7)
        
        # Add simulation info
        ax4.text(0.02, 0.97, f"Bankroll inicial: ${initial_bankroll}\nApuesta: ${bet_size}",
                transform=ax4.transAxes, va='top', fontsize=9)
        
        # Adjust layout
        plt.tight_layout()
        
        # Save plot
        plt.savefig(f"{target_directory}/{safe_name}_analysis.png", dpi=300)
        plt.close()
        
        print(f"Análisis para {method_name} guardado: {target_directory}/{safe_name}_analysis.png")
        return True
        
    except Exception as e:
        print(f"Error al generar análisis para {methodology['name']}: {e}")
        return False

def plot_bankroll_survival(final_combinations, target_directory="output/graphs", initial_bankroll=1000):
    """
    Generate a bar chart showing the expected bankroll survival (number of spins until bankruptcy)
    for each methodology.
    
    Args:
        final_combinations: List of dictionaries with methodology data
        target_directory: Directory to save the plot
        initial_bankroll: Initial bankroll in dollars
        
    Returns:
        bool: True if plotting was successful
    """
    try:
        # Create directory if it doesn't exist
        os.makedirs(target_directory, exist_ok=True)
        
        # Simulation parameters
        max_spins = 10000  # Maximum number of spins to simulate
        bet_size = 10  # Base betting unit
        
        # Results tracking
        survival_data = {}
        
        # Calculate baseline (random chance)
        avg_coverage = sum(len(combo["numbers"]) for combo in final_combinations) / len(final_combinations)
        baseline_prob = avg_coverage / 38
        
        # Run multiple simulations for more reliable results
        num_simulations = 10
        
        # Process each methodology
        all_methods = [{"name": "Estrategia Aleatoria", "rate": baseline_prob * 100, "numbers": []}] + final_combinations
        
        for combo in all_methods:
            total_spins = 0
            win_prob = combo["rate"] / 100
            
            for sim in range(num_simulations):
                balance = initial_bankroll
                np.random.seed(42 + sim)  # Different seed for each sim
                
                for spin in range(max_spins):
                    if balance <= 0:
                        total_spins += spin
                        break
                    
                    current_bet = min(bet_size, balance)
                    
                    # Calculate payout for win
                    if combo["name"] == "Estrategia Aleatoria":
                        payout_multiplier = 36 / avg_coverage - 1
                    else:
                        payout_multiplier = 36 / len(combo["numbers"]) - 1
                    
                    # Simulate the bet
                    if np.random.random() < win_prob:  # Win
                        balance += current_bet * payout_multiplier
                    else:  # Loss
                        balance -= current_bet
                
                if balance > 0:  # If didn't go bankrupt in max_spins
                    total_spins += max_spins
            
            # Calculate average survival
            avg_survival = total_spins / num_simulations
            survival_data[combo["name"]] = avg_survival
        
        # Sort by survival duration
        sorted_methods = sorted(survival_data.items(), key=lambda x: x[1], reverse=True)
        method_names = [item[0] for item in sorted_methods]
        survival_values = [item[1] for item in sorted_methods]
        
        # Create figure
        plt.figure(figsize=(14, 8))
        
        # Create colormap based on survival time
        max_survival = max(survival_values)
        colors = [plt.cm.viridis(val / max_survival) for val in survival_values]
        
        # Create the bar chart
        bars = plt.bar(method_names, survival_values, color=colors)
        
        # Add data labels
        for bar, val in zip(bars, survival_values):
            plt.text(bar.get_x() + bar.get_width()/2, val + 5, 
                    f'{val:.0f}', ha='center', va='bottom', fontsize=9)
        
        # Add labels and title
        plt.title(f"Duración Esperada del Bankroll por Metodología (Inicial: ${initial_bankroll})", fontsize=15)
        plt.xlabel("Metodología")
        plt.ylabel("Número de apuestas promedio hasta bancarrota")
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.xticks(rotation=45, ha='right')
        
        # Add bet size information
        plt.figtext(0.02, 0.02, f"Tamaño de apuesta: ${bet_size}", fontsize=9)
        
        plt.tight_layout()
        plt.savefig(f"{target_directory}/bankroll_survival.png", dpi=300)
        plt.close()
        
        print(f"Gráfica de supervivencia del bankroll guardada: {target_directory}/bankroll_survival.png")
        return True
        
    except Exception as e:
        print(f"Error al generar gráfica de supervivencia del bankroll: {e}")
        return False

def plot_strategy_comparison(strategies, output_path):
    """
    Plot a comparison of multiple strategies based on win rate and performance.
    
    Args:
        strategies: List of tuples (strategy_name, win_rate, performance)
        output_path: Path to save the plot
    """
    # Extract data from strategies
    names = [s[0] for s in strategies]
    win_rates = [s[1] for s in strategies]
    performances = [s[2] for s in strategies]
    
    # Set up the figure
    fig, ax1 = plt.subplots(figsize=(12, 8))
    
    # Plot win rates as bars
    x = np.arange(len(names))
    bar_width = 0.35
    
    bars = ax1.bar(x, win_rates, bar_width, label='Tasa de Victoria (%)', color='skyblue')
    
    # Add values on top of bars
    for bar in bars:
        height = bar.get_height()
        ax1.annotate(f'{height:.2f}%',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')
    
    # Create a second y-axis for performance
    ax2 = ax1.twinx()
    line = ax2.plot(x, performances, 'o-', color='red', label='Rendimiento vs Aleatorio (%)')
    
    # Add values next to points
    for i, perf in enumerate(performances):
        ax2.annotate(f'{perf:+.2f}%',
                    xy=(i, perf),
                    xytext=(10, 0),  # 10 points horizontal offset
                    textcoords="offset points",
                    ha='left', va='center')
    
    # Set up the axes
    ax1.set_xlabel('Estrategia', fontsize=12)
    ax1.set_ylabel('Tasa de Victoria (%)', color='blue', fontsize=12)
    ax2.set_ylabel('Rendimiento vs Aleatorio (%)', color='red', fontsize=12)
    
    # Set tick parameters
    ax1.set_xticks(x)
    ax1.set_xticklabels(names, rotation=45, ha='right')
    ax1.tick_params(axis='y', labelcolor='blue')
    ax2.tick_params(axis='y', labelcolor='red')
    
    # Add a reference line at 0% performance
    ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.7)
    
    # Add a random expectation line at 21.05% for win rate (8 numbers out of 38)
    ax1.axhline(y=21.05, color='green', linestyle='--', alpha=0.7, label='Expectativa Aleatoria (21.05%)')
    
    # Add legends
    lines, labels = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines + lines2, labels + labels2, loc='upper left')
    
    # Add a title
    plt.title('Comparación de Estrategias de Ruleta', fontsize=16)
    
    # Adjust layout
    fig.tight_layout()
    
    # Save the figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()

def plot_performance_history(analyzer, output_path):
    """
    Plot the performance history of the analyzer.
    
    Args:
        analyzer: AdvancedRouletteAnalyzer instance
        output_path: Path to save the plot
    """
    # Get recent history
    recent_history = analyzer.get_recent_history(100)
    
    # Count occurrences of each number
    number_counts = {}
    for num in recent_history:
        if num not in number_counts:
            number_counts[num] = 0
        number_counts[num] += 1
    
    # Calculate expected frequency
    expected_freq = len(recent_history) / 38
    
    # Prepare data for plotting
    numbers = sorted(number_counts.keys())
    frequencies = [number_counts.get(num, 0) for num in numbers]
    
    # Calculate deviation from expected
    deviations = [(freq - expected_freq) / expected_freq * 100 for freq in frequencies]
    
    # Create the plot
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))
    
    # Plot frequencies
    bars = ax1.bar(numbers, frequencies, color='skyblue')
    ax1.axhline(y=expected_freq, color='red', linestyle='--', 
               label=f'Esperado ({expected_freq:.2f})')
    
    # Highlight highest and lowest frequency numbers
    max_freq = max(frequencies)
    min_freq = min(frequencies)
    
    for i, bar in enumerate(bars):
        if bar.get_height() == max_freq:
            bar.set_color('green')
        elif bar.get_height() == min_freq:
            bar.set_color('red')
    
    ax1.set_xlabel('Número')
    ax1.set_ylabel('Frecuencia')
    ax1.set_title('Distribución de Resultados Recientes')
    ax1.legend()
    
    # Plot deviation from expected
    bars = ax2.bar(numbers, deviations, color='lightgreen')
    ax2.axhline(y=0, color='black', linestyle='-')
    
    # Color positive and negative bars differently
    for i, bar in enumerate(bars):
        if bar.get_height() < 0:
            bar.set_color('salmon')
    
    ax2.set_xlabel('Número')
    ax2.set_ylabel('Desviación del Esperado (%)')
    ax2.set_title('Desviación de la Distribución Uniforme')
    
    # Adjust layout
    plt.tight_layout()
    
    # Save the figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
    
    return True 