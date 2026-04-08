import numpy as np
import matplotlib.pyplot as plt

class HodgkinHuxley:
    """
    Biophysical Hodgkin-Huxley Model (1952)
    Simulates the membrane potential using Sodium, Potassium, and Leak channel kinetics.
    """
    def __init__(self):
        # Biophysical Parameters (Modern Convention: V_rest ~ -65 mV)
        self.C_m  = 1.0      # Membrane capacitance (uF/cm^2)
        self.g_Na = 120.0    # Sodium max conductance (mS/cm^2)
        self.g_K  = 36.0     # Potassium max conductance (mS/cm^2)
        self.g_L  = 0.3      # Leak max conductance (mS/cm^2)
        self.E_Na = 50.0     # Sodium reversal potential (mV)
        self.E_K  = -77.0    # Potassium reversal potential (mV)
        self.E_L  = -54.387  # Leak reversal potential (mV)

    def vtrap(self, x, y):
        """Safe division to avoid 'divide by zero' in transition rates."""
        if abs(x/y) < 1e-6:
            return y * (1 - x/y/2)
        return x / (np.exp(x/y) - 1)

    def simulate(self, I_amp, T, dt):
        """Runs the simulation and returns time, voltage, and gating variables."""
        t = np.arange(0, T, dt)
        V = np.zeros_like(t)
        m = np.zeros_like(t)
        h = np.zeros_like(t)
        n = np.zeros_like(t)
        
        # Initial Conditions (Resting State)
        V[0] = -65.0
        m[0], h[0], n[0] = 0.052, 0.596, 0.317

        for i in range(1, len(t)):
            # Apply step current between 10% and 90% of simulation time
            I = I_amp if (0.1*T <= t[i] <= 0.9*T) else 0.0
            
            Vm = V[i-1]
            
            # Transition rates
            a_m = 0.1 * self.vtrap(-(Vm + 40), 10)
            b_m = 4.0 * np.exp(-(Vm + 65) / 18)
            a_h = 0.07 * np.exp(-(Vm + 65) / 20)
            b_h = 1.0 / (1 + np.exp(-(Vm + 35) / 10))
            a_n = 0.01 * self.vtrap(-(Vm + 55), 10)
            b_n = 0.125 * np.exp(-(Vm + 65) / 80)
            
            # Euler Integration for gating variables
            m[i] = m[i-1] + dt * (a_m*(1-m[i-1]) - b_m*m[i-1])
            h[i] = h[i-1] + dt * (a_h*(1-h[i-1]) - b_h*h[i-1])
            n[i] = n[i-1] + dt * (a_n*(1-n[i-1]) - b_n*n[i-1])

            # Calculate ionic currents and update voltage
            I_ion = self.g_Na*(m[i]**3)*h[i]*(Vm - self.E_Na) + \
                    self.g_K*(n[i]**4)*(Vm - self.E_K) + \
                    self.g_L*(Vm - self.E_L)
            
            V[i] = V[i-1] + dt * (I - I_ion) / self.C_m
            
        return t, V, m, h, n

if __name__ == "__main__":
    print("Running Hodgkin-Huxley Standalone Simulation...")
    model = HodgkinHuxley()
    t, V, m, h, n = model.simulate(I_amp=10.0, T=100.0, dt=0.01)

    plt.figure(figsize=(10, 6))
    plt.plot(t, m, label='m (Na activation)', color='red')
    plt.plot(t, h, label='h (Na inactivation)', color='green')
    plt.plot(t, n, label='n (K activation)', color='blue')
    plt.title('Hodgkin-Huxley Gating Dynamics')
    plt.xlabel('Time (ms)')
    plt.ylabel('Gating Probability')
    plt.legend()
    plt.grid(True, alpha=0.3)
    
    # Save the plot
    plt.savefig('../images/image_1151a3.png', bbox_inches='tight')
    print("Plot saved to images folder.")
    plt.show()