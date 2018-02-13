import copy
class IndProbEntry(object):
    def __init__(self):
        self.record = dict()

    def __str__(self):
        stringfy = ""
        for event_type in self.record.keys():
            stringfy += event_type + " " + str(self.record[event_type]) + ' '
        return stringfy

    def __iter__(self):
        for k in self.record:
            yield self.record[k]

    def insert_prob_entry(self, event_type, prob_list):
        self.record[event_type] = copy.deepcopy(prob_list)

    def get_prob_at(self, event_type, time):
        prob = self.record[event_type][time]
        return prob


class IndProbList(object):
    def __init__(self):
        self.ind_prob_impl = dict()
        self.index = 0

    def __str__(self):
        stringfy = ""
        for agent_id in self.ind_prob_impl.keys():
            stringfy += "agent_id: " + str(agent_id) + ", " + str(self.ind_prob_impl[agent_id]) + '\n'
        return stringfy

    def __iter__(self):
        for k in self.ind_prob_impl:
            yield self.ind_prob_impl[k]

    def insert_prob_entry(self, agent_id, event_type, prob_list):
        if agent_id not in self.ind_prob_impl:
            prob_entry = IndProbEntry()
            self.ind_prob_impl[agent_id] = prob_entry
        self.ind_prob_impl[agent_id].insert_prob_entry(event_type, prob_list)

