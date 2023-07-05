import json

with open('C:\\Users\\alexa\\OneDrive\\Projects\\Python\\KI\\trainingData_date.json', 'r', encoding='utf-8') as f:
    new_training_data = json.load(f)

with open('C:\\Users\\alexa\\OneDrive\\Projects\\Python\\KI\\trainingData_located20XX.json', 'r', encoding='utf-8') as d:
    coord_training_data = json.load(d)


def run():
    data_list = list()
    not_found = 0
    count = 0
    for coord_data in coord_training_data:
        new_dict = coord_data.copy()
        new_dict.pop("_class")
        i = 0
        date_data = None
        while i < len(new_training_data) and date_data is None:
            if (new_dict["strasse"] == new_training_data[i]["strasse"] or new_dict["strasse"] == form_string(new_training_data[i]["strasse"])) \
                    and (new_dict["stadt"] == new_training_data[i]["stadt"] or new_dict["stadt"] == form_string(new_training_data[i]["stadt"])) \
                    and (new_dict["stadtteil"] == new_training_data[i]["stadtteil"] or new_dict["stadtteil"] == form_string(new_training_data[i]["stadtteil"])) \
                    and (new_dict["bundesland"] == new_training_data[i]["bundesland"] or new_dict["bundesland"] == form_string(new_training_data[i]["bundesland"])):
                date_data = new_training_data[i]
            i += 1
        if date_data is None:
            not_found += 1
            print(str(count) + " -> fail")
        else:
            new_dict["year"] = date_data["date"]
            data_list.append(new_dict)
            print(str(count) + " -> success")
        count += 1
    print("Not fount: " + str(not_found))
    with open('C:\\Users\\alexa\\OneDrive\\Projects\\Python\\KI\\trainingData_located2.json', 'w', encoding='utf-8') as d:
        json.dump(data_list, d, ensure_ascii=False, indent=4)


def form_string(string):
    t = string
    t = t.replace("ö", "oe")
    t = t.replace("Ö", "Oe")
    t = t.replace("ä", "ae")
    t = t.replace("Ä", "Ae")
    t = t.replace("ü", "ue")
    t = t.replace("Ü", "Ue")
    t = t.replace("ß", "ss")
    return t
