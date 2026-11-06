/* ---------- connect: standalone demo ----------
   The live Switch Board reads a private database that a scheduled sync fills
   from Gmail. This public copy swaps in a small in-browser store with sample
   data, so every button works and nothing leaves the visitor's browser. */
(async()=>{
  const KEY="sb-demo-v1";
  const iso=(d,h=10,m=0)=>{const x=new Date();x.setDate(x.getDate()+d);x.setHours(h,m,0,0);return x.toISOString()};
  const day=d=>{const x=new Date();x.setDate(x.getDate()+d);return new Date(x.getTime()-x.getTimezoneOffset()*60000).toISOString().slice(0,10)};
  const app=(id,company,role,status,applied,o={})=>({id,company,role,status,dateApplied:applied==null?"":day(applied),lastActivity:day(o.last??applied??0),platform:o.platform||"Company portal",cv:o.cv||"PM Core",poc:o.poc||{},referral:o.referral||"",link:"",nextStep:o.nextStep||"",nextDue:o.nextDue!=null?day(o.nextDue):"",notes:o.notes||"",history:[{date:day(applied??0),status,note:"Sample entry"}],outreach:o.outreach||[],rounds:o.rounds||[],flagged:!!o.flagged,flagNote:o.flagNote||"",source:"demo"});
  const seed=()=>({
    "apps/northwind":app("northwind","Northwind Pay","Product Manager, Merchant Growth","Interviewing",-12,{platform:"Referral",referral:"A. Mehta",cv:"PM Core",last:-1,rounds:[{id:"r1",title:"Round 2 · Hiring manager",start:iso(2,11),end:iso(2,12),mode:"Google Meet",with:"Hiring manager, Merchant team",prep:"Bring one metric you moved and how you would size the merchant opportunity.",status:"scheduled",sourceNote:"From the invite email"}]}),
    "apps/lumen":app("lumen","Lumen Health","Product Manager, Doctor Experience","Screening",-9,{platform:"Ashby",cv:"PM Core",last:-3,rounds:[{id:"r2",title:"Recruiter screen",start:iso(4,15,30),end:iso(4,16),mode:"Phone",with:"Talent partner",status:"scheduled",sourceNote:"From the invite email"}]}),
    "apps/kite":app("kite","Kite Labs","AI Product Manager","Assessment",-6,{platform:"Greenhouse",cv:"AI PM",last:-2,nextStep:"Submit take-home case",nextDue:1}),
    "apps/orbit":app("orbit","Orbit Commerce","Product Manager II","Applied",-10,{platform:"LinkedIn Easy Apply",cv:"PM Core",poc:{name:"Recruiter, Orbit",contact:"linkedin.com/in/example"}}),
    "apps/fern":app("fern","Fern Learning","Product Manager, Consumer","Applied",-23,{platform:"Lever",cv:"PM Core"}),
    "apps/quill":app("quill","Quill Docs","Associate Product Manager","Applied",-3,{platform:"Workable",cv:"AI PM"}),
    "apps/harbor":app("harbor","Harbor Freight Tech","Platform PM","Referral asked",null,{nextStep:"Send CV and referral details",nextDue:0,referral:"Friend at Harbor"}),
    "apps/pebble":app("pebble","Pebble Games","Product Manager, Economy","Rejected",-30,{platform:"Company portal",cv:"PM Core",last:-14}),
    "apps/atlas":app("atlas","Atlas Travel","Product Manager, Hotels","Interviewing",-15,{platform:"Referral",referral:"Ex-colleague",cv:"PM Core",last:-2,flagged:true,flagNote:"Sync moved this to Interviewing from a scheduling email",rounds:[{id:"r3",title:"Round 1 · Product sense",start:iso(-2,14),end:iso(-2,15),mode:"MS Teams",with:"Senior PM",status:"done",outcome:"Cleared to next round"}]}),
    "apps/cinder":app("cinder","Cinder Analytics","Product Manager","Ghosted",-35,{platform:"Job board",cv:"AI PM",last:-34}),
    "jobs/j1":{id:"j1",company:"Vela Money",title:"Product Manager, Payments",location:"Bengaluru",source:"Greenhouse",postedAt:iso(0,7),fit:82,fitWhy:"Product company, consumer payments, Bengaluru",url:"",status:"new"},
    "jobs/j2":{id:"j2",company:"Quill Docs",title:"Product Manager, AI Search",location:"Remote, India",source:"Ashby",postedAt:iso(0,5),fit:78,fitWhy:"AI-core B2B SaaS, remote India",url:"",status:"new",watchlist:true},
    "jobs/j3":{id:"j3",company:"Brightline",title:"Senior Product Manager",location:"Gurugram",source:"LinkedIn alert",postedAt:iso(-1,9),fit:61,fitWhy:"Platform role; asks 6+ years",url:"",status:"new"},
    "jobs/j4":{id:"j4",company:"Meridian Consulting",title:"Forward Deployed PM",location:"Mumbai",source:"hirist",postedAt:iso(0,3),fit:28,fitWhy:"Consulting-style and forward-deployed: scored down",url:"",status:"new",excluded:true},
    "jobs/j5":{id:"j5",company:"Tinker",title:"Product Manager, Creator Tools",location:"Bengaluru",source:"Lever",postedAt:iso(-2,12),fit:74,fitWhy:"Consumer product company",url:"",status:"new"},
    "watchlist/quill-docs":{id:"quill-docs",name:"Quill Docs",tier:"A"},
    "watchlist/vela-money":{id:"vela-money",name:"Vela Money",tier:"A"},
    "poc/p1":{id:"p1",target:"app:orbit",label:"Orbit Commerce · Product Manager II",status:"done",requestedAt:iso(-4),results:[{name:"Group PM, Checkout",title:"Named on the team page",confidence:"Likely",why:"Leads the team this role sits in"}],draft:"Hi, I applied for the PM II role on your team last week. I have shipped a self-serve tool that cut a support lookup from hours to minutes and would love ten minutes to learn what the team is solving next."},
    "applyq/q1":{id:"q1",company:"Vela Money",title:"Product Manager, Payments",ats:"Greenhouse",location:"Bengaluru",fit:82,cv:"PM Core",status:"review",reason:"Has two written questions",answers:[{q:"Why Vela?",a:"Draft answer goes here for review."},{q:"Tell us about a product you shipped end to end.",a:"Draft answer goes here for review."}]},
    "applyq/q2":{id:"q2",company:"Tinker",title:"Product Manager, Creator Tools",ats:"Lever",fit:74,cv:"PM Core",status:"drafted",reason:"No written questions; goes out at the next sync"},
    "meta/sync":{lastRun:iso(0,new Date().getHours()-2),summary:"Sample data",nextRun:iso(0,new Date().getHours()+4)}
  });
  let store;
  try{store=JSON.parse(localStorage.getItem(KEY)||"null")}catch(_){store=null}
  if(!store)store=seed();
  const save=()=>{try{localStorage.setItem(KEY,JSON.stringify(store))}catch(_){}};
  const subs=new Set();
  const emit=()=>{save();subs.forEach(f=>f())};
  const clone=o=>JSON.parse(JSON.stringify(o));
  const docRef=path=>({
    async set(v){store[path]=clone(v);emit()},
    async update(p){store[path]={...(store[path]||{}),...clone(p)};emit()},
    async delete(){delete store[path];emit()},
    onSnapshot(cb){const f=()=>cb({exists:path in store,data:()=>clone(store[path])});subs.add(f);f();return()=>subs.delete(f)}
  });
  const colDocs=col=>Object.keys(store).filter(k=>k.startsWith(col+"/")&&!k.slice(col.length+1).includes("/")).map(k=>({id:k.slice(col.length+1),data:()=>clone(store[k])}));
  db={
    doc:docRef,
    collection:col=>({doc:id=>docRef(col+"/"+id),onSnapshot(cb){const f=()=>cb({docs:colDocs(col)});subs.add(f);f();return()=>subs.delete(f)}})
  };
  state.uid="demo";
  $("banner").innerHTML=`<div class="banner">Demo with sample data. The real board fills itself from Gmail three times a day; this copy keeps your changes in your browser only. <button class="btn sm" type="button" id="resetDemo" style="margin-left:8px">Reset sample data</button></div>`;
  document.getElementById("resetDemo").onclick=()=>{store=seed();emit();toast("Sample data reset")};
  const sub=(path,key)=>db.collection(path).onSnapshot(s=>{state[key]=s.docs.map(d=>({id:d.id,...d.data()}));render()});
  sub("apps","apps");sub("jobs","jobs");sub("watchlist","watch");sub("poc","poc");sub("applyq","applyq");
  profRef().onSnapshot(s=>{state.profile=s.exists?s.data():null;state.profileLoaded=true;renderApply()});
  db.doc("meta/sync").onSnapshot(s=>{state.meta=s.exists?s.data():null;renderSync()});
})();
})();
</script>
<p style="text-align:center;font:12px var(--f-body,sans-serif);color:var(--muted,#5B6B65);padding:0 16px 32px">Built by <a href="/">Shouvik Sarkar</a> · <a href="/#projects">More projects</a></p>
</body></html>
