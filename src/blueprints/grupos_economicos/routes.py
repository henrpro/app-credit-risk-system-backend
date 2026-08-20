# Importações do projeto
from bll.grupos_economicos.tratamentos import obtem_setores_distintos, obtem_subsetores_distintos, obtem_grupos_economicos_distintos, obtem_codigo_emissor_oc3, obtem_codigo_emissor_crims
from models.models_grupos_economicos import GetSetoresModel, GetSubsetoresModel, GetGruposEconomicosDistintosModel, GetEmissoresOC3Model, GetEmissoresCRIMSModel
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request

# Cria a blueprint
grupos_economicos = Blueprint('grupos_economicos', __name__)

@grupos_economicos.route('/obtem-setores-cadastrados', methods=['GET'])
def obtem_setores_cadastrados():
    try:
        database = current_app.config['DATABASE']
        df = obtem_setores_distintos(database)
        dados = apply_model_dataclass(df, GetSetoresModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter setores cadastrados': str(e)}), 500


@grupos_economicos.route('/obtem-subsetores-cadastrados', methods=['GET'])
def obtem_subsetores_cadastrados():
    try:
        database = current_app.config['DATABASE']
        df = obtem_subsetores_distintos(database)
        dados = apply_model_dataclass(df, GetSubsetoresModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter subsetores cadastrados': str(e)}), 500


@grupos_economicos.route('/obtem-grupos-economicos-cadastrados', methods=['GET'])
def obtem_grupos_economicos_cadastrados():
    try:
        database = current_app.config['DATABASE']
        df = obtem_grupos_economicos_distintos(database)
        dados = apply_model_dataclass(df, GetGruposEconomicosDistintosModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter grupos economicos cadastrados': str(e)}), 500


@grupos_economicos.route('/obtem-emissores-oc3', methods=['GET'])
def obtem_emissores_oc3():
    try:
        filtros = request.args.to_dict()
        df = obtem_codigo_emissor_oc3(filtros['dsEmissor'])
        dados = apply_model_dataclass(df, GetEmissoresOC3Model)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter os emissores OC3': str(e)}), 500

    
@grupos_economicos.route('/obtem-emissores-crims', methods=['GET'])
def obtem_emissores_crims():
    try:
        filtros = request.args.to_dict()
        df = obtem_codigo_emissor_crims(filtros['dsEmissor'])
        dados = apply_model_dataclass(df, GetEmissoresCRIMSModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter os emissores CRIMS': str(e)}), 500


@grupos_economicos.route('/consultar-grupo-conomico', methods=['POST'])
def consultar_grupo_economico():
    try:
        pass
            
    except Exception as e:
        return jsonify({'Erro ao consultar novo grupo economico': str(e)}), 500

    
@grupos_economicos.route('/registrar-grupo-economico', methods=['POST'])
def registrar_grupo_economico():
    try:
        pass
            
    except Exception as e:
        return jsonify({'Erro ao registrar novo grupo economico': str(e)}), 500


@grupos_economicos.route('/atualizar-grupo-economico', methods=['POST'])
def atualizar_grupo_economico():
    try:
        pass
            
    except Exception as e:
        return jsonify({'Erro ao atualizar cadastro do grupo economico': str(e)}), 500


@grupos_economicos.route('/deletar-grupo-economico', methods=['POST'])
def deletar_grupo_economico():
    try:
        pass
            
    except Exception as e:
        return jsonify({'Erro ao deletar grupo economico': str(e)}), 500