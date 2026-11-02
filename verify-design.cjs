const fs=require('fs'),assert=require('node:assert/strict'),katex=require('./dist/vendor/katex/katex.min.js');
const js=fs.readFileSync('dist/app.js','utf8'),css=fs.readFileSync('dist/style.css','utf8'),html=fs.readFileSync('dist/index.html','utf8');
const formula=js.match(/katex\.render\(String.raw`([^`]+)`/)[1];
assert(katex.renderToString(formula,{displayMode:true,throwOnError:true}).includes('katex'));
assert(!/gradient\(|box-shadow|#b83465/.test(css));
assert(!js.includes('Small steps. Better predictions.'));
assert(html.includes('Niharika pawar')&&html.includes('assets/vesit-logo.jpg'));
assert(!html.includes('pill'));
console.log('KaTeX equation, academic theme, logo and author credits verified.');
