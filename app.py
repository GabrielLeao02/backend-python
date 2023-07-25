from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS  # Importe a classe CORS da extensão Flask-CORS
import bcrypt

app = Flask(__name__)
CORS(app)  # Adicione CORS ao seu aplicativo Flask

def criar_conexao():
    return mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='',
        database='sistema',
    )

@app.route('/salvarusuario', methods=['POST'])
def incluir_novo_usuario():
    try:
        conexao = criar_conexao()
        cursor = conexao.cursor()

        usuario = request.get_json()
        usuario_senha = usuario['usuario_senha']

        # Criptografe a senha usando bcrypt
        hashed_senha = bcrypt.hashpw(usuario_senha.encode('utf-8'), bcrypt.gensalt())

        # Substitua a senha original pela senha criptografada
        usuario['usuario_senha'] = hashed_senha.decode('utf-8')

        comando = "INSERT INTO `sys_usuarios` (`usuario_id`, `usuario_nome`, `usuario_cpf`, `usuario_email`, `usuario_senha`) VALUES (NULL, %s, %s, %s, %s)"
        valores = (usuario['usuario_nome'], usuario['usuario_cpf'], usuario['usuario_email'], usuario['usuario_senha'])

        cursor.execute(comando, valores)
        conexao.commit()
        cursor.close()

        return jsonify(usuario)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        conexao.close()

@app.route('/login', methods=['POST'])
def login_usuario():
    try:
        conexao = criar_conexao()
        cursor = conexao.cursor()

        usuario = request.get_json()
        email = usuario['usuario_email']
        senha_criptografada_frontend = usuario['usuario_senha']

        # Recupere a hash salgada do banco de dados para o usuário com o e-mail fornecido
        comando = "SELECT usuario_senha FROM sys_usuarios WHERE usuario_email = %s"
        cursor.execute(comando, (email,))
        resultado = cursor.fetchone()

        if resultado is not None:
            # Recupere a hash salgada armazenada no banco de dados
            senha_salgada_bd = resultado[0]

            # Verifique se a senha criptografada do frontend corresponde à hash salgada do banco de dados
            if bcrypt.checkpw(senha_criptografada_frontend.encode('utf-8'), senha_salgada_bd.encode('utf-8')):
                return jsonify({'message': 'Login com sucesso'}), 200
            else:
                return jsonify({'message': 'Senha incorreta'}), 401
        else:
            return jsonify({'message': 'Usuário não encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:    
        conexao.close()


if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)