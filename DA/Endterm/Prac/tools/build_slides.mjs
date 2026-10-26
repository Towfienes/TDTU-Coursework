// Editable academic slides from the executed notebook's authoritative summary.
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
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
const S=JSON.parse(await fs.readFile(path.join(root,'results/summary.json'),'utf8'));
const M=JSON.parse(await fs.readFile(path.join(root,'project.json'),'utf8'));
const logoBytes=new Uint8Array(await fs.readFile(path.join(root,'report/assets/tdtu-logo.png')));
const deck=Presentation.create({slideSize:{width:1280,height:720}});
deck.theme.defaultFont='Arial';
deck.theme.colorScheme={name:'TDTU Monochrome Framing with Color Evidence',themeColors:{accent1:'#2b5c8f',accent2:'#e26d5c',accent3:'#2ecc71',accent4:'#e74c3c',accent5:'#3498db',accent6:'#08519c',bg1:'#ffffff',bg2:'#eeeeee',tx1:'#000000',tx2:'#333333',dk1:'#000000',dk2:'#333333',lt1:'#ffffff',lt2:'#eeeeee',hlink:'#000000',folHlink:'#444444'}};
const line={style:'solid',fill:'#000000',width:1};
const notes=[];
const nativeTables=[];
const nativeCharts=[];
const fmt=(n,d=3)=>Number(n).toFixed(d);
const bands=Object.entries(S.performance_distribution);
const context=S.rankings.filter(r=>r.family!=='Prior grades');

