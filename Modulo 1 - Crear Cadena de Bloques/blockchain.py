# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 21:59:54 2022

@author: Luciano
"""
# Modulo 1 - Crear una Cadena de Bloques

# Importar las librerias
import datetime
import hashlib
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

# Parte 2 - Minado de un bloque de una cadena
