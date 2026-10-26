// Editable academic slides from the executed notebook's authoritative summary.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {execFileSync} from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const runtime=process.env.CODEX_PRIMARY_RUNTIME_ROOT ?? path.join(os.homedir(),'.cache/codex-runtimes/codex-primary-runtime');
const modules=path.join(runtime,'dependencies/node/node_modules');
process.env.RUNTIME_NODE_MODULES ??= modules;
process.env.RUNTIME_NODE ??= process.execPath;
process.env.RUNTIME_PYTHON ??= path.join(runtime,'dependencies/python/bin/python');
process.env.RUNTIME_BIN_DIR ??= path.join(runtime,'dependencies/bin/override');
const skill=process.env.PRESENTATION_SKILL_DIR ?? path.join(runtime,'plugins/openai-primary-runtime/plugins/presentations/skills/presentations');
const {Presentation,PresentationFile}=await import(pathToFileURL(path.join(modules,'@oai/artifact-tool/dist/artifact_tool.mjs')).href);
const {finalizePresentation,applyPresentationChartFont}=await import(pathToFileURL(path.join(skill,'container_tools/artifact_tool_utils.mjs')).href);
const narration=JSON.parse(await fs.readFile(path.join(root,'slides/narration_vi.json'),'utf8'));
const S=JSON.parse(await fs.readFile(path.join(root,'results/summary.json'),'utf8'));
const M=JSON.parse(await fs.readFile(path.join(root,'project.json'),'utf8'));
const status=JSON.parse(execFileSync(path.join(runtime,'dependencies/python/bin/python'),[path.join(root,'tools/check_readiness.py'),'--json'],{encoding:'utf8'}));
const logoBytes=new Uint8Array(await fs.readFile(path.join(root,'report/assets/tdtu-logo.png')));
const deck=Presentation.create({slideSize:{width:1280,height:720}});
deck.theme.defaultFont='Arial';
deck.theme.colorScheme={name:'TDTU Monochrome Framing with Color Evidence',themeColors:{accent1:'#4477AA',accent2:'#EE7733',accent3:'#228833',accent4:'#CC6677',accent5:'#AA3377',accent6:'#CC3311',bg1:'#ffffff',bg2:'#eeeeee',tx1:'#000000',tx2:'#333333',dk1:'#000000',dk2:'#333333',lt1:'#ffffff',lt2:'#eeeeee',hlink:'#000000',folHlink:'#444444'}};
const line={style:'solid',fill:'#000000',width:1};
const notes=[];
const nativeTables=[];
const nativeCharts=[];
const fmt=(n,d=3)=>Number(n).toFixed(d);
const pv=n=>n<.001?Number(n).toExponential(2):fmt(n,4);
const timing=[25,15,40,45,45,45,50,45,65,50,45,40,60,65,60,25];

