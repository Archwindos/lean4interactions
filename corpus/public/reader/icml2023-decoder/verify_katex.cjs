const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const katex = require('../../../../reader/preview/vendor/katex/katex.js');
const root = process.cwd();
const dir = 'corpus/public/reader/icml2023-decoder';
const inputFiles = ['content.json','symbols.json','issues.json'];
let checked=0, errors=[];
function render(tex,where,display) {
  if(!tex)return;
  checked++;
  try {katex.renderToString(tex,{displayMode:display,throwOnError:true,strict:false});}
  catch(e){errors.push({path:where,tex,message:e.message});}
}
function walk(x,where,key='') {
  if(Array.isArray(x)){x.forEach((v,i)=>walk(v,where+'/'+i,key));return;}
  if(x && typeof x==='object') {
    Object.entries(x).forEach(([k,v])=>{
      if(k==='lean'||k==='lean_refs')return;
      walk(v,where+'/'+k,k);
    });
    return;
  }
  if(typeof x!=='string')return;
  if(key.endsWith('_tex')) {render(x,where,true);return;}
  if(key.endsWith('_md')||['overview','scope','note','description','assumptions','empty_set_convention','baseline_convention'].includes(key)) {
    const re=/\$\$([\s\S]*?)\$\$|\$([^$\n]+?)\$/g;
    let m; while((m=re.exec(x))!==null) render(m[1]===undefined?m[2]:m[1],where,Boolean(m[1]));
  }
}
const hashes={};
for(const file of inputFiles){
 const bytes=fs.readFileSync(path.join(root,dir,file));
 hashes[file]=crypto.createHash('sha256').update(bytes).digest('hex');
 walk(JSON.parse(bytes),file);
}
const result={status:errors.length?'failed':'passed',engine:'Actual local KaTeX renderToString with throwOnError:true',input_hashes:hashes,checked_formulas:checked,errors};
fs.writeFileSync(path.join(dir,'verification/katex-checks.json'),JSON.stringify(result,null,2)+'\n');
process.stdout.write(JSON.stringify({status:result.status,checked_formulas:checked,errors})+'\n');
process.exit(errors.length?1:0);
