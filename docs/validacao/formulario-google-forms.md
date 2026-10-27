# Formulário de teste (Google Forms)

Monte o formulário em [forms.google.com](https://forms.google.com) copiando os textos abaixo. Leva cerca de 15 minutos.

**Configurações recomendadas** (ícone de engrenagem ⚙️):
- **Respostas → Coletar endereços de e-mail:** desativado (o nome já identifica o testador).
- **Respostas → Limitar a 1 resposta:** desativado (o upload de arquivo já exige login no Google).
- **Apresentação → Mostrar barra de progresso:** ativado.

---

## Título e descrição do formulário

**Título:** Teste do sistema Cupcake Gourmet

**Descrição:**

> Olá! Obrigado por testar meu projeto da faculdade (PIT II – Engenharia de Software). É uma loja virtual de cupcakes em que você monta o carrinho, cria uma conta e faz um pedido com pagamento na entrega.
>
> 🔗 **Link do sistema:** [cole aqui o link do Render]
>
> ⏳ O servidor é gratuito e "dorme" quando ninguém usa: o primeiro acesso pode levar cerca de 1 minuto. É normal.
>
> 🔒 Use dados fictícios no cadastro e no endereço, e uma senha que você não usa em outros sites. Nenhum valor é cobrado e nenhum pedido é entregue de verdade.
>
> O teste leva uns 15 minutos. Se algo der errado, tire um print da tela: ele vai me ajudar muito a corrigir. Pode ser sincero, os erros fazem parte do aprendizado!

---

## Seção 1 – Quem está testando

| Pergunta | Tipo | Obrigatória | Opções / observação |
|---|---|---|---|
| Nome completo | Resposta curta | Sim | |
| Data do teste | Data | Sim | |
| Curso, área ou profissão | Resposta curta | Sim | Ex.: Engenharia de Software, desenvolvedor |
| Em qual dispositivo você testou? | Caixas de seleção | Sim | Celular · Computador · Tablet |
| Qual navegador você usou? | Múltipla escolha | Sim | Chrome · Safari · Firefox · Edge · Samsung Internet · Outro |

## Seção 2 – Roteiro de testes

**Descrição da seção:**

> Faça os testes abaixo na ordem e marque o resultado de cada um. Nos testes com dados errados (CT05, CT06 e CT08), "Funcionou" significa que o sistema mostrou uma mensagem de erro clara.

**Pergunta:** Resultado de cada teste
**Tipo:** Grade de múltipla escolha · Obrigatória: Sim · ative **"Exigir uma resposta em cada linha"**

**Colunas:** Funcionou · Não funcionou · Não testei

**Linhas** (cole uma por linha):

```
CT01 – Abrir o site e ver os cupcakes com foto, descrição e preço
CT02 – Adicionar cupcakes ao carrinho e ver o total
CT03 – No carrinho, usar + e − e remover um item
CT04 – Esvaziar o carrinho
CT05 – Criar uma conta (tente antes com e-mail errado ou senha curta)
CT06 – Sair e entrar de novo na conta (tente antes com a senha errada)
CT07 – Sair da conta, montar o carrinho e clicar em Confirmar (deve pedir login e voltar ao carrinho)
CT08 – Clicar em Confirmar sem preencher a rua ou o bairro (deve mostrar erro)
CT09 – Fazer um pedido completo (deve mostrar o número do pedido)
CT10 – Abrir "Meus Pedidos" pelo ícone da caixa 📦
CT11 – Usar o site pelo celular (nada cortado ou difícil de tocar)
CT12 – Digitar um endereço que não existe, ex.: /teste no fim do link (deve mostrar "Página não encontrada")
```

## Seção 3 – Sua avaliação

| Pergunta | Tipo | Obrigatória | Texto de ajuda |
|---|---|---|---|
| O que você testou e funcionou? | Parágrafo | Sim | Conte o que deu certo e o que achou fácil de usar. |
| O que você testou e NÃO funcionou? | Parágrafo | Não | Descreva o que fez, o que aconteceu e o que esperava. Se tudo funcionou, deixe em branco. |
| Teve alguma funcionalidade que você não testou? Por quê? | Parágrafo | Não | Ex.: não encontrei a opção, faltou tempo, a página não carregou. |
| Sugestões de melhoria | Parágrafo | Não | Ideias, textos confusos, cores, qualquer coisa. |
| Prints das telas com erro | Upload de arquivo | Não | Até 5 arquivos, tipo **Imagem**, tamanho máximo **10 MB** |
| Que nota você dá para o sistema? | Escala linear | Sim | De **1** (Ruim) a **5** (Excelente) |

> O upload de arquivo exige que o testador entre com uma conta Google. Se alguém não quiser, peça os prints pelo WhatsApp ou e-mail.

## Mensagem de confirmação

Em **Configurações → Apresentação → Mensagem de confirmação**:

> Muito obrigado pelo seu tempo! 🧁 Sua avaliação vai direto para o relatório de validação do meu projeto.

---

## Depois de receber as respostas

1. Na aba **Respostas**, clique no ícone do Planilhas para ver tudo em uma planilha.
2. Os prints ficam em uma pasta no seu Google Drive. Baixe-os e salve em `docs/3-validacao/prints/` com nomes como `testador1-carrinho.png`.
3. Transcreva as respostas para o [relatório em PDF](relatorio-validacao-modelo.pdf) (uma página dupla por testador).
