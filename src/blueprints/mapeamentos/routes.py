# Importações do projeto
from models.models_mapeamentos import GetMapeamentoManagersModel, GetManagersSemMapeamentoModel, GetMapeamentoProdutosModel, GetProdutosSemMapeamentoModel, GetMapeamentoAtivosModel, GetAtivosSemMapeamentoModel, GetEmissoresCadastradosModel

from bll.mapeamentos.tratamentos import salvar_mapeamento_manager, deletar_mapeamento_manager, salvar_mapeamento_produto, deletar_mapeamento_produto, salvar_mapeamento_ativo, deletar_mapeamento_ativo
from services.mapeamentos.insumos import InsumosMapeamentos
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
import pandas as pd

# Cria a blueprint
mapeamentos = Blueprint('mapeamentos', __name__)

# ________________________________ Mapeamento Managers ______________________________

@mapeamentos.route('/consultar-mapeamentos-managers', methods=['GET'])
def consultar_mapeamentos_managers():
    try:
        database = current_app.config['DATABASE']
        df = InsumosMapeamentos.get_mapeamento_managers(database)
        dados = apply_model_dataclass(df, GetMapeamentoManagersModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter mapeamentos de managers': str(e)}), 500


@mapeamentos.route('/consultar-managers-sem-mapeamento', methods=['GET'])
def consultar_managers_sem_mapeamento():
    try:
        database = current_app.config['DATABASE']
        df = InsumosMapeamentos.get_managers_sem_mapeamento(database)
        dados = apply_model_dataclass(df, GetManagersSemMapeamentoModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter managers sem mapeamento': str(e)}), 500


@mapeamentos.route('/salvar-mapeamento-manager', methods=['POST'])
def salvar_manager():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        salvar_mapeamento_manager(database, payload)
        return jsonify({'message': 'Mapeamento de manager salvo com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao salvar mapeamento de manager': str(e)}), 500


@mapeamentos.route('/deletar-mapeamento-manager', methods=['POST'])
def deletar_manager():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        deletar_mapeamento_manager(database, payload)
        return jsonify({'message': 'Mapeamento de manager deletado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao deletar mapeamento de manager': str(e)}), 500


# ________________________________ Mapeamento Tipo Produto ______________________________

@mapeamentos.route('/consultar-mapeamentos-produtos', methods=['GET'])
def consultar_mapeamentos_produtos():
    try:
        database = current_app.config['DATABASE']
        df = InsumosMapeamentos.get_mapeamento_produtos(database)
        dados = apply_model_dataclass(df, GetMapeamentoProdutosModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter mapeamentos de produtos': str(e)}), 500


@mapeamentos.route('/consultar-produtos-sem-mapeamento', methods=['GET'])
def consultar_produtos_sem_mapeamento():
    try:
        database = current_app.config['DATABASE']
        df = InsumosMapeamentos.get_produtos_sem_mapeamento(database)
        dados = apply_model_dataclass(df, GetProdutosSemMapeamentoModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter produtos sem mapeamento': str(e)}), 500


@mapeamentos.route('/salvar-mapeamento-produto', methods=['POST'])
def salvar_produto():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        salvar_mapeamento_produto(database, payload)
        return jsonify({'message': 'Mapeamento de produto salvo com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao salvar mapeamento de produto': str(e)}), 500


@mapeamentos.route('/deletar-mapeamento-produto', methods=['POST'])
def deletar_produto():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        deletar_mapeamento_produto(database, payload)
        return jsonify({'message': 'Mapeamento de produto deletado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao deletar mapeamento de produto': str(e)}), 500


# ________________________________ Mapeamento Ativo Consumo ______________________________

@mapeamentos.route('/consultar-mapeamentos-ativos', methods=['GET'])
def consultar_mapeamentos_ativos():
    try:
        database = current_app.config['DATABASE']
        df = InsumosMapeamentos.get_mapeamento_ativos(database)
        dados = apply_model_dataclass(df, GetMapeamentoAtivosModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter mapeamentos de ativos': str(e)}), 500


@mapeamentos.route('/consultar-ativos-sem-mapeamento', methods=['GET'])
def consultar_ativos_sem_mapeamento():
    try:
        database = current_app.config['DATABASE']
        df = InsumosMapeamentos.get_ativos_sem_mapeamento(database)
        dados = apply_model_dataclass(df, GetAtivosSemMapeamentoModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter ativos sem mapeamento': str(e)}), 500


@mapeamentos.route('/consultar-emissores-cadastrados', methods=['GET'])
def consultar_emissores_cadastrados():
    try:
        database = current_app.config['DATABASE']
        df = InsumosMapeamentos.get_emissores_cadastrados(database)
        dados = apply_model_dataclass(df, GetEmissoresCadastradosModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter emissores cadastrados': str(e)}), 500


@mapeamentos.route('/salvar-mapeamento-ativo', methods=['POST'])
def salvar_ativo():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        salvar_mapeamento_ativo(database, payload)
        return jsonify({'message': 'Mapeamento de ativo salvo com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao salvar mapeamento de ativo': str(e)}), 500


@mapeamentos.route('/deletar-mapeamento-ativo', methods=['POST'])
def deletar_ativo():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        deletar_mapeamento_ativo(database, payload)
        return jsonify({'message': 'Mapeamento de ativo deletado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao deletar mapeamento de ativo': str(e)}), 500
