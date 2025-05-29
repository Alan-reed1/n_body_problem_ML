import random
import numpy as np
import matplotlib.pyplot as plt
import json
from live_plot import LivePlotter as lp

G = 1.0  # Gravitational constant, set to 1 for normalized units

def compute_forces(positions, masses):
    n = len(masses)
    forces = np.zeros_like(positions)
    for i in range(n):
        for j in range(i + 1, n):
            r_vec = positions[j] - positions[i]
            r_mag = np.linalg.norm(r_vec) + 1e-5  # softening factor to avoid div-by-zero
            force_mag = G * masses[i] * masses[j] / r_mag**2
            force_dir = r_vec / r_mag
            force = force_mag * force_dir
            forces[i] += force
            forces[j] -= force  # Newton's 3rd law
    return forces

def velocity_verlet(positions, velocities, masses, dt, steps, live=False):
    n = len(masses)
    history = []

    pos = positions.copy()
    vel = velocities.copy()
    acc = compute_forces(pos, masses) / masses[:, None]

    plotter = lp(pos, vel, masses) if live else None

    for step in range(steps):
        history.append({
            "t": step * dt,
            "particles": [
                {
                    "id": i,
                    "position": pos[i].copy().tolist(),
                    "velocity": vel[i].copy().tolist(),
                    "mass": float(masses[i])
                }
                for i in range(n)
            ]
        })

        # Velocity Verlet integration
        pos += vel * dt + 0.5 * acc * dt**2
        new_acc = compute_forces(pos, masses) / masses[:, None]
        vel += 0.5 * (acc + new_acc) * dt
        acc = new_acc

        if live:
            plotter.update(pos, vel)

    if live:
        plotter.close()

    return history

# shove the sim into matplot so I can see what is going on.
def visualize_simulation(history):
    n = len(history[0]["particles"])
    colors = ['r', 'g', 'b', 'm', 'c', 'y']
    for i in range(n):
        xs = [step["particles"][i]["position"][0] for step in history]
        ys = [step["particles"][i]["position"][1] for step in history]
        plt.plot(xs, ys, color=colors[i % len(colors)], label=f"Body {i}")

    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title("n-Body Simulation Trajectories")
    plt.legend()
    plt.axis("equal")
    plt.grid(True)
    plt.show()

# initialize the starting params for the bodies
positions = []
velocities = []
masses = []

# after the simulation has run, save the history of the sim for n steps to a json dump file
def save_simulation_to_json(history, filename="nbody_sim.json"):
    with open(filename, "w") as f:
        json.dump(history, f, indent=2)

# create a list of k (v_x, v_y) veolcity coordinates
def gen_velocities(k):
    for i in range(k):
        velocities.append([round(random.uniform(.01, 1), 3), round(random.uniform(0, 10), 3)])

# create a list of k (x, y) position coordinates
def gen_positionions(k):
    for i in range(k):
        positions.append([round(random.uniform(0, 10), 3), round(random.uniform(0, 10), 3)])

# create a list of k masses
def gen_masses(k):
    for i in range(k):
        masses.append(round(random.randint(1, 10), 3))

# create a collection of bodies that have mass, position and velocity
def generate_sim_batch(body_num=0):
    gen_velocities(body_num)
    gen_positionions(body_num)
    gen_masses(body_num)



generate_sim_batch(body_num=2)


# Convert to NumPy arrays
positions = np.array(positions)
velocities = np.array(velocities)
masses = np.array(masses)

# Simulate
dt = 0.01
steps = 20000
data = velocity_verlet(positions, velocities, masses, dt, steps, live=False)

save_simulation_to_json(data)
# visualize_simulation(data)


