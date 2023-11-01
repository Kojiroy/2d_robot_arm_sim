import numpy as np

def find_nearest(array : np.array, value : float):
    idx = (np.abs(array-value)).argmin()
    return array[idx]

def find_lowest(array : np.array):
    return array[array.argmin()]

def find_highest(array : np.array):
    return array[array.argmax()]