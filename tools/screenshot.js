const {chromium}=require('playwright');
(async()=>{const [,,url,out,w,h,dark]=process.argv;const b=await chromium.launch();const p=await b.newPage({viewport:{width:+w||1280,height:+h||900},colorScheme:dark?'dark':'light'});
const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
await p.goto(url,{waitUntil:'load'});await p.evaluate(()=>document.querySelectorAll('.rv').forEach(e=>e.classList.add('in')));await p.waitForTimeout(1200);await p.screenshot({path:out,fullPage:process.env.FULL==='1'});
console.log(JSON.stringify({errs,title:await p.title(),overflow:await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth)}));await b.close()})();
