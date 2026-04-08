import time
import matplotlib.pyplot as plt
from hh_simulation import HodgkinHuxley
from iz_simulation import Izhikevich

def run_comparison():
    # Experimental Parameters
    T  = 100.0     # Total simulation time (ms)
    dt = 0.01      # Time step (ms)
    I_input = 10.0 # Stimulus amplitude (uA/cm^2)
    
    print("Initializing Neural Simulation Benchmark...")
    print(f"Parameters: Duration={T}ms, Step={dt}ms, Current={I_input}uA\n")

    # Initialize Models
    hh_model = HodgkinHuxley()
    iz_model = Izhikevich()

    # --- Benchmark Hodgkin-Huxley ---
    start_hh = time.perf_counter()
    t_hh, v_hh, _, _, _ = hh_model.simulate(I_input, T, dt)
    hh_duration = time.perf_counter() - start_hh
    print(f"[HH Model] Execution Time: {hh_duration:.5f} seconds")

    # --- Benchmark Izhikevich ---
    start_iz = time.perf_counter()
    t_iz, v_iz = iz_model.simulate(I_input, T, dt)
    iz_duration = time.perf_counter() - start_iz
    print(f"[IZ Model] Execution Time: {iz_duration:.5f} seconds")
    
    # Calculate Metrics
    speedup = hh_duration / iz_duration if iz_duration > 0 else 0
    print(f"\n---> RESULT: Izhikevich is ~{speedup:.1f}x faster\n")

    # --- Generate Comparative Plot ---
    plt.figure(figsize=(14, 8))
    
    # Subplot 1: HH
    plt.subplot(2, 1, 1)
    plt.title(f"Hodgkin-Huxley Model (Biophysically Realistic)\nExecution Time: {hh_duration:.4f}s", fontsize=14)
    plt.plot(t_hh, v_hh, color='blue', lw=1.5)
    plt.ylabel("Voltage (mV)", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.axhline(-65, color='red', linestyle='--', alpha=0.5, label='Resting Potential')
    plt.legend(loc='upper right')

    # Subplot 2: Izhikevich
    plt.subplot(2, 1, 2)
    plt.title(f"Izhikevich Model (Computationally Efficient)\nExecution Time: {iz_duration:.4f}s", fontsize=14)
    plt.plot(t_iz, v_iz, color='green', lw=1.5)
    plt.ylabel("Voltage (mV)", fontsize=12)
    plt.xlabel("Time (ms)", fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.axhline(-65, color='red', linestyle='--', alpha=0.5, label='Resting Potential')

    plt.tight_layout()
    
    # Save the output
    try:
        plt.savefig('../images/comparative_spike_plot.png', dpi=300, bbox_inches='tight')
        print("Success: comparative_spike_plot.png saved to 'images' directory.")
    except FileNotFoundError:
        print("Note: 'images' directory not found. Please create it to save the plots automatically.")
    
    plt.show()

if __name__ == "__main__":
    run_comparison()