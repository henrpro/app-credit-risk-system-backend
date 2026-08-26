# Importações do projeto
from models.models_solicitar_alcada import GetTipoEventosModel, GetRatingsDistintosModel, GetLimitesGrupoEconomicoModel, GetDisponivelFlexibilizacaoModel
from bll.solicitar_alcada.tratamentos import obtem_eventos_disponiveis, realiza_insert_solicitacao_alcada
from services.solicitar_alcada.insumos import InsumosSolicitarAlcada
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request

# Cria a blueprint
solicitar_alcada = Blueprint('solicitar_alcada', __name__)

# _______________________________ Geral _______________________________

@solicitar_alcada.route('/obtem-tipos-eventos', methods=['GET'])
def obtem_tipos_eventos():
    try:
        database = current_app.config['DATABASE']
        filtros = request.args.to_dict()
        df = obtem_eventos_disponiveis(database, filtros['dsGrupo'], filtros['dsProfile'])
        dados = apply_model_dataclass(df, GetTipoEventosModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter tipos de eventos cadastrados': str(e)}), 500


@solicitar_alcada.route('/obtem-ratings-distintos', methods=['GET'])
def obtem_ratings_distintos():
    try:
        database = current_app.config['DATABASE']
        df = InsumosSolicitarAlcada.get_ratings_distintos(database)
        dados = apply_model_dataclass(df, GetRatingsDistintosModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter ratings distintos': str(e)}), 500


@solicitar_alcada.route('/limites-aprovados-grupo-economico', methods=['GET'])
def obtem_limites_aprovados_grupo_economico():
    try:
        database = current_app.config['DATABASE']
        filtros = request.args.to_dict()
        df = InsumosSolicitarAlcada.get_limites_aprovados_by_grupo(database, filtros['dsGrupo'], filtros['dsProfile'])
        dados = apply_model_dataclass(df, GetLimitesGrupoEconomicoModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter os limites aprovados para o grupo': str(e)}), 500


@solicitar_alcada.route('/disponivel-flexibilizacao-grupo-economico', methods=['GET'])
def obtem_disponivel_flexibilizacao_grupo_economico():
    try:
        database = current_app.config['DATABASE']
        filtros = request.args.to_dict()
        df = InsumosSolicitarAlcada.get_disponivel_flexibilizacao(database, filtros['dsGrupo'], filtros['dsProfile'])
        dados = apply_model_dataclass(df, GetDisponivelFlexibilizacaoModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter os limites aprovados para o grupo': str(e)}), 500

# _______________________________ Insert _______________________________

@solicitar_alcada.route('/insert-solicitacao-alcada', methods=['POST'])
def insert_solicitacao_alcada():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        realiza_insert_solicitacao_alcada(database, payload)
        return jsonify({'message': 'Solicitação de alçada recebida com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao receber solicitação de alçada': str(e)}), 500
