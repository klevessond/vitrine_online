import os

# Precisa vir ANTES de importar o app: o banco é configurado no db.init_app()
os.environ['DATABASE_URL'] = 'sqlite:///:memory:'

import pytest
from app import app, db
from models import Produto, Cliente, Pedido, ItemPedido


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
    assert "R$ 15,00".encode() in resposta.data


def test_total_com_dois_itens(cliente):
    """Dois itens iguais devem somar o dobro do preço."""
    cliente.get('/adicionar/1')
    resposta = cliente.get('/adicionar/1', follow_redirects=True)
    assert "R$ 30,00".encode() in resposta.data


def test_adicionar_produto_inexistente(cliente):
    """Um produto que não existe não deve ser adicionado (erro tratado)."""
    resposta = cliente.get('/adicionar/999', follow_redirects=True)
    assert resposta.status_code == 200
    with cliente.session_transaction() as sessao:
        assert not sessao.get('carrinho')


def test_limpar_carrinho(cliente):
    """Esvaziar o carrinho deve remover todos os itens."""
    cliente.get('/adicionar/1')
    cliente.get('/limpar_carrinho')
    resposta = cliente.get('/carrinho')
    assert "carrinho está vazio".encode() in resposta.data


@pytest.mark.parametrize('rota', ['/login', '/erro-login'])
def test_paginas_abrem(cliente, rota):
    """As páginas de login e de erro de login devem responder sem erro."""
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

# ---------------------- Carrinho com quantidades ----------------------

def test_carrinho_agrupa_quantidade(cliente):
    """Adicionar o mesmo produto duas vezes mostra '2x' em uma única linha."""
    cliente.get('/adicionar/1')
    resposta = cliente.get('/adicionar/1', follow_redirects=True)
    assert "2x Teste Velvet".encode() in resposta.data
    assert resposta.data.count("x Teste Velvet".encode()) == 1


def test_diminuir_e_remover_item(cliente):
    """Os botões − e Remover alteram o carrinho sem esvaziar tudo."""
    cliente.get('/adicionar/1')
    cliente.get('/adicionar/1')
    resposta = cliente.get('/diminuir/1', follow_redirects=True)
    assert "1x Teste Velvet".encode() in resposta.data
    resposta = cliente.get('/remover/1', follow_redirects=True)
    assert "carrinho está vazio".encode() in resposta.data


def test_preco_no_padrao_brasileiro(cliente):
    """A vitrine mostra o preço com vírgula: R$ 15,00."""
    resposta = cliente.get('/')
    assert "R$ 15,00".encode() in resposta.data


# ---------------------- Finalizar pedido ----------------------

ENDERECO = {'rua': 'Av. Principal', 'numero': '123', 'complemento': 'Apto 42',
            'bairro': 'Centro', 'pagamento': 'pix'}


def test_finalizar_pedido_com_sucesso(cliente):
    """Pedido válido é gravado com itens, preço, total e status 'recebido'."""
    cadastrar(cliente)
    cliente.get('/adicionar/1')
    cliente.get('/adicionar/1')
    resposta = cliente.post('/finalizar', data=ENDERECO, follow_redirects=True)

    assert resposta.status_code == 200
    assert "Pedido Confirmado".encode() in resposta.data
    assert "Pedido nº <strong>1</strong>".encode() in resposta.data
    assert "R$ 30,00".encode() in resposta.data

    with app.app_context():
        pedido = db.session.get(Pedido, 1)
        assert pedido.status == 'recebido'
        assert pedido.forma_pagamento == 'pix'
        assert pedido.valor_total == 30
        assert len(pedido.itens) == 1
        assert pedido.itens[0].quantidade == 2
        assert pedido.itens[0].preco_unitario == 15


def test_finalizar_esvazia_carrinho(cliente):
    """Depois de confirmar, o carrinho fica vazio."""
    cadastrar(cliente)
    cliente.get('/adicionar/1')
    cliente.post('/finalizar', data=ENDERECO)
    with cliente.session_transaction() as sessao:
        assert not sessao.get('carrinho')


def test_finalizar_sem_login(cliente):
    """RN05: sem login, vai para o login e não grava pedido."""
    cliente.get('/adicionar/1')
    resposta = cliente.post('/finalizar', data=ENDERECO, follow_redirects=True)
    assert "Faça login para finalizar o seu pedido".encode() in resposta.data
    with app.app_context():
        assert Pedido.query.count() == 0


