import json

def get_dict_id_index(target_id, target_list): # find list index of dict id
    for i in range(len(target_list)):
        if target_list[i]["id"] == target_id:
            return i
    return -1

def get_attributes(): # return config data
    with open('../config/config.json') as json_data_file:
        data = json.load(json_data_file)
    return data

def get_ids(target_type): # return list of ids of target type from config data
    with open('../config/config.json') as json_data_file:
        data = json.load(json_data_file)

    id_list = []
    for attributes in data[target_type]["attributes"]:
        id_list.append(attributes["id"])

    return id_list