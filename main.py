# Main Klasse für das Starten des Projekts
import city_data_service

if __name__ == '__main__':
    tmep = city_data_service.get_nearest_city(52.1085288, 11.619955)
    print(tmep)