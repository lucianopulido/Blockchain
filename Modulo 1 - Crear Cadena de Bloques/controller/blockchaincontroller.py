# Importar las librerias
import http
from flask import Flask, jsonify
from service.blockchainservice import *

# Parte 2 - Minado de un bloque de una cadena

# Crear una aplicación web

# Creo una instancia de flask para crear una app web
app = Flask(__name__)

# Crear una blockchain

# Creo una instancia de una cadena de bloques
blockchain = BlockchainService()


# Minar un nuevo bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = previous_block['hash']
    block = blockchain.create_block(proof, previous_hash)
    response = {
        'message': 'Felicidades, has minado un nuevo bloque!',
        'index': block['index'],
        'timestamp': block['timestamp'],
        'proof': block['proof'],
        'previous_hash': block['previous_hash'],
        'hash': block['hash']
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
