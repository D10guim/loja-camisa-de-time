import os
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Diocli2021@localhost/loja_camisas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Camisa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100))
    tamanho = db.Column(db.String(10))
    preco = db.Column(db.Float)
    imagem_url = db.Column(db.String(255))

    # O to_dict PRECISA estar indentado dentro da classe
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "tamanho": self.tamanho,
            "preco": self.preco,
            "imagem": self.imagem_url
        }

@app.route('/uploads/<filename>')
def servir_imagem(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/camisas', methods=['GET', 'POST'])
def gerenciar_camisas():
    if request.method == 'POST':
        # --- CORREÇÃO: Pegando os dados do formulário ---
        nome = request.form.get('nome')
        tamanho = request.form.get('tamanho')
        preco = request.form.get('preco')
        foto = request.files.get('foto') 
        
        url_foto = None
        if foto and foto.filename != '':
            nome_arquivo = secure_filename(foto.filename)
            caminho_salvamento = os.path.join(app.config['UPLOAD_FOLDER'], nome_arquivo)
            foto.save(caminho_salvamento)
            url_foto = f"http://127.0.0.1:5000/uploads/{nome_arquivo}"

        # Salva no MySQL
        nova_camisa = Camisa(
            nome=nome, 
            tamanho=tamanho, 
            preco=float(preco) if preco else 0.0, 
            imagem_url=url_foto
        )
        db.session.add(nova_camisa)
        db.session.commit()
        
        return jsonify({"mensagem": "Camisa cadastrada com sucesso!"}), 201
    
    # Se for GET, retorna a lista para o catálogo
    camisas = Camisa.query.all()
    return jsonify([c.to_dict() for c in camisas])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)