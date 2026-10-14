# GBMar — legibilidade dos temas

Correção solicitada para aplicação imediata no site. Base do repositório: `89d36997484b59dbdc7efb7bd37f13d93a01fd88`; HTML de referência SHA-256 `7f55e71ac4a5003a9f234cdc67ccbeab1df5431c011bcadce528431627f86d6f`.

## Problemas comprovados e correções

- Notas, rótulos de indicadores e metadados de ocorrências usavam `--muted`, um token de fundo. Agora usam `--text`.
- Textos secundários compartilhados passam a usar a tinta principal do tema, eliminando combinações claras sobre claro. O token de fundo `--muted` permanece intacto.
- Títulos de ocorrências deixam de usar as cores fixas dos marcadores como tinta. As cores e categorias dos marcadores e legendas não mudam.
- Links de evidências permanecem identificáveis por sublinhado, com texto adaptado ao tema.
- Textos operacionais pequenos passam a 12 px, inclusive no celular; códigos dos postos passam a 11 px. A organização e os controles permanecem os mesmos.
- Letras e números sobre o mapa ganham fundo opaco. Atribuição, escala e aviso cartográfico deixam de depender da imagem de fundo para o contraste.
- O tema Original inicia em claro, com texto escuro, mesmo quando o sistema está escuro. A escolha explícita de aparência Escuro continua disponível. Temas previamente escolhidos não são apagados; o tema azul permanece disponível. Não houve escrita em armazenamento do navegador.

## Medição por tema

Razão de contraste por luminância sRGB. As paletas foram extraídas do runtime entregue. Para Original foram usados os valores padrão claro/escuro da folha de estilo, correspondentes a Classic. O mínimo corrigido considera o texto principal e secundário sobre seis superfícies do tema. Critério: pelo menos 4,5:1; não é uma auditoria WCAG integral nem inspeção visual.

| Tema | Aparência | Nota antes, na superfície | Menor razão corrigida nas seis superfícies |
| --- | --- | ---: | ---: |
| Original theme | Claro | 1.04:1 | 15.25:1 |
| Original theme | Escuro | 1.09:1 | 13.20:1 |
| Classic | Claro | 1.04:1 | 15.25:1 |
| Classic | Escuro | 1.09:1 | 13.20:1 |
| Neutral | Claro | 1.09:1 | 15.63:1 |
| Neutral | Escuro | 1.15:1 | 11.49:1 |
| Dark pixel | Escuro | 1.28:1 | 11.51:1 |
| Scientific blue | Claro | 1.11:1 | 14.23:1 |
| Scientific blue | Escuro | 1.20:1 | 10.79:1 |
| Sticker pop | Claro | 1.10:1 | 15.66:1 |
| Sticker pop | Escuro | 1.13:1 | 12.24:1 |

Também foram conferidos dez pares fixos: filtros, aba selecionada, agrupamentos, código de posto, aviso, medição, recorte vazio, atribuição, link da atribuição e tooltip. Todos passaram em 4,5:1. Valores completos em `THEMES_CONTRAST.json`.

## Validação e limites

**40 testes aprovados**, incluindo 25 testes existentes de integridade, autoria, filtros, períodos, postos, georreferenciamento, tubarões, contagens e CSV. Os testes adicionais cobrem o catálogo completo, os contrastes calculados e a rotina real de aparência extraída do runtime (com DOM mínimo, não um navegador).

```sh
node --test tests/*.test.mjs
python3 tools/improve_theme_contrast.py --check
python3 tools/hide_platform_actions.py --check
```

O navegador disponibilizado retornou `ERR_BLOCKED_BY_CLIENT` ao acessar o site. A visualização humana, a cascata CSS efetivamente renderizada, o layout em dispositivos reais e o funcionamento completo da escolha de temas pela interface não puderam ser confirmados. Os resultados não abrangem todos os estados possíveis de componentes do runtime nem os textos presentes nas imagens cartográficas externas. Recomenda-se a conferência visual dos painéis Filtros, Análise, Registros, detalhes e Sobre o autor em cada tema após a implantação.

## Preservação e reversão

O patch adiciona exclusivamente uma camada CSS ao HTML publicado e atualiza o hash/tamanho no manifesto. A remoção exata dessa camada recupera o hash do HTML anterior. A verificação de integridade da autoria foi estendida para validar essa camada antes de conferir a versão anterior; não aceita conteúdo arbitrário.

JSON e runtime permanecem byte a byte iguais. Preservados os 3.471 registros analíticos, 3.340 valores distintos no campo protocolo, 16 postos, coordenadas, categorias, contagens, fontes, filtros, exportações, autoria e ocultação dos controles solicitados. A página `postos.html` e seus assets não são alterados. O PR nº 1 de refinamento permanece separado; não foi incorporado.

Alteração em branch e PR próprios. Reversão pelo commit restaura juntos o HTML e o manifesto. O script aceita somente o HTML de referência ou seu resultado exato.
