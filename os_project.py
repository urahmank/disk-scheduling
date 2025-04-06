import matplotlib.pyplot as plt

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
    requests = requests.copy()  # Copy the list to avoid modifying the original

    while requests:
        # Find the closest request to the current head position
        closest_request = min(requests, key=lambda x: abs(x - head_position))
        total_movement += abs(closest_request - head_position)
        head_position = closest_request
        sequence.append(head_position)
        requests.remove(closest_request)

    return total_movement, sequence

# Function to calculate total head movement in SCAN (Elevator Algorithm)
def scan(requests, head, disk_size):
    total_movement = 0
    head_position = head
    sequence = [head]
    requests = sorted(requests)

    # Split the requests into two parts: those less than the head and those greater than the head
    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    # First service requests to the right, then reverse to the left
    for request in right:
        total_movement += abs(request - head_position)
        head_position = request
        sequence.append(head_position)

    if head_position != disk_size - 1:
        # Go to the end of the disk
        total_movement += abs((disk_size - 1) - head_position)
        sequence.append(disk_size - 1)
        head_position = disk_size - 1

    for request in reversed(left):
        total_movement += abs(request - head_position)
        head_position = request
        sequence.append(head_position)

    return total_movement, sequence

# Function to calculate total head movement in C-SCAN
def c_scan(requests, head, disk_size):
    total_movement = 0
    head_position = head
    sequence = [head]
    requests = sorted(requests)

    right = [r for r in requests if r >= head]
    left = [r for r in requests if r < head]

    # First service requests to the right, then jump to the beginning and service the left
    for request in right:
        total_movement += abs(request - head_position)
        head_position = request
        sequence.append(head_position)

    if head_position != disk_size - 1:
        # Go to the end of the disk
        total_movement += abs((disk_size - 1) - head_position)
        head_position = disk_size - 1
        sequence.append(disk_size - 1)

    # Jump back to the beginning
    total_movement += disk_size - 1
    sequence.append(0)
    head_position = 0

    for request in left:
        total_movement += abs(request - head_position)
        head_position = request
        sequence.append(head_position)

    return total_movement, sequence

# Function to calculate total head movement in LOOK
def look(requests, head):
    total_movement = 0
    head_position = head
    sequence = [head]
    requests = sorted(requests)

    left = [r for r in requests if r < head]
    right = [r for r in requests if r >= head]

    # First service requests to the right, then reverse to the left
    for request in right:
        total_movement += abs(request - head_position)
        head_position = request
        sequence.append(head_position)

    for request in reversed(left):
        total_movement += abs(request - head_position)
        head_position = request
        sequence.append(head_position)

    return total_movement, sequence

# Function to calculate total head movement in C-LOOK
def c_look(requests, head):
    total_movement = 0
    head_position = head
    sequence = [head]
    requests = sorted(requests)

    right = [r for r in requests if r >= head]
    left = [r for r in requests if r < head]

    # First service requests to the right, then jump to the smallest request
    for request in right:
        total_movement += abs(request - head_position)
        head_position = request
        sequence.append(head_position)

    # Jump back to the smallest request
    if left:
        total_movement += abs(head_position - left[0])
        head_position = left[0]
        sequence.append(head_position)

    for request in left:
        total_movement += abs(request - head_position)
        head_position = request
        sequence.append(head_position)

    return total_movement, sequence

# Function to plot the head movements
def plot_movements(algorithm_name, sequence):
    plt.figure()
    plt.plot(sequence, marker='o')
    plt.title(f'{algorithm_name} Disk Scheduling')
    plt.xlabel('Sequence of Requests')
    plt.ylabel('Cylinder Number')
    plt.grid(True)
    plt.show()

# Example usage
requests = [98, 183, 37, 122, 14, 124, 65, 67]
head = 53
disk_size = 200  # Assume disk size is 200 cylinders

# Run each algorithm and display results
algorithms = {
    "FCFS": fcfs,
    "SSTF": sstf,
    "SCAN": scan,
    "C-SCAN": c_scan,
    "LOOK": look,
    "C-LOOK": c_look
}

for name, algorithm in algorithms.items():
    if name in ["SCAN", "C-SCAN"]:
        total_movement, sequence = algorithm(requests, head, disk_size)
    else:
        total_movement, sequence = algorithm(requests, head)

    print(f"{name}: Total Head Movement = {total_movement}")
    plot_movements(name, sequence)