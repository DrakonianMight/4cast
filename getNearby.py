import pandas as pd
import numpy as np

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth
    specified in decimal degrees using the Haversine formula.
    
    Parameters:
    - lat1, lon1: Latitude and longitude of point 1 in decimal degrees.
    - lat2, lon2: Latitude and longitude of point 2 in decimal degrees.
    
    Returns:
    - Distance in kilometers between the two points.
    """
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Radius of Earth in kilometers
    r = 6371.0
    return c * r

def find_nearby_sites(df, distance_threshold=100):
    """
    Identify sites within a specified distance of each other.
    
    Parameters:
    - df (pd.DataFrame): DataFrame with columns ['site_name', 'latitude', 'longitude'].
    - distance_threshold (float): Distance in kilometers to consider sites as "nearby".
    
    Returns:
    - nearby_sites (list): A list of tuples with site names that are within the distance threshold.
    """
    nearby_sites = []
    
    # Iterate through each site and compare with others
    for i, row1 in df.iterrows():
        for j, row2 in df.iterrows():
            if i < j:  # To avoid duplicate checks and self-comparison
                distance = haversine(row1['latitude'], row1['longitude'], row2['latitude'], row2['longitude'])
                if distance <= distance_threshold:
                    nearby_sites.append((row1['site_name'], row2['site_name'], distance))
    
    return nearby_sites

# Example usage
data = {
    'site_name': ['Site A', 'Site B', 'Site C', 'Site D'],
    'latitude': [-27.4808, -27.4882, -27.4840, -27.5500],
    'longitude': [153.0389, 153.0431, 153.0400, 153.1000]
}

df = pd.DataFrame(data)

# Find nearby sites within 100 km
nearby_sites = find_nearby_sites(df, distance_threshold=100)

print("Nearby sites within 100 km:")
for site1, site2, distance in nearby_sites:
    print(f"{site1} is within {distance:.2f} km of {site2}")