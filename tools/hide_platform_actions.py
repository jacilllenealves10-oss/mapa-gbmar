#!/usr/bin/env python3
"""Aplica/confere a ocultação solicitada e o crédito de autoria no GitHub Pages."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re

BASE_HASH = "d90c5b894ecd268b4ae61a72e7dcdcc5771438195165404fddda7efc556a1238"
SNAPSHOT_HASH = "b3f4840d6c0327c3d849fc692ce6de10421f2f2a63d4a7621de014fdacd77f93"
RUNTIME_HASH = "9e3ede84b28aded3c7379b6e6a5611f0d95b9977eb0f781e279ceefabfcbd27e"
STYLE = '''<style id="gbmar-public-actions">
/* GitHub Pages: ocultar somente Ask ChatGPT e Publish, por solicitação do responsável. */
button.dashboard-ask-button[aria-label="Ask ChatGPT"],
button.dashboard-publish-button[aria-label="Publish"],
button.dashboard-publish-button[aria-label="Publish changes"],
.dashboard-header-action-menu .dashboard-action-menu-item:has(> [data-dashboard-icon="chatBubble"]),
.dashboard-header-action-menu .dashboard-action-menu-item:has(> [data-dashboard-icon="globe"]),
.dashboard-native-overflow option[value="ask"],
.dashboard-native-overflow option[value="publish"] {
  display: none !important;
}
.gb-app { display: flex; flex-direction: column; min-height: 0; }
.gb-app > .gb-mapframe { height: auto; flex: 1; min-height: 0; }
.gb-author { position: relative; flex: 0 0 auto; display: flex; flex-wrap: wrap;
  align-items: center; gap: 2px 14px; padding: 6px 14px; font-size: 12px;
  line-height: 1.5; color: var(--text); background: var(--surface);
  border-bottom: 1px solid var(--border); z-index: 700; }
.gb-author > span { overflow-wrap: anywhere; }
.gb-author-about { margin-left: auto; }
.gb-author-about > summary { cursor: pointer; padding: 5px 0; }
.gb-author-about > summary:focus-visible { outline: 2px solid var(--text); outline-offset: 3px; }
.gb-author-panel { position: absolute; right: 10px; top: calc(100% + 6px);
  box-sizing: border-box; width: 330px; max-width: calc(100vw - 32px);
  max-height: 50dvh; overflow-y: auto; padding: 14px 16px;
  border: 1px solid var(--border); border-radius: 10px;
  background: var(--surface); color: var(--text); box-shadow: 0 6px 20px #0002; }
.gb-author-panel p { margin: 0 0 8px; }
.gb-author-panel p:last-child { margin-bottom: 0; }
</style>
'''
AUTHOR_FUNCTION = '''function GbmarAuthorCredit() {
  return jsxRuntime.jsxs('header', { className: 'gb-author', children: [
    jsxRuntime.jsx('span', { children: 'Desenvolvido por ASP BM BRAGANÇA' }),
    jsxRuntime.jsxs('details', { className: 'gb-author-about', children: [
      jsxRuntime.jsx('summary', { children: 'Sobre o autor' }),
      jsxRuntime.jsxs('div', { className: 'gb-author-panel', children: [
        jsxRuntime.jsx('p', { children: jsxRuntime.jsx('strong', { children: 'ASP BM BRAGANÇA' }) }),
        jsxRuntime.jsx('p', { children: 'João Renato Batista de Bragança, Aspirante a Oficial do Corpo de Bombeiros Militar de Pernambuco, com atuação no Grupamento de Bombeiros Marítimo (GBMar).' }),
        jsxRuntime.jsx('p', { children: 'Responsável pelo desenvolvimento e pela organização deste mapa de consulta estatística e geográfica.' })
      ] })
    ] })
  ] });
}

'''
CHANGES = [
    ('function DashboardContent(){', AUTHOR_FUNCTION + 'function DashboardContent(){'),
    ('return jsxRuntime.jsx(\'article\', { className: "gb-app", \'data-dashboard-layout\': "viewport", children: jsxRuntime.jsxs(\'div\', { className: "gb-mapframe", children: [',
     'return jsxRuntime.jsxs(\'article\', { className: "gb-app", \'data-dashboard-layout\': "viewport", children: [jsxRuntime.jsx(GbmarAuthorCredit, {}), jsxRuntime.jsxs(\'div\', { className: "gb-mapframe", children: ['),
    (']})});\n}\n\n// The canonical App imports both entrypoints.',
     ']})]});\n}\n\n// The canonical App imports both entrypoints.')
]


def replace_checked(html, reverse=False):
    for before, after in CHANGES:
        old, new = (after, before) if reverse else (before, after)
        assert html.count(old) == 1, 'Trecho de apresentação diferente; revisar manualmente.'
        html = html.replace(old, new, 1)
    return html


def digest(value):
    return hashlib.sha256(value).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    docs = Path(__file__).resolve().parents[1] / 'docs'
    path = docs / 'index.html'
    raw = path.read_bytes()
    html = raw.decode()
    manifest_path = docs / 'data-app-build.json'
    manifest = json.loads(manifest_path.read_text())
    snapshot = (docs / manifest['snapshot']['path']).read_bytes()
    assert digest(snapshot) == SNAPSHOT_HASH, 'Base diferente; interrompido.'
    runtime = re.search(r'<script src="data:text/javascript;charset=utf-8;base64,([^"]+)"', html)
    assert runtime and digest(base64.b64decode(runtime[1])) == RUNTIME_HASH, 'Runtime diferente.'
    original = digest(raw) == BASE_HASH
    if not original:
        assert html.count(STYLE) == 1, 'Estilo diferente ou duplicado.'
        assert digest(replace_checked(html.replace(STYLE, '', 1), reverse=True).encode()) == BASE_HASH, 'Alterações fora do escopo.'
    if args.check:
        assert not original, 'Ocultação ainda não aplicada.'
        assert manifest['html'] == {'path': 'index.html', 'sha256': digest(raw), 'bytes': len(raw)}
        assert manifest['runtimeSha256'] == RUNTIME_HASH
        assert manifest['snapshot']['sha256'] == SNAPSHOT_HASH
        print('OK: somente apresentação e autoria alteradas; HTML original recuperável, dados e runtime preservados.')
        return
    if not original:
        print('Já aplicado; nenhum arquivo alterado.')
        return
    assert html.count('</head>') == 1
    result = replace_checked(html).replace('</head>', STYLE + '</head>', 1).encode()
    manifest['html'] = {'path': 'index.html', 'sha256': digest(result), 'bytes': len(result)}
    path.write_bytes(result)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print('CSS aplicado e hash do HTML atualizado.')


if __name__ == '__main__':
    main()
