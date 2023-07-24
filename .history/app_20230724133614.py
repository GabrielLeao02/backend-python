from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

conexao = mysql.connector.connect(
    host='127.0.0.1',
    user='root',
    password='',
    database='sistema',
)
cursor = conexao.cursor()

@app.route('/salvarusuario', methods=['POST'])
def incluir_novo_usuario():
    usuario = request.get_json()
    # comando = "INSERT INTO `sys_usuarios` (`usuario_id`, `usuario_nome`, `usuario_cpf`, `usuario_email`, `usuario_senha`) VALUES (NULL, %s, %s, %s, %s)"
    # valores = (usuario['usuario_nome'], usuario['usuario_cpf'], usuario['usuario_email'], usuario['usuario_senha'])
    
    # cursor.execute(comando, valores)
    # conexao.commit()  # Importante fazer o commit após a execução da inserção
    return jsonify(usuario['nome'])

@app.teardown_appcontext
def fechar_conexao(error):
    cursor.close()
    conexao.close()

if __name__ == '__main__':
    app.run(port=5000, host='localhost', debug=True)
