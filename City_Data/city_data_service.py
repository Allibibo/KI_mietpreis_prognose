import json

with open('city_ranking_data.json', 'r') as r:
    city_ranking_data_list = json.load(r)

with open('city_population_data.json', 'r') as p:
    city_population_data_list = json.load(p)

with open('city_base_data.json', 'r') as b:
    city_base_data_list = json.load(b)


def get_location_statistics(location_lat: float, location_lng: float, year: int):
    city_list = get_nearest_cities(5, location_lat, location_lng)
    calc_portion(city_list)
    statistic_list = list()
    for city in city_list:
        statistic = _get_city_params(year, city)
        statistic["portion"] = city["portion"]
        statistic_list.append(statistic)
    avr_rating = 0
    avr_acc_population = 0
    avr_population_change_last_year = 0
    avr_persons_per_km2 = 0
    for statistic in statistic_list:
        avr_rating += statistic["rating"] * statistic["portion"]
        avr_acc_population += statistic["acc_population"] * statistic["portion"]
        avr_population_change_last_year += statistic["population_change_last_year"] * statistic["portion"]
        avr_persons_per_km2 += statistic["persons_per_km2"] * statistic["portion"]
    return {
        "city_avr_rating": round(avr_rating, 2),
        "city_avr_acc_population_change": round(avr_acc_population, 2),
        "city_avr_population_change_last_year": round(avr_population_change_last_year, 2),
        "city_avr_persons_per_km2": round(avr_persons_per_km2, 2),
        "closest_city_distance": round(city_list[0]["distance"], 2)
    }


def calc_portion(city_list):
    min_dist = city_list[0]["distance"]
    max_dist = city_list[-1]["distance"]
    weight_sum = 0
    for city in city_list:
        weight = (1 - ((city["distance"] - min_dist) / (max_dist - min_dist))) + 0.5
        city["weight"] = weight
        weight_sum += weight
    for city in city_list:
        city["portion"] = round(city["weight"] / weight_sum, 2)


def _get_ranking_data_by_id(id_1):
    city = None
    run = 0
    while run < len(city_ranking_data_list) and city is None:
        city_data = city_ranking_data_list[run]
        if city_data["id"] == id_1:
            city = city_data
        run += 1

    return city


def _get_population_data_by_id(id_2):
    city = None
    run = 0
    while run < len(city_population_data_list) and city is None:
        city_data = city_population_data_list[run]
        if city_data["id"] == id_2:
            city = city_data
        run += 1

    return city


def _get_city_params(year, city):
    ranking = _get_ranking_data_by_id(city["id"])
    population = _get_population_data_by_id(city["id"])
    new_city_data = dict()
    new_city_data["rating"] = get_average_rating(ranking, year)
    new_city_data["acc_population"] = _get_accumulated_population_changes(population, year)
    new_city_data["population_change_last_year"] = _get_population_changes_last_year(population, year)
    new_city_data["persons_per_km2"] = _get_persons_per_km2(population, year)
    return new_city_data


def _get_accumulated_population_changes(population, year):
    statistic_years = [1939, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2011, 2012,
                       2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
                       2023, 2024, 2025]
    acc_percent_changes = 0
    fst = 0
    snd = 1
    while snd < len(statistic_years) and statistic_years[snd] <= year:
        fst_popu = population[str(statistic_years[fst])]
        snd_popu = population[str(statistic_years[snd])]
        percent = ((snd_popu - fst_popu) / fst_popu) * 100
        acc_percent_changes += percent
        fst += 1
        snd += 1
    return acc_percent_changes


def _get_population_changes_last_year(population, year):
    statistic_years = [1939, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2011, 2012,
                       2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
                       2023, 2024, 2025]
    idx = 0
    while idx < len(statistic_years) and statistic_years[idx] != year:
        idx += 1
    fst_popu = population[str(statistic_years[idx - 1])]
    snd_popu = population[str(statistic_years[idx])]
    return ((snd_popu - fst_popu) / fst_popu) * 100


def _get_persons_per_km2(population, year):
    statistic_years = [1939, 1950, 1960, 1970, 1980, 1990, 2000, 2010, 2011, 2012,
                       2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022,
                       2023, 2024, 2025]
    idx = 0
    while idx < len(statistic_years) and not statistic_years[idx] == year:
        idx += 1
    return round(population[str(statistic_years[idx])] / population["area"])


def get_nearest_cities(num_cities: int, location_lat: float, location_lng: float):
    nearest_city_list = list()
    for city_data in city_base_data_list:
        v1 = city_data["lat"] - location_lat
        v2 = city_data["lng"] - location_lng
        city_data["distance"] = abs((v1 * v1) + (v2 * v2))
        nearest_city_list = _add_if_nearer(num_cities, nearest_city_list, city_data)
    return nearest_city_list


def _add_if_nearer(num_cities, nearest_city_list, new_city):
    data_list = nearest_city_list.copy()
    if len(data_list) == 0:
        data_list.append(new_city)
        return data_list
    if new_city["distance"] < data_list[-1]["distance"] or len(data_list) < num_cities:
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


def get_average_rating(ranking_data, year):
    rating_multiplier = 4

    rating_sum = 0
    num_of_rating = 0
    run_year = 2010
    rating_dic = ranking_data["rating"]
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


def fill_up_to_2025(population_data):
    res = list()
    for data in population_data:
        d21 = data["2021"]
        d22 = data["2022"]
        diff = d22 - d21
        data["2023"] = d22 + (diff * 1)
        data["2024"] = d22 + (diff * 2)
        data["2025"] = d22 + (diff * 3)
        res.append(data.copy())
    return res

def test():
    res = list()
    for population_data in city_population_data_list:
        d10 = population_data["2010"]
        d20 = population_data["2020"]
        diff = d20 - d10
        step = diff / 10
        data = population_data.copy()
        run = 1
        while (2010 + run) < 2020:
            data[str(2010 + run)] = round(d10 + (step * run))
            run += 1
        res.append(data)
    with open('City_Data/city_population_data.json', 'w', encoding='utf-8') as d:
        json.dump(res, d, ensure_ascii=False, indent=4)
