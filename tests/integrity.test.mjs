import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {createHash} from 'node:crypto';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';

const root = new URL('../', import.meta.url);
const htmlBytes = readFileSync(new URL('docs/index.html', root));
const html = htmlBytes.toString('utf8');
const manifest = JSON.parse(readFileSync(new URL('docs/data-app-build.json', root)));
const snapshotBytes = readFileSync(new URL('docs/' + manifest.snapshot.path, root));
const data = JSON.parse(snapshotBytes);
const digest = value => createHash('sha256').update(value).digest('hex');
const core = html.slice(html.indexOf('const INITIAL='), html.indexOf('\nconst L = {};')).trim();
const snapshotHash = 'b3f4840d6c0327c3d849fc692ce6de10421f2f2a63d4a7621de014fdacd77f93';
const runtimeHash = '9e3ede84b28aded3c7379b6e6a5611f0d95b9977eb0f781e279ceefabfcbd27e';

test('base, runtime e referências relativas do Pages preservados byte a byte', () => {
  assert.equal(digest(snapshotBytes), snapshotHash);
  assert.deepEqual(manifest.snapshot, {path: 'snapshot.' + snapshotHash + '.json', sha256: snapshotHash, bytes: 5528380});
  assert.equal(manifest.sourceSnapshotSha256, snapshotHash);
  assert.equal(manifest.runtimeSha256, runtimeHash);
  const runtime = html.match(/<script src="data:text\/javascript;charset=utf-8;base64,([^"]+)"/);
  assert.ok(runtime);
  assert.equal(digest(Buffer.from(runtime[1], 'base64')), runtimeHash);
  assert.ok(html.includes('<meta name="data-app-local-snapshot" content="' + manifest.snapshot.path + '">'));
  assert.ok(html.includes('<meta name="data-app-runtime-sha256" content="' + runtimeHash + '">'));
  assert.equal(readFileSync(new URL('docs/.nojekyll', root)).length, 0);
  assert.deepEqual(manifest.html, {path: 'index.html', sha256: digest(htmlBytes), bytes: htmlBytes.length});
});

test('rotinas estatísticas, filtros, georreferenciamento e CSV sem alteração', () => {
  assert.equal(digest(core), '77347f6af8cae395d4857fc45b29677978ff21f0606bfa2dbf4d888064cee9ba');
});

test('comparação reversa recupera exatamente o HTML estável', () => {
  const result = spawnSync('python3', ['tools/refine_presentation.py', '--check'], {cwd: fileURLToPath(root), encoding: 'utf8'});
  assert.equal(result.status, 0, result.stderr || result.stdout);
});

test('JavaScript de inicialização e aplicação continua sintaticamente válido', () => {
  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  assert.equal(scripts.length, 1);
  const result = spawnSync(process.execPath, ['--check'], {input: scripts[0][1], encoding: 'utf8'});
  assert.equal(result.status, 0, result.stderr);
});

test('ressalva metodológica corresponde ao registro vazio efetivo', () => {
  const rows = data.queries.registros.rows;
  assert.deepEqual(rows.filter(r => r.protocolo === '').map(r => r.id), ['2546']);
  assert.equal(new Set(rows.filter(r => r.protocolo !== '').map(r => r.protocolo)).size, 3339);
  assert.equal(new Set(rows.map(r => r.protocolo)).size, 3340);
});

test('token textual escolhido supera 4,5:1 nos dois temas padrão', () => {
  function luminance(hex) {
    const values = hex.match(/../g).map(v => parseInt(v, 16) / 255).map(v => v <= 0.04045 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4);
    return values[0] * 0.2126 + values[1] * 0.7152 + values[2] * 0.0722;
  }
  for (const [fg, bg] of [['1a1c1f', 'fcfcfc'], ['ffffff', '212121']]) {
    const values = [luminance(fg), luminance(bg)].sort((a, b) => a - b);
    assert.ok((values[1] + 0.05) / (values[0] + 0.05) >= 4.5);
  }
  assert.ok(html.includes('--color-text-foreground,light-dark(#1a1c1f,#fff)'));
  // Verificação das cores padrão do código; não substitui inspeção visual de temas externos.
});

test('CSV exportado conserva todas as células, inclusive identificadores longos', async () => {
  const {csvContent} = await import('data:text/javascript;base64,' + Buffer.from(core + '\nexport {csvContent};').toString('base64'));
  const csv = csvContent(data.queries.registros.rows);
  const check = `import csv,io,json,sys
rows=json.load(open(sys.argv[1]))['queries']['registros']['rows']
parsed=list(csv.reader(io.StringIO(sys.stdin.read().lstrip('\\ufeff')),delimiter=';'))
keys=list(rows[0])
assert parsed[0]==keys
assert len(parsed)==len(rows)+1
def text(v):
    if v is None:return ''
    if isinstance(v,bool):return str(v).lower()
    return str(v)
for source,actual in zip(rows,parsed[1:]):
    expected=[text(source[k]) for k in keys]
    expected=["'"+v if v[:1] in ['=','+','@'] else v for v in expected]
    assert actual==expected,source['id']
assert len(keys)==53
`;
  const result = spawnSync('python3', ['-c', check, fileURLToPath(new URL('docs/' + manifest.snapshot.path, root))], {input: csv, encoding: 'utf8', maxBuffer: 10 * 1024 * 1024});
  assert.equal(result.status, 0, result.stderr);
});
