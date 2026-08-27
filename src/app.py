# Importações do projeto
from blueprints.consultar_solicitacao.routes import consultar_solicitacao
from blueprints.gestao_de_usuarios.routes import gestao_de_usuarios
from blueprints.grupos_economicos.routes import grupos_economicos
from blueprints.solicitar_alcada.routes import solicitar_alcada
from blueprints.mapeamentos.routes import mapeamentos
from blueprints.login.routes import login
from config.config import init_config

# Importações de bibliotecas
from flask_cors import CORS
from flask import Flask

# Instancia a aplicação
app = Flask(__name__)
CORS(app)

config = init_config()
app.json.ensure_ascii = False
app.config['JSON_AS_ASCII'] = False
app.secret_key = config['secret_key']
app.config['DATABASE'] = config['database']

# Registra as blueprints
app.register_blueprint(consultar_solicitacao, url_prefix='/v1/consultar-solicitacao')
app.register_blueprint(gestao_de_usuarios, url_prefix='/v1/gestao-de-usuarios')
app.register_blueprint(grupos_economicos, url_prefix='/v1/grupos-economicos')
app.register_blueprint(solicitar_alcada, url_prefix='/v1/solicitar-alcada')
app.register_blueprint(mapeamentos, url_prefix='/v1/mapeamentos')
app.register_blueprint(login, url_prefix='/v1/login')

# Inicia a aplicação
if __name__ == '__main__':
    app.run(debug=(config['env'] == 'dev'), host='0.0.0.0', port=config['porta'])