function text(slide,value,x,y,w,h,size=24,bold=false,options={}){
  const shape=slide.shapes.add({geometry:'textbox',name:options.name ?? String(value).slice(0,55),position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  shape.text=String(value);
  shape.text.style={fontSize:size*4/3,typeface:options.mono?'DejaVu Sans Mono':'Arial',color:options.color ?? '#000000',bold,alignment:options.align ?? 'left',verticalAlignment:'top',insets:0,autoFit:'none',wrap:'square'};
  return shape;
}
function rule(slide,x,y,w,h=1.4){slide.shapes.add({geometry:'rect',name:'Thin monochrome rule',position:{left:x,top:y,width:w,height:h},fill:'#000000',line:{fill:'none',width:0}});}
function slide(title,note,duration,source='Executed notebook and results/summary.json'){
  const s=deck.slides.add();s.background.fill='#ffffff';
  s.images.add({blob:logoBytes,contentType:'image/png',alt:'Original Ton Duc Thang University logo',fit:'contain',position:{left:42,top:20,width:158,height:88}});
  text(s,title,240,45,990,66,32,true,{name:'Slide title'});rule(s,40,126,1200);
  const number=deck.slides.items.length;
  text(s,String(number).padStart(2,'0'),1180,678,60,24,11,false,{align:'right'});
  const seconds=timing[number-1] ?? 0; const full=`Thời lượng dự kiến: ${seconds ? seconds+' giây' : 'phụ lục dự phòng'}.\n${narration[number-1]}\nNguồn: ${source}.`;
  s.speakerNotes.text=full;
  notes.push({slide:number,title,seconds,notes:full});
  return s;
}
function rows(slide,items,x=80,y=180,w=1120,gap=105,size=24){
  items.forEach((item,i)=>{text(slide,String(i+1).padStart(2,'0'),x,y+i*gap,65,50,size,true);text(slide,item,x+85,y+i*gap,w-85,gap-12,size);});
}
function table(slide,headers,body,x=70,y=180,w=1140,h=350,widths=null,size=19){
  const values=[headers,...body].map(row=>row.map(String));
  const t=slide.tables.add({rows:values.length,columns:headers.length,left:x,top:y,width:w,height:h,values,
    columnTracks:(widths ?? headers.map(()=>1)).map(value=>({mode:'fr',value}))});
  t.styleOptions={headerRow:false,bandedRows:false};
  t.borders.assign({fill:'#888888',width:.8,style:'solid'});
  for(let r=0;r<values.length;r++)for(let c=0;c<headers.length;c++){
    const cell=t.getCell(r,c);cell.fill=r===0?'#e5e5e5':'#ffffff';
    cell.text.style={fontSize:size*4/3,typeface:'Arial',color:'#000000',bold:r===0,alignment:c===0?'left':'center',verticalAlignment:'middle',insets:size<=18?0:9,wrap:'square',autoFit:'none'};
  }
  if(size<=18)t.cells.block({row:0,column:0,rowCount:values.length,columnCount:headers.length}).assign({margins:{top:0,bottom:0,left:8,right:8}});
  nativeTables.push(deck.slides.items.length);
  return t;
}
function chart(slide,type,config){
  // Excel chart workbooks retain at most 15 significant digits; 12 is ample for these displayed scores.
  config={...config,series:config.series.map(series=>({...series,values:series.values.map(value=>Number(value.toPrecision(12))),...(series.xValues?{xValues:series.xValues.map(value=>Number(value.toPrecision(12)))}:{})}))};
  const c=slide.charts.add(type,{position:{left:65,top:172,width:840,height:440},chartFill:'#ffffff',plotAreaFill:'#ffffff',hasLegend:false,
    xAxis:{textStyle:{fontSize:24,fill:'#000000'},line,majorGridlines:null},
    yAxis:{textStyle:{fontSize:24,fill:'#000000'},line,majorGridlines:{fill:'#dddddd',width:.7,style:'solid'}},...config});
  applyPresentationChartFont(c,{fontFamily:'Arial'});
  nativeCharts.push(deck.slides.items.length);
  return c;
}
function side(slide,headline,body){text(slide,headline,940,205,290,100,27,true);text(slide,body,940,320,290,235,20);}
function takeaway(slide,value){text(slide,value,80,625,1120,45,19);}

function axis(title,min,max,step){return {title,min,max,...(step?{majorUnit:step}:{}),textStyle:{fontSize:22,fill:'#000000'},line,majorGridlines:{fill:'#dddddd',width:.7,style:'solid'}};}
function series(name,x,y,color='#4477AA',points=false){return {name,xValues:x,values:y,fill:color,line:points?{fill:'none',width:0}:{fill:color,width:2,style:'solid'},marker:points?{symbol:'circle',size:5,fill:color}:{symbol:'none'}};}
// Equal-length scatter series avoid a LibreOffice cache rendering defect. Repeated vertices preserve the original density polygon.
function densityPolygon(name,x,y,color){const xx=x.flatMap(v=>Array(6).fill(v)),yy=y.flatMap(v=>Array(6).fill(v));if(xx.length!==150||yy.length!==150)throw Error('Expected25densitybins');return series(name,xx,yy,color);}
let s=slide('Data Analysis and Visualization','');
text(s,'Abalone Measurements\nand Shell Rings',80,178,1120,145,42,true);
text(s,'Exploration, Statistical Inference and Regression',80,345,1120,55,26);
text(s,M.authors.map(a=>`${a.name}  ${a.id}`).join('\n'),80,430,690,160,18);
text(s,`Theory N4 · VibeCoding_Expert\nAdvisor: ${M.advisor}\n20 October 2026`,790,445,430,150,18);
takeaway(s,status.ready?'Theory endterm · group-confirmed submission details':'REVIEW COPY · video link and contribution records await group confirmation');

s=slide('Report video','');
text(s,'YouTube report',80,190,1120,70,36,true);
text(s,M.youtube_url ?? 'Video link pending group recording',80,300,1120,120,28);
text(s,'Planned duration: 12 minutes\nRequired duration: 7–15 minutes\nVideo deadline: end of 21 October 2026',80,450,1120,155,23);
takeaway(s,status.ready?'Published report video · link confirmed by the group':'This slide must contain the actual published link before submission.');

s=slide('Dataset and research questions','','', 'Nash et al.(1994), https://doi.org/10.24432/C55C7W; retained abalone.names');
table(s,['Property','Documented source'],[['Observations / columns','4,177 / 9'],['Predictors / response','8 original inputs / Rings'],['Groups','M: 1,528 · F: 1,307 · I: 1,342'],['Stored measurements','Scaled dimensions and weights'],['Licence','CC BY 4.0']],80,178,1120,350,[1.2,2.5],21);
takeaway(s,'One dataset connects distributions, group inference, correlation and prediction.');

s=slide('Quality checks and holdout design','');
rows(s,['Preserve raw data; audit two zero heights','Training: 3,341 · holdout: 836 · seed 42','Fit imputation and scaling within each training fold','Flag unusual values; retain them in the primary model'],80,180,1120,105,24);
takeaway(s,'The test set does not guide preprocessing, feature selection or deletion.');

s=slide('Distribution of recorded length','','', 'Notebook1; exported length histogram, 25 equal-width bins');
const ld=S.chart_data.length_density;
chart(s,'bar',{categories:ld.hist_x.map(v=>fmt(v,2)),series:[{name:'Observed density',values:ld.hist_y,fill:'#4477AA',line}],barOptions:{direction:'column',gapWidth:0},xAxis:{...axis('Length bin centre (scaled)',undefined,undefined),tickLabelInterval:4},yAxis:axis('Density',0,4.5,1)});
side(s,'Training n = 3,341',`Mean: ${fmt(S.descriptive.length.mean)}\nMedian: ${fmt(S.descriptive.length['50%'])}\nSD: ${fmt(S.descriptive.length.std)}`);
takeaway(s,'A smooth physical measurement need not follow a Normal distribution.');

s=slide('Length differs across recorded groups','');
const gs=S.chart_data.length_group;
chart(s,'bar',{categories:gs.map(r=>`${r.sex}\nn=${r.count}`),series:[{name:'Mean length',values:gs.map(r=>r.mean),fill:'#4477AA',line,points:gs.map((r,idx)=>({idx,fill:{F:'#CC6677',I:'#228833',M:'#4477AA'}[r.sex]}))}],barOptions:{direction:'column',gapWidth:100},dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0.000',textStyle:{fontSize:24,fill:'#000000'}},xAxis:axis('Recorded group (I = infant)'),yAxis:axis('Mean length (scaled)',0,.7,.1)});
side(s,'I means infant','Group comparisons mix biological sex and developmental status.');
takeaway(s,'Observed group differences do not establish a causal mechanism.');

s=slide('Length against a Normal candidate','','', 'Notebook2; SciPy1.15.3 goodness_of_fit documentation');
chart(s,'scatter',{series:[densityPolygon('Observed density polygon',ld.hist_x,ld.hist_y,'#4477AA'),series('Fitted Normal',ld.x,ld.normal,'#CC3311')],scatterOptions:{style:'lineWithMarkers'},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:18,fill:'#000000'}},xAxis:axis('Length (scaled)',0,.9,.2),yAxis:axis('Density',0,4.5,1)});
side(s,'Normal rejected',`AD = ${fmt(S.distribution[0].ad,2)}\nHolm p = 0.0015\n1,999 simulations`);
takeaway(s,'The Monte Carlo p-value reaches its resolution floor of 0.0005 before Holm.');

s=slide('Weight and candidate distributions','','', 'Notebook2; exported fitted densities and observed bin densities');
const wd=S.chart_data.weight_density;
chart(s,'scatter',{series:[densityPolygon('Observed density polygon',wd.hist_x,wd.hist_y,'#EE7733'),series('Normal',wd.x,wd.normal,'#4477AA'),series('Lognormal',wd.x,wd.lognormal,'#228833')],scatterOptions:{style:'lineWithMarkers'},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:18,fill:'#000000'}},xAxis:axis('Whole weight (scaled)',0,3,.5),yAxis:axis('Density',0,1.6,.4)});
side(s,'Both rejected','Normal AD: 16.47\nLognormal AD: 86.51\n\nHolm p = 0.0015');
takeaway(s,'Rejection is a valid finding; no extra families are searched to obtain a preferred p-value.');

