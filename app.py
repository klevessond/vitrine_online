from flask import Flask, render_template
from models import db, Produto
import os

app = Flask(__name__)

# Configuração da base de dados PostgreSQL. O Render injeta o DATABASE_URL automaticamente.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Cria as tabelas automaticamente (útil para o ambiente de testes e primeira execução)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # O Controlador consulta o Modelo de Dados
    cupcakes = Produto.query.all()
    # O Controlador envia a resposta para a View
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/carrinho')
def carrinho():
    return render_template('carrinho.html')

@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

if __name__ == '__main__':
    app.run(debug=True)