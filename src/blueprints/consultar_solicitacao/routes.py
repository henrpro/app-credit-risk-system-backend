# Importações do projeto
from models.models_consultar_solicitacao import GetSolicitacoesPendentesModel
from services.consultar_solicitacao.insumos import InsumosConsultarSolicitacao
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
import pandas as pd

# Cria a blueprint
consultar_solicitacao = Blueprint('consultar_solicitacao', __name__)

# _______________________________ Rotas _______________________________

@consultar_solicitacao.route('/obtem-solicitacoes-pendentes', methods=['GET'])
def obtem_solicitacoes_pendentes():
    try:
        database = current_app.config['DATABASE']
        filtros = request.args.to_dict()
        mesa = filtros.get('mesa') or filtros.get('dsProfile')
        df = InsumosConsultarSolicitacao.get_solicitacoes_pendentes(database, mesa)
        dados = apply_model_dataclass(df, GetSolicitacoesPendentesModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter solicitacoes pendentes': str(e)}), 500


@consultar_solicitacao.route('/atualizar-status-aprovacao-pendente', methods=['POST'])
def atualizar_status_aprovacao_pendente():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        id_solicitacao = payload.get('idSolicitacao')
        InsumosConsultarSolicitacao.execute_update_status_aprovacao_pendente(database, id_solicitacao)
        return jsonify({'message': 'Status da solicitação atualizado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao atualizar status da solicitacao': str(e)}), 500
