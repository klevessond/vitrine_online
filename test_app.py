import os

# Precisa vir ANTES de importar o app: o banco é configurado no db.init_app()
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import pytest
from app import app, db
from models import Produto, Cliente


@pytest.fixture
def cliente():
    # Configura o app para testes com uma base de dados temporária em memória
    app.config['TESTING'] = True

    with app.app_context():
        db.drop_all()
        db.create_all()
        # Insere um dado fictício no Model para testar a integração
        novo_cupcake = Produto(nome="Teste Velvet", preco=15.00, imagem_url="")
        db.session.add(novo_cupcake)
        db.session.commit()

    with app.test_client() as client:
        yield client


def test_pagina_inicial(cliente):
    """Verifica se o controlador devolve a View HTML com os dados do Model."""
    resposta = cliente.get('/')
    assert resposta.status_code == 200
    assert "Teste Velvet".encode() in resposta.data


def test_carrinho_vazio(cliente):
    """O carrinho sem itens deve abrir e mostrar a mensagem de vazio."""
    resposta = cliente.get('/carrinho')
    assert resposta.status_code == 200
    assert "carrinho está vazio".encode() in resposta.data


def test_adicionar_ao_carrinho(cliente):
    """Adicionar um produto deve levá-lo ao carrinho com o total correto."""
    resposta = cliente.get('/adicionar/1', follow_redirects=True)
    assert resposta.status_code == 200
    assert "Teste Velvet".encode() in resposta.data
    assert "R$ 15.00".encode() in resposta.data


def test_total_com_dois_itens(cliente):
    """Dois itens iguais devem somar o dobro do preço."""
    cliente.get('/adicionar/1')
    resposta = cliente.get('/adicionar/1', follow_redirects=True)
    assert "R$ 30.00".encode() in resposta.data


def test_adicionar_produto_inexistente(cliente):
    """Um produto que não existe não deve ser adicionado (erro tratado)."""
    resposta = cliente.get('/adicionar/999', follow_redirects=True)
    assert resposta.status_code == 200
    with cliente.session_transaction() as sessao:
        assert sessao.get('carrinho', []) == []


def test_limpar_carrinho(cliente):
    """Esvaziar o carrinho deve remover todos os itens."""
    cliente.get('/adicionar/1')
    cliente.get('/limpar_carrinho')
    resposta = cliente.get('/carrinho')
    assert "carrinho está vazio".encode() in resposta.data


@pytest.mark.parametrize('rota', ['/login', '/erro-login', '/sucesso'])
def test_paginas_abrem(cliente, rota):
    """As páginas de login, erro e sucesso devem responder sem erro."""
    assert cliente.get(rota).status_code == 200


# ---------------------- Cadastro e login ----------------------

def cadastrar(cliente, nome='Maria Silva', email='maria@email.com', senha='segredo123'):
    """Função auxiliar que envia o formulário de cadastro."""
    return cliente.post('/cadastro', data={'nome': nome, 'email': email, 'senha': senha},
                        follow_redirects=True)


def test_cadastro_com_sucesso(cliente):
    """Um cadastro válido cria o cliente e já deixa ele logado."""
    resposta = cadastrar(cliente)
    assert resposta.status_code == 200
    assert "Cadastro realizado com sucesso".encode() in resposta.data
    assert "Olá, Maria".encode() in resposta.data
    with app.app_context():
        assert Cliente.query.filter_by(email='maria@email.com').count() == 1


def test_senha_guardada_com_hash(cliente):
    """A senha nunca deve ser guardada em texto puro no banco."""
    cadastrar(cliente)
    with app.app_context():
        maria = Cliente.query.filter_by(email='maria@email.com').first()
        assert maria.senha_hash != 'segredo123'
        assert maria.verificar_senha('segredo123')


def test_cadastro_email_duplicado(cliente):
    """Não pode haver dois clientes com o mesmo e-mail."""
    cadastrar(cliente)
    cliente.get('/logout')
    resposta = cadastrar(cliente, nome='Outra Pessoa')
    assert resposta.status_code == 400
    assert "já está cadastrado".encode() in resposta.data
    with app.app_context():
        assert Cliente.query.count() == 1


def test_cadastro_senha_curta(cliente):
    """Senhas com menos de 6 caracteres devem ser recusadas."""
    resposta = cadastrar(cliente, senha='123')
    assert resposta.status_code == 400
    assert "pelo menos 6 caracteres".encode() in resposta.data


def test_cadastro_email_invalido(cliente):
    """E-mails sem formato válido devem ser recusados."""
    resposta = cadastrar(cliente, email='maria-sem-arroba')
    assert resposta.status_code == 400
    assert "e-mail válido".encode() in resposta.data


def test_cadastro_mantem_dados_digitados(cliente):
    """Quando há erro, o nome digitado continua no formulário."""
    resposta = cadastrar(cliente, senha='123')
    assert 'value="Maria Silva"'.encode() in resposta.data


def test_login_com_sucesso(cliente):
    """Com e-mail e senha corretos o cliente entra na conta."""
    cadastrar(cliente)
    cliente.get('/logout')
    resposta = cliente.post('/login', data={'email': 'MARIA@email.com ', 'senha': 'segredo123'},
                            follow_redirects=True)
    assert resposta.status_code == 200
    assert "Bem-vindo(a) de volta".encode() in resposta.data
    with cliente.session_transaction() as sessao:
        assert sessao.get('cliente_id') is not None


def test_login_senha_errada(cliente):
    """Senha errada mostra a tela de acesso negado."""
    cadastrar(cliente)
    cliente.get('/logout')
    resposta = cliente.post('/login', data={'email': 'maria@email.com', 'senha': 'errada'})
    assert resposta.status_code == 401
    assert "Acesso Negado".encode() in resposta.data


def test_login_email_inexistente(cliente):
    """E-mail não cadastrado também mostra acesso negado."""
    resposta = cliente.post('/login', data={'email': 'ninguem@email.com', 'senha': 'qualquer'})
    assert resposta.status_code == 401


def test_login_campos_vazios(cliente):
    """Login sem preencher os campos mostra mensagem de erro."""
    resposta = cliente.post('/login', data={'email': '', 'senha': ''})
    assert resposta.status_code == 400
    assert "Preencha o e-mail e a senha".encode() in resposta.data


def test_logout(cliente):
    """Ao sair, o cliente deixa de estar logado."""
    cadastrar(cliente)
    resposta = cliente.get('/logout', follow_redirects=True)
    assert "Você saiu da sua conta".encode() in resposta.data
    with cliente.session_transaction() as sessao:
        assert 'cliente_id' not in sessao