import numpy as np

def find_nearest(array : np.array, value : float):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

def find_lowest(array : np.array):
    return array[array.argmin()]

def find_highest(array : np.array):
    return array[array.argmax()]

def check_points(corners : np.array, state : np.array, boundary : np.array):
    # Return false if it hits something, true if movement is safe.
    hit = False

    # Reset x, y
    lowest_x = find_lowest(corners[:, 0])
    lowest_y = find_lowest(corners[:, 1])
    highest_x = find_highest(corners[:, 0])
    highest_y = find_highest(corners[:, 1])
    # print(f"Printing corners:\n{corners}")
    if lowest_x <= 0 :
        state[0][0] += -lowest_x # Becomes positive
        state[1][0] *= -1 if state[1][0] < 0 else 1
        hit = True
        # print(f"Hit left side with {lowest_x}")
    elif highest_x >= boundary[0]:
        state[0][0] += -highest_x + boundary[0] # Becomes negative
        state[1][0] *= -1 if state[1][0] > 0 else 1
        hit = True
        # print(f"Hit right side with {highest_x}")
    if lowest_y <= 0:
        state[0][1] += -lowest_y # becomes positive
        state[1][1] *= -1 if state[1][1] < 0 else 1
        hit = True
        # print(f"Hit floor with {lowest_y}")
    elif highest_y >=  boundary[1]:
        state[0][1] += -highest_y +  boundary[1] # Becomes negative
        state[1][1] *= -1 if state[1][1] > 0 else 1
        hit = True
        # print(f"Hit ceil with {highest_x}")
    return (not hit, state)