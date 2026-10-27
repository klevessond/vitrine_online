from datetime import datetime, timezone
from decimal import Decimal

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Produto(db.Model):
    __tablename__ = 'produtos'
    id_produto = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    imagem_url = db.Column(db.String(255))


class Cliente(db.Model):
    __tablename__ = 'clientes'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    criado_em = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def definir_senha(self, senha):
        """Guarda apenas o hash da senha, nunca a senha em texto puro."""
        self.senha_hash = generate_password_hash(senha)

    def verificar_senha(self, senha):
        """Compara a senha digitada com o hash guardado no banco."""
        return check_password_hash(self.senha_hash, senha)

# Formas de pagamento aceitas na entrega (RN08): valor gravado -> texto exibido
FORMAS_PAGAMENTO = {
    'cartao': 'Cartão de crédito / débito',
    'pix': 'PIX',
    'dinheiro': 'Dinheiro',
}

# Situações possíveis de um pedido (RN11): valor gravado -> texto exibido
STATUS_PEDIDO = {
    'recebido': 'Recebido',
    'em_preparo': 'Em preparo',
    'saiu_entrega': 'Saiu para entrega',
    'entregue': 'Entregue',
    'cancelado': 'Cancelado',
}


class Pedido(db.Model):
    __tablename__ = 'pedidos'
    id_pedido = db.Column(db.Integer, primary_key=True)
    id_cliente = db.Column(db.Integer, db.ForeignKey('clientes.id_cliente'), nullable=False, index=True)
    data_pedido = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    rua = db.Column(db.String(150), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    complemento = db.Column(db.String(60))
    bairro = db.Column(db.String(80), nullable=False)
    forma_pagamento = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='recebido')
    valor_total = db.Column(db.Numeric(10, 2), nullable=False)

    cliente = db.relationship('Cliente', backref=db.backref('pedidos', lazy=True))
    # Composição: os itens não existem sem o pedido (ON DELETE CASCADE)
    itens = db.relationship('ItemPedido', backref='pedido', lazy=True,
                            cascade='all, delete-orphan')

    def calcular_total(self):
        """RN10: soma de quantidade x preço unitário de todos os itens."""
        return sum((item.subtotal() for item in self.itens), Decimal('0.00'))

    @property
    def pagamento_texto(self):
        return FORMAS_PAGAMENTO.get(self.forma_pagamento, self.forma_pagamento)

    @property
    def status_texto(self):
        return STATUS_PEDIDO.get(self.status, self.status)

    @property
    def endereco_completo(self):
        endereco = f'{self.rua}, {self.numero}'
        if self.complemento:
            endereco += f' - {self.complemento}'
        return f'{endereco} - {self.bairro}'


class ItemPedido(db.Model):
    __tablename__ = 'itens_pedido'
    __table_args__ = (db.UniqueConstraint('id_pedido', 'id_produto', name='uq_itens_pedido_produto'),)

    id_item = db.Column(db.Integer, primary_key=True)
    id_pedido = db.Column(db.Integer, db.ForeignKey('pedidos.id_pedido', ondelete='CASCADE'),
                          nullable=False, index=True)
    id_produto = db.Column(db.Integer, db.ForeignKey('produtos.id_produto'), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    # RN09: preço do produto no momento da compra
    preco_unitario = db.Column(db.Numeric(10, 2), nullable=False)

    produto = db.relationship('Produto')

    def subtotal(self):
        return self.preco_unitario * self.quantidade
