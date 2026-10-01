/* Actual local KaTeX parse of the formula fields and Markdown math served by the reader. */
const fs=require('fs'),path=require('path'),crypto=require('crypto');
const root=process.cwd(),work=path.join(root,'reader');
const katex=require(path.join(root,'web/static/vendor/katex/katex.min.js'));
const input=path.join(root,'corpus/public/reader/icml2023-bayesian/content.json'),value=JSON.parse(fs.readFileSync(input,'utf8'));
const errors=[];let checked=0;
function parse(tex,where){if(typeof tex!=='string'||!tex.trim())return;checked++;try{katex.renderToString(tex,{throwOnError:true,strict:'ignore',trust:false,displayMode:true});}catch(e){errors.push({where,tex,error:String(e.message)});}}
function walk(x,where){
 if(typeof x==='string'){const re=/\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|(?<!\$)\$(?!\$)[^\n$]+\$/g;let m;while((m=re.exec(x))!==null){const token=m[0];parse(token.startsWith('$')?token.slice(token.startsWith('$$')?2:1,token.startsWith('$$')?-2:-1):token.slice(2,-2),where+'@'+m.index);}return;}
 if(Array.isArray(x)){x.forEach((v,i)=>walk(v,where+'['+i+']'));return;}if(!x||typeof x!=='object')return;
 for(const [k,v]of Object.entries(x)){
  if(k.endsWith('_tex')&&typeof v==='string')parse(v,where+'.'+k);
  else if(k.endsWith('_tex')&&Array.isArray(v))v.forEach((tex,i)=>parse(tex,where+'.'+k+'['+i+']'));
  else if(typeof v==='string'){
   const text=v.replace(/```[\s\S]*?```/g,'');const re=/\$\$[\s\S]*?\$\$|\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|(?<!\$)\$(?!\$)[^\n$]+\$/g;let m;
   while((m=re.exec(text))!==null){const token=m[0];parse(token.startsWith('$')?token.slice(token.startsWith('$$')?2:1,token.startsWith('$$')?-2:-1):token.slice(2,-2),where+'.'+k+'@'+m.index);}
  }else walk(v,where+'.'+k);
 }
}
walk(value,'$');const inputHashes={};[input,__filename,path.join(root,'web/static/vendor/katex/katex.min.js')].forEach(p=>{inputHashes[path.relative(root,p)]=crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');});
const report={status:errors.length?'failed':'passed',scope:'formula_rendering_only',engine:'actual local KaTeX',input_sha256:inputHashes[path.relative(root,input)],input_hashes:inputHashes,checked,errors};
const evidence=path.join(work,'evidence/twelve-paper-20261001');fs.mkdirSync(evidence,{recursive:true});
fs.writeFileSync(path.join(root,'corpus/public/reader/icml2023-bayesian/verification/math-rendering-check.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify({status:report.status,checked,errors:errors.slice(0,10)}));process.exitCode=errors.length?1:0;
