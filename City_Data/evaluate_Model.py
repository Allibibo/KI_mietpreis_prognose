import json
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from sklearn.model_selection import train_test_split


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
            y_timestep.append(timestep_data['rent'])

        X.append(X_timestep)
        y.append(y_timestep)

    return np.array(X), np.array(y)


def _formate_features(data_list):
    features = []
    for data in data_list:
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
    return np.array(features)


def plot_history(history):
    # Verlustkurven plotten
    plt.subplot(1, 2, 1)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Modellverlust')
    plt.ylabel('Verlust')
    plt.xlabel('Epoche')
    plt.legend(['Training', 'Validierung'], loc='upper right')

    # Genauigkeitskurven plotten
    plt.subplot(1, 2, 2)
    plt.plot(history.history['accuracy'])
    plt.plot(history.history['val_accuracy'])
    plt.title('Modellgenauigkeit')
    plt.ylabel('Genauigkeit')
    plt.xlabel('Epoche')
    plt.legend(['Training', 'Validierung'], loc='lower right')

    # Diagramm anzeigen
    plt.show()


def evaluate_model(model, X_test, y_test):
    # Modell auf Testdaten evaluieren
    loss, accuracy = model.evaluate(X_test, y_test)
    print("Testverlust:", loss)
    print("Testgenauigkeit:", accuracy)


if __name__ == '__main__':
    with open('final_data_3d.json', 'r') as r:
        test_data = json.load(r)

    test_data = [test_data[0]]

    features, c = prepare_data_for_lstm(test_data)
    loaded_model = tf.keras.models.load_model("Model/m2")
    print("Modell wurde geladen.")

    # Anpassung des Vorhersagehorizonts
    prediction_horizon = 12

    # Anpassung des Zielzeitpunkts für die Vorhersage
    target_year = 30  # Gewünschter Vorhersagezeitpunkt

    # Erstellen der Eingabedaten für den gewünschten Vorhersagezeitpunkt
    X_target = np.array([[[target_year, 0, 0]]])  # Beispiel: Angabe des Jahres 2030

    # Wiederholen der Eingabedaten für den gewünschten Vorhersagezeitpunkt für den Vorhersagehorizont
    X_target_extended = np.repeat(X_target, prediction_horizon, axis=1)

    # Vorhersagen mit dem geladenen Modell
    predictions = loaded_model.predict(X_target_extended)
    print(predictions)

    # sum = 0
    # run = 0
    # while run < len(test_data):
    #     sum += abs(test_data[run]['rent'] - predictions[run])
    #     run += 1
    #
    # print(sum / len(predictions))
