import numpy as np
from live_plot import LivePlotter as lp

G = .01 # Gravitational constant, set to 1 for normalized units

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

    acc = compute_forces(positions, masses) / masses[:, None]

    plotter = lp(positions, velocities, masses) if live else None

    for step in range(steps):
        history.append({
            "t": step * dt,
            "particles": [
                {
                    "id": i,
                    "position": positions[i].copy().tolist(),
                    "velocity": velocities[i].copy().tolist(),
                    "mass": float(masses[i])
                }
                for i in range(n)
            ]
        })

        # Velocity Verlet integration
        positions += velocities * dt + 0.5 * acc * dt**2
        new_acc = compute_forces(positions, masses) / masses[:, None]
        velocities += 0.5 * (acc + new_acc) * dt
        acc = new_acc

        if live:
            plotter.update(positions, velocities)

    if live:
        plotter.close()

    return history