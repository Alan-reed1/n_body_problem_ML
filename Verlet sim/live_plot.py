import matplotlib.pyplot as plt

class LivePlotter:
    def __init__(self, positions, velocities, masses):
        self.n = len(masses)
        self.masses = masses

        # Setup figure
        self.fig, self.ax = plt.subplots()
        self.scat = self.ax.scatter(positions[:, 0], positions[:, 1], s=masses * 10, label="Bodies")
        self.quiv = self.ax.quiver(
            positions[:, 0], positions[:, 1], velocities[:, 0], velocities[:, 1],
            color='black', scale=100, width=0.002
        )
        self.mass_labels = [
            self.ax.text(positions[i, 0] + 0.2, positions[i, 1] + 0.2, f"m={masses[i]:.2f}", fontsize=8)
            for i in range(self.n)
        ]

        self.ax.set_xlim(0, 15)
        self.ax.set_ylim(0, 15)
        self.ax.set_title("Live n-body Simulation")
        self.ax.set_xlabel("X Position")
        self.ax.set_ylabel("Y Position")
        self.ax.grid(True)
        plt.ion()
        plt.legend()
        plt.show()

    def update(self, positions, velocities):
        self.scat.set_offsets(positions)
        self.quiv.set_offsets(positions)
        self.quiv.set_UVC(velocities[:, 0], velocities[:, 1])
        for i, label in enumerate(self.mass_labels):
            label.set_position((positions[i, 0] + 0.2, positions[i, 1] + 0.2))
        plt.draw()
        plt.pause(0.001)

    def close(self):
        plt.ioff()
        plt.show()
