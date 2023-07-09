import json
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from sklearn.model_selection import train_test_split

if __name__ == '__main__':

    with open('test_data.json', 'r') as r:
        test_data = json.load(r)

    features = []
    for data in test_data:
        # f = [data['roomCount'], data['propertyAge']]
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

    loaded_model = tf.keras.models.load_model("Model")
    print("Modell wurde geladen.")

    # Vorhersagen mit dem geladenen Modell
    predictions = loaded_model.predict(features)

    sum = 0
    run = 0
    while run < len(test_data):
        sum += abs(test_data[run]['rent'] - predictions[run])
        run += 1

    print(sum / len(predictions))