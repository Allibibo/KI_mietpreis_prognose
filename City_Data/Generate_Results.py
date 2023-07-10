import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tensorflow.keras import regularizers

from City_Data import Attribute


def prepare_data_for_lstm(data):
    X = []
    y = []

    for time_steps in data:
        X_timestep = []
        y_timestep = []

        for timestep_data in time_steps:
            X_timestep.append([
                timestep_data['roomCount'],
                timestep_data['propertyAge'],
                timestep_data['livingSpace'],
                timestep_data['hasBasement'],
                timestep_data['hasBalcony'],
                timestep_data['parkingLotCount'],
                timestep_data['hasGarden'],
                timestep_data['hasElevator'],
                timestep_data['year'],
                timestep_data['houseType apartment'],
                timestep_data['houseType ground_floor'],
                timestep_data['houseType half_basement'],
                timestep_data['houseType roof_storey'],
                timestep_data['houseType maisonette'],
                timestep_data['houseType raised_ground_floor'],
                timestep_data['houseType terraced_flat'],
                timestep_data['houseType other'],
                timestep_data['houseType penthouse'],
                timestep_data['houseType loft'],
                timestep_data['bundesland Berlin'],
                timestep_data['bundesland Bremen'],
                timestep_data['bundesland Nordrhein Westfalen'],
                timestep_data['bundesland Hamburg'],
                timestep_data['bundesland Sachsen Anhalt'],
                timestep_data['bundesland Niedersachsen'],
                timestep_data['bundesland Baden Wuerttemberg'],
                timestep_data['bundesland Rheinland Pfalz'],
                timestep_data['bundesland Hessen'],
                timestep_data['bundesland Brandenburg'],
                timestep_data['bundesland Sachsen'],
                timestep_data['bundesland Thueringen'],
                timestep_data['bundesland Bayern'],
                timestep_data['bundesland Mecklenburg Vorpommern'],
                timestep_data['bundesland Schleswig Holstein'],
                timestep_data['bundesland Saarland'],
                timestep_data['city_avr_rating'],
                timestep_data['city_avr_acc_population_change'],
                timestep_data['city_avr_population_change_last_year'],
                timestep_data['city_avr_persons_per_km2'],
                timestep_data['closest_city_distance']
            ])
            #y_timestep.append(timestep_data['rent'])

        X.append(X_timestep)
        y.append(y_timestep)

    return np.array(X), np.array(y)


def _generate_results_LSTM(data_list):
    with open('final_data_2_timeline_fut.json', 'r', encoding='utf-8') as file:
        timeline_fut_data = json.load(file)

    with open('final_data_3d_fut.json', 'r', encoding='utf-8') as file:
        data_3d_fut_data = json.load(file)

    loaded_model = tf.keras.models.load_model("Model/m2")

    res_list = list()
    for data in data_list:
        id = None
        for timeline_fut in timeline_fut_data:
            if data["Latitude"] == timeline_fut["Latitude"] and data["Longitude"] == timeline_fut["Longitude"] \
                    and data["livingSpace"] == timeline_fut["livingSpace"] \
                    and data["roomCount"] == timeline_fut["roomCount"] \
                    and data["propertyAge"] == timeline_fut["propertyAge"] \
                    and data["houseType"] == timeline_fut["houseType"]:
                id = timeline_fut["id"]
                break

        data_line = None
        for data_3d_fut in data_3d_fut_data:
            if data_3d_fut[0]["id"] == id:
                data_line = data_3d_fut
                break

        year = data["year"]
        min_year = year - 11
        new_data_line = list()
        for d in data_line:
            if min_year <= d["year"] <= year:
               new_data_line.append(d)

        features, c = prepare_data_for_lstm([new_data_line])
        predictions = loaded_model.predict(features)
        data["rent"] = int(predictions[0][0])
        res_list.append(data)

    return res_list


def _generate_results(data):
    feature_list = Attribute.generate_features(data)

    features = []
    for data in feature_list:
        f = [data['roomCount'], data['propertyAge'], data['livingSpace'], data['hasBasement'], data['hasBalcony'],
             data['parkingLotCount'], data['hasGarden'], data['hasElevator'], data['year'] * 100,
             data['houseType apartment'],
             data['houseType ground_floor'], data['houseType half_basement'], data['houseType roof_storey'],
             data['houseType maisonette'], data['houseType raised_ground_floor'], data['houseType terraced_flat'],
             data['houseType other'], data['houseType penthouse'], data['houseType loft'], data['bundesland Berlin'],
             data['bundesland Bremen'], data['bundesland Nordrhein Westfalen'], data['bundesland Hamburg'],
             data['bundesland Sachsen Anhalt'], data['bundesland Niedersachsen'], data['bundesland Baden Wuerttemberg'],
             data['bundesland Rheinland Pfalz'], data['bundesland Hessen'], data['bundesland Brandenburg'],
             data['bundesland Sachsen'], data['bundesland Thueringen'], data['bundesland Bayern'],
             data['bundesland Mecklenburg Vorpommern'], data['bundesland Schleswig Holstein'],
             data['bundesland Saarland'], data['city_avr_rating'], data['city_avr_acc_population_change'],
             data['city_avr_population_change_last_year'], data['city_avr_persons_per_km2'],
             data['closest_city_distance']]
        features.append(f)

    features = np.array(features)

    scaler = StandardScaler()
    features = scaler.fit_transform(features)

    loaded_model = tf.keras.models.load_model("Model/m1")
    predictions = loaded_model.predict(features)
    return predictions


def _get_average_rent(data_list):
    sum = 0
    for data in data_list:
        sum += data["rent"]
    return sum / len(data_list)


if __name__ == '__main__':
    with open('../Historical_Data/trainingData_fut_2022.json', 'r', encoding='utf-8') as file:
        data_list = json.load(file)

# Für die Vorhersage mit dem RNN
    # predictions = _generate_results(data_list)
    # run = 0
    # for data in data_list:
    #     data["rent"] = int(predictions[run][0])
    #     run += 1

    data_list = _generate_results_LSTM(data_list)
    print("average: " + str(_get_average_rent(data_list)))

    # with open('../Historical_Data/trainingData_fut_2025_RNN_res.json', 'w', encoding='utf-8') as file_1:
    #     json.dump(data_list, file_1, ensure_ascii=False, indent=2)
