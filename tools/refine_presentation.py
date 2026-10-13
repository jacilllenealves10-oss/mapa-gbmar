#!/usr/bin/env python3
"""Patch estritamente delimitado do artefato estável; não recompila o runtime.

Aplicar: python3 tools/refine_presentation.py
Conferir: python3 tools/refine_presentation.py --check
Aceita somente o HTML da revisão estável documentada ou o resultado exato.
"""
import argparse
import hashlib
import json
from pathlib import Path

BASE_COMMIT = "65470566ec4904f562ffe8a5c9e46924c3594deb"
BASE_HTML_SHA256 = "d90c5b894ecd268b4ae61a72e7dcdcc5771438195165404fddda7efc556a1238"
SNAPSHOT_SHA256 = "b3f4840d6c0327c3d849fc692ce6de10421f2f2a63d4a7621de014fdacd77f93"
RUNTIME_SHA256 = "9e3ede84b28aded3c7379b6e6a5611f0d95b9977eb0f781e279ceefabfcbd27e"
CHANGES = [
    ('<html lang="en">', '<html lang="pt-BR">'),
    ('.gb-note{font-size:11px;line-height:1.65;color:var(--muted);margin:7px 0 13px}',
     '.gb-note{font-size:11px;line-height:1.65;color:var(--text);margin:7px 0 13px}'),
    ('.gb-record small{color:var(--muted);font-size:10px;overflow-wrap:anywhere}',
     '.gb-record small{color:var(--text);font-size:10px;overflow-wrap:anywhere}'),
    ('.gb-metrics span{font-size:11px;color:var(--muted)}',
     '.gb-metrics span{font-size:11px;color:var(--text)}'),
    ('.gb-compact small{color:var(--muted)}',
     '.gb-compact small{color:var(--text)}'),
    ('title: "Comparação dos 15 postos"', 'title: "Comparação dos postos cadastrados"'),
    ("options: ['Todos','Coordenadas informadas','Sem coordenadas','Coordenadas inválidas','Fora da janela de PE — conferir','Sem ponto utilizável','Com alerta geográfico']",
     "options: ['Todos','Coordenadas informadas','Sem coordenadas','Coordenadas inválidas','Fora da janela de PE — conferir',{value:'Sem ponto utilizável',label:'Sem coordenada original utilizável'},'Com alerta geográfico']"),
    ('Base: 3.486 linhas recebidas; 15 cópias idênticas removidas; 3.471 linhas analíticas, 3.340 protocolos. Dos protocolos,',
     'Base: 3.486 linhas recebidas; 15 cópias idênticas removidas; 3.471 linhas analíticas e 3.340 valores distintos no campo protocolo. Esse total inclui 3.339 identificadores preenchidos e um valor vazio (linha analítica 2546), pendente de conferência na fonte. A contagem existente foi preservada. Dos protocolos,')
]


def sha256(value):
    return hashlib.sha256(value).hexdigest()


def replace_checked(html, reverse=False):
    for before, after in CHANGES:
        old, new = (after, before) if reverse else (before, after)
        if html.count(old) != 1:
            raise ValueError(f"Trecho ausente ou ambíguo; revisão manual necessária: {old[:90]}")
        html = html.replace(old, new, 1)
    return html


def check_result(html):
    original = replace_checked(html, reverse=True).encode("utf-8")
    if sha256(original) != BASE_HTML_SHA256:
        raise ValueError("Há alterações fora dos oito trechos autorizados.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    docs = Path(__file__).resolve().parents[1] / "docs"
    html_path, manifest_path = docs / "index.html", docs / "data-app-build.json"
    manifest = json.loads(manifest_path.read_text())
    snapshot = (docs / manifest["snapshot"]["path"]).read_bytes()
    if sha256(snapshot) != SNAPSHOT_SHA256:
        raise ValueError("Base diferente da revisão estável; operação interrompida.")
    raw = html_path.read_bytes()
    html = raw.decode("utf-8")
    is_original = sha256(raw) == BASE_HTML_SHA256
    if not is_original:
        check_result(html)
    if args.check:
        if is_original:
            raise ValueError("As correções ainda não foram aplicadas.")
        if manifest["html"] != {"path": "index.html", "sha256": sha256(raw), "bytes": len(raw)}:
            raise ValueError("Manifesto HTML incompatível.")
        print("OK: somente os oito trechos de apresentação foram alterados; base preservada.")
        return
    if not is_original:
        print("Correções já aplicadas; nenhum arquivo alterado.")
        return
    result = replace_checked(html)
    check_result(result)
    content = result.encode("utf-8")
    manifest["html"] = {"path": "index.html", "sha256": sha256(content), "bytes": len(content)}
    html_path.write_bytes(content)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print("Oito trechos de apresentação corrigidos; integridade do HTML atualizada.")


if __name__ == "__main__":
    main()
