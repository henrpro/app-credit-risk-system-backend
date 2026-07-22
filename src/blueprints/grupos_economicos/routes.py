# Importações do projeto
from bll.login.tratamentos import autenticar_usuario, obter_dados_usuario

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
from typing import Tuple, Any

# Cria a blueprint
grupos_economicos = Blueprint('grupos_economicos', __name__)

