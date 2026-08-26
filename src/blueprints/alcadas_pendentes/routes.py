# Importações do projeto
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request

# Cria a blueprint
alcadas_pendentes = Blueprint('alcadas_pendentes', __name__)

@alcadas_pendentes.route('/', methods=['GET'])
def fetch_alcadas_pendentes():
    pass


@alcadas_pendentes.route('/obtem-dados-solicitacao', methods=['GET'])
def obtem_dados_solicitacao():
    pass

@alcadas_pendentes.route('/responder-alcada', methods=['GET'])
def responder_alcada():
    pass