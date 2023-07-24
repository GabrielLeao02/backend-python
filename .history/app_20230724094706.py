from flask import Flask, jsonify, request

app = Flask(__name__)

livros = [
    {
        'id': 1,
        'titulo': 'Livro 1', 
        'autor': 'autor livro 1',
        
    },
    {
        'id': 2,
        'titulo': 'Livro 2', 
        'autor': 'autor livro 2',
        
    },
    {
        'id': 3,
        'titulo': 'Livro 3', 
        'autor': 'autor livro 3',
        
    }
]

@app.route('/livros', methods=['GET'])
def obeter_livros():
    return jsonify(livros)

@app.route('/livros/<int:id>', methods=['GET'])
def obter_livro_por_id(id):
    for livro in livros:
        if livro.get('id') ==  id:
            return jsonify(livro)

@app.route('/livros/<int:id>', methods=['PUT'])
def editar_livro_por_id(id):
    livro_alterado = request.get_json()
    for indice, livro in enumerate(livros):
        if livro.get('id') == id:
            livros[indice].update(livro_alterado)
            return jsonify(livros[indice])

app.run(port=5000, host='localhost',debug=True)