import json

def get_dict_id_index(target_id, target_list): # find list index of dict id
    for i in range(len(target_list)):
        if target_list[i]["id"] == target_id:
            return i
    return -1