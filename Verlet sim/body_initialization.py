import random

# create a list of k (v_x, v_y) velocity coordinates
def gen_velocities(arr, k):
    for i in range(k):
        arr.append([round(random.uniform(.01, .1), 4), round(random.uniform(.01, .1), 4)])

# create a list of k (x, y) position coordinates
def gen_positions(arr, k):
    for i in range(k):
        arr.append([round(random.uniform(0, 10), 3), round(random.uniform(0, 10), 3)])

# create a list of k masses
def gen_masses(arr, k):
    for i in range(k):
        arr.append(round(random.randint(1, 10), 3))

# create a collection of bodies that have mass, position and velocity
def generate_sim_batch(vel, pos, mass, body_num=0):
    gen_velocities(vel, body_num)
    gen_positions(pos, body_num)
    gen_masses(mass, body_num)