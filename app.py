from flask import Flask, render_template, session, redirect, url_for
from models import db, Produto
import os

app = Flask(__name__)

# Chave secreta necessária para usar a sessão (carrinho).
# No Render, crie a variável de ambiente SECRET_KEY com um texto aleatório e longo.
app.secret_key = os.environ.get('SECRET_KEY', 'chave-de-desenvolvimento')

# Configuração da base de dados. O Render fornece a DATABASE_URL.
# Algumas URLs começam com "postgres://", mas o SQLAlchemy 2.x só aceita "postgresql://".
db_url = os.environ.get('DATABASE_URL', 'sqlite:///local.db')
if db_url.startswith('postgres://'):
    db_url = db_url.replace('postgres://', 'postgresql://', 1)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Cria as tabelas (se ainda não existirem) e insere os cupcakes iniciais.
# Não usamos db.drop_all() para não apagar os dados a cada deploy.
with app.app_context():
    db.create_all()

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
    # Só adiciona se o produto existir
    if db.session.get(Produto, id_produto) is None:
        return redirect(url_for('index'))

    # Cria um carrinho vazio na sessão, se não existir
    carrinho_atual = session.get('carrinho', [])
    carrinho_atual.append(id_produto)
    session['carrinho'] = carrinho_atual

    return redirect(url_for('carrinho'))


@app.route('/carrinho')
def carrinho():
    itens_no_carrinho = []
    total = 0

    # Se houver itens na sessão, procura-os na base de dados
    for id_prod in session.get('carrinho', []):
        produto = db.session.get(Produto, id_prod)
        if produto:
            itens_no_carrinho.append(produto)
            total += produto.preco

    return render_template('carrinho.html', itens=itens_no_carrinho, total=total)


@app.route('/limpar_carrinho')
def limpar_carrinho():
    session.pop('carrinho', None)  # Apaga o carrinho da sessão
    return redirect(url_for('index'))


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/erro-login')
def erro_login():
    return render_template('erro-login.html')


@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')


if __name__ == '__main__':
    app.run(debug=True)