s=slide('Three prespecified hypothesis tests','','', 'Notebook3; SciPy Welch t-test, statsmodels anova_oneway');
table(s,['Test','Null hypothesis'],[['Welch t','Mean Rings(M) = mean Rings(F)'],['Chi-square','Group and ring band are independent'],['Welch ANOVA','Mean Length(F) = mean Length(I) = mean Length(M)']],70,185,1140,300,[1,3],21);
text(s,'α = 0.05 · Holm correction across the three primary questions',80,535,1120,75,23);
takeaway(s,'Methods still assume appropriate sampling independence; missing batch IDs limit inference.');

s=slide('Results and effect magnitude','');
table(s,['Test','Statistic','Holm p'],[['Welch t',fmt(S.welch.statistic,3),pv(S.hypotheses[0].p_holm)],['Chi-square',fmt(S.chi.statistic,2),pv(S.hypotheses[1].p_holm)],['Welch ANOVA',fmt(S.anova.F,2),pv(S.hypotheses[2].p_holm)]],70,185,1140,280,[1.6,1,1.4],23);
text(s,`M − F: ${fmt(S.welch.difference)} rings\n95% CI [${fmt(S.welch.ci_low)}, ${fmt(S.welch.ci_high)}]`,80,500,650,100,24,true);
text(s,`Cramér’s V = ${fmt(S.chi.cramers_v)}\nMinimum expected count: 334.7`,800,500,420,100,21);
takeaway(s,'Statistical significance and practical magnitude answer different questions.');

