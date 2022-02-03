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
from flask import  Flask, jsonify

# Parte 1 - Crear la cadena de bloques

class Blockchain:
    
    def __init__(self):
        self.chain = []
        self.create_block(proof = 1, previous_hash = '0' )
        


# Parte 2 - Minado de un bloque de una cadena
