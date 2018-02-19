import json
import numpy as np

class fixed_encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(fixed_encoder, self).default(obj)

def get_dict_id_index(target_id, target_list): # find list index of dict id
    for i in range(len(target_list)):
        if target_list[i]["id"] == target_id:
            return i
    return -1
    