s=slide('Pearson and Spearman associations','');
const labels=['length','diameter','height','whole','shucked','viscera','shell','rings'];const keys=Object.keys(S.spearman);
const columnLabels=['Len','Dia','Hgt','Whole','Shuck','Visc','Shell','Rings'];
const cell=42,baseX=195,baseY=245;
// Fixed signed domain matches the report: blue negative, neutral zero, red positive.
function correlationFill(value){
 const t=Math.min(1,Math.abs(value)),start=[247,247,247],end=value<0?[33,102,172]:[178,24,43];
 return '#'+start.map((v,i)=>Math.round(v+(end[i]-v)*t).toString(16).padStart(2,'0')).join('');
}
if(correlationFill(-1)!=='#2166ac'||correlationFill(0)!=='#f7f7f7'||correlationFill(1)!=='#b2182b')throw Error('Invalid signed correlation color scale');
keys.forEach((k,i)=>{text(s,labels[i],baseX-115,baseY+i*cell+10,110,28,14,false,{align:'right'});text(s,columnLabels[i],baseX+i*cell,baseY-29,cell,24,10,false,{align:'center'});
 keys.forEach((j,c)=>{const value=S.spearman[k][j];s.shapes.add({geometry:'rect',name:`Spearman ${k} ${j}`,position:{left:baseX+c*cell,top:baseY+i*cell,width:cell,height:cell},fill:correlationFill(value),line:{fill:'#ffffff',width:1}});text(s,fmt(value,2),baseX+c*cell,baseY+i*cell+11,cell,27,10,false,{align:'center',color:Math.abs(value)>.65?'#ffffff':'#000000'});});});
