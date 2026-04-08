import numpy as np
import matplotlib.pyplot as plt

class Izhikevich:
    """
    Phenomenological Izhikevich Model (2003)
    Simulates spiking behavior using a highly efficient 2D system with a reset mechanism.
    """
    def __init__(self, a=0.02, b=0.2, c=-65.0, d=8.0):
        # Default parameters set for Regular Spiking (RS) neuron
        self.a = a
        self.b = b
        self.c = c
        self.d = d

    def simulate(self, I_amp, T, dt):
        """Runs the simulation and returns time and voltage arrays."""
        t = np.arange(0, T, dt)
        V = np.zeros_like(t)
        u = np.zeros_like(t)
        
        # Initial Conditions
        V[0] = -65.0
        u[0] = self.b * V[0]

        for i in range(1, len(t)):
            # Apply step current between 10% and 90% of simulation time
            I = I_amp if (0.1*T <= t[i] <= 0.9*T) else 0.0
            
            v_curr = V[i-1]
            u_curr = u[i-1]
            
            # Euler Integration for continuous dynamics
            v_next = v_curr + dt * (0.04*v_curr**2 + 5*v_curr + 140 - u_curr + I)
            u_next = u_curr + dt * (self.a * (self.b*v_curr - u_curr))
            
            # Discrete Reset Mechanism (The Spike)
            if v_next >= 30.0:
                V[i] = 30.0      # Cap the spike for visualization
                V[i-1] = 30.0    # Ensure sharp peak
                V[i] = self.c    # Reset voltage
                u[i] = u_next + self.d # Reset recovery
            else:
                V[i] = v_next
                u[i] = u_next
                
        return t, V

if __name__ == "__main__":
    print("Running Izhikevich Standalone Simulation...")
    model = Izhikevich()
    t, V = model.simulate(I_amp=10.0, T=100.0, dt=0.01)

    plt.figure(figsize=(10, 4))
    plt.plot(t, V, color='green')
    plt.title('Izhikevich Spiking Dynamics')
    plt.xlabel('Time (ms)')
    plt.ylabel('Voltage (mV)')
    plt.grid(True, alpha=0.3)
    plt.show()