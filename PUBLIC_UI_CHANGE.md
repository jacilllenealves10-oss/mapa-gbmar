# GBMar — controles públicos e autoria

Pedido expresso: retirar “Ask ChatGPT” e “Publish” do site original e exibir “Desenvolvido por ASP BM BRAGANÇA”, com seção discreta “Sobre o autor”. Esta entrega é independente do PR de refinamento técnico anterior.

## Alteração

- CSS incorporado ao HTML oculta os dois botões por rótulo acessível, os itens correspondentes do menu por identificador de ícone e as opções correspondentes do menu nativo.
- “Save”, “Cancel”, exportações, edição e demais ações não são selecionados pelas regras. Não houve remoção de dependências nem modificação do runtime.
- Faixa compacta no topo do conteúdo do mapa com o crédito exato. A seção do autor usa `details`/`summary`, fica fechada inicialmente e abre/fecha por clique ou teclado. O texto identifica João Renato Batista de Bragança como Aspirante a Oficial do CBMPE, com atuação no GBMar, responsável pelo desenvolvimento e organização do mapa.
- O mapa ocupa o espaço restante com flexbox; a faixa permite quebra de linha em telas estreitas. A biografia tem largura e altura máximas e rolagem própria.
- O manifesto conserva as referências do JSON e runtime e atualiza apenas tamanho e hash do HTML.

## Integridade e testes

O script `tools/hide_platform_actions.py` exige o hash do HTML de referência. Sua verificação inversa recupera exatamente o HTML anterior, demonstrando que as alterações se limitam ao CSS e à inclusão do componente de autoria. O JSON continua com SHA-256 `b3f4840d6c0327c3d849fc692ce6de10421f2f2a63d4a7621de014fdacd77f93`; o runtime mantém `9e3ede84b28aded3c7379b6e6a5611f0d95b9977eb0f781e279ceefabfcbd27e`.

```sh
python3 tools/hide_platform_actions.py --check
node --test tests/public-ui-*.test.mjs
```

São 25 testes: integridade do patch, sintaxe do JavaScript, estrutura acessível da autoria e 22 verificações das funções extraídas do HTML, cobrindo contagens, filtros, postos, períodos, georreferenciamento, tubarões, auditoria e exportação. Referências preservadas: 3.471 linhas, 3.340 valores distintos no campo protocolo e 16 postos, incluindo P05 de Jaboatão. Nenhuma mudança de dados ou métodos.

Limite de validação: navegador público bloqueado no ambiente e Chromium local indisponível. Não se declara teste visual concluído. A ocultação de opções em seletores nativos pode variar conforme navegador/sistema; os menus personalizados usam `:has`, disponível em navegadores modernos. Nenhum script foi adicionado para remover nós controlados pelo runtime. A ocultação é de apresentação, não uma mudança de permissões.

## Publicação e reversão

Implementação em branch separada, seguida de PR exclusivo para os pedidos autorizados. A página `docs/postos.html` e seus assets, presentes no commit-base `1a3f2c7352c26e3024ee98f817f3c55c191a57d3`, permanecem inalterados. O PR de refinamento anterior continua separado e precisará atualizar sua base antes de eventual integração.

Para reverter, reverter o commit desta alteração, restaurando juntos o HTML e seu manifesto. Não alterar o JSON. Para reproduzir em uma cópia limpa do commit-base, adicionar o script desta entrega e executá-lo sem `--check`.
