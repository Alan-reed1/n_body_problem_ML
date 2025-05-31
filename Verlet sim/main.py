import numpy as np
import json
import body_initialization as bi
import visualize_sim as vs
import verlet as verlet

def is_stable():
    pass

# initialize the starting params for the bodies
positions = []
velocities = []
masses = []

# Convert to NumPy arrays
positions = np.array(positions)
velocities = np.array(velocities)
masses = np.array(masses)

# after the simulation has run, save the history of the sim for n steps to a json dump file
def save_simulation_to_json(history, filename="nbody_sim.json"):
    with open(filename, "w") as f:
        json.dump(history, f, indent=2)

# Simulation options
dt = 0.01
steps = 20000
live = False
bodies = 2

# initialize bodies
bi.generate_sim_batch(velocities, positions, masses, bodies)





# Run the sim
data = verlet.velocity_verlet(positions, velocities, masses, dt, steps, live=live)

save_simulation_to_json(data)

# optional: visualize the simulation
vs.visualize_simulation(data)




