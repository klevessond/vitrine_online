# 🧁 Cupcake Gourmet — Vitrine Online

Aplicação web de uma loja virtual de cupcakes gourmet, desenvolvida para o **Projeto Integrador Transdisciplinar em Engenharia de Software II** (Cruzeiro do Sul Virtual).

O sistema foi planejado no PIT I (histórias de usuário, UML e protótipos de tela) e implementado no PIT II, seguindo o padrão de arquitetura **MVC**.

**🔗 Aplicação publicada:** [cole aqui o link do Render]

**👤 Autor:** Klevesson Douglas Rodrigues da Silva Conrado — RGM 37167103

---

## Documentação do projeto

| Pasta | Conteúdo |
|---|---|
| [docs/1-planejamento](docs/1-planejamento/) | Situação 1: escopo e backlog, modelagem UML, IHC, projeto do banco de dados e dicionário de dados |
| [docs/3-validacao](docs/3-validacao/) | Situação 3: formulário de teste, relatório de validação com 5 testadores e correções |

## Funcionalidades

- **Vitrine virtual:** lista os cupcakes com foto, descrição e preço no padrão brasileiro (R$ 12,00).
- **Carrinho de compras:** adicionar, aumentar ou diminuir a quantidade, remover um item ou esvaziar tudo, com contador no ícone 🛒.
- **Cadastro de clientes:** nome, e-mail e senha, com validação dos dados.
- **Login e logout:** acesso à conta com e-mail e senha.
- **Finalização do pedido:** endereço de entrega e pagamento na entrega (cartão, PIX ou dinheiro). O pedido é gravado no banco com o preço da época da compra.
- **Login no meio da compra:** quem não está logado é levado ao login e depois volta ao carrinho, sem perder os itens nem o endereço digitado.
- **Pedido confirmado:** número do pedido, itens, total, endereço e forma de pagamento.
- **Meus pedidos:** histórico com data, itens, total e status de cada pedido.
- **Segurança:** senhas guardadas apenas como *hash*, e cada cliente só vê os próprios pedidos.
- **Tratamento de erros:** mensagens claras em todos os formulários e páginas amigáveis para erro 404 e 500.
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
| **Model** | `models.py` | Classes `Produto`, `Cliente`, `Pedido` e `ItemPedido`, que viram tabelas no banco. |
| **View** | `templates/` | Páginas HTML que o usuário vê. |
| **Controller** | `app.py` | Rotas que recebem as requisições, aplicam as regras de negócio e escolhem a View. |

```
vitrine_online/
├── app.py                # Controller: rotas e regras de negócio
├── models.py             # Model: Produto, Cliente, Pedido e ItemPedido
├── test_app.py           # Testes automatizados (pytest)
├── requirements.txt      # Dependências do projeto
├── docs/                 # Documentação (UML, IHC, banco de dados)
├── static/
│   └── imagens/          # Fotos dos cupcakes
└── templates/            # Views (HTML)
    ├── index.html        # Vitrine
    ├── carrinho.html     # Carrinho e finalização do pedido
    ├── sucesso.html      # Pedido confirmado
    ├── meus_pedidos.html # Histórico de pedidos
    ├── login.html        # Login e cadastro
    ├── erro-login.html   # Acesso negado
    ├── erro.html         # Páginas de erro 404 e 500
    └── _mensagens.html   # Bloco reutilizável de mensagens
```

## Banco de dados

O sistema usa quatro tabelas: `clientes`, `produtos`, `pedidos` e `itens_pedido`. Um cliente faz vários pedidos, e cada pedido tem um ou mais itens, cada um ligado a um produto.

O diagrama, a normalização, o script SQL e o dicionário de dados completo estão em [docs/1-planejamento/04-banco-de-dados.md](docs/1-planejamento/04-banco-de-dados.md).

## Manual de uso

1. **Ver os produtos:** ao abrir o site, a vitrine mostra todos os cupcakes disponíveis.
2. **Montar o carrinho:** clique em **Adicionar** no cupcake desejado. No carrinho, use **+** e **−** para mudar a quantidade, **Remover** para tirar um item ou **Esvaziar Carrinho** para recomeçar. Para continuar comprando, use a seta **←** no topo.
3. **Criar uma conta:** clique no ícone 👤, escolha a aba **Quero me cadastrar** e preencha nome, e-mail e uma senha de pelo menos 6 caracteres. Ao concluir, você já entra logado.
4. **Entrar na conta:** clique no ícone 👤, preencha e-mail e senha na aba **Já sou cliente** e clique em **Entrar**.
5. **Finalizar o pedido:** no carrinho, preencha rua, número e bairro (o complemento é opcional), escolha a forma de pagamento na entrega e clique em **Confirmar**. Se você não estiver logado, o sistema pede o login e depois volta ao carrinho com tudo preenchido.
6. **Acompanhar os pedidos:** clique no ícone 📦 no topo da vitrine (ou em **Acompanhar em Meus Pedidos**, na confirmação) para ver o histórico e o status de cada pedido.
7. **Sair:** clique em **Sair** no topo da página.

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

São 36 testes automatizados, que usam um banco temporário em memória (não alteram dados reais). Eles cobrem:

- **vitrine:** exibição dos produtos e preço no padrão brasileiro;
- **carrinho:** vazio, adicionar, agrupar quantidades, diminuir, remover, esvaziar, soma do total e produto inexistente;
- **cadastro:** sucesso, senha guardada com hash, e-mail duplicado, e-mail inválido, senha curta e manutenção dos dados após um erro;
- **login:** sucesso, senha errada, e-mail inexistente, campos vazios e logout;
- **pedido:** finalização com sucesso, carrinho esvaziado, exigência de login, volta ao carrinho após o login, carrinho vazio, endereço incompleto, pagamento inválido e preço histórico preservado;
- **meus pedidos e segurança:** listagem, lista vazia, exigência de login, bloqueio do pedido de outro cliente, página 404 e horário de Brasília.

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

- [x] Salvar o pedido no banco (tabelas `pedidos` e `itens_pedido`).
- [x] Exigir login para finalizar a compra.
- [x] Área do cliente com histórico de pedidos.
- [ ] Trocar as fotos por imagens de cupcakes com licença livre.
- [ ] Testes com usuários reais e correções (Situação-problema 3).
- [ ] Painel do administrador para manter produtos e atualizar o status dos pedidos.
