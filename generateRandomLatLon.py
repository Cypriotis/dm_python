import random
from geopy.distance import distance

def generate_synthetic_locations(num_pairs, max_distance):
    europe_lat_range = (36.0, 71.0)
    europe_lon_range = (-26.0, 45.0)
    locations = []
    for _ in range(num_pairs):
        pair = []
        for _ in range(4):
            valid = False
            while not valid:
                lat = random.uniform(europe_lat_range[0], europe_lat_range[1])
                lon = random.uniform(europe_lon_range[0], europe_lon_range[1])
                point = (lat, lon)
                if all(distance(point, p) <= max_distance for p in pair):
                    pair.append(point)
                    valid = True
        locations.append(pair)
    return locations