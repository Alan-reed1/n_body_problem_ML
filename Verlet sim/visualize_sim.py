import matplotlib.pyplot as plt

# shove the sim into matplot, so I can see what is going on.
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