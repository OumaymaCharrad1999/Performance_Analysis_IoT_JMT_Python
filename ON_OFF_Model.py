import numpy as np
import matplotlib.pyplot as plt

def simulate_queue(arrival_rate, service_rate, sim_time, t_on, t_off):
    num_arrivals = np.random.poisson(arrival_rate * sim_time)
    arrival_times = np.cumsum(np.random.exponential(1/arrival_rate, num_arrivals))
    service_times = np.random.exponential(service_rate, num_arrivals)
    queue = []
    response_times = []
    server_on = True
    server_switch_time = 0
    time = 0

    for i in range(num_arrivals):
        time = arrival_times[i]
        
        while server_switch_time < time:
            if server_on:
                server_switch_time += np.random.exponential(t_on)
            else:
                server_switch_time += np.random.exponential(t_off)
            server_on = not server_on
        
        if server_on:
            if queue:
                service_start = max(queue[-1], time)
            else:
                service_start = time
            service_end = service_start + service_times[i]
            queue.append(service_end)
            response_times.append(service_end - time)

    return np.mean(response_times)



def plot_response_times(arrival_rates, t_on_off_values, service_rate, sim_time):
    for t_on_off in TON_TOFF_values:
        response_times = []
        for arrival_rate in arrival_rates:
            response_time = simulate_queue(arrival_rate, service_rate, sim_time, t_on_off, t_on_off)
            response_times.append(response_time)
        plt.plot(arrival_rates, response_times, label=f'TON = TOFF = {t_on_off} seconds')
    plt.xlabel('Arrival Rate (lambda)')
    plt.ylabel('Response Time (seconds)')
    plt.title('Response time for various TON, TOFF parameters')
    plt.legend()
    plt.grid()
    plt.show()



# Simulation parameters
D = 0.125
TON_TOFF_values = [20, 40, 60]
arrival_rates = np.linspace(0.05, 4, 50)

# Simulate response times for various TON and TOFF parameters
plot_response_times(arrival_rates, TON_TOFF_values, D, 1000)

