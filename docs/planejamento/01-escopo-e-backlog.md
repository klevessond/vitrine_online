# 1. Escopo e Backlog do Produto

## 1.1 Contexto do negócio

Uma loja de cupcakes gourmet quer vender pela internet. Uma tentativa anterior falhou porque os requisitos foram mal levantados e o aplicativo não funcionava, o que gerou reclamações e arranhou a imagem da loja. Por isso, o foco deste projeto é um sistema **simples, confiável e fácil de usar**, construído em ciclos curtos e validado com usuários.

## 1.2 Objetivo

Oferecer uma **vitrine virtual** em que o cliente escolha os cupcakes, monte o carrinho, faça o pedido com entrega e pagamento na entrega, e acompanhe seus pedidos, pelo celular ou pelo computador.

## 1.3 Escopo

| Dentro do escopo (MVP) | Fora do escopo (versões futuras) |
|---|---|
| Vitrine com foto, descrição e preço | Pagamento online (gateway de cartão ou PIX automático) |
| Carrinho de compras | Cálculo de frete por CEP |
| Cadastro, login e logout de clientes | Recuperação de senha por e-mail |
| Pedido com endereço e forma de pagamento na entrega | Cupons de desconto |
| Histórico de pedidos do cliente | Aplicativo nativo para Android/iOS |
| Mensagens de erro claras | Painel administrativo completo |

### Revisão do escopo em relação ao PIT I (melhoria contínua)

| Mudança | Motivo |
|---|---|
| Aplicativo mobile nativo → **aplicação web responsiva** | Funciona no celular e no computador com um único código, e pode ser publicada gratuitamente no Render. |
| Pagamento online → **pagamento na entrega** (cartão, PIX ou dinheiro) | Integrar um gateway exige contrato e homologação; o pagamento na entrega atende o MVP sem riscos. |
| Painel do administrador → **versão futura** | O cliente final é a prioridade; os produtos podem ser cadastrados direto no banco por enquanto. |

## 1.4 Atores

| Ator | Descrição |
|---|---|
| **Visitante** | Pessoa que acessa a loja sem estar logada. Vê a vitrine e usa o carrinho. |
| **Cliente** | Visitante cadastrado e logado. Finaliza pedidos e vê o histórico. |
| **Administrador** | Funcionário da loja (versão futura). Mantém produtos e atualiza o status dos pedidos. |

## 1.5 Histórias de usuário

Prioridade: **A** = essencial, **B** = importante, **C** = desejável. Pontos na escala de Fibonacci (1, 2, 3, 5, 8).

| ID | História de usuário | Pontos | Prioridade | Situação |
|---|---|---|---|---|
| US01 | Como **visitante**, quero ver os cupcakes com foto, descrição e preço, para escolher o que comprar. | 2 | A | ✅ Implementada |
| US02 | Como **visitante**, quero adicionar um cupcake ao carrinho, para comprar mais de um produto de uma vez. | 3 | A | ✅ Implementada |
| US03 | Como **visitante**, quero ver os itens do carrinho e o total, para saber quanto vou pagar. | 2 | A | ✅ Implementada |
| US04 | Como **visitante**, quero esvaziar o carrinho, para recomeçar a escolha. | 1 | B | ✅ Implementada |
| US05 | Como **visitante**, quero criar uma conta com nome, e-mail e senha, para poder fazer pedidos. | 3 | A | ✅ Implementada |
| US06 | Como **cliente**, quero entrar com e-mail e senha, para acessar minha conta. | 3 | A | ✅ Implementada |
| US07 | Como **cliente**, quero sair da conta, para proteger meus dados em um aparelho compartilhado. | 1 | B | ✅ Implementada |
| US08 | Como **usuário**, quero mensagens claras quando eu errar algum dado, para saber como corrigir. | 2 | A | ✅ Implementada |
| US09 | Como **cliente**, quero informar o endereço de entrega, para receber os cupcakes em casa. | 2 | A | 🟡 Tela pronta |
| US10 | Como **cliente**, quero escolher pagar com cartão, PIX ou dinheiro na entrega, para usar o meio que prefiro. | 2 | A | 🟡 Tela pronta |
| US11 | Como **cliente**, quero confirmar o pedido e ter ele registrado, para que a loja comece a preparar. | 5 | A | 🔜 Próxima sprint |
| US12 | Como **cliente**, quero ver a confirmação com o número do pedido, para ter certeza de que deu certo. | 2 | A | 🟡 Tela pronta |
| US13 | Como **cliente**, quero ver meus pedidos anteriores e o status de cada um, para acompanhar a entrega. | 3 | B | 🔜 Próxima sprint |
| US14 | Como **visitante**, quero alterar a quantidade ou remover um item do carrinho, sem esvaziar tudo. | 3 | B | 🔜 Próxima sprint |
| US15 | Como **visitante**, quero ser levado ao login ao finalizar sem estar logado, e voltar ao carrinho depois, para não perder minha compra. | 2 | B | 🔜 Próxima sprint |
| US16 | Como **administrador**, quero cadastrar, editar e desativar cupcakes, para manter a vitrine atualizada. | 8 | C | Futuro |
| US17 | Como **administrador**, quero mudar o status dos pedidos, para informar o cliente sobre a entrega. | 5 | C | Futuro |
| US18 | Como **cliente**, quero recuperar minha senha pelo e-mail, para não perder o acesso à conta. | 5 | C | Futuro |

