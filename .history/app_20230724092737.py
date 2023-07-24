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

@app.route('/livros')
def obeter_livros():
    return jsonify(livros)

app.run(port=5000, host='localhost',debug=True)