import hashlib
import requests
from playsound import playsound

import time
import sys
import json


def proof_of_work(block):
    """
    Simple Proof of Work Algorithm
    Stringify the block and look for a proof.
    Loop through possibilities, checking each one against `valid_proof`
    in an effort to find a number that is a valid proof
    :return: A valid proof for the provided block
    """
    block_string = json.dumps(block, sort_keys=True)
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1
    return proof
    


def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?  Return true if the proof is valid
    :param block_string: <string> The stringified block to use to
    check in combination with `proof`
    :param proof: <int?> The value that when combined with the
    stringified previous block results in a hash that has the
    correct number of leading zeroes.
    :return: True if the resulting hash is a valid proof, False otherwise
    """
    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    
    return guess_hash[:6] == '000000'


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    # f = open("my_id.txt", "r")
    id = 'seth nadu'
    # print("ID is", id)
    # f.close()

    coins = 0
    # Run forever until interrupted
    while True:
        
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            continue

        # TODO: Get the block from `data` and use it to look for a new proof
        lblock = data['last_block']
        time_start = time.time()
        print('**********************************')
        print("Started searching ")
        new_proof = proof_of_work(lblock)
        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}

        re = requests.post(url=node + "/mine", json=post_data)
        try: 
            new_data = re.json()

            # TODO: If the server responds with a 'message' 'New Block Forged'
            # add 1 to the number of coins mined and print it.  Otherwise,
            # print the message from the server.
            if new_data["message"] == "Success":
                time_stop = time.time()
                print('')
                print(f"Finished searching, Time: {(time_stop - time_start):1f}")
                coins += 1
                # playsound('coin.mp3')
                print(new_data['message'])
                print(f'Coins mined: {coins}')
                print('')
                print("--------- Last Block ---------")
                print("Index: ", new_data['block']['index'])
                print("Previous Hash: ", new_data['block']['previous_hash'])
                print("Proof: ", new_data['block']['proof'])
                print("TimeStamp: ", new_data['block']['timestamp'])
                print("Transactions: ", new_data['block']['transactions'])
                print("")
            else:
                time_stop = timeit.timeit()
                print(f"Finished searching, Time: {(time_stop - time_start):1f}")
                print(new_data["message"])
        except:
            print("None JSON Response")
