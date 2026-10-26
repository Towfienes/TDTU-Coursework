// Export the measured HTML deck as editable PowerPoint text, lines, fills and logos.
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {createRequire} from 'node:module';
import {chromium} from '../render/node_modules/playwright-core/index.mjs';
const here=path.dirname(fileURLToPath(import.meta.url));
const runtime='/home/towfienes/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/package.json';
const PptxGenJS=createRequire(runtime)('pptxgenjs');
const browser=await chromium.launch({executablePath:'/home/towfienes/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome',args:['--no-sandbox']});
const page=await browser.newPage();
await page.goto('file://'+path.join(here,'deck.html'));
await page.evaluate(()=>document.fonts.ready);
const slides=await page.evaluate(()=>[...document.querySelectorAll('.slide')].map(section=>{
 const bounds=section.getBoundingClientRect();
 const rect=r=>({x:(r.left-bounds.left)/96,y:(r.top-bounds.top)/96,w:r.width/96,h:r.height/96});
 const hex=c=>{const m=c.match(/\d+/g);return m?m.slice(0,3).map(v=>(+v).toString(16).padStart(2,'0')).join(''):'000000';};
 const shapes=[];
 for(const el of section.querySelectorAll('*')){
  const r=rect(el.getBoundingClientRect()),s=getComputedStyle(el);
  if(s.backgroundColor!=='rgba(0, 0, 0, 0)'&&s.backgroundColor!=='rgb(255, 255, 255)')shapes.push({...r,fill:hex(s.backgroundColor)});
  for(const side of ['Top','Bottom','Left','Right']){
   const width=parseFloat(s['border'+side+'Width']);
   if(width>0){const horizontal=side==='Top'||side==='Bottom';shapes.push({x:r.x+(side==='Right'?r.w:0),y:r.y+(side==='Bottom'?r.h:0),w:horizontal?r.w:0,h:horizontal?0:r.h,line:hex(s['border'+side+'Color']),width:width*.75});}
  }
 }
 const texts=[],walker=document.createTreeWalker(section,NodeFilter.SHOW_TEXT);
 let node;
 while((node=walker.nextNode())){
  const style=getComputedStyle(node.parentElement);let run=null;
  const flush=()=>{if(run&&run.text.trim())texts.push({...run,text:run.text.replace(/\s+/g,' '),fontSize:parseFloat(style.fontSize)*.75,bold:parseInt(style.fontWeight)>=600,italic:style.fontStyle==='italic',color:hex(style.color)});run=null;};
  for(let i=0;i<node.length;i++){
   const range=document.createRange();range.setStart(node,i);range.setEnd(node,i+1);const box=range.getBoundingClientRect();
   if(!box.width||!box.height)continue;
   const r=rect(box),char=style.textTransform==='uppercase'?node.textContent[i].toUpperCase():node.textContent[i];
   if(run&&Math.abs(run.y-r.y)<.01){run.text+=char;run.w=r.x+r.w-run.x;}
   else{flush();run={...r,text:char};}
  }
  flush();
 }
 return {texts,shapes,images:[...section.querySelectorAll('img')].map(el=>({...rect(el.getBoundingClientRect()),data:el.src}))};
}));
await browser.close();
const pptx=new PptxGenJS();pptx.defineLayout({name:'TDTU',width:40/3,height:7.5});pptx.layout='TDTU';pptx.author='SaigonBite team';pptx.subject='Part 1 Solution Pitch';pptx.title='SaigonBite — Presentation 1';pptx.lang='en-GB';
const notes=await fs.readFile(path.join(here,'Part1_SpeakerNotes.md'),'utf8');
for(const [i,model] of slides.entries()){
 const slide=pptx.addSlide();slide.background={color:'FFFFFF'};
 for(const s of model.shapes)slide.addShape(s.line?'line':'rect',{x:s.x,y:s.y,w:s.w,h:s.h,line:s.line?{color:s.line,width:s.width}:{transparency:100},...(s.fill?{fill:{color:s.fill}}:{})});
 for(const img of model.images)slide.addImage(img);
 for(const t of model.texts)slide.addText(t.text,{x:t.x,y:t.y-.015,w:t.w+.05,h:Math.max(t.h+.03,t.fontSize/72*1.3),fontFace:'Times New Roman',fontSize:t.fontSize,bold:t.bold,italic:t.italic,color:t.color,margin:0,valign:'top',paraSpaceAfterPt:0,lineSpacingMultiple:1,wrap:false,breakLine:false});
 const start=notes.indexOf(`## Slide ${i+1} `),end=notes.indexOf(`## Slide ${i+2} `);
 slide.addNotes(notes.slice(start,end<0?notes.indexOf('## Rehearsal'):end));
}
await pptx.writeFile({fileName:path.join(here,'Part1_Pitch.pptx')});
console.log('Exported 5 editable slides with Vietnamese speaker notes');
