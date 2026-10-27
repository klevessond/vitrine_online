import os
import re
from datetime import timezone, timedelta
from decimal import Decimal

from flask import Flask, render_template, session, redirect, url_for, request, flash, abort
from models import db, Produto, Cliente, Pedido, ItemPedido, FORMAS_PAGAMENTO

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


# Regras de validação
SENHA_MINIMA = 6
PADRAO_EMAIL = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')
QUANTIDADE_MAXIMA = 50  # por produto, para evitar pedidos absurdos


# ---------------------- Funções auxiliares ----------------------

@app.template_filter('moeda')
def formatar_moeda(valor):
    """Formata no padrão brasileiro: 1234.5 -> 'R$ 1.234,50'."""
    texto = f'{Decimal(valor or 0):,.2f}'
    return 'R$ ' + texto.replace(',', 'X').replace('.', ',').replace('X', '.')


try:
    from zoneinfo import ZoneInfo
    FUSO_BRASIL = ZoneInfo('America/Sao_Paulo')
except Exception:  # sistema sem base de fusos: usa UTC-3 fixo
    FUSO_BRASIL = timezone(timedelta(hours=-3))


@app.template_filter('data_br')
def formatar_data(data):
    """O banco guarda em UTC; exibe no horário de Brasília: '15/10/2026 16:13'."""
    if not data:
        return ''
    if data.tzinfo is None:
        data = data.replace(tzinfo=timezone.utc)
    return data.astimezone(FUSO_BRASIL).strftime('%d/%m/%Y %H:%M')


@app.context_processor
def dados_globais():
    """Disponibiliza o cliente logado e o nº de itens do carrinho para todos os templates."""
    id_cliente = session.get('cliente_id')
    cliente = db.session.get(Cliente, id_cliente) if id_cliente else None
    return {'cliente_logado': cliente,
            'qtd_carrinho': sum(obter_carrinho().values())}


def cliente_atual():
    id_cliente = session.get('cliente_id')
    return db.session.get(Cliente, id_cliente) if id_cliente else None


def obter_carrinho():
    """Lê o carrinho da sessão no formato {id_produto: quantidade}."""
    bruto = session.get('carrinho', {})
    if isinstance(bruto, list):  # formato antigo: lista de ids repetidos
        convertido = {}
        for id_prod in bruto:
            convertido[id_prod] = convertido.get(id_prod, 0) + 1
        return convertido
    return {int(chave): qtd for chave, qtd in bruto.items()}


def salvar_carrinho(carrinho):
    # A sessão é guardada em JSON, que só aceita chaves de texto
    session['carrinho'] = {str(chave): qtd for chave, qtd in carrinho.items() if qtd > 0}


def itens_do_carrinho():
    """Monta a lista de itens com produto, quantidade e subtotal, e o total geral."""
    itens, total = [], Decimal('0.00')
    for id_prod, quantidade in obter_carrinho().items():
        produto = db.session.get(Produto, id_prod)
        if produto:
            subtotal = produto.preco * quantidade
            itens.append({'produto': produto, 'quantidade': quantidade, 'subtotal': subtotal})
            total += subtotal
    return itens, total


def ir_para_login(mensagem, destino):
    """Guarda para onde voltar depois do login e leva o usuário à tela de login."""
    session['depois_do_login'] = destino
    flash(mensagem, 'erro')
    return redirect(url_for('login'))


def destino_apos_login():
    destino = session.pop('depois_do_login', None)
    return redirect(url_for(destino) if destino in ('carrinho', 'meus_pedidos') else url_for('index'))


# ---------------------- Vitrine e carrinho ----------------------

@app.route('/')
def index():
    cupcakes = Produto.query.all()
    return render_template('index.html', cupcakes=cupcakes)


@app.route('/adicionar/<int:id_produto>')
def adicionar(id_produto):
    if db.session.get(Produto, id_produto) is None:
        return redirect(url_for('index'))

    carrinho = obter_carrinho()
    carrinho[id_produto] = min(carrinho.get(id_produto, 0) + 1, QUANTIDADE_MAXIMA)
    salvar_carrinho(carrinho)
    return redirect(url_for('carrinho'))


@app.route('/diminuir/<int:id_produto>')
def diminuir(id_produto):
    carrinho = obter_carrinho()
    if id_produto in carrinho:
        carrinho[id_produto] -= 1
        salvar_carrinho(carrinho)
    return redirect(url_for('carrinho'))


@app.route('/remover/<int:id_produto>')
def remover(id_produto):
    carrinho = obter_carrinho()
    carrinho.pop(id_produto, None)
    salvar_carrinho(carrinho)
    return redirect(url_for('carrinho'))


@app.route('/carrinho')
def carrinho():
    itens, total = itens_do_carrinho()
    # Dados do checkout guardados quando o usuário precisou fazer login (US15)
    dados = session.pop('dados_checkout', {})
    return render_template('carrinho.html', itens=itens, total=total, dados=dados,
                           formas_pagamento=FORMAS_PAGAMENTO)


