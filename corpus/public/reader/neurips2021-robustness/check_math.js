/* Parse every reader formula using the actual locally served KaTeX engine. */
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=process.cwd(),dir=path.join(root,'corpus/public/reader/neurips2021-robustness');
const engine=path.join(root,'reader/preview/vendor/katex/katex.js');
const katex=require(engine),input=path.join(dir,'content.json');
const errors=[];let checked=0;
function parse(tex,where){if(typeof tex!=='string'||!tex.trim())return;checked++;try{katex.renderToString(tex,{throwOnError:true,strict:'ignore',trust:false,displayMode:true});}catch(e){errors.push({where,tex,error:e.message});}}
function markdown(s,where){const re=/\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|(?<!\$)\$(?!\$)[^\n$]+\$/g;let m;while((m=re.exec(s.replace(/```[\s\S]*?```/g,'')))!==null){let t=m[0];parse(t[0]==='$'?t.slice(t.startsWith('$$')?2:1,t.startsWith('$$')?-2:-1):t.slice(2,-2),where+'@'+m.index);}}
function walk(x,where){if(typeof x==='string'){markdown(x,where);return;}if(Array.isArray(x)){x.forEach((v,i)=>walk(v,where+'['+i+']'));return;}if(!x||typeof x!=='object')return;for(const [k,v]of Object.entries(x)){if(k.endsWith('_tex')){if(Array.isArray(v))v.forEach((t,i)=>parse(t,where+'.'+k+'['+i+']'));else parse(v,where+'.'+k);}else walk(v,where+'.'+k);}}
walk(JSON.parse(fs.readFileSync(input,'utf8')),'$');
const hashes={};for(const p of [input,__filename,engine])hashes[path.relative(root,p)]=crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const report={status:errors.length?'failed':'passed',scope:'formula_rendering_only',engine:'actual reader KaTeX 0.16.22',input_hashes:hashes,checked,errors};
fs.writeFileSync(path.join(dir,'verification/math-rendering-check.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({status:report.status,checked,errors:errors.slice(0,12)}));process.exitCode=errors.length?1:0;
