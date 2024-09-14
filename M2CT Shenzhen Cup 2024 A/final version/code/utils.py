import numpy as np

def distance(p_1: np.ndarray, p_2: np.ndarray):
    if p_1.shape == p_2.shape:
        return np.sqrt(np.sum(np.square(p_1 - p_2)))
    

@np.vectorize(signature='(n),()->(n)')
def convert(coordinates: np.ndarray, type: str):
    base_lon = 110
    base_lat = 27
    converted = np.zeros(3)
    match type:
        case 'xyz':
            converted[0] = (coordinates[0] - base_lon) * 97.304
            converted[1] = (coordinates[1] - base_lat) * 111.263
            converted[2] = coordinates[2] / 1000
        case 'blh':
            converted[0] = coordinates[0] / 97.304 + base_lon
            converted[1] = coordinates[1] / 111.263 + base_lat
            converted[2] = coordinates[2] * 1000
    return converted