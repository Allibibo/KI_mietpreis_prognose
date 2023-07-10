import numpy as np
import pyspark
import pandas as pd
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, FloatType
from pyspark.ml.feature import VectorAssembler
from sklearn.linear_model import LinearRegression


# Lade die Daten
def load_data(file_name):
    with open(file_name, 'r') as file:
        loaded_data = json.load(file)
    return loaded_data


def train_Linear_Regression(input_data):
    # Trainingsdaten einlesen
    with open('short_data.json', 'r') as file:
        training_data = json.load(file)

    # Trainingsdaten in separate Arrays konvertieren
    X_train = np.array([[data['roomCount'], data['propertyAge'], data['livingSpace'], data['hasBasement'],
                         data['hasBalcony'], data['parkingLotCount'], data['hasGarden'], data['hasElevator'],
                         data['houseType apartment'], data['houseType ground_floor'], data['houseType half_basement'],
                         data['houseType roof_storey'], data['houseType maisonette'],
                         data['houseType raised_ground_floor'],
                         data['houseType terraced_flat'], data['houseType other'], data['houseType penthouse'],
                         data['houseType loft'], data['bundesland Berlin'], data['bundesland Bremen'],
                         data['bundesland Nordrhein Westfalen'], data['bundesland Hamburg'],
                         data['bundesland Sachsen Anhalt'],
                         data['bundesland Niedersachsen'], data['bundesland Baden Wuerttemberg'],
                         data['bundesland Rheinland Pfalz'],
                         data['bundesland Hessen'], data['bundesland Brandenburg'], data['bundesland Sachsen'],
                         data['bundesland Thueringen'], data['bundesland Bayern'],
                         data['bundesland Mecklenburg Vorpommern'],
                         data['bundesland Schleswig Holstein'], data['bundesland Saarland'], data['city_avr_rating'],
                         data['city_avr_acc_population_change'], data['city_avr_population_change_last_year'],
                         data['city_avr_persons_per_km2'], data['closest_city_distance']]
                        for data in training_data])
    y_train = np.array([data['rent'] for data in training_data])

    # Lineare Regression erstellen und trainieren
    regression = LinearRegression()
    regression = regression.fit(X_train, y_train)

    return regression


def test_Linear_Regression(test_data, regression, spark):
    features = ["roomCount", "propertyAge", "livingSpace", "hasBasement", "hasBalcony", "parkingLotCount", "hasGarden",
                "hasElevator", "houseType apartment", "houseType ground_floor", "houseType half_basement",
                "houseType roof_storey", "houseType maisonette", "houseType raised_ground_floor",
                "houseType terraced_flat", "houseType other", "houseType penthouse", "houseType loft",
                "bundesland Berlin", "bundesland Bremen", "bundesland Nordrhein Westfalen", "bundesland Hamburg",
                "bundesland Sachsen Anhalt", "bundesland Niedersachsen", "bundesland Baden Wuerttemberg",
                "bundesland Rheinland Pfalz", "bundesland Hessen", "bundesland Brandenburg", "bundesland Sachsen",
                "bundesland Thueringen", "bundesland Bayern", "bundesland Mecklenburg Vorpommern",
                "bundesland Schleswig Holstein", "bundesland Saarland", "city_avr_rating",
                "city_avr_acc_population_change", "city_avr_population_change_last_year",
                "city_avr_persons_per_km2", "closest_city_distance"]

    schema = StructType([
        StructField("roomCount", IntegerType()), StructField("propertyAge", IntegerType()),
        StructField("livingSpace", FloatType()),
        StructField("hasBasement", IntegerType()), StructField("hasBalcony", IntegerType()),
        StructField("parkingLotCount", IntegerType()),
        StructField("hasGarden", IntegerType()), StructField("hasElevator", IntegerType()),
        StructField("rent", FloatType()),
        StructField("year", IntegerType()), StructField("houseType apartment", IntegerType()),
        StructField("houseType ground_floor", IntegerType()),
        StructField("houseType half_basement", IntegerType()), StructField("houseType roof_storey", IntegerType()),
        StructField("houseType maisonette", IntegerType()),
        StructField("houseType raised_ground_floor", IntegerType()),
        StructField("houseType terraced_flat", IntegerType()), StructField("houseType other", IntegerType()),
        StructField("houseType penthouse", IntegerType()), StructField("houseType loft", IntegerType()),
        StructField("bundesland Berlin", IntegerType()),
        StructField("bundesland Bremen", IntegerType()), StructField("bundesland Nordrhein Westfalen", IntegerType()),
        StructField("bundesland Hamburg", IntegerType()),
        StructField("bundesland Sachsen Anhalt", IntegerType()), StructField("bundesland Niedersachsen", IntegerType()),
        StructField("bundesland Baden Wuerttemberg", IntegerType()),
        StructField("bundesland Rheinland Pfalz", IntegerType()), StructField("bundesland Hessen", IntegerType()),
        StructField("bundesland Brandenburg", IntegerType()),
        StructField("bundesland Sachsen", IntegerType()), StructField("bundesland Thueringen", IntegerType()),
        StructField("bundesland Bayern", IntegerType()),
        StructField("bundesland Mecklenburg Vorpommern", IntegerType()),
        StructField("bundesland Schleswig Holstein", IntegerType()), StructField("bundesland Saarland", IntegerType()),
        StructField("city_avr_rating", FloatType()), StructField("city_avr_acc_population_change", FloatType()),
        StructField("city_avr_population_change_last_year", FloatType()),
        StructField("city_avr_persons_per_km2", FloatType()), StructField("closest_city_distance", FloatType())
    ])

    # Instantiate the assembler
    assembler = VectorAssembler(inputCols=features, outputCol='rent_target')

    # Load test data
    test_data = load_data(test_data)

    # Convert test_data list to DataFrame
    test_data_df = spark.createDataFrame(test_data, schema)

    # Assemble features for test data
    assembled_test_data = assembler.transform(test_data_df)

    # Extract features from assembled test data
    X_test = np.array(assembled_test_data.select('rent_target').collect()).reshape(-1, len(features))

    # Make predictions on the test data
    predictions = regression.predict(X_test)

    # Convert predictions to a Pandas Series
    y_pred = pd.Series(predictions)

    # Print the predictions
    for i, data_point in enumerate(test_data):
        print(f"Property {i + 1}: Predicted rent price = {y_pred[i]}")


