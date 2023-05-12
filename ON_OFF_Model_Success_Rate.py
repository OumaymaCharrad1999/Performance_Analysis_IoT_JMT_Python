import numpy as np
import matplotlib.pyplot as plt

# Define a function to calculate the success rate
def calc_success_rate(arrival_rate, service_rate, sim_time, ton, toff, lifetime, zeta, K):
    num_arrivals = np.random.poisson(arrival_rate * sim_time)    
    arrival_times = np.random.exponential(1/arrival_rate, num_arrivals)
    service_times = np.random.exponential(service_rate, num_arrivals)
    queue = []
    successful = 0
    total = 0
    server_on = True
    server_switch_time = 0
    t = 0

    for i in range(len(arrival_times)):
        t += arrival_times[i]
        total += 1
        
        while server_switch_time < t:
            if server_on:
                server_switch_time += np.random.exponential(ton)
            else:
                server_switch_time += np.random.exponential(toff)
            server_on = not server_on
        
        if server_on:
            if queue:
                service_start = max(queue[-1], t)
            else:
                service_start = t
            
            service_end = service_start + service_times[i]
            
            if K != np.inf:
                queue = [t for t in queue if t >= (t - K/zeta)]
            
            if lifetime != np.inf and (service_end - t) > lifetime:
                continue
            
            if len(queue) < K * zeta:
                queue.append(service_end)
                successful += 1

    return successful / total



# Simulation parameters
D = 0.125
TON_TOFF = 20
arrival_rates = np.linspace(0.05, 3.9, 50)
experiments = [
    {"zeta": 1, "lifetime": np.inf, "K": np.inf},
    {"zeta": 1, "lifetime": 30, "K": np.inf},
    {"zeta": 0.75, "lifetime": np.inf, "K": np.inf},
    {"zeta": 1, "lifetime": np.inf, "K": 100},
]

# Simulation
for idx, exp in enumerate(experiments, 1):
    success_rates = []
    for rate in arrival_rates:
        rate_success = calc_success_rate(rate, D, 1000, TON_TOFF, TON_TOFF, exp["lifetime"], exp["zeta"], exp["K"])
        success_rates.append(rate_success)
    
    plt.plot(arrival_rates, success_rates, label=f'Experiment {idx}')

plt.xlabel('Arrival Rate (lambda)')
plt.ylabel('Success Rate')
plt.title('Success rates for various ON/OFF model parameters')
plt.legend()
plt.grid()
plt.show()
