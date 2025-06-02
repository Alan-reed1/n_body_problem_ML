import json
import numpy as np

# TODO
# we are going to create an n-dimensional vector that includes at least 6 metrics:

# 0	Energy Drift	Total energy should be conserved (small ΔE okay)	ΔE from initial
# 1	Angular Momentum Drift	Conserved in isolated systems	ΔL from initial
# 2	Min Distance Spike	Close approaches may indicate chaos/collision	Smallest r₁₂
# 3	Body Escape	Large separation indicates escape trajectory	Max r from center
# 4	Velocity Oscillation	Wild fluctuations = chaotic transfer of energy	Var(‖v‖) over window
# 5	Center of Mass Drift	System drifting too far implies imbalance	ΔCOM from initial
# We will take in the JSON data and run a pass over it in order to define
# this vector. From the vector, we will attempt to create a 'stability score'

# to assign to each sim. We will give the sim and the score to the ML model as training and see how close it
# can come to reaching the same score given the same starting data. OR we simply create some score threshold
# and passing a boolean stable/non-stable orbit and have the ML model spit that out instead.
# Something like that. We will see. For now, we need to create the evaluation logic and
# start trying to run passes over the JSON file. We want to be able to prematurely throw away the sim data
# if the score is too low. We don't need to look at it anymore. I think what would be cooler is just making
# the stability boolean and trying to let the model figure out what makes an initial condition stable, because
# eventually I would like to just pass in initial conditions and instantly be told stable or not. Anyway,
# 2AM ramble finished. Good luck to myself tomorrow trying to figure out how to actually put all this
# junk together and make something that actually works

# Alright lets get started: Day 1.

# I reckon I'll start by getting all these metrics. We are reading from the file, formatted like so:
# [
#   {
#     "t": 0.0,
#     "particles": [
#       {
#         "id": 0,
#         "position": [
#           7.468,
#           4.926
#         ],
#         "velocity": [
#           0.0623,
#           0.0817
#         ],
#         "mass": 1.0
#       },
#       {
#         "id": 1,
#         "position": [
#           6.204,
#           1.488
#         ],
#         "velocity": [
#           0.0803,
#           0.0416
#         ],
#         "mass": 4.0
#       }
#     ]
#   },

# ------ CENTRAL CONTROL ------
def compute_metrics_from_json(json_path):
    with open(json_path, "r") as f:
        snapshots = json.load(f)

    state = MetricState(initial_snapshot=snapshots[0])

    for snapshot in snapshots:
        state.update_energy_drift(snapshot)

    return state.get_results()


# ----- METRICS -----
class MetricState:
    # initialize states
    def __init__(self, initial_snapshot):
        # energy init
        self.initial_energy = self.compute_energy(*initial_snapshot["particles"])
        self.max_energy_drift = 0.0

        # ang. momentum init
        self.initial_angular = self.compute_angular_momentum(initial_snapshot["particles"])
        self.max_angular_drift = 0.0

    # ---- COMPUTATIONS ----

    @staticmethod
    # total energy computation
    def compute_energy(p1, p2, G=1.0):
        v1 = np.linalg.norm(p1["velocity"])
        v2 = np.linalg.norm(p2["velocity"])
        ke = 0.5 * p1["mass"] * v1**2 + 0.5 * p2["mass"] * v2**2

        r = np.linalg.norm(np.array(p1["position"]) - np.array(p2["position"]))
        pe = -G * p1["mass"] * p2["mass"] / r

        return ke + pe

    # conserved angular momentum quantity
    @staticmethod
    def compute_angular_momentum(particles):
        total_L = 0.0
        for p in particles:
            x, y = p["position"]
            vx, vy = p["velocity"]
            m = p["mass"]
            total_L += m * (x * vy - y * vx)
        return total_L

    # ---- UPDATES -----

    # since they all follow the same ideas, I'll explain one:
    def update_energy_drift(self, snapshot):
        # Grab the current energy of the system using compute_energy()
        current_E = self.compute_energy(*snapshot["particles"])
        # quantify the drift magnitude from the initial conditions
        drift = abs((current_E - self.initial_energy) / self.initial_energy)
        # see if the current drift is more than the previous max
        self.max_energy_drift = max(self.max_energy_drift, drift)

    def update_angular_drift(self, snapshot, epsilon=1e-8):
        # Divide by 0 threshold: prevent misleadingly large L values.
        if abs(self.initial_angular) < epsilon:
            self.max_angular_drift = None  # or np.nan or "undefined"
            return

        current_L = self.compute_angular_momentum(snapshot["particles"])
        drift = abs((current_L - self.initial_angular) / self.initial_angular)
        self.max_angular_drift = max(self.max_angular_drift, drift)

    def update_all(self, snapshot):
        self.update_energy_drift(snapshot)
        self.update_angular_drift(snapshot)

    # return metric results
    def get_results(self):
        return {
            "energy_drift": self.max_energy_drift,
            "angular_drift": self.max_angular_drift if self.max_angular_drift is not None else "undefined"
        }


