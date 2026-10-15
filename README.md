# Situação-problema 1 – Revisão do Planejamento

Revisão e atualização do planejamento feito no PIT I, aplicando a melhoria contínua (*Kaizen*) antes e durante o desenvolvimento.

| Documento | Conteúdo | Exigência atendida |
|---|---|---|
| [1. Escopo e Backlog](01-escopo-e-backlog.md) | Contexto, escopo revisado, 18 histórias de usuário, mapa de afinidade, regras de negócio, critérios de aceitação e tarefas | Verificar e adequar o escopo e a ideia |
| [2. Modelagem UML](02-modelagem-uml.md) | Casos de uso (diagrama e 3 expandidos), classes, arquitetura MVC, sequência, atividades e estados | Verificar e adequar a modelagem UML |
| [3. IHC](03-ihc.md) | Princípios, telas reais, campos, catálogo de mensagens, mapa navegacional, mapa conceitual e revisão da interface | Verificar e adequar a IHC |
| [4. Banco de Dados](04-banco-de-dados.md) | Projeto conceitual, lógico normalizado (1FN–3FN), físico e dicionário de dados | Projetos conceitual, lógico e físico + dicionário de dados |
| [schema.sql](schema.sql) | Script de criação do banco em PostgreSQL | Projeto físico |
| [telas/](telas/) | Capturas das telas da aplicação | Protótipo revisado |

## Legenda usada nos documentos

| Símbolo | Significado |
|---|---|
| ✅ | Implementado e funcionando |
| 🟡 | Parcialmente implementado (por exemplo, a tela existe mas a função ainda não) |
| 🔜 | Planejado para a próxima sprint |

## Principais mudanças em relação ao PIT I

1. O aplicativo mobile nativo virou uma **aplicação web responsiva**, publicada no Render.
2. O pagamento online virou **pagamento na entrega** (cartão, PIX ou dinheiro).
3. O painel do administrador passou para uma **versão futura**.
4. Foram criadas **11 regras de negócio** numeradas, referenciadas nos casos de uso e no dicionário de dados.
5. O banco ganhou a entidade associativa **ItemPedido**, que guarda o preço do momento da compra.
6. A revisão das telas reais encontrou **7 melhorias de interface**, que entraram no backlog.
