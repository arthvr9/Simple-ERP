import mysql.connector as mysql
import base64
import hashlib
import os

def clear():
    os.system('cls')

def conectar():
    return mysql.connect(user='root',
                         password='arthur06',
                         database='erp',
                         host='localhost')

def hash_senha(senha: str) -> str:
    # Gera o hash SHA-256 da senha
    sha256_hash = hashlib.sha256(senha.encode('utf-8')).digest()
    
    # Converte o hash para uma string base64
    base64_hash = base64.b64encode(sha256_hash).decode('utf-8')
    
    # Trunca o hash para 40 caracteres
    truncated_hash = base64_hash[:40]
    
    return truncated_hash

def registrar():
    conexao = conectar()
    cursor = conexao.cursor()
    
    try:
        indice_query = 'SELECT COUNT(*) FROM users'
        cursor.execute(indice_query)
        max_indice = cursor.fetchone()[0]
        count_rows = max_indice + 1
        
        user = input('Digite o nome de usuário: ')
        senha = input('Digite a senha: ')
        status = 'S'
        senha_hash = hash_senha(senha)
        
        comando = 'INSERT INTO users (user_id, username, password, status) VALUES (%s, %s, %s, %s)'
        cursor.execute(comando, (count_rows, user, senha_hash, status))
        conexao.commit()
    finally:
        cursor.close()
        conexao.close()

clear()
registrar()
