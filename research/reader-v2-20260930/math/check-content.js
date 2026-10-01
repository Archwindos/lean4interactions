const fs=require('fs');
const katex=require('../preview/vendor/katex/katex.min.js');
const base='research/reader-v2-20260930';
const data=JSON.parse(fs.readFileSync(base+'/data/math-content.json','utf8'));
let count=0; const failures=[];
function math(tex,path,display){
 count++;
 try{katex.renderToString(tex,{throwOnError:true,strict:'error',displayMode:display});}
 catch(e){failures.push({path,tex,error:String(e)});}
}
function walk(value,path,key){
 if(typeof value==='string'){
  if(key==='statement_tex'||key==='formula_tex'||key==='symbol_tex'||key==='display_statement_tex') math(value,path,true);
  if(key.endsWith('_md')||key==='overview'||key==='caveats'){
   const pat=/\\\(([\s\S]*?)\\\)|\\\[([\s\S]*?)\\\]/g;
   let m; while((m=pat.exec(value))!==null) math(m[1]!==undefined?m[1]:m[2],path+'@'+m.index,m[2]!==undefined);
   if(value.includes('_\\(')||value.includes('Δᵢ\\(')||value.includes('\\)_g'))failures.push({path,error:'fragmented inline TeX'});
  }
 }else if(Array.isArray(value))value.forEach((v,i)=>walk(v,path+'['+i+']',key));
 else if(value&&typeof value==='object')Object.entries(value).forEach(([k,v])=>walk(v,path+'.'+k,k));
}
walk(data,'math-content','');
const out={schema_version:1,scope:'All standalone TeX fields and delimited inline/display mathematics in authored prose',formula_count:count,failures,status:failures.length?'failed':'passed'};
fs.writeFileSync(base+'/math/content-math-check.json',JSON.stringify(out,null,2)+'\n');
process.stdout.write(JSON.stringify({formula_count:count,status:out.status,failures},null,2)+'\n');
process.exitCode=failures.length?1:0;
