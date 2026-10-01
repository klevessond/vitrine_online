from flask import Flask, render_template, session, redirect, url_for
from models import db, Produto
import os

app = Flask(__name__)

# Configuração da base de dados PostgreSQL. O Render injeta o DATABASE_URL automaticamente.
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Cria as tabelas automaticamente (útil para o ambiente de testes e primeira execução)
# Cria as tabelas automaticamente
# Cria as tabelas e insere os dados
with app.app_context():
    # Remove as tabelas antigas para limpar os links desconfigurados (usar apenas em fase de testes)
    db.drop_all() 
    db.create_all()
    
    # Insere os cupcakes apontando para a pasta /static/imagens/
    if not Produto.query.first():
        cupcake1 = Produto(nome="Red Velvet", descricao="Delicioso cupcake vermelho", preco=12.00, imagem_url="/static/imagens/red-velvet.jpg")
        cupcake2 = Produto(nome="Duplo Chocolate", descricao="Massa e cobertura de chocolate", preco=10.00, imagem_url="/static/imagens/chocolate.jpg")
        cupcake3 = Produto(nome="Limão Siciliano", descricao="Toque cítrico e refrescante", preco=11.00, imagem_url="/static/imagens/limao.jpg")
        
        db.session.add_all([cupcake1, cupcake2, cupcake3])
        db.session.commit()
@app.route('/')
def index():
    # O Controlador consulta o Modelo de Dados
    cupcakes = Produto.query.all()
    # O Controlador envia a resposta para a View
    return render_template('index.html', cupcakes=cupcakes)

@app.route('/adicionar/<int:id_produto>')
def adicionar(id_produto):
    # Cria um carrinho vazio na sessão, se não existir
    if 'carrinho' not in session:
        session['carrinho'] = []
    
    # Adiciona o ID do produto ao carrinho
    carrinho_atual = session['carrinho']
    carrinho_atual.append(id_produto)
    session['carrinho'] = carrinho_atual
    
    return redirect(url_for('carrinho'))

@app.route('/carrinho')
def carrinho():
    itens_no_carrinho = []
    total = 0
    
    # Se houver itens na sessão, procura-os na base de dados
    if 'carrinho' in session and session['carrinho']:
        for id_prod in session['carrinho']:
            produto = Produto.query.get(id_prod)
            if produto:
                itens_no_carrinho.append(produto)
                total += produto.preco
                
    return render_template('carrinho.html', itens=itens_no_carrinho, total=total)

@app.route('/limpar_carrinho')
def limpar_carrinho():
    session.pop('carrinho', None) # Apaga a sessão
    return redirect(url_for('index'))

@app.route('/login')
def login():
    return render_template('login.html')
    
@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')

if __name__ == '__main__':
    app.run(debug=True)