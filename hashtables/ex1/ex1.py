#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_retrieve)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    # array of weights
    # length of array as int
    # goal weight as int

    # loop through array and add to hashtable with the weight and array index.

    # if goal weight - currently checked wieght == value in hash HashTable
    #     return index value as tuple with other index value

    for i in range(length):
        hash_table_insert(ht, weights[i], i)

    for weight in weights:
        if hash_table_retrieve(ht, limit - weight):
            A = hash_table_retrieve(ht, weight)
            B = hash_table_retrieve(ht, limit - weight)

            if A >= B:
                return (A, B)
            else:
                return (B, A)

    return None


def print_answer(answer):
    if answer is not None:
        print(str(answer[0] + " " + answer[1]))
    else:
        print("None")
