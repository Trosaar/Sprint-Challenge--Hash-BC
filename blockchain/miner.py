import hashlib
import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import random

# def proof_of_work(block):
#     """
#     Simple Proof of Work Algorithm
#     Stringify the block and look for a proof.
#     Loop through possibilities, checking each one against `valid_proof`
#     in an effort to find a number that is a valid proof
#     :return: A valid proof for the provided block
#     """
#     block_string = json.dumps(block, sort_keys=True)
#     proof = 0

#     while valid_proof(block_string, proof) is False:
#         proof += 1

#     # return proof
#     return proof


# def valid_proof(block_string, proof):
#     """
#     Validates the Proof:  Does hash(block_string, proof) contain 6
#     leading zeroes?  Return true if the proof is valid
#     :param block_string: <string> The stringified block to use to
#     check in combination with `proof`
#     :param proof: <int?> The value that when combined with the
#     stringified previous block results in a hash that has the
#     correct number of leading zeroes.
#     :return: True if the resulting hash is a valid proof, False otherwise
#     """
#     guess = block_string + str(proof) 
#     guess = guess.encode()
    
#     hash_value = hashlib.sha256(guess).hexdigest()
    
#     return hash_value[:3] == '000'

def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last five digits of hash(p) are equal
    to the first five digits of hash(p')
    - IE:  last_hash: ...AE912345, new hash 12345888...
    - p is the previous proof, and p' is the new proof
    - Use the same method to generate SHA-256 hashes as the examples in class
    """

    start = timer()

    print("Searching for next proof")
    proof = 0

    last_proof
    last_hash = str(last_proof) 
    last_hash = last_hash.encode()
    last_hash_value = hashlib.sha256(last_hash).hexdigest()


    while valid_proof(last_hash_value, proof) is False:
        proof += 1

    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last five characters of
    the hash of the last proof match the first five characters of the hash
    of the new proof?

    IE:  last_hash: ...AE912345, new hash 12345E88...
    """

    guess = str(proof) 
    guess = guess.encode()
    
    hash_value = hashlib.sha256(guess).hexdigest()
    
    return last_hash[-5:] == hash_value[:5]


    # TODO: Your code here!
    pass


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com/api"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    if id == 'NONAME\n':
        print("ERROR: You must change your name in `my_id.txt`!")
        exit()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        new_proof = proof_of_work(data.get('proof'))

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
