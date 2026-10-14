import {readFileSync} from 'node:fs';
import {fileURLToPath} from 'node:url';
import vm from 'node:vm';

export const html = readFileSync(new URL('../docs/index.html', import.meta.url), 'utf8');
export const runtime = Buffer.from(html.match(/<script src="data:text\/javascript;charset=utf-8;base64,([^"]+)"/)[1], 'base64').toString();
const start = runtime.indexOf('var T5=[{id:`original`');
const end = runtime.indexOf(';function E5(', start);
if (start < 0 || end < start) throw Error('Paletas do runtime mudaram; revisar extração.');
export const themes = vm.runInNewContext(runtime.slice(start + 'var T5='.length, end), {}, {timeout: 1000});
export function luminance(hex) {
  let value = hex.replace('#', '');
  if (value.length === 3) value = [...value].map(c => c + c).join('');
  if (!/^[0-9a-f]{6}$/i.test(value)) throw Error('Cor não opaca: ' + hex);
  const c = value.match(/../g).map(v => parseInt(v,16)/255).map(v => v <= 0.04045 ? v/12.92 : ((v+.055)/1.055)**2.4);
  return c[0]*.2126+c[1]*.7152+c[2]*.0722;
}
export function contrast(a,b) {
  const [low,high] = [luminance(a),luminance(b)].sort((a,b)=>a-b);
  return (high+.05)/(low+.05);
}
const backgroundNames = ['background','surface','surface-raised','muted','control','control-hover'];
export const themeResults = themes.flatMap(theme => {
  const paletteTheme = theme.id === 'original' ? themes.find(t=>t.id==='codex-classic') : theme;
  return (theme.darkOnly ? ['dark'] : ['light','dark']).map(scheme => {
    const tokens = scheme==='dark' && !theme.darkOnly ? paletteTheme.darkTokens : paletteTheme.tokens;
    const pairs = backgroundNames.map((background,index)=>({background,foreground:tokens[6],color:tokens[index],ratio:contrast(tokens[6],tokens[index])}));
    return {theme:theme.id,label:theme.label,scheme,
      oldOperationalNoteRatio:contrast(tokens[3],tokens[1]),
      oldSecondarySurfaceRatio:contrast(tokens[7],tokens[1]),
      correctedMinimumRatio:Math.min(...pairs.map(p=>p.ratio)),pairs};
  });
});
export const fixedResults = [
  ['Filtros e Fechar','#fff','#163c4d'],
  ['Aba selecionada','#005560','#e3f2f3'],
  ['Agrupamentos e tubarão','#fff','#163c4d'],
  ['Código dos postos','#fff','#183a4b'],
  ['Aviso cartográfico','#6d541c','#fff5df'],
  ['Medição','#143644','#fff'],
  ['Recorte vazio','#173c4c','#fff'],
  ['Atribuição e escala','#333','#fff'],
  ['Link da atribuição','#005a7a','#fff'],
  ['Tooltip','#222','#fff']
].map(([label,foreground,background])=>({label,foreground,background,ratio:contrast(foreground,background)}));

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  console.log(JSON.stringify({method:'Razão de luminância sRGB; cores dos temas extraídas do runtime entregue. Não é inspeção visual nem auditoria WCAG integral.',threshold:4.5,themeResults,fixedResults},null,2));
}
