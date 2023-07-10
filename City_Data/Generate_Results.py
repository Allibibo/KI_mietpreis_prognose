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


def _generate_results(data):
    feature_list = Attribute.generate_features(data)

    features = []
    for data in feature_list:
        f = [data['roomCount'], data['propertyAge'], data['livingSpace'], data['hasBasement'], data['hasBalcony'],
             data['parkingLotCount'], data['hasGarden'], data['hasElevator'], data['year'] * 100, data['houseType apartment'],
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
    with open('../Historical_Data/trainingData_fut_2025.json', 'r', encoding='utf-8') as file:
        data_list = json.load(file)

    predictions = _generate_results(data_list)
    run = 0
    for data in data_list:
        data["rent"] = int(predictions[run][0])
        run += 1

    print("average: " + str(_get_average_rent(data_list)))

    with open('../Historical_Data/trainingData_fut_2025_RNN_res.json', 'w', encoding='utf-8') as file_1:
        json.dump(data_list, file_1, ensure_ascii=False, indent=2)
