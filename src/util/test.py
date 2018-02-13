from IndProb import *

i = IndProbList()
i.insert_prob_entry(1, "push", [0.1])
i.insert_prob_entry(2, "push", [0.2])
i.insert_prob_entry(1, "pull", [0.2])
print i

for x in i.items():
    print x
    print type(x)
