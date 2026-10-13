# GBMar — refinamento técnico controlado

Revisão de referência: `65470566ec4904f562ffe8a5c9e46924c3594deb`.
Entrega em branch separada, para revisão. Sem merge ou publicação.

## Alterações delimitadas

| Problema comprovado no código | Antes | Proposta aplicada | Benefício verificável |
| --- | --- | --- | --- |
| Cor de fundo usada como cor de texto em quatro seletores próprios | `.gb-note`, `.gb-record small`, `.gb-metrics span` e a regra final de `.gb-compact small` usavam `--muted` | Usam o token textual existente `--text`; dimensões e disposição preservadas | Contraste calculado sobre a superfície padrão passa de cerca de 1,04:1 / 1,09:1 para 16,64:1 / 16,10:1 nos temas claro / escuro |
| Idioma HTML incompatível com o conteúdo | `lang="en"` | `lang="pt-BR"` | Identificação correta do idioma para tecnologias assistivas |
| Título com quantidade desatualizada | “Comparação dos 15 postos” | “Comparação dos postos cadastrados” | Título compatível com os 16 postos sem fixar nova quantidade no código |
| Rótulo podia ser confundido com ausência de qualquer localização | “Sem ponto utilizável” | “Sem coordenada original utilizável” | Explicita o significado do filtro; valor interno e resultados preservados, inclusive pontos inferidos |
| Contagem sem ressalva sobre identificador vazio | Metodologia descrevia 3.340 protocolos sem a ressalva | Explicita 3.340 valores distintos: 3.339 identificadores preenchidos e um valor vazio na linha analítica 2546 | Torna a limitação da fonte visível sem corrigir dados ou mudar a contagem |

São oito substituições exatas no HTML: quatro regras CSS, idioma e três textos/rótulos. O manifesto recebeu somente o novo tamanho e SHA-256 do HTML. O arquivo aumentou 253 bytes. Não foram introduzidas dependências, requisições, páginas ou componentes de interface.

## Método e riscos

O repositório contém um artefato gerado, com runtime incorporado e JSON externo. Esta entrega não pretende reconstruir o projeto-fonte completo. `tools/refine_presentation.py` documenta e reproduz o patch delimitado sobre o HTML estável. Só aceita o hash original ou o resultado exato; se a versão mudar, interrompe a operação para revisão manual. O teste inverso recupera o hash do HTML original, comprovando a ausência de outras modificações, inclusive nos terceiros incorporados.

O runtime, o código cartográfico, o carregador do JSON e as funções de negócio permanecem byte a byte iguais. `--muted` não foi redefinido globalmente. O token `--text` já é usado pela aplicação; o contraste calculado refere-se às cores padrão do código. Temas externos e a composição visual ainda exigem inspeção em navegador. O rótulo mais longo pode ocupar mais espaço no seletor em celulares; esse é um ponto explícito da revisão visual.

A ressalva metodológica descreve a base atual, como o restante da metodologia existente. Se a base for atualizada, deve ser revisada junto com as demais referências estáticas. O valor vazio não foi convertido em protocolo fictício nem removido dos totais. Sua conferência exige consulta à fonte e autorização específica para eventual mudança de dados.

## Regressão automatizada

Requisitos de execução: Node.js com suporte a `node:test` e Python 3; sem instalação de pacotes.

```sh
node --test tests/*.test.mjs
python3 tools/refine_presentation.py --check
```

Resultado nesta revisão: **29 testes aprovados, zero falhas**. Os 22 testes funcionais executam as funções extraídas do próprio HTML entregue. Os sete testes adicionais verificam integridade, delimitação do patch, sintaxe, contraste padrão, ressalva e exportação. O teste CSV compara todas as células após leitura com um analisador independente.

| Referência de regressão | Versão estável e proposta |
| --- | --- |
| Linhas analíticas | 3.471 |
| Valores distintos no campo protocolo, incluindo vazio | 3.340 |
| Identificadores preenchidos distintos | 3.339 |
| Postos | 16; Olinda 2, Recife 10, Jaboatão 4 |
| Posto 05 de Jaboatão | 11 protocolos, mantidos no filtro individual e no conjunto |
| Protocolos com prevenção / outra natureza | 3.142 / 200; interseção preservada |
| Afogamentos / vítimas fatais pela rotina existente | 43 / 10 |
| Pontos de linhas com coordenadas originais / incluindo inferências | 1.226 / 1.580 |
| Linhas pendentes de localização | 1.891, mantidas nos totais |
| Registros de tubarão | 3; um original, dois inferidos; cancelamento preservado |
| Exportação integral CSV | 3.471 linhas de dados, 53 campos; todas as células conferidas |

