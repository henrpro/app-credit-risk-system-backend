# Importações do projeto
from models.models_gestao_de_usuarios import GetUsuariosCadastradosModel, GetUsuariosModel
from bll.gestao_de_usuarios.tratamentos import realizar_cadastro_usuario
from services.gestao_de_usuarios.insumos import InsumosGestaoUsuarios
from utils.api_functions import apply_model_dataclass

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
import pandas as pd

# Cria a blueprint
gestao_de_usuarios = Blueprint('gestao_de_usuarios', __name__)

# _______________________________ Rotas _______________________________

@gestao_de_usuarios.route('/consultar-usuarios-cadastrados', methods=['GET'])
def consultar_usuarios_cadastrados():
    try:
        database = current_app.config['DATABASE']
        df = InsumosGestaoUsuarios.get_usuarios_cadastrados(database)
        dados = apply_model_dataclass(df, GetUsuariosCadastradosModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao obter usuarios cadastrados': str(e)}), 500


@gestao_de_usuarios.route('/consultar-usuario', methods=['GET'])
def consultar_usuario():
    try:
        database = current_app.config['DATABASE']
        filtros = request.args.to_dict()
        df = InsumosGestaoUsuarios.get_usuario(database, filtros['cdUser'])
        dados = apply_model_dataclass(df, GetUsuariosModel)
        return jsonify([ob.__dict__ for ob in dados])
    except Exception as e:
        return jsonify({'Erro ao consultar usuario': str(e)}), 500


@gestao_de_usuarios.route('/cadastrar-usuario', methods=['POST'])
def cadastrar_usuario():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        realizar_cadastro_usuario(database, payload)
        return jsonify({'message': 'Usuário cadastrado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao cadastrar usuario': str(e)}), 500


@gestao_de_usuarios.route('/deletar-usuario', methods=['POST'])
def deletar_usuario():
    try:
        database = current_app.config['DATABASE']
        payload = request.json
        InsumosGestaoUsuarios.execute_delete_usuario(database, payload.get('cdUser'))
        return jsonify({'message': 'Usuário deletado com sucesso.'}), 200
    except Exception as e:
        return jsonify({'Erro ao deletar usuario': str(e)}), 500
