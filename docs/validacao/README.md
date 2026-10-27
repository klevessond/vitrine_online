# Situação-problema 3 – Validação com Usuários

Testes do sistema publicado feitos por cinco colegas de curso ou profissionais da área, seguidos das correções e da documentação do que mudou.

| Arquivo | Para que serve |
|---|---|
| [formulario-google-forms.md](formulario-google-forms.md) | Textos e perguntas prontos para montar o formulário de teste no Google Forms |
| [relatorio-validacao-modelo.pdf](relatorio-validacao-modelo.pdf) | Modelo do relatório em PDF preenchível: capa, roteiro, laudo dos 5 testadores, problemas e correções, conclusão |
| `prints/` | Pasta para os prints enviados pelos testadores (crie quando receber o primeiro) |

## Passo a passo

**1. Prepare o sistema**
- Confira se a última versão está no ar no Render.
- Faça você mesmo os 12 casos de teste do roteiro antes de enviar. É melhor você achar os erros óbvios do que seus colegas.

**2. Monte o formulário** seguindo o [guia do Google Forms](formulario-google-forms.md). Não esqueça de colar o link do Render na descrição.

**3. Convide cinco pessoas.** Prefira perfis variados: colegas do curso, alguém da área e pelo menos uma pessoa testando pelo celular. Mensagem sugerida:

> Oi, [nome]! Tudo bem? Estou terminando meu projeto integrador da faculdade: uma loja virtual de cupcakes. Você poderia testar e responder um formulário rápido (uns 15 minutos)? Preciso de 5 avaliações até [data]. 🧁
>
> 📝 Formulário com as instruções: [link do Google Forms]
>
> Pode ser bem sincero, encontrar erros é justamente o objetivo. Obrigado!

**4. Acompanhe as respostas.** Peça para enviarem até uma data e lembre quem ainda não respondeu 2 dias antes.

**5. Preencha o relatório em PDF.** Abra o `relatorio-validacao-modelo.pdf` no **Adobe Acrobat Reader** (gratuito) ou no navegador (Chrome ou Edge) e:
- preencha a capa e a tabela de resumo;
- transcreva cada resposta do formulário na página dupla do testador correspondente;
- liste os problemas na página "Problemas encontrados e correções", **uma linha por problema**, mesmo que mais de um testador tenha relatado.

**6. Corrija o que for pertinente.** Para cada correção:
- faça um commit com mensagem clara, por exemplo: `Corrige botão Confirmar cobrindo opção de pagamento (testadores 1 e 3)`;
- atualize a coluna "O que foi feito" e a "Situação" no relatório;
- se decidir **não** corrigir algo, escreva o motivo (por exemplo: "fora do escopo do MVP, entrou no backlog como US19").

**7. Escreva a conclusão** na última página e salve o PDF final com o nome `relatorio-validacao.pdf` nesta pasta.

**8. Grave o vídeo** (cerca de 5 minutos) mostrando o sistema funcionando e as mudanças feitas a partir dos testes.

**9. Suba tudo no GitHub:** o relatório final, a pasta `prints/` e as correções no código.

## Dicas

- **Não esconda falhas.** O PDF da disciplina é explícito: os erros fazem parte da avaliação, porque mostram o processo de melhoria contínua.
- **Ao salvar no navegador**, use "Imprimir → Salvar como PDF" apenas na versão final; ao imprimir, os campos deixam de ser editáveis.
- **Se um testador encontrar um problema grave** (algo que impede o uso), corrija logo e peça para ele testar de novo. Registre isso no relatório.
