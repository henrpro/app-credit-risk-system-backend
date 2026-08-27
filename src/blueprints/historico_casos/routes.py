# Importações do projeto
from bll.historico_casos.tratamentos import obter_descricao_solicitacao_historico
from models.models_historico_casos import GetSolicitacoesFinalizadasModel
from services.historico_casos.insumos import InsumosHistoricoCasos
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
import pandas as pd

# Cria a blueprint
historico_casos = Blueprint('historico_casos', __name__)

# _______________________________ Rotas _______________________________

@historico_casos.route('/obtem-solicitacoes-finalizadas', methods=['GET'])
def obtem_solicitacoes_finalizadas():
    try:
        database = current_app.config['DATABASE']
        filtros = request.args.to_dict()
        mesa = filtros.get('dsProfile')
        df = InsumosHistoricoCasos.get_solicitacoes_finalizadas(database, mesa)
        dados = apply_model_dataclass(df, GetSolicitacoesFinalizadasModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter historico de solicitacoes finalizadas': str(e)}), 500


@historico_casos.route('/obtem-dados-solicitacao', methods=['GET'])
def obtem_dados_solicitacao():
    try:
        database = current_app.config['DATABASE']
        filtros = request.args.to_dict()
        id_solicitacao = filtros.get('idSolicitacao')
        detalhes = obter_descricao_solicitacao_historico(database, id_solicitacao)
        return jsonify(detalhes), 200
    except Exception as e:
        return jsonify({'Erro ao obter descricao da solicitacao no historico': str(e)}), 500
