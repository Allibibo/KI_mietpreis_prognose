# Main Klasse für das Starten des Projekts
import city_data_service

if __name__ == '__main__':
    #tmep = city_data_service.get_nearest_city(52.1085288, 11.619955)
    temp = city_data_service.get_nearest_cities(5, 52.1085288, 11.619955)
    print(temp)
    for city_data in temp:
        print(city_data_service.get_average_rating(city_data, 2019))