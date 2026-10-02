import os
import re

from flask import Flask, render_template, session, redirect, url_for, request, flash
from models import db, Produto, Cliente

app = Flask(__name__)

# Chave secreta necessária para usar a sessão (carrinho e login).
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


# Regras de validação do cadastro
SENHA_MINIMA = 6
PADRAO_EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


@app.context_processor
def cliente_logado():
    """Disponibiliza o cliente logado (ou None) para todos os templates."""
    id_cliente = session.get('cliente_id')
    cliente = db.session.get(Cliente, id_cliente) if id_cliente else None
    return {'cliente_logado': cliente}


# ---------------------- Vitrine e carrinho ----------------------

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

    carrinho_atual = session.get('carrinho', [])
    carrinho_atual.append(id_produto)
    session['carrinho'] = carrinho_atual

    return redirect(url_for('carrinho'))


@app.route('/carrinho')
def carrinho():
    itens_no_carrinho = []
    total = 0

    for id_prod in session.get('carrinho', []):
        produto = db.session.get(Produto, id_prod)
        if produto:
            itens_no_carrinho.append(produto)
            total += produto.preco

    return render_template('carrinho.html', itens=itens_no_carrinho, total=total)


@app.route('/limpar_carrinho')
def limpar_carrinho():
    session.pop('carrinho', None)
    return redirect(url_for('index'))


# ---------------------- Cadastro, login e logout ----------------------

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html', aba='login')

    email = request.form.get('email', '').strip().lower()
    senha = request.form.get('senha', '')

    if not email or not senha:
        flash('Preencha o e-mail e a senha.', 'erro')
        return render_template('login.html', aba='login', email=email), 400

    cliente = Cliente.query.filter_by(email=email).first()
    if cliente is None or not cliente.verificar_senha(senha):
        # Mesma mensagem para e-mail inexistente e senha errada (segurança)
        return render_template('erro-login.html'), 401

    session['cliente_id'] = cliente.id_cliente
    flash(f'Bem-vindo(a) de volta, {cliente.nome}!', 'sucesso')
    return redirect(url_for('index'))


@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form.get('nome', '').strip()
    email = request.form.get('email', '').strip().lower()
    senha = request.form.get('senha', '')

    erros = []
    if not nome:
        erros.append('Informe o seu nome.')
    if not PADRAO_EMAIL.match(email):
        erros.append('Informe um e-mail válido.')
    if len(senha) < SENHA_MINIMA:
        erros.append(f'A senha deve ter pelo menos {SENHA_MINIMA} caracteres.')
    if not erros and Cliente.query.filter_by(email=email).first():
        erros.append('Este e-mail já está cadastrado. Faça login.')

    if erros:
        for erro in erros:
            flash(erro, 'erro')
        # Devolve o formulário com os dados já digitados (exceto a senha)
        return render_template('login.html', aba='cadastro', nome=nome, email=email), 400

    novo_cliente = Cliente(nome=nome, email=email)
    novo_cliente.definir_senha(senha)
    db.session.add(novo_cliente)
    db.session.commit()

    # Após o cadastro, o cliente já entra logado
    session['cliente_id'] = novo_cliente.id_cliente
    flash(f'Cadastro realizado com sucesso. Olá, {nome}!', 'sucesso')
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('cliente_id', None)
    flash('Você saiu da sua conta.', 'sucesso')
    return redirect(url_for('index'))


@app.route('/erro-login')
def erro_login():
    return render_template('erro-login.html')


@app.route('/sucesso')
def sucesso():
    return render_template('sucesso.html')


if __name__ == '__main__':
    app.run(debug=True)