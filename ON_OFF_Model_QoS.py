import numpy as np
import matplotlib.pyplot as plt

def simulate_queue(arrival_rate, service_rate, sim_time, t_on, t_off, lifetime, zeta, K):
    num_arrivals = np.random.poisson(arrival_rate * sim_time)
    arrival_times = np.random.exponential(1/arrival_rate, num_arrivals)
    service_times = np.random.exponential(service_rate, num_arrivals)
    queue = []
    response_times = []
    server_on = True
    server_switch_time = 0
    time = 0

    for i in range(len(arrival_times)):
        time += arrival_times[i]
        if server_on:
            if len(queue) < K * zeta:
                if queue:
                    service_start = max(queue[-1], time)
                else:
                    service_start = time

                service_end = service_start + service_times[i]

                if service_end - time <= lifetime:
                    queue.append(service_end)
                    response_times.append(service_end - time)
            
            if server_switch_time <= time:
                server_on = False
                server_switch_time = time + np.random.exponential(t_off)
        else:
            if server_switch_time <= time:
                server_on = True
                server_switch_time = time + np.random.exponential(t_on)

    return np.mean(response_times)



# Simulation parameters
D = 0.125
TON_TOFF_value = 20
arrival_rates = np.linspace(0.05, 3.9, 50)
experiments = [
    {"zeta": 1, "lifetime": np.inf, "K": np.inf},
    {"zeta": 1, "lifetime": 30, "K": np.inf},
    {"zeta": 0.75, "lifetime": np.inf, "K": np.inf},
    {"zeta": 1, "lifetime": np.inf, "K": 100},
]

# Simulation
for idx, exp in enumerate(experiments, 1):
    response_times = [simulate_queue(
        arrival_rate, D, 1000, TON_TOFF_value, TON_TOFF_value, exp["lifetime"], exp["zeta"], exp["K"]
    ) for arrival_rate in arrival_rates]
    
    plt.plot(arrival_rates, response_times, label=f'Experiment {idx}')

plt.xlabel('Arrival Rate (lambda)')
plt.ylabel('Response Time (seconds)')
plt.title('Response time for various ON/OFF model parameters')
plt.legend()
plt.grid()
plt.show()
