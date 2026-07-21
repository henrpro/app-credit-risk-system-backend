# Importações do projeto
from blueprints.login.routes import login

from config.config import init_config

# Importações de bibliotecas
from flask_cors import CORS
from flask import Flask

# Instancia a aplicação
app = Flask(__name__)
CORS(app)

config = init_config()
app.secret_key = config['secret_key']
app.config['DATABASE'] = config['database']

# Registra as blueprints
app.register_blueprint(login, url_prefix='/v1/login')

# Inicia a aplicação
if __name__ == '__main__':
    app.run(debug=(config['env'] == 'dev'), host='0.0.0.0', port=config['porta'])