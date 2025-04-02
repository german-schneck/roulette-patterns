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

def plot_methodology_pl_simulation(final_combinations, target_directory="output/graphs", initial_bankroll=1000):
    """
    Generate a simulation of P/L (Profit/Loss) for each methodology.
    Simulates betting until the bankroll reaches 0 or a maximum number of spins.
    
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
        max_spins = 5000  # Maximum number of spins to simulate
        bet_size = 10  # Base betting unit
        
        # Create figure
        plt.figure(figsize=(14, 8))
        
        # Calculate baseline (random chance)
        avg_coverage = sum(len(combo["numbers"]) for combo in final_combinations) / len(final_combinations)
        baseline_prob = avg_coverage / 38
        
        # Results tracking
        bankruptcies = {}  # Track when each strategy goes bankrupt
        max_duration = 0  # Track the longest lasting strategy
        
        # For comparison, add a random strategy performance line
        random_pl = []
        balance = initial_bankroll
        np.random.seed(42)  # For reproducibility
        spins_count = 0
        
        for spin in range(max_spins):
            if balance <= 0:
                bankruptcies["Estrategia Aleatoria"] = spin
                break
                
            current_bet = min(bet_size, balance)  # Can't bet more than remaining bankroll
            
            # Simulating a bet with random chance
            if np.random.random() < baseline_prob:  # Win
                balance += current_bet * (36 / avg_coverage - 1)  # Payout adjusted for coverage
            else:  # Loss
                balance -= current_bet
                
            random_pl.append(balance)
            spins_count = spin + 1
            
        max_duration = max(max_duration, spins_count)
        
        # Plot random strategy as a reference
        plt.plot(range(spins_count), random_pl, 'k--', label='Estrategia Aleatoria', alpha=0.5)
        
        # Simulate and plot each methodology
        methodology_results = {}
        
        for combo in final_combinations:
            pl_curve = []
            balance = initial_bankroll
            win_prob = combo["rate"] / 100
            
            np.random.seed(42)  # Same seed for fair comparison
            spins_count = 0
            
            for spin in range(max_spins):
                if balance <= 0:
                    bankruptcies[combo["name"]] = spin
                    break
                    
                current_bet = min(bet_size, balance)  # Can't bet more than remaining bankroll
                
                # Simulating a bet with methodology's win probability
                if np.random.random() < win_prob:  # Win
                    balance += current_bet * (36 / len(combo["numbers"]) - 1)  # Payout adjusted for coverage
                else:  # Loss
                    balance -= current_bet
                    
                pl_curve.append(balance)
                spins_count = spin + 1
                
            max_duration = max(max_duration, spins_count)
            methodology_results[combo["name"]] = {
                "curve": pl_curve,
                "duration": spins_count,
                "final_balance": balance
            }
        
        # Plot each methodology curve with adjusted length
        for name, data in methodology_results.items():
            plt.plot(range(data["duration"]), data["curve"], label=f"{name} (${data['final_balance']:.0f})")
        
        # Add bankruptcy marks
        for name, spin in bankruptcies.items():
            plt.axvline(x=spin, color='red', linestyle=':', alpha=0.5)
            plt.text(spin, initial_bankroll * 0.8, f"{name} quebró", 
                    rotation=90, ha='right', va='center', fontsize=8)
        
        # Add labels and title
        plt.title(f"Simulación de Evolución del Bankroll (Inicial: ${initial_bankroll})", fontsize=15)
        plt.xlabel("Número de Apuestas")
        plt.ylabel("Bankroll ($)")
        plt.grid(True, linestyle='--', alpha=0.7)
        
        # Add horizontal line at 0 and initial bankroll
        plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
        plt.axhline(y=initial_bankroll, color='g', linestyle='--', alpha=0.3)
        
        # Format y-axis with dollar symbol
        formatter = ticker.FormatStrFormatter('$%1.0f')
        plt.gca().yaxis.set_major_formatter(formatter)
        
        # Add legend outside of plot
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
        plt.tight_layout()
        
        # Set xlim to show full range
        plt.xlim(0, max_duration)
        
        # Save plot
        plt.savefig(f"{target_directory}/bankroll_simulation.png", dpi=300)
        plt.close()
        
        print(f"Gráfica de simulación de bankroll guardada: {target_directory}/bankroll_simulation.png")
        return True
        
    except Exception as e:
        print(f"Error al generar gráfica de simulación de bankroll: {e}")
        return False

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