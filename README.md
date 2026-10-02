# 🧁 Cupcake Gourmet — Vitrine Online

Aplicação web de uma loja virtual de cupcakes gourmet, desenvolvida para o **Projeto Integrador Transdisciplinar em Engenharia de Software II** (Cruzeiro do Sul Virtual).

O sistema foi planejado no PIT I (histórias de usuário, UML e protótipos de tela) e implementado no PIT II, seguindo o padrão de arquitetura **MVC**.

**🔗 Aplicação publicada:** [cole aqui o link do Render]

**👤 Autor:** Klevesson Douglas Rodrigues da Silva Conrado — RGM 37167103

---

## Funcionalidades

- **Vitrine virtual:** lista os cupcakes com foto, descrição e preço.
- **Carrinho de compras:** adicionar produtos, ver o total e esvaziar o carrinho.
- **Cadastro de clientes:** nome, e-mail e senha, com validação dos dados.
- **Login e logout:** acesso à conta com e-mail e senha.
- **Segurança:** as senhas são guardadas apenas como *hash* (nunca em texto puro).
- **Tratamento de erros:** mensagens claras para e-mail inválido, senha curta, e-mail já cadastrado, campos vazios, login incorreto e produto inexistente.
- **Interface responsiva:** funciona bem no computador e no celular.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3 |
| Framework web | Flask 3.0 |
| Banco de dados | PostgreSQL (produção) e SQLite (desenvolvimento) |
| ORM | Flask-SQLAlchemy / SQLAlchemy |
| Front-end | HTML5, CSS3, JavaScript e templates Jinja2 |
| Testes | pytest |
| Servidor | Gunicorn |
| Hospedagem | Render |

## Arquitetura (MVC)

| Camada | Onde fica | Responsabilidade |
|---|---|---|
| **Model** | `models.py` | Classes `Produto` e `Cliente`, que viram tabelas no banco. O `Cliente` também cuida da criptografia da senha. |
| **View** | `templates/` | Páginas HTML que o usuário vê. |
| **Controller** | `app.py` | Rotas que recebem as requisições, aplicam as regras e escolhem a View. |

```
vitrine_online/
├── app.py              # Controller: rotas e regras de negócio
├── models.py           # Model: classes Produto e Cliente
├── test_app.py         # Testes automatizados (pytest)
├── requirements.txt    # Dependências do projeto
├── static/
│   └── imagens/        # Fotos dos cupcakes
└── templates/          # Views (HTML)
    ├── index.html      # Vitrine
    ├── carrinho.html   # Carrinho e checkout
    ├── login.html      # Login e cadastro
    ├── erro-login.html # Acesso negado
    ├── sucesso.html    # Pedido confirmado
    └── _mensagens.html # Bloco reutilizável de mensagens
```

## Banco de dados

**Tabela `produtos`**

| Campo | Tipo | Regras | Descrição |
|---|---|---|---|
| id_produto | INTEGER | Chave primária | Identificador do produto |
| nome | VARCHAR(100) | Obrigatório | Nome do cupcake |
| descricao | VARCHAR(255) | Opcional | Descrição curta |
| preco | NUMERIC(10,2) | Obrigatório | Preço em reais |
| imagem_url | VARCHAR(255) | Opcional | Caminho da foto |

**Tabela `clientes`**

| Campo | Tipo | Regras | Descrição |
|---|---|---|---|
| id_cliente | INTEGER | Chave primária | Identificador do cliente |
| nome | VARCHAR(100) | Obrigatório | Nome completo |
| email | VARCHAR(120) | Obrigatório e único | E-mail usado no login |
| senha_hash | VARCHAR(255) | Obrigatório | Hash da senha |
| criado_em | TIMESTAMP | Obrigatório | Data e hora do cadastro |

## Manual de uso

1. **Ver os produtos:** ao abrir o site, a vitrine mostra todos os cupcakes disponíveis.
2. **Comprar:** clique em **Adicionar** no cupcake desejado. Você é levado ao carrinho, que mostra os itens e o total. Para continuar comprando, use a seta **←** no topo.
3. **Esvaziar o carrinho:** no carrinho, clique em **Esvaziar Carrinho**.
4. **Criar uma conta:** clique no ícone 👤, escolha a aba **Quero me cadastrar** e preencha nome, e-mail e uma senha de pelo menos 6 caracteres. Ao concluir, você já entra logado.
5. **Entrar na conta:** clique no ícone 👤, preencha e-mail e senha na aba **Já sou cliente** e clique em **Entrar**.
6. **Sair:** com a conta aberta, clique em **Sair** no topo da página.
7. **Finalizar o pedido:** no carrinho, preencha o endereço, escolha a forma de pagamento e clique em **Confirmar**.

## Como rodar no seu computador

Pré-requisito: Python 3.10 ou superior.

```bash
# 1. Baixar o projeto
git clone https://github.com/klevessond/vitrine_online.git
cd vitrine_online

# 2. Criar e ativar um ambiente virtual
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux / macOS:
source .venv/bin/activate

# 3. Instalar as dependências
pip install -r requirements.txt

# 4. Iniciar a aplicação
python app.py
```

Depois, abra **http://127.0.0.1:5000** no navegador. Localmente, o sistema usa um banco SQLite criado automaticamente.

## Testes

```bash
pytest -v
```

São 20 testes automatizados, que usam um banco temporário em memória (não alteram dados reais). Eles cobrem:

- vitrine exibindo os produtos;
- carrinho vazio, adicionar item, soma do total, produto inexistente e esvaziar carrinho;
- cadastro válido, senha guardada com hash, e-mail duplicado, e-mail inválido, senha curta e manutenção dos dados digitados após um erro;
- login correto, senha errada, e-mail inexistente, campos vazios e logout;
- abertura das páginas de login, erro e sucesso.

## Deploy no Render

1. Crie um banco **PostgreSQL** no Render.
2. Crie um **Web Service** ligado a este repositório, com:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
3. Em **Environment**, crie as variáveis:
   - `DATABASE_URL`: a *Internal Database URL* do banco PostgreSQL.
   - `SECRET_KEY`: um texto aleatório e longo (protege a sessão dos usuários).

As tabelas e os produtos iniciais são criados automaticamente na primeira execução.

## Próximos passos

- [ ] Salvar o pedido no banco (tabelas `pedidos` e `itens_pedido`).
- [ ] Exigir login para finalizar a compra.
- [ ] Área do cliente com histórico de pedidos.
- [ ] Testes com usuários reais e correções (Situação-problema 3).
