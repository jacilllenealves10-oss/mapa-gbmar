#!/usr/bin/env python3
"""Correção delimitada de legibilidade; preserva dados, runtime e escolha de tema."""
import argparse
import hashlib
import json
from pathlib import Path

BASE_HASH = '7f55e71ac4a5003a9f234cdc67ccbeab1df5431c011bcadce528431627f86d6f'
STYLE = '''<style id="gbmar-readable-themes">
/* Primeiro acesso: Original claro. A opção Escuro continua disponível. */
:root:not([data-app-appearance="dark"]):is(:not([data-app-theme]),[data-app-theme="original"]) {
  --fixed-theme-scheme: light;
  color-scheme: light;
}
/* O token muted é fundo; não deve ser usado como tinta. */
:root { --secondary: var(--text) !important; }
.gb-note, .gb-record small, .gb-metrics span, .gb-compact small,
.gb-record > b { color: var(--text) !important; }
.gb-body a, .gb-record a, .source-links a, .source-pill[href]:hover, .notes a {
  color: var(--text); text-decoration: underline; text-underline-offset: 2px;
}
.theme-preview-type > span { color: var(--preview-text); }
/* Textos operacionais pequenos: leitura mínima de 12 px, inclusive no celular. */
.gb-note, .gb-legend, .gb-field, .gb-check, .gb-metrics span,
.gb-method, .gb-app table, .gb-app th, .gb-record small,
.gb-compact span, .gb-compact small, .gb-mapnotice { font-size: 12px; }
.gb-record small { line-height: 1.6; }
/* Rótulos sobre o mapa precisam de fundo opaco, pois a imagem varia. */
.gb-count { color: #fff; background: #163c4d; border-radius: 4px;
  font-size: 12px; line-height: 16px; text-shadow: none; }
.gb-post-marker span, .gb-postsample { font-size: 11px; }
.gb-mapnotice { background: #fff5df; color: #6d541c; }
.gb-map .leaflet-control-attribution, .gb-map .leaflet-control-scale-line {
  background: #fff; color: #333; text-shadow: none;
}
.gb-map .leaflet-control-attribution a { color: #005a7a; }
</style>
'''


def digest(value):
    return hashlib.sha256(value).hexdigest()


def restore_base(html):
    assert html.count(STYLE) == 1, 'Camada de contraste ausente, diferente ou duplicada.'
    original = html.replace(STYLE, '', 1)
    assert digest(original.encode()) == BASE_HASH, 'Alteração fora da camada autorizada.'
    return original


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    docs = Path(__file__).resolve().parents[1] / 'docs'
    html_path = docs / 'index.html'
    manifest_path = docs / 'data-app-build.json'
    raw = html_path.read_bytes()
    html = raw.decode()
    manifest = json.loads(manifest_path.read_text())
    is_original = digest(raw) == BASE_HASH
    if not is_original:
        restore_base(html)
    if args.check:
        assert not is_original, 'Correção não aplicada.'
        assert manifest['html'] == {'path': 'index.html', 'sha256': digest(raw), 'bytes': len(raw)}
        print('OK: somente a camada CSS autorizada foi adicionada; manifesto consistente.')
        return
    if not is_original:
        print('Correção já aplicada; nenhum arquivo alterado.')
        return
    assert html.count('</head>') == 1
    result = html.replace('</head>', STYLE + '</head>', 1).encode()
    manifest['html'] = {'path': 'index.html', 'sha256': digest(result), 'bytes': len(result)}
    html_path.write_bytes(result)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('Contraste e padrão claro aplicados; manifesto atualizado.')


if __name__ == '__main__':
    main()
