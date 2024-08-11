from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from flask_cors import *
import hashlib
import base64
from flask_login import login_user, login_required, current_user, LoginManager, UserMixin
import mysql.connector as mysql

def conectar():
    return mysql.connect(user='root',
                         password='arthur06',
                         database='erp',
                         host='localhost')

main_bp = Blueprint('main', __name__)

class User(UserMixin):  # Classe para verificar se o usuário está logado
    def __init__(self, user_id):
        self.id = user_id

# Configurar o LoginManager
login_manager = LoginManager()

# Inicializar o pool de conexões global
pool = conectar()

def hash_password(password: str) -> str:
    # Gera o hash SHA-256 da senha
    sha256_hash = hashlib.sha256(password.encode('utf-8')).digest()
    # Converte o hash para uma string base64
    base64_hash = base64.b64encode(sha256_hash).decode('utf-8')
    # Trunca o hash para 40 caracteres
    truncated_hash = base64_hash[:40]
    return truncated_hash

def verificar(username: str, senha: str) -> bool:
    conexao = pool
    try:
        cursor = conexao.cursor()
        comando = '''SELECT password FROM erp.users WHERE username = %s AND STATUS = 'S' '''
        cursor.execute(comando, (username,))
        resultado = cursor.fetchone()

        if resultado:
            senha_hash = resultado[0]  # Puxa o primeiro resultado da query do banco de dados
            novo_hash = hash_password(senha)  # Cria um novo hash com a senha digitada pelo usuário
            return novo_hash == senha_hash  # Compara os dois hashes
        return False
    finally:
        cursor.close()

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@main_bp.route('/', methods=['GET', 'POST'])  # Página padrão do site
def login():
    if request.method == 'POST':
        usuario = request.form['username']
        password = request.form['password']

        if verificar(usuario, password):
            user = User(usuario)
            login_user(user)
            return redirect(url_for('main.success'))
        else:
            return redirect(url_for('main.failure'))

    return render_template('index.html')

@main_bp.route('/clientes')
@login_required  # Exige que o usuário esteja logado para acessar a página
def success():
    return render_template('clientes.html')

@main_bp.route('/failure')
def failure():
    return render_template('failure.html')