for(let i=0;i<32;i++)s.shapes.add({geometry:'rect',name:`Correlation scale ${i}`,position:{left:554,top:baseY+i*10.5,width:16,height:10.5},fill:correlationFill(1-2*i/31),line:{fill:'none',width:0}});
for(const [label,y] of [['+1',baseY-4],['0',baseY+155],['−1',baseY+314]])text(s,label,577,y,42,25,12);
text(s,'Spearman ρ',195,169,500,42,25,true);
text(s,'Shell weight ↔ Rings',670,235,550,60,27,true);text(s,`Pearson r = ${fmt(S.correlations.shell_weight.pearson,3)}\nSpearman ρ = ${fmt(S.correlations.shell_weight.spearman,3)}\nn = 3,341`,670,340,550,170,25);
takeaway(s,'High correlation among measurements can destabilize conditional regression slopes.');

s=slide('Shell weight and Rings','');
const sc=S.chart_data.shell_scatter;
chart(s,'scatter',{series:[series('Training specimens',sc.x,sc.y,'#4477AA',true)],scatterOptions:{style:'marker'},xAxis:axis('Shell weight (scaled)',0,1.1,.2),yAxis:axis('Rings (count)',0,30,5)});
side(s,'ρ = 0.693','Marginal association\n\nInteger rings create overlapping points.');
takeaway(s,'This relationship is descriptive; it is not an independent causal effect.');

s=slide('Multiple linear regression design','','', 'Notebook5; scikit-learn1.6 common pitfalls and pipeline documentation');
text(s,'Rings = β₀ + Σ βⱼxⱼ + ε',80,185,1120,70,30,true);
table(s,['Model','Inputs'],[['Baseline','Training mean only'],['Compact','Group + dimensions + whole weight'],['Full','All eight original inputs']],70,300,1140,240,[1,3],23);
takeaway(s,'Fivefold CV fits a new imputer, scaler and regression within every training fold.');

s=slide('Holdout performance and model limits','');
chart(s,'bar',{categories:S.test_metrics.map(r=>r.model),series:[{name:'MAE',values:S.test_metrics.map(r=>r.mae),fill:'#4477AA',line},{name:'RMSE',values:S.test_metrics.map(r=>r.rmse),fill:'#EE7733',line}],barOptions:{direction:'column',grouping:'clustered',gapWidth:80},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:20,fill:'#000000'}},dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0.00',textStyle:{fontSize:22,fill:'#000000'}},xAxis:axis('Prespecified models'),yAxis:axis('Test error (rings)',0,4,1)});
side(s,'Full R² = 0.526','RMSE: 2.25 rings\n31.1% below baseline\n\nOne out-of-range prediction');
takeaway(s,'High VIF, heteroskedasticity and influence limit coefficient interpretation.');

s=slide('Reproducible code demonstration','');
rows(s,['Verify source checksum and saved train/test indexes','Inspect hypotheses, confidence interval and Holm correction','Show preprocessing inside CV and the test prediction CSV','Trace report and slide numbers back to the exported summary'],80,180,1120,105,24);
takeaway(s,'The executed notebook remains available as the offline demonstration fallback.');

