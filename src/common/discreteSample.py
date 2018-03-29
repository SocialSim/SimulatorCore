import random
import time


def sample(values, probs):
    '''
    This function is used to sample a discrete sample from the given distribution.
    :param values: The given sample space
    :param probs: The corresponding probability distribution; note this should be a cumulative probability distribution.
    :return:
    '''
    assert(len(values) == len(probs))
    rand = random.random()

    index = binarySearch(probs, rand)

    if index == -1 or index >= len(values):
        print("Invalud sample!")
    else:
        return values[index]

def binarySearch(probs, rand):
    '''
    Given the random number, find the corresponding slot, return the index.
    :param probs: [0.1, 0.3, 0.7, 1]
    :param rand:
    :return:
    '''
    low = 0
    high = len(probs)
    while low <= high:

        mid = (low + high) / 2

        if mid == 0:
            prev = 0
        else:
            prev = probs[mid - 1]

        if probs[mid] >= rand and prev < rand:
            return mid
        elif prev >= rand:
            high = mid - 1
        else:
            low = mid + 1
    #Do not rand
    return -1


if __name__ == '__main__':

    values = range(9)
    probs = [float(i+1)/9 for i in range(9)]

    start = time.time()
    count = 0
    for i in range(1000000):
       if sample(values, probs) == 1:
           count +=1
    print(count)
    end = time.time()
    print("Time: %f s"%(end-start))