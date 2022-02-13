# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 21:59:54 2022

@author: Luciano
"""
# Modulo 1 - Crear una Cadena de Bloques

# Importar las librerias
import datetime
import hashlib
import http
import json
from flask import Flask, jsonify


# Parte 1 - Crear la cadena de bloques

class Blockchain:
    # constructor de la clase
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    # Este método sirve para crear un nuevo bloque y agregarlo a la cadena
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash
                 }

        self.chain.append(block)
        return block

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
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False

            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            if hash_operation[0:4] != '0000':
                return False

            previous_block = block
            block_index += 1

        return True


# Parte 2 - Minado de un bloque de una cadena

# Crear una aplicación web

# Creo una instancia de flask para crear una app web
app = Flask(__name__)

# Crear una blockchain

# Creo una instancia de una cadena de bloques
blockchain = Blockchain()


# Minar un nuevo bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Felicidades, has minado un nuevo bloque!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash']
    }
    return jsonify(response), http.HTTPStatus.OK


# Obtener la cadena de bloques completa
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), http.HTTPStatus.OK


@app.route('/is_valid', methods=['GET'])
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {
            'message': 'Todo correcto. La cadena de bloques es valida.',
            'is_chain_valid': is_valid}
    else:
        response = {
            'message': 'Error. La cadena de bloques no es valida.',
            'is_chain_valid': is_valid}
    return jsonify(response), http.HTTPStatus.OK


# Ejecutar la app
app.run(host='0.0.0.0', port=5000)
