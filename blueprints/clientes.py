from flask import Blueprint, request, redirect, url_for, flash, render_template, jsonify
from flask_cors import *
from flask_login import login_user, login_required, current_user, LoginManager, UserMixin
import mysql.connector as mysql
import pandas as pd

def conectar():
    return mysql.connect(
        user='root',
        password='arthur06',
        database='erp',
        host='localhost'
    )
    
clientes_bp = Blueprint('clientes', __name__)

@clientes_bp.route('/clientes', methods=['GET', 'POST'])

def clientes():
    if request.method == 'POST':
        if request.form['action'] == 'criar':
            try:
                criarCliente()
            except mysql.Error as err:
                flash(err)            
            return redirect(url_for('clientes.clientes'))
        
        elif request.form['action'] == 'listar':
            try:
                listarClientes()
            except mysql.Error as err:
                flash(err)
            return redirect(url_for('clientes.clientes'))
        
        elif request.form['action'] == 'deletar':
            if deletarClientes():
                return redirect(url_for('clientes.clientes'))
            else:
                flash('Erro ao deletar cliente')
    return render_template('clientes.html')

def criarCliente():
    conexao = conectar()
    
    if request.method == 'POST':
        nome = request.form['nome']
        contato = request.form['contato']
        endereco = request.form['endereco']
        cnpj = request.form['identificador']
        pedidos = request.form['pedidos']
        
        try:
            cursor = conexao.cursor()

            cursor.execute('SELECT COUNT(*) FROM erp.clientes')
            valor = cursor.fetchone()[0] + 1
            
            comando = '''INSERT INTO erp.clientes (idcliente, nome, contato, endereco, cnpj, qtd_pedidos) 
                         VALUES (%s, %s, %s, %s, %s, %s)'''
            cursor.execute(comando, (valor, nome, contato, endereco, cnpj, pedidos))
            conexao.commit()
            return True
        except mysql.Error as e:
            print(e)
            return False
        finally:
            flash('Cliente cadastrado com sucesso!')
            cursor.close()
            conexao.close()

def listarClientes():
    
    conexao = conectar()    
    if request.method == 'GET':
        try:
            cursor = conexao.cursor()
            comando = '''SELECT nome, contato, endereco, cnpj, qtd_pedidos FROM erp.clientes'''
            cursor.execute(comando)
            valores = cursor.fetchall()
            separado = pd.DataFrame(valores, columns=['nome', 'contato', 'endereco', 'identificador', 'pedidos'])
            print(separado)
            return separado
        except mysql.Error as e:
            print(e)
            return False
        finally:
            cursor.close()
        
def deletarClientes():
    conexao = conectar()
    
    info = ...
    
    try:
        cursor = conexao.cursor()
        comando = '''DELETE FROM erp.clientes WHERE nome = %s'''
        cursor.execute(comando, (info))
        conexao.commit()
        return True
    except mysql.Error as e:
        print(e)
        return False
    finally:
        cursor.close()
        
        

    