s=slide('Conclusions and limitations','');
text(s,'Distribution candidates rejected',80,195,1120,60,29,true);
text(s,'Full-model test MAE: 1.60 rings',80,300,1120,60,29,true);
text(s,'Historical sampling, collinearity and residual patterns limit generalization.',80,420,1120,100,25);
takeaway(s,'Observed association and predictive improvement do not establish biological causation.');

s=slide('Appendix: definitions and inference','');
rows(s,['Welch t: mean difference / estimated standard error','Chi-square: Σ (observed − expected)² / expected','Classical ANOVA: MS between / MS within','Holm: control the three prespecified primary questions'],80,180,1120,105,23);

s=slide('Appendix: regression diagnostics','');
table(s,['Check','Observed evidence'],[['Design rank','10 / 10'],['Breusch–Pagan p',pv(S.diagnostics.bp_p)],['Cook > 4/n','212 training records'],['Full coefficient covariance','HC3; numeric slopes per training SD'],['Sensitivity design','Filter inner train; keep validation unchanged']],70,180,1140,350,[1.4,2.6],21);
takeaway(s,'The primary model retains influential observations; sensitivity is reported separately.');

s=slide('References','','', 'Primary sources listed on this slide and in report References');
text(s,'Nash et al. (1994). Abalone. UCI Machine Learning Repository.\nhttps://doi.org/10.24432/C55C7W\n\nSciPy 1.15.3 — statistical tests and goodness of fit\nhttps://docs.scipy.org/doc/scipy-1.15.3/\n\nStatsmodels — Welch ANOVA, HC3 and influence\nhttps://www.statsmodels.org/\n\nScikit-learn 1.6 — preprocessing and validation\nhttps://scikit-learn.org/1.6/',80,180,1120,440,20);
takeaway(s,'Public dataset reused with attribution under CC BY 4.0.');

if(deck.slides.items.length!==19)throw Error('Expected16main+3appendices');
if(notes.slice(0,16).reduce((v,n)=>v+n.seconds,0)!==720)throw Error('Expected12minutes');
const staging=path.join(root,'.build/slides');await fs.mkdir(path.join(staging,'final'),{recursive:true});
const candidate=path.join(staging,'candidate.pptx');await(await PresentationFile.exportPptx(deck)).save(candidate);
const revision=Date.now(),final=path.join(staging,'final',`validated-${revision}.pptx`),receiptPath=path.join(staging,`validation-${revision}.json`);
await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:final,pythonExecutable:path.join(runtime,'dependencies/python/bin/python'),integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),explicitTotalSlideCount:19,requiredNativeTableOwnerSlides:nativeTables,requiredNativeChartOwnerSlides:nativeCharts,materializeLiteralChartWorkbooks:true,layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...nativeTables.flatMap(n=>['--require-native-table-slide',String(n)])],fontPolicy:{basis:'design',families:['Arial','DejaVu Sans Mono']},verifyArtifactToolImport:true,receiptPath});
await fs.copyFile(final,path.join(root,'slides',`${M.prefix}_Presentation${status.ready?'':'_REVIEW'}.pptx`));await fs.copyFile(receiptPath,path.join(staging,'validation.json'));
await fs.writeFile(path.join(root,'slides/Speaker_Notes_VI.md'),'# Lời thoại và notes tiếng Việt\n\n16 slide chính dự kiến 720 giây = 12 phút; 3 phụ lục không tính trong video. Chưa có xác nhận đã diễn tập.\n\n'+notes.map(n=>`## Slide ${n.slide} — ${n.title}\n\n${n.notes}\n`).join('\n'));
await fs.writeFile(path.join(staging,'slide_content.json'),JSON.stringify(notes,null,2));
console.log(JSON.stringify({slides:19,nativeTables,nativeCharts,durationSeconds:720}));
