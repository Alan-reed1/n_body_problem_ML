import random
import numpy as np

# Initialize empty lists
positions = []
velocities = []
masses = []

def velocity(k):
    for i in range(k):
        velocities.append([round(random.uniform(0, 10), 3), round(random.uniform(0, 10), 3)])

def position(k):
    for i in range(k):
        positions.append([round(random.uniform(0, 10), 3), round(random.uniform(0, 10), 3)])

def mass(k):
    for i in range(k):
        masses.append([round(random.uniform(0, 10), 3)])

def generate_sim_batch(body_num=0):
    velocity(body_num)
    position(body_num)
    mass(body_num)

# Example: generate data for 5 bodies
generate_sim_batch(body_num=5)

# Convert to NumPy arrays
positions = np.array(positions)
velocities = np.array(velocities)
masses = np.array(masses)

# Print the results
print("Positions:\n", positions)
print("Velocities:\n", velocities)
print("Masses:\n", masses)
