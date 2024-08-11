from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from flask_cors import *
from flask_login import login_user, login_required, current_user, LoginManager, UserMixin
import mysql.connector as mysql

def conectar():
    return mysql.connect(
        user='root',
        password='arthur06',
        database='erp',
        host='localhost'
    )
    
clientes_bp = Blueprint('clientes', __name__)

def criarCliente(nome, contato, endereco, cep, cnpj):
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        comando = '''INSERT INTO erp.clientes (nome, contato, endereco, cep, cnpj) VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(comando, (nome, contato, endereco, cep, cnpj))
        conexao.commit()
        return True
    except mysql.Error as e:
        print(e)
        return False
    finally:
        cursor.close()

def listarClientes():
    conexao = conectar()
    try:
        cursor = conexao.cursor()
        comando = '''SELECT nome, contato, endereco FROM erp.clientes'''
        cursor.execute(comando)
        valores = cursor.fetchall()
        return valores
    except mysql.Error as e:
        print(e)
        return False
    finally:
        cursor.close()

    