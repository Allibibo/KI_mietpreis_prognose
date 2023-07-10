# Main Klasse für das Starten des Projekts
import json

from City_Data import city_data_service

if __name__ == '__main__':
    pass
    #tmep = city_data_service.get_nearest_city(52.1085288, 11.619955)
    #temp = city_data_service.get_nearest_cities(5, 52.1085288, 11.619955)
    #print(temp)
    #for city_data in temp:
    #    print(city_data_service.get_average_rating(city_data, 2019))
    #city_data_service.test()
    #temp = city_data_service.get_location_statistics(52.1085288, 11.619955, 2013)
    #print(temp)

# Hinzufügen von populations daten
#     file_name = 'city_population_data.json'
#     with open(file_name, 'r', encoding='utf-8') as file:
#         loaded_data = json.load(file)
#
#     data = city_data_service.fill_up_to_2025(loaded_data)
#
#     with open('city_population_data.json', 'w', encoding='utf-8') as file:
#         json.dump(data, file, ensure_ascii=False, indent=2)