import mysql.connector as mysql
import os

def clear():
    os.system('cls')

def conectar():
    return mysql.connect(user='root',
                         password='arthur06',
                         database='erp',
                         host='localhost')

def desabilitar():
    conexao = conectar()
    cursor = conexao.cursor()
    
    try:
        user = input('Digite o nome de usuário: ')
        
        comando = 'SELECT * FROM users WHERE username = %s'
        cursor.execute(comando, (user,))
        resultado = cursor.fetchone()
        
        if not resultado:
            print('Usuário não encontrado')
            return
        
        comando = 'UPDATE users SET status = %s WHERE username = %s'
        cursor.execute(comando, ('N', user))
        conexao.commit()
        print("Usuário desativado com sucesso!")

    finally:
        cursor.close()
        conexao.close()
        
clear()
desabilitar()