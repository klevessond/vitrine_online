-- =====================================================================
-- Cupcake Gourmet - Vitrine Online
-- Projeto físico do banco de dados (PostgreSQL)
-- PIT II - Situação-problema 1
-- =====================================================================
-- Observação: no sistema, as tabelas são criadas automaticamente pelo
-- SQLAlchemy (db.create_all()). Este script documenta a mesma estrutura
-- e pode ser usado para criar o banco manualmente.
-- =====================================================================

-- ---------------------------------------------------------------------
-- Tabela: clientes
-- Pessoas cadastradas que podem fazer login e pedidos.
-- ---------------------------------------------------------------------
CREATE TABLE clientes (
    id_cliente   SERIAL        PRIMARY KEY,
    nome         VARCHAR(100)  NOT NULL,
    email        VARCHAR(120)  NOT NULL,
    senha_hash   VARCHAR(255)  NOT NULL,
    criado_em    TIMESTAMP     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_clientes_email UNIQUE (email)
);

-- ---------------------------------------------------------------------
-- Tabela: produtos
-- Cupcakes exibidos na vitrine.
-- ---------------------------------------------------------------------
CREATE TABLE produtos (
    id_produto   SERIAL         PRIMARY KEY,
    nome         VARCHAR(100)   NOT NULL,
    descricao    VARCHAR(255),
    preco        NUMERIC(10,2)  NOT NULL,
    imagem_url   VARCHAR(255),
    CONSTRAINT ck_produtos_preco CHECK (preco > 0)
);

-- ---------------------------------------------------------------------
-- Tabela: pedidos
-- Cabeçalho do pedido: quem comprou, onde entregar e como pagar.
-- ---------------------------------------------------------------------
CREATE TABLE pedidos (
    id_pedido        SERIAL         PRIMARY KEY,
    id_cliente       INTEGER        NOT NULL,
    data_pedido      TIMESTAMP      NOT NULL DEFAULT CURRENT_TIMESTAMP,
    rua              VARCHAR(150)   NOT NULL,
    numero           VARCHAR(10)    NOT NULL,
    complemento      VARCHAR(60),
    bairro           VARCHAR(80)    NOT NULL,
    forma_pagamento  VARCHAR(10)    NOT NULL,
    status           VARCHAR(20)    NOT NULL DEFAULT 'recebido',
    valor_total      NUMERIC(10,2)  NOT NULL,
    CONSTRAINT fk_pedidos_cliente
        FOREIGN KEY (id_cliente) REFERENCES clientes (id_cliente),
    CONSTRAINT ck_pedidos_pagamento
        CHECK (forma_pagamento IN ('cartao', 'pix', 'dinheiro')),
    CONSTRAINT ck_pedidos_status
        CHECK (status IN ('recebido', 'em_preparo', 'saiu_entrega', 'entregue', 'cancelado')),
    CONSTRAINT ck_pedidos_total CHECK (valor_total > 0)
);

CREATE INDEX ix_pedidos_cliente ON pedidos (id_cliente);

-- ---------------------------------------------------------------------
-- Tabela: itens_pedido
-- Cada cupcake de um pedido, com a quantidade e o preço da época.
-- ---------------------------------------------------------------------
CREATE TABLE itens_pedido (
    id_item         SERIAL         PRIMARY KEY,
    id_pedido       INTEGER        NOT NULL,
    id_produto      INTEGER        NOT NULL,
    quantidade      INTEGER        NOT NULL,
    preco_unitario  NUMERIC(10,2)  NOT NULL,
    CONSTRAINT fk_itens_pedido
        FOREIGN KEY (id_pedido) REFERENCES pedidos (id_pedido) ON DELETE CASCADE,
    CONSTRAINT fk_itens_produto
        FOREIGN KEY (id_produto) REFERENCES produtos (id_produto),
    CONSTRAINT uq_itens_pedido_produto UNIQUE (id_pedido, id_produto),
    CONSTRAINT ck_itens_quantidade CHECK (quantidade > 0),
    CONSTRAINT ck_itens_preco CHECK (preco_unitario > 0)
);

CREATE INDEX ix_itens_pedido ON itens_pedido (id_pedido);

-- ---------------------------------------------------------------------
-- Carga inicial: cupcakes da vitrine
-- ---------------------------------------------------------------------
INSERT INTO produtos (nome, descricao, preco, imagem_url) VALUES
    ('Red Velvet',      'Delicioso cupcake vermelho',      12.00, '/static/imagens/red-velvet.jpg'),
    ('Duplo Chocolate', 'Massa e cobertura de chocolate',  10.00, '/static/imagens/chocolate.jpg'),
    ('Limão Siciliano', 'Toque cítrico e refrescante',     11.00, '/static/imagens/limao.jpg');
