from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app) #js comunicar com o python

# Configuração do Banco de Dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:suasenha@localhost:5432/loja_camisas'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo da Camisa
class Camisa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    tamanho = db.Column(db.String(10), nullable=False)
    preco = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {"id": self.id, "nome": self.nome, "tamanho": self.tamanho, "preco": self.preco}

# Rota para Criar e Listar (Funcionalidade AC1)
@app.route('/camisas', methods=['GET', 'POST'])
def gerenciar_camisas():
    if request.method == 'POST':
        dados = request.json
        nova_camisa = Camisa(
            nome=dados['nome'], 
            tamanho=dados['tamanho'], 
            preco=dados['preco']
        )
        db.session.add(nova_camisa)
        db.session.commit()
        return jsonify({"mensagem": "Camisa cadastrada com sucesso!"}), 201
    
    # Se for GET, lista todas
    camisas = Camisa.query.all()
    return jsonify([c.to_dict() for c in camisas])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)