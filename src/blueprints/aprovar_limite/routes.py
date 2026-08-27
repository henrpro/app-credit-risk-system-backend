# Importações do projeto
from bll.aprovar_limite.tratamentos import obter_aprovacoes_pendentes_consolidadas, obter_detalhes_solicitacao_aprovacao, processar_decisao_limite
from models.models_aprovar_limite import GetAprovacoesPendentesModel
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
import pandas as pd

# Cria a blueprint
aprovar_limite = Blueprint('aprovar_limite', __name__)

# _______________________________ Rotas _______________________________

@aprovar_limite.route('/', methods=['GET'])
@aprovar_limite.route('/consultar-aprovacoes-pendentes', methods=['GET'])
def consultar_aprovacoes_pendentes():
    try:
        database = current_app.config['DATABASE']
        df = obter_aprovacoes_pendentes_consolidadas(database)
        dados = apply_model_dataclass(df, GetAprovacoesPendentesModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter aprovações pendentes': str(e)}), 500


@aprovar_limite.route('/obtem-dados-solicitacao', methods=['GET'])
def obtem_dados_solicitacao():
    try:
        database = current_app.config['DATABASE']
        filtros = request.args.to_dict()
        ids_solicitacao_raw = filtros.get('idSolicitacao')
        detalhes = obter_detalhes_solicitacao_aprovacao(database, ids_solicitacao_raw)
        return jsonify(detalhes), 200
    except Exception as e:
        return jsonify({'Erro ao obter detalhes da solicitação de aprovação': str(e)}), 500


@aprovar_limite.route('/aprovar-limite', methods=['POST'])
def decidir_limite():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        resultado = processar_decisao_limite(database, payload)
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'Erro ao processar aprovação do limite': str(e)}), 500
