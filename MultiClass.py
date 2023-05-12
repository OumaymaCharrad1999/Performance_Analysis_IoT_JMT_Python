import numpy as np
import matplotlib.pyplot as plt
import random

def calculate_service_time(service_rate):
    return np.random.exponential(1/service_rate)



def calculate_response_time(queue, service_time):
    if not queue:
        return service_time
    else:
        return max(queue[-1], service_time)



def choose_class(classes):
    arrival_rates = [cls["arrival_rate"] for cls in classes]
    return np.random.choice(len(classes), p=arrival_rates/np.sum(arrival_rates))



def simulate_priority_queue(classes, sim_time):
    response_times = [0] * len(classes)
    queue = [[] for _ in classes]

    for _ in range(sim_time):
        class_idx = choose_class(classes)
        service_time = calculate_service_time(classes[class_idx]["service_rate"])
        response_time = calculate_response_time(queue[class_idx], service_time)
        queue[class_idx].append(response_time)
        response_times[class_idx] += response_time

    mean_response_times = [rt / sim_time for rt in response_times]

    return mean_response_times



# Scenario 1: ρ=0.69, 19 classes
classes_1 = [{"arrival_rate": random.uniform(0.01, 0.1), "service_rate": random.uniform(0.05, 0.5)} for _ in range(19)]
mean_response_times_1 = simulate_priority_queue(classes_1, 1000)

# Scenario 2: ρ=0.89, 9 classes
classes_2 = [{"arrival_rate": random.uniform(0.01, 0.1), "service_rate": random.uniform(0.05, 0.5)} for _ in range(9)]
mean_response_times_2 = simulate_priority_queue(classes_2, 1000)


plt.plot(range(1, len(classes_1) + 1), mean_response_times_1, 'o-', label='Scenario 1: ρ=0.69, 19 classes')
plt.plot(range(1, len(classes_2) + 1), mean_response_times_2, 'x-', label='Scenario 2: ρ=0.89, 9 classes')

plt.xlabel('Classes')
plt.ylabel('Response Time (seconds)')
plt.title('Response time for various classes of messages assigned with different priority parameters')
plt.legend()
plt.grid()
plt.show()