def ask_user_Linear_Regression(regression):
    # Bundesland-Mapping
    bundesland_mapping = {
        "Berlin": "bundesland Berlin",
        "Bremen": "bundesland Bremen",
        "Nordrhein Westfalen": "bundesland Nordrhein Westfalen",
        "Hamburg": "bundesland Hamburg",
        "Sachsen Anhalt": "bundesland Sachsen Anhalt",
        "Niedersachsen": "bundesland Niedersachsen",
        "Baden Wuerttemberg": "bundesland Baden Wuerttemberg",
        "Rheinland Pfalz": "bundesland Rheinland Pfalz",
        "Hessen": "bundesland Hessen",
        "Brandenburg": "bundesland Brandenburg",
        "Sachsen": "bundesland Sachsen",
        "Thueringen": "bundesland Thueringen",
        "Bayern": "bundesland Bayern",
        "Mecklenburg Vorpommern": "bundesland Mecklenburg Vorpommern",
        "Schleswig Holstein": "bundesland Schleswig Holstein",
        "Saarland": "bundesland Saarland"
    }

    # House-Type-Mapping
    house_type_mapping = {
        "Wohnung": "houseType apartment",
        "Erdgeschoss": "houseType ground_floor",
        "Halbkeller": "houseType half_basement",
        "Dachgeschoss": "houseType roof_storey",
        "Maisonette": "houseType maisonette",
        "Hochparterre": "houseType raised_ground_floor",
        "Reihenwohnung": "houseType terraced_flat",
        "Andere": "houseType other",
        "Penthouse": "houseType penthouse",
        "Loft": "houseType loft"
    }

    # Eingabe von Attributen durch den Benutzer
    user_input = {
        "roomCount": int(input("Anzahl der Zimmer: ")),
        "propertyAge": int(input("Alter des GebÃ¤udes (in Jahren): ")),
        "livingSpace": float(input("WohnflÃ¤che (in Quadratmetern): ")),
        "hasBasement": int(input("Hat das GebÃ¤ude einen Keller? (0 fÃ¼r Nein, 1 fÃ¼r Ja): ")),
        "hasBalcony": int(input("Hat das GebÃ¤ude einen Balkon? (0 fÃ¼r Nein, 1 fÃ¼r Ja): ")),
        "parkingLotCount": int(input("Anzahl der ParkplÃ¤tze: ")),
        "hasGarden": int(input("Hat das GebÃ¤ude einen Garten? (0 fÃ¼r Nein, 1 fÃ¼r Ja): ")),
        "hasElevator": int(input("Hat das GebÃ¤ude einen Aufzug? (0 fÃ¼r Nein, 1 fÃ¼r Ja): ")),
        "houseType": input(
            "Haus-Typ (Wohnung, Erdgeschoss, Halbkeller, Dachgeschoss, Maisonette, Hochparterre, Reihenwohnung, Andere, Penthouse, Loft): "),
        "city_avr_rating": float(input("Durchschnittliche Bewertung der Stadt: ")),
        "city_avr_acc_population_change": float(
            input("Durchschnittliche jÃ¤hrliche BevÃ¶lkerungszunahme der Stadt (%): ")),
        "city_avr_population_change_last_year": float(
            input("BevÃ¶lkerungsverÃ¤nderung der Stadt im letzten Jahr (%): ")),
        "city_avr_persons_per_km2": float(
            input("Durchschnittliche Anzahl von Personen pro Quadratkilometer in der Stadt: ")),
        "closest_city_distance": float(input("Entfernung zur nÃ¤chsten Stadt (in Kilometern): "))
    }

    # Eingabe des Bundeslands durch den Benutzer
    user_bundesland = input("Bundesland eingeben: ")
    selected_bundesland = bundesland_mapping.get(user_bundesland, "bundesland Berlin")

    # Eingabe des Haus-Typs durch den Benutzer
    user_house_type = user_input.get('houseType', 'Wohnung')
    selected_house_type = house_type_mapping.get(user_house_type, "houseType apartment")

    # Eingabe des Benutzers in ein separates Array konvertieren
    X_user = np.array(
        [(user_input['roomCount'], user_input['propertyAge'], user_input['livingSpace'], user_input['hasBasement'],
          user_input['hasBalcony'], user_input['parkingLotCount'], user_input['hasGarden'], user_input['hasElevator'],
          0 if selected_bundesland != "bundesland Bremen" else 1,
          0 if selected_bundesland != "bundesland Nordrhein Westfalen" else 1,
          0 if selected_bundesland != "bundesland Hamburg" else 1,
          0 if selected_bundesland != "bundesland Sachsen Anhalt" else 1,
          0 if selected_bundesland != "bundesland Niedersachsen" else 1,
          0 if selected_bundesland != "bundesland Baden Wuerttemberg" else 1,
          0 if selected_bundesland != "bundesland Rheinland Pfalz" else 1,
          0 if selected_bundesland != "bundesland Hessen" else 1,
          0 if selected_bundesland != "bundesland Brandenburg" else 1,
          0 if selected_bundesland != "bundesland Sachsen" else 1,
          0 if selected_bundesland != "bundesland Thueringen" else 1,
          0 if selected_bundesland != "bundesland Bayern" else 1,
          0 if selected_bundesland != "bundesland Mecklenburg Vorpommern" else 1,
          0 if selected_bundesland != "bundesland Berlin" else 1,
          0 if selected_bundesland != "bundesland Schleswig Holstein" else 1,
          0 if selected_bundesland != "bundesland Saarland" else 1,
          1 if selected_house_type == "houseType apartment" else 0,
          1 if selected_house_type == "houseType ground_floor" else 0,
          1 if selected_house_type == "houseType half_basement" else 0,
          1 if selected_house_type == "houseType roof_storey" else 0,
          1 if selected_house_type == "houseType maisonette" else 0,
          1 if selected_house_type == "houseType raised_ground_floor" else 0,
          1 if selected_house_type == "houseType terraced_flat" else 0,
          1 if selected_house_type == "houseType other" else 0,
          1 if selected_house_type == "houseType penthouse" else 0, 1 if selected_house_type == "houseType loft" else 0,
          user_input['city_avr_rating'], user_input['city_avr_acc_population_change'],
          user_input['city_avr_population_change_last_year'], user_input['city_avr_persons_per_km2'],
          user_input['closest_city_distance'])
         for data in training_data])

    # Vorhersage fÃ¼r die Eingabe des Benutzers machen
    prediction = regression.predict(X_user)

    print("Vorhersage fÃ¼r den Mietpreis: ", prediction[0])


def main():
    input_data = 'short_data.json'
    test_data = 'short_data.json'

    spark = SparkSession.builder.getOrCreate()
    # Trainieren des Model
    regression = train_Linear_Regression(input_data)

    # Testen mit den Testdaten
    test_Linear_Regression(test_data, regression, spark)

    # Abfrage an den Nutzer
    ask_user_Linear_Regression(regression)


if __name__ == "__main__":
    main()