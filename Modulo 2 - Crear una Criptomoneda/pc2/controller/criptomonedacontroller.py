# Importar las librerias
import http
from flask import Flask, jsonify, request
from uuid import uuid4
from service.criptomonedaservice import *

# Parte 2 - Minado de un bloque de una cadena

# Crear una aplicación web

# Creo una instancia de flask para crear una app web
app = Flask(__name__)
# Crear la dirección del nodo en el puerto 5000
node_address = str(uuid4()).replace('-', '')
# Crear una blockchain

# Creo una instancia de una cadena de bloques
blockchain = CriptomonedaService()


# Minar un nuevo bloque
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = previous_block['hash']
    index_block = blockchain.add_transactions(sender=node_address, receiver='Camila Pulido', amount=10)
    block = blockchain.create_block(proof, previous_hash)
    return block, http.HTTPStatus.OK


# Obtener la cadena de bloques completa
@app.route('/get_chain', methods=['GET'])
def get_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return response, http.HTTPStatus.OK


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
    return response, http.HTTPStatus.OK


@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json = request.get_json()
    transaction_keys = ['sender', 'receiver', 'amount']

    if not all(key in json for key in transaction_keys):
        return 'Faltan algunos elementos de la transacción', http.HTTPStatus.NOT_FOUND
    index = blockchain.add_transactions(json['sender'], json['receiver'], json['amount'])
    response = {
        'message': f'La transacción será añadida al bloque {index}'
    }
    return response, http.HTTPStatus.CREATED


# Parte 3 - Descentralizar la Cadena de Bloques

# Conectar Nuevos Nodos
@app.route('/connect_node', methods=['POST'])
def connect_node():
    json = request.get_json()
    nodes = json.get('nodes')
    if nodes is None:
        return 'No hay nodos para añadir', http.HTTPStatus.NOT_FOUND

    for node in nodes:
        blockchain.add_node(node)

    response = {
        'message': 'Todos los nodos han sido Conectados. La cadena de bloques de la criptomoneda '
                   'contiene ahora los nodos siguientes',
        'nodes': list(blockchain.nodes)
    }
    return response, http.HTTPStatus.CREATED


# Remplazar la cadena por la más larga (si es necesario)
@app.route('/replace_chain', methods=['GET'])
def replace_chain():
    is_chain_replace = blockchain.replace_chain()
    if is_chain_replace:
        response = {
            'message': 'Los nodos tenían diferentes cadenas, que han sido remplazadas por la más larga.',
            'new_chain': blockchain.chain}
    else:
        response = {
            'message': 'Todo Correcto. La cadena en todos los nodos ya es la más larga',
            'current_chain': blockchain.chain}
    return response, http.HTTPStatus.OK


# Ejecutar la app
app.run(host='0.0.0.0', port=5002)
