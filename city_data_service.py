import json

with open('./city_data.json', 'r') as f:
    city_data_list = json.load(f)


def get_nearest_city(location_lat, location_lng):
    nearest_city_distance = 99999999999
    nearest_city = None
    for city_data in city_data_list:
        v1 = city_data["lat"] - location_lat
        v2 = city_data["lng"] - location_lng
        distance = (v1 * v1) + (v2 * v2)
        if distance < nearest_city_distance:
            nearest_city_distance = distance
            nearest_city = city_data

    return nearest_city