def test_login_volta_ao_carrinho_com_dados(cliente):
    """US15: depois do login, volta ao carrinho com itens e endereço preservados."""
    cadastrar(cliente)
    cliente.get('/logout')
    cliente.get('/adicionar/1')
    cliente.post('/finalizar', data=ENDERECO)
    resposta = cliente.post('/login', data={'email': 'maria@email.com', 'senha': 'segredo123'},
                            follow_redirects=True)
    assert "Finalizar Pedido".encode() in resposta.data
    assert "1x Teste Velvet".encode() in resposta.data
    assert 'value="Av. Principal"'.encode() in resposta.data


def test_finalizar_carrinho_vazio(cliente):
    """RN06: carrinho vazio não pode ser finalizado."""
    cadastrar(cliente)
    resposta = cliente.post('/finalizar', data=ENDERECO, follow_redirects=True)
    assert "carrinho está vazio".encode() in resposta.data
    with app.app_context():
        assert Pedido.query.count() == 0


def test_finalizar_endereco_incompleto(cliente):
    """RN07: sem rua, mostra erro e mantém os dados digitados."""
    cadastrar(cliente)
    cliente.get('/adicionar/1')
    dados = dict(ENDERECO, rua='')
    resposta = cliente.post('/finalizar', data=dados)
    assert resposta.status_code == 400
    assert "Preencha rua, número e bairro".encode() in resposta.data
    assert 'value="Centro"'.encode() in resposta.data
    with app.app_context():
        assert Pedido.query.count() == 0


def test_finalizar_pagamento_invalido(cliente):
    """RN08: só cartão, PIX ou dinheiro."""
    cadastrar(cliente)
    cliente.get('/adicionar/1')
    resposta = cliente.post('/finalizar', data=dict(ENDERECO, pagamento='cheque'))
    assert resposta.status_code == 400
    assert "Escolha uma forma de pagamento".encode() in resposta.data


def test_preco_do_pedido_nao_muda(cliente):
    """RN09: mudar o preço do produto não altera pedidos antigos."""
    cadastrar(cliente)
    cliente.get('/adicionar/1')
    cliente.post('/finalizar', data=ENDERECO)
    with app.app_context():
        produto = db.session.get(Produto, 1)
        produto.preco = 99
        db.session.commit()
        pedido = db.session.get(Pedido, 1)
        assert pedido.itens[0].preco_unitario == 15
        assert pedido.valor_total == 15


# ---------------------- Meus pedidos e segurança ----------------------

def test_meus_pedidos_lista_pedidos(cliente):
    """US13: o cliente vê seus pedidos com o status."""
    cadastrar(cliente)
    cliente.get('/adicionar/1')
    cliente.post('/finalizar', data=ENDERECO)
    resposta = cliente.get('/meus-pedidos')
    assert resposta.status_code == 200
    assert "Pedido nº 1".encode() in resposta.data
    assert "Recebido".encode() in resposta.data
    assert "Av. Principal, 123 - Apto 42 - Centro".encode() in resposta.data


def test_meus_pedidos_vazio(cliente):
    """Cliente sem pedidos vê uma mensagem amigável."""
    cadastrar(cliente)
    resposta = cliente.get('/meus-pedidos')
    assert "ainda não fez nenhum pedido".encode() in resposta.data


def test_meus_pedidos_exige_login(cliente):
    """Sem login, Meus Pedidos leva à tela de login."""
    resposta = cliente.get('/meus-pedidos', follow_redirects=True)
    assert "Faça login para ver os seus pedidos".encode() in resposta.data


def test_cliente_nao_ve_pedido_de_outro(cliente):
    """Um cliente não pode abrir a confirmação do pedido de outro cliente."""
    cadastrar(cliente)
    cliente.get('/adicionar/1')
    cliente.post('/finalizar', data=ENDERECO)
    cliente.get('/logout')
    cadastrar(cliente, nome='João', email='joao@email.com')
    resposta = cliente.get('/pedido/1/confirmado')
    assert resposta.status_code == 404


def test_pagina_inexistente(cliente):
    """Endereço que não existe mostra a página de erro amigável."""
    resposta = cliente.get('/pagina-que-nao-existe')
    assert resposta.status_code == 404
    assert "Página não encontrada".encode() in resposta.data


def test_data_no_horario_de_brasilia():
    """O filtro converte o horário UTC do banco para o horário de Brasília."""
    from datetime import datetime
    from app import formatar_data
    assert formatar_data(datetime(2026, 10, 15, 19, 13)) == '15/10/2026 16:13'