function text(slide,value,x,y,w,h,size=24,bold=false,options={}){
  const shape=slide.shapes.add({geometry:'textbox',name:options.name ?? String(value).slice(0,55),position:{left:x,top:y,width:w,height:h},fill:'none',line:{fill:'none',width:0}});
  shape.text=String(value);
  shape.text.style={fontSize:size*4/3,typeface:options.mono?'DejaVu Sans Mono':'Arial',color:'#000000',bold,alignment:options.align ?? 'left',verticalAlignment:'top',insets:0,autoFit:'none',wrap:'square'};
  return shape;
}
function rule(slide,x,y,w,h=1.4){slide.shapes.add({geometry:'rect',name:'Thin monochrome rule',position:{left:x,top:y,width:w,height:h},fill:'#000000',line:{fill:'none',width:0}});}
function slide(title,note,duration,source='Executed notebook and results/summary.json'){
  const s=deck.slides.add();s.background.fill='#ffffff';
  s.images.add({blob:logoBytes,contentType:'image/png',alt:'Original Ton Duc Thang University logo',fit:'contain',position:{left:42,top:20,width:158,height:88}});
  text(s,title,240,45,990,66,32,true,{name:'Slide title'});rule(s,40,126,1200);
  const number=deck.slides.items.length;
  text(s,String(number).padStart(2,'0'),1180,678,60,24,11,false,{align:'right'});
  const full=`Thời lượng dự kiến: ${duration}.\n${note}\nNguồn: ${source}.`;
  s.speakerNotes.text=full;
  notes.push({slide:number,title,duration,notes:full});
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

let s=slide('Data Analysis and Visualization','Giới thiệu nhóm bốn người và Cô Ho Thi Linh. Nêu đề tài phân tích thành tích học sinh từ dữ liệu công khai; báo cáo cuối kỳ ngày 20/10/2026. Không gọi đây là dữ liệu sinh viên TDTU.','45 giây');
text(s,'Student Performance',80,180,1120,95,48,true);
text(s,'Preprocessing, Statistics and Visualization',80,286,1120,65,27);
text(s,'ENDTERM REPORT',80,365,700,45,24,true);
text(s,M.authors.map(a=>`${a.name}  ${a.id}`).join('\n'),80,430,680,175,18);
text(s,`VibeCoding_Expert\nAdvised by\n${M.advisor}`,820,445,380,130,20);
text(s,'20 October 2026',80,648,500,35,17);

s=slide('Objectives and analytical questions','Trình bày bốn câu hỏi tương ứng bốn phần đề. Điểm nhấn là phân tích mô tả có thể chạy lại, có nguồn gốc dữ liệu và có giới hạn rõ ràng. Chuyển sang dataset trước khi giải thích kỹ thuật.','1 phút');
rows(s,['How are final grades distributed?','What changes when missing values are imputed or removed?','Which original factors have the strongest observed association with G3?','How do group comparisons and visualizations qualify the findings?'],80,175,1120,112,24);

s=slide('Dataset and provenance','Nguồn UCI Student Performance, chỉ file student-por.csv. Có 649 bản ghi, 33 cột, không thiếu ở nguồn. GP có 423 và MS có 226 bản ghi. Không gộp môn Toán vì có học sinh trùng giữa hai file. Nêu thang lý thuyết 0–20 khác miền quan sát 0–19.','1 phút 15 giây','Cortez (2008), https://doi.org/10.24432/C5TG7T; references/student.txt');
table(s,['Property','Selected data'],[['Subject','Portuguese language'],['Records / columns','649 / 33'],['Schools','GP: 423 · MS: 226'],['Original missing cells','0'],['Outcome','G3, final grade on a 0–20 scale'],['Licence','CC BY 4.0']],80,175,1120,390,[1,2.5],21);
takeaway(s,'Two Portuguese schools; findings do not directly represent TDTU students.');

s=slide('Inspect before transforming','Mở notebook mục I.1 và I.2. Giải thích delimiter chấm phẩy, kiểm checksum, shape, dtypes và info. Hiển thị cả đầu và cuối dữ liệu giúp phát hiện parse sai. Integer storage không có nghĩa studytime là số giờ thực.','1 phút');
text(s,"raw = pd.read_csv(path, sep=';')\nraw.head(5)\nraw.tail(5)\nraw.shape\nraw.dtypes\nraw.info()",80,190,760,320,21,false,{mono:true});
text(s,'649 × 33',940,215,290,80,35,true);
text(s,'Numeric, ordinal and categorical fields\n\nPreserve raw data',940,330,290,235,22);
takeaway(s,'Recorded zero grades remain observations; they are not reclassified as missing.');

s=slide('A controlled missingness experiment','Giải thích 5%×649=32,45; lấy 32 ô nên tỷ lệ là 4,93%. Che duy nhất absences, cùng mask cho hai nhánh. Seed 42 tái lập; MCAR chỉ là giả lập. Tất cả kết luận chính dùng raw đã kiểm.','1 phút');
text(s,'649',80,190,330,100,54,true);text(s,'complete original records',80,300,330,100,23);
rule(s,440,190,1.5,340);
text(s,'32',490,190,320,100,54,true);text(s,'masked absences values\n4.93% of records\nSeed 42',490,300,320,180,23);
rule(s,860,190,1.5,340);
text(s,'Two treatments',910,195,320,95,30,true);text(s,'Mean imputation\n\nDrop missing rows',910,315,320,180,23);
takeaway(s,'The missingness exercise is separate from the primary analysis of original measurements.');

s=slide('Imputation and deletion change the data','Bảng này lấy từ output chạy thật. Mean imputation dùng mean của 617 giá trị chưa bị che: 3,623987. Giữ 649 dòng nhưng giảm phân tán và tạo số lần vắng lẻ. Dropna còn 617. Cả hai bắt đầu từ cùng corrupted, không drop sau fillna.','1 phút 15 giây');
table(s,['Variant','Rows','Missing','Mean absences','Sample SD'],S.missing_comparison.map(r=>[r.variant,r.rows,r.missing_cells,fmt(r.absences_mean,4),fmt(r.absences_std,4)]),70,190,1140,310,[2.2,.8,.9,1.4,1.3],20);
text(s,'Imputation preserves rows and concentrates replacement values at the mean.',80,540,1120,75,24);
takeaway(s,'A single seeded simulation does not establish a universally best treatment.');

s=slide('Python structures and regex','Chứng minh Series→list→lọc bằng Python. Có 549 điểm ≥ 10 theo quy ước bài phân tích. Regex fullmatch lấy đúng G1/G2/G3, loại G12 và G3_extra. Không cần bịa ID cá nhân hoặc dữ liệu bẩn.','45 giây');
text(s,"grades = raw['G3'].tolist()\nselected = [g for g in grades if g >= 10]\n\ngrade_cols = [c for c in raw.columns\n              if re.fullmatch(r'G[123]', c)]",80,190,1120,250,21,false,{mono:true});
text(s,`Filtered list: ${649-S.performance_distribution['0–9'].count} grades`,80,490,1120,65,29,true);
takeaway(s,'Full matching validates actual schema names without inventing personal identifiers.');

s=slide('Indexing and a two-condition filter','Giải thích loc theo nhãn có bao gồm cận cuối 9, iloc theo vị trí. Bộ lọc studytime ≥ 2 và absences ≤ 5 cho 334/649 = 51,46%. Nhấn mạnh ngưỡng minh họa, không phải quy tắc can thiệp.','1 phút');
text(s,"df.loc[:9]\ndf.iloc[:, selected_positions]\n\ndf.loc[(df.studytime >= 2) &\n       (df.absences <= 5)]",80,190,795,270,21,false,{mono:true});
text(s,String(S.filter.count),940,215,280,90,48,true);
text(s,`${fmt(S.filter.percent,2)}% of records\n\nBoth conditions hold`,940,330,280,200,23);
takeaway(s,'The study-time variable is an ordered interval code, not a continuous hour count.');

s=slide("Three engineered features","Giải thích từng cột và thao tác insert ngay trước G3. prior_grade_mean không chứa G3; grade_progress là chênh lệch giữa hai kỳ, không tự nó chứng minh tiến bộ do can thiệp. performance_band gồm 0–9, 10–14, 15–20 là nhóm tự quy ước. Vì chứa outcome, cột này không được xếp hạng như một yếu tố giải thích.",'1 phút 15 giây');
table(s,['Feature','Definition','Purpose'],[['prior_grade_mean','(G1 + G2) / 2','Earlier-grade summary'],['grade_progress','G2 − G1','Assessment difference'],['performance_band','0–9; 10–14; 15–20','Outcome description']],70,195,1140,280,[1.5,1.4,1.5],20);
text(s,'DataFrame.insert() places prior_grade_mean immediately before G3.',80,525,1120,85,24);
takeaway(s,'All derived features are excluded from the original-factor association ranking.');

s=slide("Grouped statistics and transformation","Notebook và báo cáo có đủ count, mean, std, min, max cho cả G1, G2, G3 theo trường. Slide trích G3 và cỡ mẫu để đọc được. GP có 423 bản ghi, MS có 226; trung bình và độ phân tán khác nhau nhưng chưa điều chỉnh yếu tố khác. Chuẩn hóa min–max dùng transform trong từng trường và giữ đúng index; nhóm hằng trả 0. Đây là thang tương đối trong nhóm.",'1 phút 30 giây');
table(s,['School','n','G3 mean','G3 median','G3 SD'],S.school_g3.map(r=>[r.school,r.count,fmt(r.mean),r.median,fmt(r.std)]),70,185,1140,210,[1,1,1.4,1.4,1.4],23);
text(s,'Within-school score',80,440,1120,50,27,true);
text(s,'(G3 − school minimum) / (school maximum − school minimum)',80,505,1120,75,22);
takeaway(s,'Constant groups receive 0; the scale describes relative position within each school.');

s=slide("Association ranking: two distinct families","Có ma trận Pearson cho 16 biến số gốc và bảng Spearman bổ sung. G2 có rho khoảng 0,94445 và là điểm kỳ trước; không trình bày như một phát hiện mới về hoàn cảnh. failures có rho khoảng −0,44836, lớn nhất về trị tuyệt đối trong nhóm biến hoàn cảnh dạng số/thứ bậc đã xét. Đây không phải feature importance của mô hình đa biến. Không so mean difference của biến định tính trực tiếp với rho.",'1 phút 15 giây');
text(s,`Prior grade: G2, Spearman ρ = ${fmt(S.rankings[0].spearman_rho,4)}`,80,170,1120,55,27,true);
table(s,['Contextual numerical/ordinal factor','Spearman ρ','n'],context.slice(0,5).map(r=>[r.variable,fmt(r.spearman_rho,4),r.n]),80,250,1120,300,[2.4,1,0.8],21);
takeaway(s,'The ranking is unadjusted association among examined original numerical/ordinal factors.');

s=slide("Final-grade distribution","Histogram trong notebook dùng sns.histplot với bin một điểm. Slide dùng cùng bảng tần số đã xuất ở dạng chart chỉnh sửa được. Mean khoảng 11,906; median 12; sample SD khoảng 3,231. Giữ điểm 0 như một kết quả quan sát. Trục giữ toàn thang lý thuyết 0–20, kể cả bin rỗng.",'1 phút');
chart(s,'bar',{categories:Array.from({length:21},(_,i)=>String(i)),series:[{name:'Records',values:S.charts.histogram,fill:'#2b5c8f',line}],barOptions:{direction:'column',gapWidth:0},
  xAxis:{title:'G3 final grade (points)',textStyle:{fontSize:24,fill:'#000000'},line},
  yAxis:{title:'Number of records',min:0,majorGridlines:{fill:'#dddddd',width:.7,style:'solid'},textStyle:{fontSize:24,fill:'#000000'},line}});
side(s,`Mean ${fmt(S.grade_statistics.G3.mean,2)}`,`Median ${S.grade_statistics.G3.median}\nSample SD ${fmt(S.grade_statistics.G3.std,2)}\n\nn = 649`);
takeaway(s,'One-point-wide bins retain the integer-score distribution.');

s=slide("Final grades by school","Box plot trong notebook dùng Seaborn. Q1, median, Q3, whiskers và outliers được xuất theo cùng quy tắc 1,5 IQR. Slide dùng các đối tượng chỉnh sửa được dựng từ thống kê này để tránh khác biệt quy tắc quartile của Office. Median GP là 13, MS là 11. Khác biệt nhóm chưa điều chỉnh không chứng minh tác động của trường.",'1 phút');
const plot={left:140,top:195,width:660,height:350};
for(const value of [0,5,10,15,20]){const y=plot.top+plot.height-value/20*plot.height;rule(s,plot.left,y,plot.width,.7);text(s,value,80,y-15,50,40,18,false,{align:'right'});}
text(s,'G3 (points)',80,155,500,40,19);
const schoolColors={GP:'#2b5c8f',MS:'#e26d5c'};
['GP','MS'].forEach((school,i)=>{
  const b=S.charts.box[school],x=340+i*300,yy=value=>plot.top+plot.height-value/20*plot.height;
  rule(s,x,yy(b.whishi),1.5,yy(b.whislo)-yy(b.whishi));rule(s,x-35,yy(b.whishi),70);rule(s,x-35,yy(b.whislo),70);
  s.shapes.add({geometry:'rect',name:`${school} Q1–Q3, exported Seaborn statistics`,position:{left:x-65,top:yy(b.q3),width:130,height:yy(b.q1)-yy(b.q3)},fill:schoolColors[school],line});
  s.shapes.add({geometry:'rect',name:`${school} median`,position:{left:x-65,top:yy(b.med)-1.25,width:130,height:2.5},fill:'#f1c40f',line:{fill:'none',width:0}});
  for(const outlier of [...new Set(b.fliers)])s.shapes.add({geometry:'ellipse',name:`${school} outlier ${outlier}`,position:{left:x-4,top:yy(outlier)-4,width:8,height:8},fill:schoolColors[school],line});
  text(s,`${school} (n=${S.dataset.school_counts[school]})`,x-115,575,230,40,20,false,{align:'center'});
});
side(s,'Medians: 13 / 11','GP has a higher observed centre.\n\nMS has greater dispersion.');
takeaway(s,'Descriptive group differences do not identify a causal school effect.');

s=slide("Final grade by study-time category","So sánh mean G3 theo studytime 1–4. Bảng gốc có count và SD; các cỡ nhóm lần lượt là 212, 305, 97, 35. Nhãn trên slide giữ cả khoảng giờ và n. Nhóm trên 10 giờ nhỏ nhất. Không suy ra rằng một người học thêm giờ sẽ đạt đúng chênh lệch trung bình quan sát này.",'1 phút');
chart(s,'bar',{categories:S.group_stats.studytime.map((r,i)=>`${['<2 h','2–5 h','5–10 h','>10 h'][i]}\nn=${r.count}`),series:[{name:'Mean G3',values:S.group_stats.studytime.map(r=>r.mean),fill:'#2b5c8f',line}],barOptions:{direction:'column',gapWidth:70},
  dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0.00',textStyle:{fontSize:24,fill:'#000000'}},
  xAxis:{title:'Weekly study-time category',textStyle:{fontSize:24,fill:'#000000'},line},
  yAxis:{title:'Mean G3 (points)',min:0,max:20,majorUnit:5,textStyle:{fontSize:24,fill:'#000000'},line,majorGridlines:{fill:'#dddddd',width:.7,style:'solid'}}});
side(s,'Unequal groups','Category codes represent intervals.\n\nCounts accompany means.');
takeaway(s,'The positive association remains observational and potentially confounded.');

s=slide("Performance-band proportions","Pie chart sử dụng đúng cột tạo ở Phần II. Nhóm 0–9 có 100 bản ghi, 15,41%; 10–14 có 418, 64,41%; 15–20 có 131, 20,18%. Đây là dải điểm do nhóm quy ước để mô tả, không phải hệ thống xếp loại chính thức. Tổng count là 649 và phần trăm tổng 100 trước làm tròn.",'1 phút');
const bandColors={'0–9':'#e74c3c','10–14':'#3498db','15–20':'#2ecc71'};
chart(s,'pie',{position:{left:80,top:175,width:790,height:450},categories:bands.map(([band])=>band),series:[{name:'Records',values:bands.map(([,r])=>r.count),points:bands.map(([band],idx)=>({idx,fill:bandColors[band]||'#2b5c8f',line}))}],
  xAxis:{visible:false},yAxis:{visible:false},hasLegend:true,legend:{position:'bottom',textStyle:{fontSize:24,fill:'#000000'}},
  dataLabels:{showPercent:true,position:'bestFit',numberFormatCode:'0.0%',textStyle:{fontSize:27,fill:'#000000',bold:true}}});
side(s,'Largest band\n10–14',bands.map(([band,r])=>`${band}: ${r.count}\n${fmt(r.percent,2)}%`).join('\n\n'));
takeaway(s,'The bands are analyst-defined descriptions, not an official grading classification.');

s=slide("Earlier and final grades","Notebook dùng sns.regplot, ci=None, và độ trong suốt để thấy các tọa độ chồng nhau. Tọa độ đường fit được xuất từ lần chạy Seaborn và dùng lại trên slide. Rho khoảng 0,9445 là liên hệ, không phải nhân quả. G2 và G3 là các kỳ đánh giá liên quan nhau về thời gian và nội dung.",'1 phút');
chart(s,'scatter',{series:[{name:'Observed records',xValues:S.charts.scatter.x,values:S.charts.scatter.y,fill:'#2b5c8f',line:{fill:'none',width:0},marker:{symbol:'circle',size:4,fill:'#2b5c8f'}},
  {name:'Descriptive fitted line',xValues:S.charts.scatter.fit.x,values:S.charts.scatter.fit.y,fill:'none',line:{fill:'#d9534f',width:2.5,style:'solid'},marker:{symbol:'none'}}],scatterOptions:{style:'lineWithMarkers'},
  xAxis:{title:'G2 (points)',min:0,max:20,majorUnit:5,textStyle:{fontSize:24,fill:'#000000'},line,majorGridlines:null},
  yAxis:{title:'G3 (points)',min:0,max:20,majorUnit:5,textStyle:{fontSize:24,fill:'#000000'},line,majorGridlines:{fill:'#dddddd',width:.7,style:'solid'}}});
side(s,`ρ = ${fmt(S.rankings[0].spearman_rho,4)}`,`Pearson r = ${fmt(S.pearson_G2_G3,4)}\n\nRelated assessments at different periods`);
takeaway(s,'The fitted line describes the observations; it is not a validated forecasting model.');

s=slide("Matplotlib core from Python structures","Chỉ rõ cell III.4: dữ liệu chuyển thành list/dictionary, rồi dùng Matplotlib bar và bar_label. Giá trị là mean G1/G2 của năm bản ghi đầu, không chứa G3. Nhãn 1–5 là vị trí dòng nguồn, không phải mã hay tên cá nhân. Ví dụ nhỏ này minh họa thao tác Python và vẽ, không đại diện cho toàn bộ dataset.",'1 phút');
chart(s,'bar',{categories:S.charts.core.records,series:[{name:'Earlier-grade mean',values:S.charts.core.values,fill:'#2b5c8f',line}],barOptions:{direction:'column',gapWidth:100},
  dataLabels:{showValue:true,position:'outEnd',numberFormatCode:'0.0',textStyle:{fontSize:24,fill:'#000000'}},
  xAxis:{title:'Source row number (one-based)',textStyle:{fontSize:24,fill:'#000000'},line},
  yAxis:{title:'Mean of G1 and G2 (points)',min:0,max:20,majorUnit:5,textStyle:{fontSize:24,fill:'#000000'},line,majorGridlines:{fill:'#dddddd',width:.7,style:'solid'}}});
side(s,'List + dictionary','Only Matplotlib plots the notebook demonstration.\n\nFive records illustrate mechanics.');
takeaway(s,'This small example is not a random sample or a population trend.');

s=slide("Comprehensive report and extreme records","Hàm comprehensive_report(df) vừa in nội dung dễ đọc vừa trả dictionary để dùng lại đúng số liệu. Có 37 cột: 33 cột gốc và 4 cột dẫn xuất. Top/bottom giữ đúng 10 dòng; stable sort giữ thứ tự nguồn khi đồng hạng. Tất cả 37 cột có trong notebook và CSV; slide chỉ trích các cột có thể đọc được.",'1 phút 30 giây');
table(s,['Summary item','Count','Share'],[['Analysis records',649,'100%'],['Analysis columns',37,'33 original + 4 derived'],...bands.map(([band,r])=>[`G3 band ${band}`,r.count,`${fmt(r.percent,2)}%`])],70,190,1140,330,[1.9,1,1.7],21);
text(s,'Top/bottom: exactly ten rows; original source order resolves ties.',80,555,1120,65,23);
takeaway(s,'Complete rows and all columns are preserved in the notebook and CSV exports.');

s=slide("Code demonstration","Demo trong 3 phút: (1) mở I.3, chỉ mask 32 ô và hai kết quả mean/dropna 649/617; (2) mở II.2 và II.4, chỉ insert và transform; (3) mở IV.1 và IV.2, gọi comprehensive_report rồi xem bảng đủ cột. Chạy toàn bộ từ kernel sạch trước buổi báo cáo để kiểm tái lập. Nếu demo gặp lỗi, dùng outputs đã lưu, không chờ tải dữ liệu. Xem Demo_VI.md để có lời dẫn và mốc thời gian.",'3 phút');
rows(s,['Show the same 32-cell mask and both treatment branches.','Inspect insert(), grouped statistics and transform().','Call comprehensive_report(df) and inspect complete top/bottom rows.','Use the executed notebook if live execution fails.'],80,180,1120,108,24);

s=slide("Conclusions and limitations","Chốt phân bố điểm, liên hệ với G2 và failure categories. Nhắc giới hạn: hai trường ở Bồ Đào Nha, không đại diện TDTU; chưa điều chỉnh đa biến; không chứng minh nhân quả; chỉ một mô phỏng MCAR. Gợi ý nghiên cứu hỗ trợ học sinh là một hướng cần kiểm chứng, chưa có effect size hay mức lợi ích dự kiến.",'1 phút 30 giây');
text(s,'Observed findings',80,180,530,50,28,true);
text(s,`Final grade mean: ${fmt(S.grade_statistics.G3.mean,2)}\n\nG2 association: ρ = ${fmt(S.rankings[0].spearman_rho,4)}\n\nStrongest examined contextual rank association: failures`,80,255,530,330,23);
rule(s,650,185,1.5,395);
text(s,'Interpretation limits',710,180,500,50,28,true);
text(s,'Two schools and one subject\n\nOrdinal coding and unequal groups\n\nUnadjusted observational associations\n\nOne MCAR simulation',710,255,500,330,23);

s=slide("References","Nêu dataset và tài liệu chính thức của các thư viện. Codebook, mã nguồn và manifest có trong gói nộp. Biểu đồ phân tích sinh từ notebook; logo giữ nguồn chuẩn của trường. Trích dẫn dữ liệu theo CC BY 4.0 và chuyển sang hỏi đáp.",'30 giây','URLs displayed on this slide');
text(s,'Cortez (2008). Student Performance. UCI Machine Learning Repository.\nhttps://doi.org/10.24432/C5TG7T\n\nPandas documentation  https://pandas.pydata.org/docs/\nSeaborn API  https://seaborn.pydata.org/api.html\nMatplotlib documentation  https://matplotlib.org/stable/\nNumPy documentation  https://numpy.org/doc/',80,190,1120,415,21);
takeaway(s,'The dataset is reused under CC BY 4.0 with attribution.');

s=slide("Questions and discussion","Mời giảng viên hỏi. Chuẩn bị giải thích vì sao 32 ô chỉ là 4,93%; mean imputation thay đổi độ phân tán; tương quan G2 không chứng minh nhân quả; normalization trong nhóm không tạo thang điểm tuyệt đối; stable top ten xử lý đồng hạng ra sao. Xem Viva_VI.md.",'Theo giảng viên');
text(s,'Questions',80,210,1120,100,44,true);
text(s,'Missing data, association, group comparison and reproducibility',80,345,1120,140,28);

for(const [title,key] of [['Appendix: highest ten records','top_ten'],['Appendix: lowest ten records','bottom_ten']]){
  s=slide(title,'Bảng trên slide chọn một số cột để đọc được. Tất cả 37 cột nằm trong notebook và CSV. Source index dùng zero-based. Đồng hạng giữ thứ tự dòng nguồn; bản ghi đồng điểm bị loại không kém hơn hay tốt hơn về G3.','Dự phòng');
  table(s,['Source index','School','G1','G2','G3','Band'],S[key].map(r=>[r.source_index,r.school,r.G1,r.G2,r.G3,r.performance_band]),80,175,1120,440,[1.6,1,.8,.8,.8,1.5],18);
  takeaway(s,'Selected columns shown; the full 37-column rows are in the notebook and CSV.');
}
s=slide("Appendix: sensitivity and method checks","Bảng độ nhạy hiển thị sample SD của absences, rho với G3 và số dòng thỏa bộ lọc. Dùng cùng mask cho mọi phương pháp. Denominator raw là 649, dropna là 617. Fixture nhóm hằng trả 0; kiểm ngưỡng band tại 0, 9, 10, 14, 15, 20. Giữ nguyên mã failures và ghi chú sự mơ hồ trong codebook, không sửa ngầm.",'Dự phòng');
table(s,['Variant','n','Absences SD','ρ with G3','Filter n'],S.sensitivity.map(r=>[r.variant,r.n,fmt(r.absences_std,4),fmt(r.absences_G3_spearman,4),r.filter_count]),70,185,1140,250,[2,.7,1.3,1.3,1],19);
text(s,'Boundary checks: score bands, constant groups, zero-count categories and stable ties.',80,485,1120,90,24);
takeaway(s,'Actual failure codes are retained; the upper-code ambiguity is documented.');

if(deck.slides.items.length!==25)throw new Error('Expected 22 main + 3 appendix slides.');
const staging=path.join(root,'.build/slides');await fs.mkdir(staging,{recursive:true});
const candidate=path.join(staging,'candidate.pptx');
await (await PresentationFile.exportPptx(deck)).save(candidate);
await fs.mkdir(path.join(staging,'final'),{recursive:true});
const revision=Date.now();
const final=path.join(staging,'final',`validated-${revision}.pptx`);
const receiptPath=path.join(staging,`validation-${revision}.json`);
const result=await finalizePresentation({workspaceDir:root,candidatePath:candidate,finalPath:final,
  pythonExecutable:path.join(runtime,'dependencies/python/bin/python'),
  integrityValidatorPath:path.join(skill,'container_tools/inspect_presentation_package_integrity.py'),
  layoutValidatorPath:path.join(skill,'container_tools/inspect_presentation_layout_geometry.py'),
  explicitTotalSlideCount:25,requiredNativeTableOwnerSlides:nativeTables,requiredNativeChartOwnerSlides:nativeCharts,
  materializeLiteralChartWorkbooks:true,
  layoutArgs:['--expected-slide-size-emu','12192000,6858000','--validate-bullet-geometry','--validate-heading-fit',...nativeTables.flatMap(number=>['--require-native-table-slide',String(number)])],
  fontPolicy:{basis:'design',families:['Arial','DejaVu Sans Mono']},verifyArtifactToolImport:true,
  receiptPath});
await fs.copyFile(final,path.join(root,'slides',`${M.prefix}_Presentation.pptx`));
await fs.copyFile(receiptPath,path.join(staging,'validation.json'));
await fs.writeFile(path.join(root,'slides/Speaker_Notes_VI.md'),'# Kịch bản thuyết trình tiếng Việt\n\nThời lượng dự kiến khoảng 24,5 phút trước Q&A; chưa xác nhận đã diễn tập thực tế.\n\n'+notes.map(n=>`## Slide ${n.slide} — ${n.title}\n\n${n.notes}\n`).join('\n'),'utf8');
await fs.writeFile(path.join(staging,'slide_content.json'),JSON.stringify(notes,null,2));
console.log(JSON.stringify({slides:25,nativeTables,nativeCharts,final:path.join('slides',`${M.prefix}_Presentation.pptx`)}));
