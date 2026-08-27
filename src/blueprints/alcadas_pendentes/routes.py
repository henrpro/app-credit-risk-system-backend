# Importações do projeto
from bll.alcadas_pendentes.tratamentos import obter_alcadas_pendentes_consolidadas, obter_detalhes_alcada, realizar_resposta_alcada
from models.models_alcadas_pendentes import GetAlcadasPendentesModel
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
import pandas as pd

# Cria a blueprint
alcadas_pendentes = Blueprint('alcadas_pendentes', __name__)

# _______________________________ Rotas _______________________________

@alcadas_pendentes.route('/', methods=['GET'])
@alcadas_pendentes.route('/consultar-alcadas-pendentes', methods=['GET'])
def fetch_alcadas_pendentes():
    try:
        database = current_app.config['DATABASE']
        df = obter_alcadas_pendentes_consolidadas(database)
        dados = apply_model_dataclass(df, GetAlcadasPendentesModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter alçadas pendentes': str(e)}), 500


@alcadas_pendentes.route('/obtem-dados-solicitacao', methods=['GET'])
def obtem_dados_solicitacao():
    try:
        database = current_app.config['DATABASE']
        filtros = request.args.to_dict()
        ids_solicitacao_raw = filtros.get('idSolicitacao')
        detalhes = obter_detalhes_alcada(database, ids_solicitacao_raw)
        return jsonify(detalhes), 200
    except Exception as e:
        return jsonify({'Erro ao obter detalhes da solicitação de alçada': str(e)}), 500


@alcadas_pendentes.route('/responder-alcada', methods=['POST'])
def responder_alcada():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        realizar_resposta_alcada(database, payload)
        return jsonify({'message': 'Resposta de alçada registrada com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao responder alçada': str(e)}), 500