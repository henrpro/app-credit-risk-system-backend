# Importações do projeto
from bll.login.tratamentos import autenticar_usuario, obter_dados_usuario

# Importações de bibliotecas
from flask import Blueprint, jsonify, current_app, request
from typing import Tuple, Any

# Cria a blueprint
login = Blueprint('login', __name__)

@login.route('/authenticate', methods=['POST'])
def authenticate() -> Tuple[Any, int]:
    try:
        data = request.form.to_dict()
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({"error": "Usuario e senha sao obrigatorios"}), 400
            
        username = data['username']
        password = data['password']
        
        # Obtem o banco de dados
        database = current_app.config['DATABASE']
        
        # Chama a BLL para autenticar
        sucesso, grupo = autenticar_usuario(database, username, password)
        
        if sucesso:
            return jsonify({"success": True, "dsProfile": grupo}), 200
        else:
            return jsonify({"success": False, "message": "Usuario ou senha invalidos"}), 401
            
    except Exception as e:
        return jsonify({'Erro ao autenticar': str(e)}), 500

@login.route('/<username>', methods=['GET'])
def get_user(username: str) -> Tuple[Any, int]:
    try:
        # Obtem o banco de dados
        database = current_app.config['DATABASE']
        
        # Chama a BLL para obter os dados
        user_data = obter_dados_usuario(database, username)
        
        # Retorna o resultado
        if not user_data:
            return jsonify({"error": "Usuario nao encontrado"}), 404
            
        return jsonify(user_data), 200
        
    except Exception as e:
        return jsonify({'Erro ao obter os dados de login': str(e)}), 500
