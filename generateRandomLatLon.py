import random
from geopy.distance import distance

def generate_synthetic_locations(num_pairs, max_distance):
    central_france_lat_range = (43.895111, 50.061714)  # Latitude range for central France
    central_france_lon_range = (-0.893673, 3.918339)    # Longitude range for central France
    locations = []
    for _ in range(num_pairs):
        pair = []
        for _ in range(4):
            valid = False
            while not valid:
                lat = random.uniform(central_france_lat_range[0], central_france_lat_range[1])
                lon = random.uniform(central_france_lon_range[0], central_france_lon_range[1])
                point = (lat, lon)
                if all(distance(point, p) <= max_distance for p in pair):
                    pair.append(point)
                    valid = True
        locations.append(pair)
    return locations