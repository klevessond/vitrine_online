import pytest
from app import app, db
from models import Produto

@pytest.fixture
def cliente():
    # Configura uma base de dados temporária em memória para executar os testes
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:' 
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Insere um dado fictício no Model para testar a integração
            novo_cupcake = Produto(nome="Teste Velvet", preco=15.00, imagem_url="")
            db.session.add(novo_cupcake)
            db.session.commit()
        yield client

def test_pagina_inicial(cliente):
    """Verifica se o controlador processa a requisição e devolve a View HTML correta com os dados."""
    resposta = cliente.get('/')
    assert resposta.status_code == 200
    # Valida se o cupcake inserido no Model aparece impresso no HTML (View)
    assert b"Teste Velvet" in resposta.data