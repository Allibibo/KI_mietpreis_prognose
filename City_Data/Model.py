import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.optimizers import Adam
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from sklearn.model_selection import train_test_split
from tensorflow.keras import regularizers


def _train_deep_neural_network(model_name, full_data):
    features = []
    labels = []
    for data in full_data:
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
        l = data['rent']
        labels.append(l)
        features.append(f)

    features = np.array(features)
    labels = np.array(labels)

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Definition der Hyperparameter
    input_param_count = len(full_data[0]) -1

    # Erstellung des Modells
    model = tf.keras.models.Sequential([
        tf.keras.layers.Dense(512, activation='relu', input_shape=(input_param_count,), kernel_regularizer=regularizers.l2(0.001)),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer=Adam(learning_rate=0.001), loss='mse', metrics=['mae'])

    model.fit(X_train, y_train, epochs=1000, batch_size=512, validation_data=(X_test, y_test))

    model.summary()

    test_loss, test_mae = model.evaluate(X_test, y_test)
    print('Test Loss:', test_loss)
    print('Test MAE:', test_mae)

    model.save(model_name)


def _train_LSTM_model(model_name, full_data):

    features, labels = prepare_data_for_lstm(full_data)

    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2, random_state=42)


    # Definition der Hyperparameter
    num_units = 64  # Anzahl der Einheiten (Neuronen) pro Schicht
    num_layers = 2  # Anzahl der RNN-Schichten
    input_shape = X_train.shape[1:]  # Eingabeform (Shape)

    # Erstellung des Modells
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.LSTM(64, input_shape=(X_train.shape[1], X_train.shape[2])))
    model.add(tf.keras.layers.Dense(1))  # Dropout zur Regularisierung

    # Ausgabeschicht
    model.add(tf.keras.layers.Dense(units=1))

    # Kompilieren des Modells
    model.compile(optimizer='adam', loss='mean_squared_error')

    # Zusammenfassung des Modells
    model.summary()

    # Training des Modells
    model.fit(X_train, y_train, epochs=10, batch_size=32)

    loss = model.evaluate(X_test, y_test)
    print("Loss:", loss)

    print(model.summary())

    model.save(model_name)


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

if __name__ == '__main__':

    with open('C:\\Users\\alexa\\OneDrive\\Projects\\Python\\KI\\City_Data\\training_data_2.json', 'r') as r:
        full_data = json.load(r)
    _train_deep_neural_network("C:\\Users\\alexa\\OneDrive\\Projects\\Python\\KI\\City_Data\\Model\\m3", full_data)

    #_train_LSTM_model("Model/m2", full_data)
