import json

with open('./city_data.json', 'r') as f:
    city_data_list = json.load(f)


def _get_city_dir(name):
    city = None
    for city_data in city_data_list:
        if city_data["city"] == name:
            city = city_data

    return city


def _get_all_city_names():
    city_name_list = []
    for city_data in city_data_list:
        city_name_list.append(city_data["city"])


def get_nearest_city(location_lat, location_lng):
    return get_nearest_cities(1, location_lat, location_lng)


def get_nearest_cities(num_cities, location_lat, location_lng):
    nearest_city_list = list()
    for city_data in city_data_list:
        v1 = city_data["lat"] - location_lat
        v2 = city_data["lng"] - location_lng
        city_data["distance"] = (v1 * v1) + (v2 * v2)
        nearest_city_list = _add_if_nearer(num_cities, nearest_city_list, city_data)
    return nearest_city_list


def _add_if_nearer(num_cities, nearest_city_list, new_city):
    data_list = nearest_city_list.copy()
    if len(data_list) == 0:
        data_list.append(new_city)
        return data_list
    if new_city["distance"] < data_list[-1]["distance"]:
        if len(data_list) >= num_cities:
            data_list.pop(-1)
        run = 0
        while 0 <= run < len(data_list):
            if new_city["distance"] < data_list[run]["distance"]:
                data_list.insert(run, new_city)
                run = -1
            else:
                run += 1
        if run == len(data_list):
            data_list.append(new_city)
    return data_list


def get_average_rating(city_data, year):
    rating_multiplier = 4
    rating_sum = 0
    num_of_rating = 0
    run_year = 2010
    rating_dic = city_data["city_rating"]
    while run_year <= year and run_year <= 2022:
        rating = rating_dic[str(run_year)]
        if rating <= 10:
            rating_sum += rating * rating_multiplier
            num_of_rating += rating_multiplier
        else:
            rating_sum += rating
            num_of_rating += 1
        run_year += 1
    return round(rating_sum / num_of_rating)