Preservados: filtros por cidade, posto, período, categoria, natureza, origem da localização e auditoria; combinação de filtros; períodos inclusivos e progressão cumulativa; raios geodésicos; busca por protocolo; recorte vazio; evidências e coordenadas originais; distinção entre atendimento e cancelamento; divergências municipais; vínculos por texto e distância; exportação e proveniência.

O JSON mantém SHA-256 `b3f4840d6c0327c3d849fc692ce6de10421f2f2a63d4a7621de014fdacd77f93` e 5.528.380 bytes. O runtime mantém SHA-256 `9e3ede84b28aded3c7379b6e6a5611f0d95b9977eb0f781e279ceefabfcbd27e`. As referências relativas e `.nojekyll` foram preservadas para GitHub Pages. O novo HTML tem SHA-256 `eb7529ed0f96bba214cc10b2ca7d67f7be979264e95a7e337cacab4169aa51c3` e 3.058.983 bytes.

## Inspeção visual pendente e critérios de aceitação

O navegador disponível bloqueou o acesso ao site com `ERR_BLOCKED_BY_CLIENT` durante a auditoria. Não há validação visual concluída em computador ou celular. Testes de sintaxe e integridade não comprovam renderização, carregamento de mapas externos ou interação real com o navegador.

Antes de aprovar publicação, servir esta branch localmente e comparar com a versão estável nas mesmas dimensões. `python3 -m http.server 8000 --directory docs` disponibiliza o conteúdo em `http://localhost:8000/?view=1&tab=dashboard`.

- [ ] Conferir computador e celular, inclusive largura de 360 px: ausência de sobreposição e corte; leitura dos textos alterados nos temas claro e escuro.
- [ ] Abrir/recolher o painel no canto superior direito; alternar abas; confirmar navegação e controles cartográficos.
- [ ] Conferir mapa, camadas, zoom, agrupamentos, legenda, postos e pop-ups, incluindo P05 de Jaboatão.
- [ ] Exercitar cada filtro disponível e combinações; limpar filtros; conferir igualdade dos resultados com a versão estável.
- [ ] Avançar período e reprodução temporal; conferir totais, listagens e recorte vazio.
- [ ] Conferir originais/inferidos, os três registros de tubarão e a auditoria geográfica.
- [ ] Baixar CSV pela interface e conferir arquivo; a preservação textual de protocolos na abertura em planilhas depende das opções de importação do programa.
- [ ] Conferir ausência de erros no console e falhas na obtenção de JSON, runtime e bases cartográficas.
- [ ] Aprovar expressamente merge e publicação somente após resolver qualquer regressão observada.

## Itens adiados e preservação

“Ask ChatGPT” e “Publish” pertencem ao runtime incorporado; sua presença efetiva na versão pública não foi confirmada visualmente nesta auditoria. Eles não foram ocultados nem removidos, e não houve alteração do modo de hospedagem. Fontes muito pequenas em telas estreitas e semântica de abas ficam para revisão com inspeção visual e de acessibilidade. Não há redesenho, troca de paleta, alteração dos dados, categorias, métodos estatísticos, coordenadas, identificadores ou relacionamentos.

## Reprodução e reversão

O script é idempotente para este resultado e falha diante de outra versão. Para reproduzir em uma cópia da branch de revisão, restaurar somente `docs/index.html` e `docs/data-app-build.json` a partir do commit de referência e executar `python3 tools/refine_presentation.py`; depois executar os testes. Não executar a reprodução sobre trabalho local não salvo.

A branch estável permanece intacta. Antes de merge, basta fechar o PR para descartar a proposta. Se posteriormente aprovada e incorporada, a alteração pode ser revertida pelo commit correspondente, restaurando juntos o HTML e seu manifesto, sem tocar no JSON.
