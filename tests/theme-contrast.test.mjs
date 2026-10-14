import {test} from 'node:test';
import assert from 'node:assert/strict';
import vm from 'node:vm';
import {spawnSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {themeResults,fixedResults,runtime,html} from '../tools/theme_contrast.mjs';

test('catálogo completo: seis temas e onze combinações de aparência',()=>{
  assert.equal(new Set(themeResults.map(t=>t.theme)).size,6);
  assert.equal(themeResults.length,11);
  assert.ok(html.includes('--color-text-foreground,light-dark(#1a1c1f,#fff)'));
});
for (const result of themeResults) {
  test(`contraste ${result.label} / ${result.scheme}: texto operacional e secundário`,()=>{
    for (const pair of result.pairs) assert.ok(pair.ratio>=4.5,JSON.stringify(pair));
    assert.ok(result.oldOperationalNoteRatio<2,'O teste deve detectar o defeito anterior.');
  });
}
test('pares opacos sobre mapa e controles fixos têm contraste suficiente',()=>{
  for(const result of fixedResults)assert.ok(result.ratio>=4.5,JSON.stringify(result));
});
test('somente CSS adicionado; verificações de integridade anteriores continuam exigidas',()=>{
  const result=spawnSync('python3',['tools/improve_theme_contrast.py','--check'],{cwd:fileURLToPath(new URL('../',import.meta.url)),encoding:'utf8'});
  assert.equal(result.status,0,result.stderr);
});

// Testa a rotina real de aparência extraída do runtime com um DOM mínimo.
// Não equivale a renderizar a cascata CSS ou a interface em navegador.
test('padrão claro no sistema escuro, escolha explícita de escuro e temas alternativos',()=>{
  const start=runtime.indexOf('var G7=globalThis.document?.documentElement');
  const end=runtime.indexOf(';function QFe(',start);
  assert.ok(start>=0&&end>start);
  const element={dataset:{},style:{setProperty(){}}};
  const context=vm.createContext({
    document:{documentElement:element},
    matchMedia:()=>({matches:true,addEventListener(){}}),
    getComputedStyle:()=>({getPropertyValue:()=>element.dataset.appAppearance!=='dark'&&(!element.dataset.appTheme||element.dataset.appTheme==='original')?'light':''}),
    O5:(theme,scheme)=>{element.style.colorScheme=theme==='dark-pixel'?'dark':scheme;},D5:()=>{}
  });
  vm.runInContext(runtime.slice(start,end),context);
  assert.equal(element.dataset.colorScheme,'light');
  vm.runInContext('J7("dark")',context);
  assert.equal(element.dataset.colorScheme,'dark');
  vm.runInContext('J7("light")',context);
  assert.equal(element.dataset.colorScheme,'light');
  element.dataset.appTheme='dark-pixel';
  vm.runInContext('J7("light")',context);
  assert.equal(element.dataset.colorScheme,'dark');
  element.dataset.appTheme='scientific-blue';
  vm.runInContext('J7("light")',context);
  assert.equal(element.dataset.colorScheme,'light');
  vm.runInContext('J7("dark")',context);
  assert.equal(element.dataset.colorScheme,'dark');
});
