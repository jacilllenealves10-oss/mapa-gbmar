import {test} from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';

const root = new URL('../', import.meta.url);
const html = readFileSync(new URL('docs/index.html', root), 'utf8');

test('patch limitado, hash do HTML consistente, dados e runtime originais', () => {
  const result = spawnSync('python3', ['tools/hide_platform_actions.py', '--check'], {cwd: fileURLToPath(root), encoding: 'utf8'});
  assert.equal(result.status, 0, result.stderr || result.stdout);
});

test('JavaScript completo continua sintaticamente válido', () => {
  const scripts = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)];
  assert.equal(scripts.length, 1);
  const result = spawnSync(process.execPath, ['--check'], {input: scripts[0][1], encoding: 'utf8'});
  assert.equal(result.status, 0, result.stderr);
});

test('autoria exata e seção nativa recolhida, sem ação externa', () => {
  const start = html.indexOf('function GbmarAuthorCredit()');
  const end = html.indexOf('function DashboardContent()', start);
  assert.ok(start >= 0 && end > start);
  const jsx = (tag, props) => ({tag, props});
  const context = vm.createContext({jsxRuntime: {jsx, jsxs: jsx}});
  const header = vm.runInContext(html.slice(start, end) + '\nGbmarAuthorCredit()', context);
  assert.equal(header.tag, 'header');
  assert.equal(header.props.children[0].props.children, 'Desenvolvido por ASP BM BRAGANÇA');
  const details = header.props.children[1];
  assert.equal(details.tag, 'details');
  assert.ok(!details.props.open);
  assert.equal(details.props.children[0].tag, 'summary');
  assert.equal(details.props.children[0].props.children, 'Sobre o autor');
  const tags = [];
  function visit(node) {
    if (!node || typeof node !== 'object') return;
    if (Array.isArray(node)) return node.forEach(visit);
    tags.push(node.tag);
    visit(node.props.children);
  }
  visit(header);
  assert.ok(!tags.includes('script') && !tags.includes('iframe') && !tags.includes('a'));
});
