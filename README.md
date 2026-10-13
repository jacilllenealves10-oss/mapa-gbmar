# GBMar — mapa de ocorrências e prevenções

Site estático com os dados revisados de 01/01 a 12/10/2026. Revisão de 13/10/2026: 16 postos cadastrados, incluindo o Posto 05 de Jaboatão (Hotel Dan Inn Mar), com 11 protocolos associados.

Preserva os filtros recolhíveis, análises por cidade e posto, evolução temporal, exportações, auditoria e a distinção entre coordenadas originais e inferidas. O fundo cartográfico Esri depende de internet; não exige chave de API nem banco de dados.

## Publicação

Repositório: `mapa-gbmar`, na conta conectada `jacilllenealves10-oss`.
Os arquivos estáticos estão em docs. Em Settings → Pages → Source, selecione Deploy from a branch; escolha main e /docs; clique Save. A ativação do Pages precisa ser concluída nas configurações do repositório.

Cada atualização dos arquivos na pasta docs será publicada pelo GitHub Pages após essa configuração.

Documentação: https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages

## Validação

22 testes automatizados aprovados; build estático concluído. Validação visual em navegador e verificação de implantação ainda pendentes. O ponto J05 é um medoide aproximado com seis protocolos de apoio; não é levantamento GPS oficial. Não confundir postos cadastrados com postos ativados diariamente.

O arquivo JSON identificado por hash contém os dados completos usados pelo mapa. Mantenha-o junto de index.html; publique os dois arquivos da mesma versão. As estatísticas usam protocolo distinto e preservam os registros sem ponto nos totais.
