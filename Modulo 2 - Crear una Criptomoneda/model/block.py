import datetime

from model.transaction import Transaction


class Block:
    def __init__(self, length_chain, proof, previous_hash):
        self.index = (length_chain + 1)
        self.timestamp = str(datetime.datetime.now())
        self.proof = proof
        self.previous_hash = previous_hash
        self.hash = 0
        self.transactions = []
