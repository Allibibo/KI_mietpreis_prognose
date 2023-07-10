import json
import random
from collections import OrderedDict
from City_Data import city_data_service


# Lade die Daten
def load_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as file:
        loaded_data = json.load(file)
    return loaded_data


# Sonderzeichen behandeln
def handle_special_characters(value):
    if isinstance(value, str):  # Überprüfen, ob der Wert ein String ist
        # Umlaute umwandeln
        value = value.replace("ß", "ss")
        value = value.replace("ä", "ae")
        value = value.replace("Ä", "Ae")
        value = value.replace("Ü", "Ue")
        value = value.replace("ü", "ue")
        value = value.replace("ö", "oe")
    return value


# Sonderzeichen in den geladenen Daten ersetzen
def handle_special_chars_in_data(loaded_data):
    decoded_data = []
    for dictionary in loaded_data:
        new_dict = {}
        for key, value in dictionary.items():
            new_dict[key] = handle_special_characters(value)
        decoded_data.append(new_dict)
    return decoded_data


# Speichern der endgültigen Daten in eine JSON-Datei
def save_to_json(data, output_filename):
    with open(output_filename, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


# Daten splitten
def handle_datasplit(loaded_data):
    splitted_data = []
    for data in loaded_data:
        new_dict = {}
        for key, value in data.items():
            new_dict[key] = change_values_to_zero_one(key, value)
        splitted_data.append(new_dict)
    return splitted_data


# Daten in Integer 0,1 umwandeln
def change_values_to_zero_one(key, value):
    if isinstance(value, bool):  # Überprüfen ob der Wert Boolean ist
        value = int(value)
    else:
        if isinstance(key, str):
            if key == "roomCount":  # Raumanzahl verarbeiten
                value = value

    return value


# Daten transformieren
def splitdata(loaded_data, attributeList):
    attribute_Map = OrderedDict()  # Map mit gewählten Attributen aufbauen
    for attribute in attributeList:
        attribute_Map[attribute] = []
    for eintrag in loaded_data:  # Map mit values füllen
        for attribute in attributeList:
            value = attribute_Map[attribute]
            if str(eintrag[attribute]) not in value:  # Überprüfen auf doppelte Werte
                value.append(eintrag[attribute])
            attribute_Map[attribute] = value
    for eintrag in loaded_data:
        for key in attribute_Map:
            for value in attribute_Map[key]:
                eintrag[key + ' ' + str(value)] = 0  # Inital auf Null setzen
            eintrag[key + ' ' + str(eintrag[key])] = 1
            eintrag.pop(key)
    return loaded_data


# Attribute entfernen
def pop_Attribute(loaded_data, attributeList):
    for eintrag in loaded_data:
        for attribute in attributeList:
            eintrag.pop(attribute, None)
    return loaded_data

def generate_features(data):
    loaded_data = data.copy()
    loaded_data = handle_special_chars_in_data(loaded_data)

    # Umwandeln der Attribute
    loaded_data = splitdata(loaded_data,
                            ['houseType', 'bundesland'])  # , 'stadt', 'livingSpace', 'houseType', 'bundesland'
    loaded_data = handle_datasplit(loaded_data)

    for data in loaded_data:
        data.update(city_data_service.get_location_statistics(data["Latitude"], data["Longitude"], data["year"] + 2000))

    # Entfernen von Attributen
    loaded_data = pop_Attribute(loaded_data,
                                ['stadtteil', 'plz', 'strasse', 'address', 'stadt', 'Latitude', 'Longitude'])

    return loaded_data

def main():
    input_filename_1 = '../Historical_Data/trainingData_located2010_2.json'
    input_filename_2 = '../Historical_Data/trainingData_located2011_2.json'
    input_filename_3 = '../Historical_Data/trainingData_located2012_2.json'
    input_filename_4 = '../Historical_Data/trainingData_located2013_2.json'
    input_filename_5 = '../Historical_Data/trainingData_located2014_2.json'
    input_filename_6 = '../Historical_Data/trainingData_located2015_2.json'
    input_filename_7 = '../Historical_Data/trainingData_located2016_2.json'
    input_filename_8 = '../Historical_Data/trainingData_located2017_2.json'
    input_filename_9 = '../Historical_Data/trainingData_located2018_2.json'
    input_filename_10 = '../Historical_Data/trainingData_located2019_2.json'
    input_filename_11 = '../Historical_Data/trainingData_located2020_2.json'
    input_filename_12 = '../Historical_Data/trainingData_located2021_2.json'
    output_filename = "final_data_2.json"

    # Lade die Daten ein
    loaded_data = load_data(input_filename_1)
    loaded_data.extend(load_data(input_filename_2))
    loaded_data.extend(load_data(input_filename_3))
    loaded_data.extend(load_data(input_filename_4))
    loaded_data.extend(load_data(input_filename_5))
    loaded_data.extend(load_data(input_filename_6))
    loaded_data.extend(load_data(input_filename_7))
    loaded_data.extend(load_data(input_filename_8))
    loaded_data.extend(load_data(input_filename_9))
    loaded_data.extend(load_data(input_filename_10))
    loaded_data.extend(load_data(input_filename_11))
    loaded_data.extend(load_data(input_filename_12))

    # Handle special characters
    loaded_data = handle_special_chars_in_data(loaded_data)

    # Umwandeln der Attribute
    loaded_data = splitdata(loaded_data,
                            ['houseType', 'bundesland'])  # , 'stadt', 'livingSpace', 'houseType', 'bundesland'
    loaded_data = handle_datasplit(loaded_data)

    for data in loaded_data:
        data.update(city_data_service.get_location_statistics(data["Latitude"], data["Longitude"], data["year"] + 2000))

    # Entfernen von Attributen
    loaded_data = pop_Attribute(loaded_data, ['stadtteil', 'plz', 'strasse', 'address', 'stadt', 'Latitude', 'Longitude'])

    # Speichern der endgültigen Daten in eine JSON-Datei
    print("Udpated: " + str(len(loaded_data)))
    save_to_json(loaded_data, output_filename)


def main_2():
    input_filename = 'final_data_2_timeline_fut.json'
    output_filename = "final_data_3d_fut.json"

    # Lade die Daten ein
    loaded_data = load_data(input_filename)

    # Handle special characters
    loaded_data = handle_special_chars_in_data(loaded_data)

    # Umwandeln der Attribute
    loaded_data = splitdata(loaded_data, ['houseType', 'bundesland'])
    loaded_data = handle_datasplit(loaded_data)

    max_id = 0
    for data in loaded_data:
        data.update(city_data_service.get_location_statistics(data["Latitude"], data["Longitude"], data["year"] + 2000))
        if data["id"] > max_id:
            max_id = data["id"]

    # Entfernen von Attributen
    loaded_data = pop_Attribute(loaded_data,
                                ['stadtteil', 'plz', 'strasse', 'address', 'stadt', 'Latitude', 'Longitude'])

    res_list = []
    for i in range(0, max_id):
        res_list.append(list())

    for data in loaded_data:
        #id = data.pop("id")
        id = data["id"]
        res_list[id - 1].append(data)

    run = 0
    while run < len(res_list):
        res_list[run] = sorted(res_list[run], key=lambda x: x["year"])
        run += 1

    # Speichern der endgültigen Daten in eine JSON-Datei
    save_to_json(res_list, output_filename)


def get_equal(full_data_list):
    same_list = list()
    fst_data = full_data_list.pop(0)
    same_list.append(fst_data)
    run = 0
    while run < len(full_data_list):
        data = full_data_list[run]
        if fst_data["strasse"] == data["strasse"] and fst_data["stadt"] == data["stadt"] and \
                fst_data["stadtteil"] == data["stadtteil"] and fst_data["plz"] == data["plz"]:
            same_list.append(full_data_list.pop(run))
        else:
            run += 1
    return same_list


def _split_in_training_and_test_data(total_data: list):
    training_data = list()
    test_data = list()
    for data in total_data:
        if random.random() <= 0.8:
            _add_random_order(training_data, data)
        else:
            _add_random_order(test_data, data)
    return training_data, test_data


def _add_random_order(data_list, elem):
    if random.random() > 0.5:
        data_list.append(elem)
    else:
        data_list.insert(0, elem)


def _build_raw_data_2():
    input_filename_1 = '../Historical_Data/trainingData_located2010_2.json'
    input_filename_2 = '../Historical_Data/trainingData_located2011_2.json'
    input_filename_3 = '../Historical_Data/trainingData_located2012_2.json'
    input_filename_4 = '../Historical_Data/trainingData_located2013_2.json'
    input_filename_5 = '../Historical_Data/trainingData_located2014_2.json'
    input_filename_6 = '../Historical_Data/trainingData_located2015_2.json'
    input_filename_7 = '../Historical_Data/trainingData_located2016_2.json'
    input_filename_8 = '../Historical_Data/trainingData_located2017_2.json'
    input_filename_9 = '../Historical_Data/trainingData_located2018_2.json'
    input_filename_10 = '../Historical_Data/trainingData_located2019_2.json'
    input_filename_11 = '../Historical_Data/trainingData_located2020_2.json'
    input_filename_12 = '../Historical_Data/trainingData_located2021_2.json'
    input_filename_13 = '../Historical_Data/trainingData_fut_2022.json'
    input_filename_14 = '../Historical_Data/trainingData_fut_2023.json'
    input_filename_15 = '../Historical_Data/trainingData_fut_2024.json'
    input_filename_16 = '../Historical_Data/trainingData_fut_2025.json'
    output_filename = "final_data_2_timeline_fut.json"

    # Lade die Daten ein
    loaded_data_1 = handle_special_chars_in_data(load_data(input_filename_1))
    loaded_data_2 = handle_special_chars_in_data(load_data(input_filename_2))
    loaded_data_3 = handle_special_chars_in_data(load_data(input_filename_3))
    loaded_data_4 = handle_special_chars_in_data(load_data(input_filename_4))
    loaded_data_5 = handle_special_chars_in_data(load_data(input_filename_5))
    loaded_data_6 = handle_special_chars_in_data(load_data(input_filename_6))
    loaded_data_7 = handle_special_chars_in_data(load_data(input_filename_7))
    loaded_data_8 = handle_special_chars_in_data(load_data(input_filename_8))
    loaded_data_9 = handle_special_chars_in_data(load_data(input_filename_9))
    loaded_data_10 = handle_special_chars_in_data(load_data(input_filename_10))
    loaded_data_11 = handle_special_chars_in_data(load_data(input_filename_11))
    loaded_data_12 = handle_special_chars_in_data(load_data(input_filename_12))
    loaded_data_13 = handle_special_chars_in_data(load_data(input_filename_13))
    loaded_data_14 = handle_special_chars_in_data(load_data(input_filename_14))
    loaded_data_15 = handle_special_chars_in_data(load_data(input_filename_15))
    loaded_data_16 = handle_special_chars_in_data(load_data(input_filename_16))

    highest_id = 0
    data_list = list()
    while len(loaded_data_2) > 0 or len(loaded_data_3) > 0 or len(loaded_data_4) > 0 or len(loaded_data_5) > 0 \
            or len(loaded_data_6) > 0 or len(loaded_data_7) > 0 or len(loaded_data_8) > 0 or len(loaded_data_9) > 0 \
            or len(loaded_data_10) > 0 or len(loaded_data_11) > 0 or len(loaded_data_12) > 0 or len(loaded_data_13) > 0 \
            or len(loaded_data_14) > 0 or len(loaded_data_15) > 0 or len(loaded_data_16) > 0:
        print(len(loaded_data_2))
        if len(loaded_data_2) > 0:
            data_2 = loaded_data_2.pop(0)
        else:
            data_2 = None
        if len(loaded_data_3) > 0:
            data_3 = loaded_data_3.pop(0)
        else:
            data_3 = None
        if len(loaded_data_4) > 0:
            data_4 = loaded_data_4.pop(0)
        else:
            data_4 = None
        if len(loaded_data_5) > 0:
            data_5 = loaded_data_5.pop(0)
        else:
            data_5 = None
        if len(loaded_data_6) > 0:
            data_6 = loaded_data_6.pop(0)
        else:
            data_6 = None
        if len(loaded_data_7) > 0:
            data_7 = loaded_data_7.pop(0)
        else:
            data_7 = None
        if len(loaded_data_8) > 0:
            data_8 = loaded_data_8.pop(0)
        else:
            data_8 = None
        if len(loaded_data_9) > 0:
            data_9 = loaded_data_9.pop(0)
        else:
            data_9 = None
        if len(loaded_data_10) > 0:
            data_10 = loaded_data_10.pop(0)
        else:
            data_10 = None
        if len(loaded_data_11) > 0:
            data_11 = loaded_data_11.pop(0)
        else:
            data_11 = None
        if len(loaded_data_12) > 0:
            data_12 = loaded_data_12.pop(0)
        else:
            data_12 = None
        if len(loaded_data_13) > 0:
            data_13 = loaded_data_13.pop(0)
        else:
            data_13 = None
        if len(loaded_data_14) > 0:
            data_14 = loaded_data_14.pop(0)
        else:
            data_14 = None
        if len(loaded_data_15) > 0:
            data_15 = loaded_data_15.pop(0)
        else:
            data_15 = None
        if len(loaded_data_16) > 0:
            data_16 = loaded_data_16.pop(0)
        else:
            data_16 = None

        run = 0
        while run < len(loaded_data_1) and (data_2 is not None or data_3 is not None or data_4 is not None \
                                            or data_5 is not None or data_6 is not None or data_7 is not None or data_8 is not None \
                                            or data_9 is not None or data_10 is not None or data_11 is not None or data_12 is not None):
            data_1 = loaded_data_1[run]
            if data_2 is not None and data_1["Latitude"] == data_2["Latitude"] \
                    and data_1["Longitude"] == data_2["Longitude"] and data_1["livingSpace"] == data_2["livingSpace"] \
                    and data_1["roomCount"] == data_2["roomCount"] and data_1["propertyAge"] == data_2["propertyAge"] \
                    and data_1["houseType"] == data_2["houseType"]:
                if "id" in data_1:
                    data_2["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_2["id"] = highest_id
                data_list.append(data_2)
                data_2 = None
            if data_3 is not None and data_1["Latitude"] == data_3["Latitude"] \
                    and data_1["Longitude"] == data_3["Longitude"] and data_1["livingSpace"] == data_3["livingSpace"] \
                    and data_1["roomCount"] == data_3["roomCount"] and data_1["propertyAge"] == data_3["propertyAge"] \
                    and data_1["houseType"] == data_3["houseType"]:
                if "id" in data_1:
                    data_3["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_3["id"] = highest_id
                data_list.append(data_3)
                data_3 = None
            if data_4 is not None and data_1["Latitude"] == data_4["Latitude"] \
                    and data_1["Longitude"] == data_4["Longitude"] and data_1["livingSpace"] == data_4["livingSpace"] \
                    and data_1["roomCount"] == data_4["roomCount"] and data_1["propertyAge"] == data_4["propertyAge"] \
                    and data_1["houseType"] == data_4["houseType"]:
                if "id" in data_1:
                    data_4["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_4["id"] = highest_id
                data_list.append(data_4)
                data_4 = None
            if data_5 is not None and data_1["Latitude"] == data_5["Latitude"] \
                    and data_1["Longitude"] == data_5["Longitude"] and data_1["livingSpace"] == data_5["livingSpace"] \
                    and data_1["roomCount"] == data_5["roomCount"] and data_1["propertyAge"] == data_5["propertyAge"] \
                    and data_1["houseType"] == data_5["houseType"]:
                if "id" in data_1:
                    data_5["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_5["id"] = highest_id
                data_list.append(data_5)
                data_5 = None
            if data_6 is not None and data_1["Latitude"] == data_6["Latitude"] \
                    and data_1["Longitude"] == data_6["Longitude"] and data_1["livingSpace"] == data_6["livingSpace"] \
                    and data_1["roomCount"] == data_6["roomCount"] and data_1["propertyAge"] == data_6["propertyAge"] \
                    and data_1["houseType"] == data_6["houseType"]:
                if "id" in data_1:
                    data_6["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_6["id"] = highest_id
                data_list.append(data_6)
                data_6 = None
            if data_7 is not None and data_1["Latitude"] == data_7["Latitude"] \
                    and data_1["Longitude"] == data_7["Longitude"] and data_1["livingSpace"] == data_7["livingSpace"] \
                    and data_1["roomCount"] == data_7["roomCount"] and data_1["propertyAge"] == data_7["propertyAge"] \
                    and data_1["houseType"] == data_7["houseType"]:
                if "id" in data_1:
                    data_7["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_7["id"] = highest_id
                data_list.append(data_7)
                data_7 = None
            if data_8 is not None and data_1["Latitude"] == data_8["Latitude"] \
                    and data_1["Longitude"] == data_8["Longitude"] and data_1["livingSpace"] == data_8["livingSpace"] \
                    and data_1["roomCount"] == data_8["roomCount"] and data_1["propertyAge"] == data_8["propertyAge"] \
                    and data_1["houseType"] == data_8["houseType"]:
                if "id" in data_1:
                    data_8["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_8["id"] = highest_id
                data_list.append(data_8)
                data_8 = None
            if data_9 is not None and data_1["Latitude"] == data_9["Latitude"] \
                    and data_1["Longitude"] == data_9["Longitude"] and data_1["livingSpace"] == data_9["livingSpace"] \
                    and data_1["roomCount"] == data_9["roomCount"] and data_1["propertyAge"] == data_9["propertyAge"] \
                    and data_1["houseType"] == data_9["houseType"]:
                if "id" in data_1:
                    data_9["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_9["id"] = highest_id
                data_list.append(data_9)
                data_9 = None
            if data_10 is not None and data_1["Latitude"] == data_10["Latitude"] \
                    and data_1["Longitude"] == data_10["Longitude"] and data_1["livingSpace"] == data_10["livingSpace"] \
                    and data_1["roomCount"] == data_10["roomCount"] and data_1["propertyAge"] == data_10["propertyAge"] \
                    and data_1["houseType"] == data_10["houseType"]:
                if "id" in data_1:
                    data_10["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_10["id"] = highest_id
                data_list.append(data_10)
                data_10 = None
            if data_11 is not None and data_1["Latitude"] == data_11["Latitude"] \
                    and data_1["Longitude"] == data_11["Longitude"] and data_1["livingSpace"] == data_11["livingSpace"] \
                    and data_1["roomCount"] == data_11["roomCount"] and data_1["propertyAge"] == data_11["propertyAge"] \
                    and data_1["houseType"] == data_11["houseType"]:
                if "id" in data_1:
                    data_11["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_11["id"] = highest_id
                data_list.append(data_11)
                data_11 = None
            if data_12 is not None and data_1["Latitude"] == data_12["Latitude"] \
                    and data_1["Longitude"] == data_12["Longitude"] and data_1["livingSpace"] == data_12["livingSpace"] \
                    and data_1["roomCount"] == data_12["roomCount"] and data_1["propertyAge"] == data_12["propertyAge"] \
                    and data_1["houseType"] == data_12["houseType"]:
                if "id" in data_1:
                    data_12["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_12["id"] = highest_id
                data_list.append(data_12)
                data_12 = None
            if data_13 is not None and data_1["Latitude"] == data_13["Latitude"] \
                    and data_1["Longitude"] == data_13["Longitude"] and data_1["livingSpace"] == data_13["livingSpace"] \
                    and data_1["roomCount"] == data_13["roomCount"] and data_1["propertyAge"] == data_13["propertyAge"] \
                    and data_1["houseType"] == data_13["houseType"]:
                if "id" in data_1:
                    data_13["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_13["id"] = highest_id
                data_list.append(data_13)
                data_13 = None
            if data_14 is not None and data_1["Latitude"] == data_14["Latitude"] \
                    and data_1["Longitude"] == data_14["Longitude"] and data_1["livingSpace"] == data_14["livingSpace"] \
                    and data_1["roomCount"] == data_14["roomCount"] and data_1["propertyAge"] == data_14["propertyAge"] \
                    and data_1["houseType"] == data_14["houseType"]:
                if "id" in data_1:
                    data_14["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_14["id"] = highest_id
                data_list.append(data_14)
                data_14 = None
            if data_15 is not None and data_1["Latitude"] == data_15["Latitude"] \
                    and data_1["Longitude"] == data_15["Longitude"] and data_1["livingSpace"] == data_15["livingSpace"] \
                    and data_1["roomCount"] == data_15["roomCount"] and data_1["propertyAge"] == data_15["propertyAge"] \
                    and data_1["houseType"] == data_15["houseType"]:
                if "id" in data_1:
                    data_15["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_15["id"] = highest_id
                data_list.append(data_15)
                data_15 = None
            if data_16 is not None and data_1["Latitude"] == data_16["Latitude"] \
                    and data_1["Longitude"] == data_16["Longitude"] and data_1["livingSpace"] == data_16["livingSpace"] \
                    and data_1["roomCount"] == data_16["roomCount"] and data_1["propertyAge"] == data_16["propertyAge"] \
                    and data_1["houseType"] == data_16["houseType"]:
                if "id" in data_1:
                    data_16["id"] = data_1["id"]
                else:
                    highest_id += 1
                    data_1["id"] = highest_id
                    data_16["id"] = highest_id
                data_list.append(data_16)
                data_16 = None
            run += 1
    data_list.extend(loaded_data_1)
    save_to_json(data_list, output_filename)


def remove_double(data_list):
    result_list = list()
    double_data_count = 0

    while len(data_list) > 0:
        run = 0
        data = data_list.pop(0)
        while run < len(data_list):
            d = data_list[run]
            if data is not None and data["Latitude"] == d["Latitude"] and data["Longitude"] == d["Longitude"] \
                    and data["livingSpace"] == d["livingSpace"] and data["roomCount"] == d["roomCount"] \
                    and data["propertyAge"] == d["propertyAge"] and data["houseType"] == d["houseType"]:
                data_list.pop(run)
                double_data_count += 1
            else:
                run += 1
        result_list.append(data)
    print("Duplicates: " + str(double_data_count))
    return result_list


def create_future_data(data):
    data_list_2022 = list()
    data_list_2023 = list()
    data_list_2024 = list()
    data_list_2025 = list()

    for d in data:
        d.pop("rent")
        d["year"] = 22
        data_list_2022.append(d.copy())
        d["year"] = 23
        data_list_2023.append(d.copy())
        d["year"] = 24
        data_list_2024.append(d.copy())
        d["year"] = 25
        data_list_2025.append(d.copy())

    save_to_json(data_list_2022, '../Historical_Data/trainingData_fut_2022.json')
    save_to_json(data_list_2023, '../Historical_Data/trainingData_fut_2023.json')
    save_to_json(data_list_2024, '../Historical_Data/trainingData_fut_2024.json')
    save_to_json(data_list_2025, '../Historical_Data/trainingData_fut_2025.json')


if __name__ == "__main__":
    # Erstelle Trainingsvariablen aus Daten
    # main()

    main_2()

# Erstellen der Zukünftigen Rohdaten
    #data = load_data('../Historical_Data/trainingData_located2021_2.json')
    #create_future_data(data)

# Gleiche Immobilenstammdaten aus den verschiedenen Jahren werden mit der salben ID versehen um sie
# folgend und eine 3d Liste zusammenführen zu können.
#     _build_raw_data_2()
#     data = load_data('final_data_2_timeline.json')
#     i = 0
#     for d in data:
#        if not 'id' in d:
#            i += 1
#     print("No ID: " + str(i))

# num_list = list()
# for i in range(0, 117360):
#    num_list.append(0)

# for d in data:
#    if 'id' in d:
#        num_list[d['id']] += 1
# print(num_list)

# Löschen doppelter Werte in Liste
# data = load_data('../Historical_Data/trainingData_located2021.json')
# print(len(data))
# data = remove_double(data)
# save_to_json(data, '../Historical_Data/trainingData_located2021_2.json')

# Aufteilen in Training und Test Daten
# total_data_list = load_data('final_data_2.json')
# training_data, test_data = _split_in_training_and_test_data(total_data_list)
# save_to_json(training_data, 'training_data_2.json')
# save_to_json(test_data, 'test_data_2.json')
