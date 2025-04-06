import matplotlib.pyplot as plt
from sklearn.neighbors import KNeighborsRegressor
import numpy as np

# Function to calculate total head movement in FCFS
def fcfs(requests, head):
    total_movement = 0
    head_position = head
    sequence = [head]

    for request in requests:
        total_movement += abs(request - head_position)
        head_position = request
        sequence.append(head_position)

    return total_movement, sequence

# Function to calculate total head movement in SSTF
def sstf(requests, head):
    total_movement = 0
    head_position = head
    sequence = [head]
    requests = requests.copy()

    while requests:
        closest_request = min(requests, key=lambda x: abs(x - head_position))
        total_movement += abs(closest_request - head_position)
        head_position = closest_request
        sequence.append(head_position)
        requests.remove(closest_request)

    return total_movement, sequence

# Scan algorithm
def scan(requests, head, disk_size=200):
    total_movement = 0
    head_position = head
    sequence = [head]
    requests.sort()

    left = [r for r in requests if r < head_position]
    right = [r for r in requests if r >= head_position]
    for r in reversed(left):
        total_movement += abs(head_position - r)
        head_position = r
        sequence.append(head_position)
    for r in right:
        total_movement += abs(head_position - r)
        head_position = r
        sequence.append(head_position)

    return total_movement, sequence

# Circular Scan (C-SCAN) algorithm
def cscan(requests, head, disk_size=200):
    total_movement = 0
    head_position = head
    sequence = [head]
    requests.sort()

    left = [r for r in requests if r < head_position]
    right = [r for r in requests if r >= head_position]

    for r in right:
        total_movement += abs(head_position - r)
        head_position = r
        sequence.append(head_position)

    if left:
        total_movement += abs(disk_size - head_position)
        head_position = 0
        sequence.append(head_position)

        for r in left:
            total_movement += abs(head_position - r)
            head_position = r
            sequence.append(head_position)

    return total_movement, sequence

# LOOK algorithm
def look(requests, head):
    total_movement = 0
    head_position = head
    sequence = [head]
    requests.sort()

    left = [r for r in requests if r < head_position]
    right = [r for r in requests if r >= head_position]

    for r in reversed(left):
        total_movement += abs(head_position - r)
        head_position = r
        sequence.append(head_position)
    for r in right:
        total_movement += abs(head_position - r)
        head_position = r
        sequence.append(head_position)

    return total_movement, sequence

# C-LOOK algorithm
def clook(requests, head):
    total_movement = 0
    head_position = head
    sequence = [head]
    requests.sort()

    left = [r for r in requests if r < head_position]
    right = [r for r in requests if r >= head_position]

    for r in right:
        total_movement += abs(head_position - r)
        head_position = r
        sequence.append(head_position)

    if left:
        head_position = left[-1]
        for r in reversed(left):
            total_movement += abs(head_position - r)
            head_position = r
            sequence.append(head_position)

    return total_movement, sequence

# KNN-based prediction function
def predict_next_request(requests, head, k=3):
    """
    Predict the next request based on historical requests using KNN.
    """
    historical_requests = np.array([
        [10, 20], [20, 40], [30, 10], [50, 60],
        [60, 40], [70, 30], [80, 90], [90, 100],
        [53, 65], [65, 67], [67, 124]
    ])

    X_train = historical_requests[:, 0].reshape(-1, 1)  # Head positions
    y_train = historical_requests[:, 1]                 # Next requests

    knn = KNeighborsRegressor(n_neighbors=k)
    knn.fit(X_train, y_train)

    next_request = knn.predict([[head]])
    return int(next_request[0])

# Plotting function
def plot_head_movement(sequence, algorithm_name):
    plt.figure(figsize=(10, 5))
    plt.plot(sequence, marker='o', linestyle='-', color='b')
    plt.title(f'Head Movement - {algorithm_name}')
    plt.xlabel('Step')
    plt.ylabel('Head Position')
    plt.grid(True)
    plt.show()

# Main function to run each algorithm and plot
if __name__ == '__main__':
    queue = [98, 183, 37, 122, 14, 124, 65, 67]
    head_start = 53
    disk_size = 200

    # FCFS with prediction
    total_movement, sequence = fcfs(queue + [predict_next_request(queue, head_start)], head_start)
    print(f"FCFS with Prediction Total Head Movement: {total_movement}")
    plot_head_movement(sequence, "FCFS with Prediction")

    # SSTF with prediction
    total_movement, sequence = sstf(queue + [predict_next_request(queue, head_start)], head_start)
    print(f"SSTF with Prediction Total Head Movement: {total_movement}")
    plot_head_movement(sequence, "SSTF with Prediction")

    # SCAN with prediction
    total_movement, sequence = scan(queue + [predict_next_request(queue, head_start)], head_start, disk_size)
    print(f"SCAN with Prediction Total Head Movement: {total_movement}")
    plot_head_movement(sequence, "SCAN with Prediction")

    # C-SCAN with prediction
    total_movement, sequence = cscan(queue + [predict_next_request(queue, head_start)], head_start, disk_size)
    print(f"C-SCAN with Prediction Total Head Movement: {total_movement}")
    plot_head_movement(sequence, "C-SCAN with Prediction")

    # LOOK with prediction
    total_movement, sequence = look(queue + [predict_next_request(queue, head_start)], head_start)
    print(f"LOOK with Prediction Total Head Movement: {total_movement}")
    plot_head_movement(sequence, "LOOK with Prediction")

    # C-LOOK with prediction
    total_movement, sequence = clook(queue + [predict_next_request(queue, head_start)], head_start)
    print(f"C-LOOK with Prediction Total Head Movement: {total_movement}")
    plot_head_movement(sequence, "C-LOOK with Prediction")