## 1.6 Mapa de afinidade

As histórias foram agrupadas por tema:

| Vitrine e Carrinho | Conta do Cliente | Pedido e Entrega | Administração |
|---|---|---|---|
| US01 Ver produtos | US05 Criar conta | US09 Endereço | US16 Manter produtos |
| US02 Adicionar ao carrinho | US06 Login | US10 Pagamento | US17 Status do pedido |
| US03 Ver carrinho e total | US07 Logout | US11 Confirmar pedido | |
| US04 Esvaziar carrinho | US08 Mensagens de erro | US12 Confirmação | |
| US14 Alterar quantidade | US18 Recuperar senha | US13 Histórico | |
| | | US15 Login no checkout | |

## 1.7 Regras de negócio

| ID | Regra |
|---|---|
| RN01 | Cada e-mail só pode ser cadastrado uma vez. |
| RN02 | A senha deve ter no mínimo 6 caracteres e é guardada apenas como *hash*. |
| RN03 | O e-mail é guardado em letras minúsculas e sem espaços, para que "Maria@Email.com" e "maria@email.com" sejam o mesmo cadastro. |
| RN04 | Em um login inválido, o sistema não informa se o erro foi no e-mail ou na senha (evita que alguém descubra quais e-mails estão cadastrados). |
| RN05 | Somente clientes logados podem finalizar um pedido. |
| RN06 | Um carrinho vazio não pode ser finalizado. |
| RN07 | Rua, número e bairro são obrigatórios na entrega; o complemento é opcional. |
| RN08 | O pagamento é feito na entrega, por cartão, PIX ou dinheiro. |
| RN09 | O preço de cada item é registrado no momento da compra e não muda se o preço do produto mudar depois. |
| RN10 | O total do pedido é a soma de quantidade × preço unitário de todos os itens. |
| RN11 | Todo pedido começa com o status "recebido" e segue: recebido → em preparo → saiu para entrega → entregue. Um pedido pode ser cancelado antes de sair para entrega. |

## 1.8 Critérios de aceitação das histórias principais

Formato **Dado / Quando / Então**:

**US05 – Criar conta**
- **Dado** que estou na aba "Quero me cadastrar", **quando** preencho nome, um e-mail válido e uma senha com 6 ou mais caracteres, **então** a conta é criada, entro logado e vejo "Olá, [nome]" na vitrine.
- **Dado** que o e-mail já existe, **quando** tento cadastrar, **então** vejo "Este e-mail já está cadastrado. Faça login." e o nome digitado continua no formulário.
- **Dado** que a senha tem menos de 6 caracteres, **quando** tento cadastrar, **então** vejo uma mensagem pedindo pelo menos 6 caracteres.

**US06 – Login**
- **Dado** que tenho conta, **quando** informo e-mail e senha corretos, **então** entro na conta e vejo uma mensagem de boas-vindas.
- **Dado** que errei a senha ou o e-mail, **quando** tento entrar, **então** vejo a tela "Acesso Negado" com a opção de tentar novamente.

**US11 – Confirmar pedido**
- **Dado** que estou logado, com itens no carrinho e endereço preenchido, **quando** clico em "Confirmar", **então** o pedido é gravado com status "recebido", o carrinho é esvaziado e vejo a confirmação com o número do pedido.
- **Dado** que não estou logado, **quando** clico em "Confirmar", **então** sou levado ao login e, depois de entrar, volto ao carrinho com meus itens.
- **Dado** que deixei a rua em branco, **quando** clico em "Confirmar", **então** vejo uma mensagem indicando o campo obrigatório e meus dados digitados continuam na tela.

## 1.9 Tarefas da próxima sprint

| História | Tarefa | Estimativa |
|---|---|---|
| US11 | Criar os modelos `Pedido` e `ItemPedido` no `models.py` | 2 h |
| US11 | Dar `name` aos campos do checkout e enviar o formulário via POST | 1 h |
| US11 | Criar a rota `/finalizar` com as validações RN05 a RN10 | 4 h |
| US11 | Escrever os testes do pedido | 3 h |
| US12 | Mostrar o número e o resumo do pedido na tela de sucesso | 2 h |
| US13 | Criar a rota e a tela "Meus pedidos" | 4 h |
| US14 | Agrupar itens iguais e criar os botões + / − / remover | 4 h |
| US15 | Redirecionar ao login e voltar ao carrinho | 2 h |
