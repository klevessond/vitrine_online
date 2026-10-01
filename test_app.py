import os

# Precisa vir ANTES de importar o app: o banco é configurado no db.init_app()
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import pytest
from app import app, db
from models import Produto


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
