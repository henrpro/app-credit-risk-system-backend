# Importações do projeto
from models.models_grupos_economicos import GetSetoresModel, GetSubsetoresModel, GetGruposEconomicosDistintosModel, GetEmissoresOC3Model, GetEmissoresCRIMSModel, GetGruposEconomicosModel
from bll.grupos_economicos.tratamentos import obtem_grupo_economico, cadastrar_novo_grupo_economico, update_grupo_economico
from services.grupos_economicos.insumos import InsumosGruposEconomicos
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
import pandas as pd

# Cria a blueprint
grupos_economicos = Blueprint('grupos_economicos', __name__)

# _______________________________ Geral _______________________________

@grupos_economicos.route('/obtem-grupos-economicos-cadastrados', methods=['GET'])
def obtem_grupos_economicos_cadastrados():
    try:
        database = current_app.config['DATABASE']
        df = InsumosGruposEconomicos.get_grupos_economicos_distintos(database)
        dados = apply_model_dataclass(df, GetGruposEconomicosDistintosModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter grupos economicos cadastrados': str(e)}), 500


@grupos_economicos.route('/obtem-setores-cadastrados', methods=['GET'])
def obtem_setores_cadastrados():
    try:
        database = current_app.config['DATABASE']
        df = InsumosGruposEconomicos.get_setores_distintos(database)
        dados = apply_model_dataclass(df, GetSetoresModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter setores cadastrados': str(e)}), 500


@grupos_economicos.route('/obtem-subsetores-cadastrados', methods=['GET'])
def obtem_subsetores_cadastrados():
    try:
        database = current_app.config['DATABASE']
        df = InsumosGruposEconomicos.get_subsetores_distintos(database)
        dados = apply_model_dataclass(df, GetSubsetoresModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter subsetores cadastrados': str(e)}), 500

# _______________________________ Cadastrar Grupo _______________________________

@grupos_economicos.route('/obtem-emissores-oc3', methods=['GET'])
def obtem_emissores_oc3():
    try:
        filtros = request.args.to_dict()
        # df = InsumosGruposEconomicos.get_codigo_emissor_oc3(filtros['dsEmissor'])
        df = pd.DataFrame({
            'cdCnpj': ['12.345.678/0001-95', '98.765.432/0001-09', '11.223.344/0001-55', '55.443.322/0001-88'],
            'cdEmissor': ['RUMO', 'GASC', 'COSAN', 'TESOURO'],
            'dsEmissor': ['Rumo S.A.', 'Comgas', 'Cosan S.A.', 'Tesouro Nacional']
        })
        dados = apply_model_dataclass(df, GetEmissoresOC3Model)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter os emissores OC3': str(e)}), 500
    

@grupos_economicos.route('/obtem-emissores-crims', methods=['GET'])
def obtem_emissores_crims():
    try:
        filtros = request.args.to_dict()
        # df = InsumosGruposEconomicos.get_codigo_emissor_crims(filtros['dsEmissor'])
        df = pd.DataFrame({
            'cdCnpj': ['12.345.678/0001-95', '98.765.432/0001-09', '11.223.344/0001-55', '55.443.322/0001-88'],
            'cdEmissor': ['RUMO', 'GASC', 'COSAN', 'TESOURO'],
            'dsEmissor': ['Rumo S.A.', 'Comgas', 'Cosan S.A.', 'Tesouro Nacional']
        })
        dados = apply_model_dataclass(df, GetEmissoresCRIMSModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter os emissores CRIMS': str(e)}), 500


@grupos_economicos.route('/registrar-grupo-economico', methods=['POST'])
def registrar_grupo_economico():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        cadastrar_novo_grupo_economico(database, payload)
        return jsonify({'message': 'Grupo econômico registrado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao registrar novo grupo economico': str(e)}), 500

# _______________________________ Consultar Grupo _______________________________

@grupos_economicos.route('/consultar-grupo-conomico', methods=['GET'])
def consultar_grupo_economico():
    try:
        database = current_app.config['DATABASE']
        filtros = request.args.to_dict()
        df = obtem_grupo_economico(database, filtros['dsGrupo'])
        dados = apply_model_dataclass(df, GetGruposEconomicosModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao consultar grupo economico': str(e)}), 500

# _______________________________ Atualizar Grupo _______________________________

@grupos_economicos.route('/atualizar-grupo-economico', methods=['POST'])
def atualizar_grupo_economico():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        update_grupo_economico(database, payload)
        return jsonify({'message': 'Grupo econômico atualizado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao atualizar cadastro do grupo economico': str(e)}), 500

# _______________________________ Deletar Grupo _______________________________

@grupos_economicos.route('/deletar-grupo-economico', methods=['POST'])
def deletar_grupo_economico():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        InsumosGruposEconomicos.deletar_grupo_completo(database, payload.get('idGrupo'))
        return jsonify({'message': 'Grupo econômico deletado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao deletar grupo economico': str(e)}), 500