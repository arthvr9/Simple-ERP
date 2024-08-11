from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager

app = Flask(__name__, template_folder='templates')
CORS(app)
app.secret_key = 'ERP'

login_manager = LoginManager()
login_manager.login_view = 'main.login'
login_manager.init_app(app)

# Certifique-se de que a classe User e o blueprint sejam importados corretamente
from blueprints.main import main_bp, User
from blueprints.clientes import clientes_bp

# Registrar o Blueprint na aplicação Flask
app.register_blueprint(main_bp, url_prefix='/')
app.register_blueprint(clientes_bp, url_prefix='/clientes')

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
