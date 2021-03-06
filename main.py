import datetime
import hashlib
import json
# Install these libraries with pip3 install:
from flask import Flask, jsonify
from flask_ngrok import run_with_ngrok

class Blockchain:
    def __init__(self):
        self.chain = []
        # Genesis block
        self.create_block(proof = 1, previous_hash = '0')
    
    def create_block(self, proof, previous_hash):
        # Create a new block and add it to the chain
        # proof: proof of work (Nounce of current block) (proof != hash), previous_hash: hash of previous block
        # Block structure:
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash}
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        # Return the previous block of the chain
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        # Find a number p' such that hash(pp') contains leading 4 zeroes, where p is the previous p'
        # p: previous proof (Nounce of the previous block), p': new proof
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        # Hash a block
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        # Check if a given blockchain is valid
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True

    