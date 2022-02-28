# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 21:59:54 2022

@author: Luciano
"""
# Modulo 2 - Crear una Criptomoneda

# Importar las librerias
import datetime
import hashlib
import json
from urllib.parse import urlparse
from model.block import Block
from model.transaction import Transaction


# Parte 1 - Crear la Criptomoneda

class CriptomonedaService:
    # constructor de la clase
    def __init__(self):
        self.chain = []
        # simula la mempool
        self.create_block(proof=1, previous_hash='0')
        self.nodes = set()

    # Este método sirve para crear un nuevo bloque y agregarlo a la cadena
    def create_block(self, proof, previous_hash):
        block = Block(len(self.chain), proof, previous_hash)
        # Despues de crear el bloque limpio la mempool de transacciones
        block.transactions = []
        # creo y guardo el hash en el bloque, cuando lo creo
        hash = self.hash(block)
        block.hash = hash
        self.chain.append(block.__dict__)
        return block.__dict__

    # Este método sirve para obtener el último bloque
    def get_previous_block(self):
        return self.chain[-1]

    # Este método sirve para minar un bloque
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            # esta linea obtiene el hash, al cual tenemos que verificar que tenga tantos ceros a la izquierda y que sea menor
            # a un hash dado. Se crea el problema a resolver por el minero con una ecuación como parametro de la función
            # hash 256, se lo convierte a string, le da el formato correcto de sha256 y se lo vuelve a convertir a un número de 64 bytes
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[0:4] == '0000':
                check_proof = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block.__dict__, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != previous_block['hash']:
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            if hash_operation[0:4] != '0000':
                return False

            previous_block = block
            block_index += 1

        return True

    def add_transactions(self, block, sender, receiver, amount):
        transaction = Transaction(sender, receiver, amount)
        block.transactions.append(transaction.__dict__)
        previous_block = self.get_previous_block()
        return previous_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

# Parte 3 - Descentralizar la cadena de bloques
