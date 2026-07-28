# Importações do projeto
from utils.api_functions import apply_model_dataclass
from services.login.insumos import InsumosLogin
from models.models_login import GetLoginModel

# Importações de bibliotecas
from typing import Tuple, Optional, Dict, Any

def autenticar_usuario(database: str, username: str, password_attempt: str) -> Tuple[bool, Optional[str]]:

    """
    Função que valida as credenciais do usuário e retorna sucesso e grupo.
    """

    # Busca os dados do usuário no banco
    dados = InsumosLogin.get_user(database, username)
    
    # Verifica se o usuário existe
    if dados.empty:
        return False, None
        
    # Aplica o modelo de dataclass
    dados_model = apply_model_dataclass(dados, GetLoginModel)
    user_data = dados_model[0].__dict__
    
    # Verifica se a senha confere
    if user_data.get('cdPassword') == password_attempt:
        return True, user_data.get('dsProfile')
    
    return False, None

def obter_dados_usuario(database: str, username: str) -> Optional[Dict[str, Any]]:

    """
    Função que obtem os dados do usuário.
    """

    # Busca os dados do usuário no banco
    dados = InsumosLogin.get_user(database, username)
    
    # Verifica se o usuário existe
    if dados.empty:
        return None
        
    # Aplica o modelo de dataclass
    dados_model = apply_model_dataclass(dados, GetLoginModel)
    user_data = dados_model[0].__dict__
    
    return user_data
