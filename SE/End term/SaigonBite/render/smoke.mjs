import { chromium } from 'playwright-core';
const exe='/home/towfienes/.cache/ms-playwright/chromium-1248/chrome-linux64/chrome';
const b=await chromium.launch({executablePath:exe,args:['--no-sandbox']});
const p=await b.newPage();
await p.setContent('<h1 style="font-family:Times New Roman">SaigonBite smoke</h1>');
const buf=await p.pdf({format:'A4',printBackground:true,
  margin:{top:'35mm',bottom:'30mm',left:'35mm',right:'20mm'}});
console.log('PDF bytes:',buf.length);
await b.close();