@app.route('/limpar_carrinho')
def limpar_carrinho():
    session.pop('carrinho', None)
    return redirect(url_for('index'))


# ---------------------- Pedido ----------------------

@app.route('/finalizar', methods=['POST'])
def finalizar():
    dados = {
        'rua': request.form.get('rua', '').strip(),
        'numero': request.form.get('numero', '').strip(),
        'complemento': request.form.get('complemento', '').strip(),
        'bairro': request.form.get('bairro', '').strip(),
        'pagamento': request.form.get('pagamento', ''),
    }

    # RN05: só cliente logado finaliza o pedido
    cliente = cliente_atual()
    if cliente is None:
        session['dados_checkout'] = dados  # não perde o que já foi digitado
        return ir_para_login('Faça login para finalizar o seu pedido.', 'carrinho')

    itens, total = itens_do_carrinho()

    # RN06: carrinho vazio não pode ser finalizado
    if not itens:
        flash('O seu carrinho está vazio.', 'erro')
        return redirect(url_for('carrinho'))

    # RN07 e RN08: endereço obrigatório e forma de pagamento válida
    erros = []
    if not (dados['rua'] and dados['numero'] and dados['bairro']):
        erros.append('Preencha rua, número e bairro para a entrega.')
    if dados['pagamento'] not in FORMAS_PAGAMENTO:
        erros.append('Escolha uma forma de pagamento.')
    limites = {'rua': 150, 'numero': 10, 'complemento': 60, 'bairro': 80}
    for campo, limite in limites.items():
        if len(dados[campo]) > limite:
            erros.append(f'O campo {campo} aceita no máximo {limite} caracteres.')

    if erros:
        for erro in erros:
            flash(erro, 'erro')
        return render_template('carrinho.html', itens=itens, total=total, dados=dados,
                               formas_pagamento=FORMAS_PAGAMENTO), 400

    pedido = Pedido(
        cliente=cliente,
        rua=dados['rua'],
        numero=dados['numero'],
        complemento=dados['complemento'] or None,
        bairro=dados['bairro'],
        forma_pagamento=dados['pagamento'],
        status='recebido',  # RN11
    )
    for item in itens:
        # RN09: guarda o preço atual do produto
        pedido.itens.append(ItemPedido(produto=item['produto'], quantidade=item['quantidade'],
                                       preco_unitario=item['produto'].preco))
    pedido.valor_total = pedido.calcular_total()  # RN10

    db.session.add(pedido)
    db.session.commit()

    session.pop('carrinho', None)
    return redirect(url_for('sucesso', id_pedido=pedido.id_pedido))


@app.route('/pedido/<int:id_pedido>/confirmado')
def sucesso(id_pedido):
    cliente = cliente_atual()
    pedido = db.session.get(Pedido, id_pedido)
    # Um cliente só pode ver os próprios pedidos
    if cliente is None or pedido is None or pedido.id_cliente != cliente.id_cliente:
        abort(404)
    return render_template('sucesso.html', pedido=pedido)


@app.route('/meus-pedidos')
def meus_pedidos():
    cliente = cliente_atual()
    if cliente is None:
        return ir_para_login('Faça login para ver os seus pedidos.', 'meus_pedidos')

    pedidos = (Pedido.query.filter_by(id_cliente=cliente.id_cliente)
               .order_by(Pedido.data_pedido.desc(), Pedido.id_pedido.desc()).all())
    return render_template('meus_pedidos.html', pedidos=pedidos)


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
        # Mesma mensagem para e-mail inexistente e senha errada (RN04)
        return render_template('erro-login.html'), 401

    session['cliente_id'] = cliente.id_cliente
    flash(f'Bem-vindo(a) de volta, {cliente.nome}!', 'sucesso')
    return destino_apos_login()


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
        return render_template('login.html', aba='cadastro', nome=nome, email=email), 400

    novo_cliente = Cliente(nome=nome, email=email)
    novo_cliente.definir_senha(senha)
    db.session.add(novo_cliente)
    db.session.commit()

    session['cliente_id'] = novo_cliente.id_cliente
    flash(f'Cadastro realizado com sucesso. Olá, {nome}!', 'sucesso')
    return destino_apos_login()


@app.route('/logout')
def logout():
    session.pop('cliente_id', None)
    flash('Você saiu da sua conta.', 'sucesso')
    return redirect(url_for('index'))


@app.route('/erro-login')
def erro_login():
    return render_template('erro-login.html')


# ---------------------- Páginas de erro ----------------------

@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template('erro.html', titulo='Página não encontrada',
                           mensagem='O endereço que você acessou não existe.'), 404


@app.errorhandler(500)
def erro_interno(erro):
    db.session.rollback()
    return render_template('erro.html', titulo='Algo deu errado',
                           mensagem='Tivemos um problema ao processar seu pedido. Tente novamente em instantes.'), 500


if __name__ == '__main__':
    app.run(debug=True)
