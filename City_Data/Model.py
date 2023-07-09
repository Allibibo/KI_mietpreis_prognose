import json
import numpy as np
import tensorflow as tf
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
from tensorflow import keras
from sklearn.model_selection import train_test_split

if __name__ == '__main__':

    with open('training_data.json', 'r') as r:
        full_data = json.load(r)

    features = []
    labels = []
    for data in full_data:
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
    num_units = 64  # Anzahl der Einheiten (Neuronen) pro Schicht
    num_layers = 2  # Anzahl der RNN-Schichten
    input_shape = X_train.shape[1:]  # Eingabeform (Shape)

    # Erstellung des Modells
    model = tf.keras.Sequential()

    # Hinzufügen der RNN-Schichten
    for _ in range(num_layers):
        model.add(tf.keras.layers.LSTM(32, input_shape=(None, len(full_data[0]) -1)))
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

    model.save("Model")
