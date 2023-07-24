from flask import Flask, jsonify, request
import mysql.connector
from flask_cors import CORS  # Importe a classe CORS da extensão Flask-CORS

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

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
