#!/bin/sh
# Publica exclusivamente o mapa de postos como site independente no Cloudflare Pages.
# Projeto sugerido: postos-gbmar-aspbraganca (domínio *.pages.dev).
# Não modifica docs/index.html, o dashboard ou outros arquivos do GBMar.
set -eu

SOURCE="docs"
TARGET="cloudflare-site"

test -s "$SOURCE/postos.html" || { echo "ERRO: docs/postos.html nao encontrado"; exit 1; }
test -s "$SOURCE/assets/leaflet-1.9.4.css" || { echo "ERRO: CSS local do Leaflet nao encontrado"; exit 1; }
test -s "$SOURCE/assets/LICENSE-leaflet.txt" || { echo "ERRO: licenca do Leaflet nao encontrada"; exit 1; }

mkdir -p "$TARGET/assets"
cp "$SOURCE/postos.html" "$TARGET/index.html"
cp "$SOURCE/postos.html" "$TARGET/postos.html"
cp "$SOURCE/assets/leaflet-1.9.4.css" "$TARGET/assets/leaflet-1.9.4.css"
cp "$SOURCE/assets/LICENSE-leaflet.txt" "$TARGET/assets/LICENSE-leaflet.txt"

echo "Cloudflare Pages: mapa de postos pronto em $TARGET/"
