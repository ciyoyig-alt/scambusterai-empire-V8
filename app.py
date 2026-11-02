from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI(title="ScambusterAI Empire V9 ULTRA")

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ScambusterAI Empire V9 ULTRA</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#020208;color:#fff;font-family:system-ui}
.hero{min-height:100vh;display:flex;align-items:center;justify-content:center;background:radial-gradient(ellipse at center,#0a1930 0%,#020208 70%);padding:20px}
.content{text-align:center;max-width:1000px;width:100%}
.badge{padding:8px 20px;border:1px solid #00ff88;border-radius:50px;color:#00ff88;font-size:11px;letter-spacing:2px;margin-bottom:20px;display:inline-block}
h1{font-size:clamp(32px,6vw,72px);font-weight:900;line-height:0.9;margin-bottom:20px}
h1 span{background:linear-gradient(90deg,#00ff88,#00aaff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{color:#8892a0;margin-bottom:30px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:25px 0}
.stat{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:14px;padding:15px}
.num{font-size:22px;font-weight:800;color:#00ff88}
.label{font-size:9px;color:#8892a0;margin-top:4px}
.dashboard{margin-top:30px;background:rgba(10,10,20,0.9);border:1px solid rgba(0,255,136,0.2);border-radius:18px;padding:14px;text-align:left}
.flows{font-family:monospace;font-size:11px;line-height:1.8;color:#00ff88;height:120px;overflow:hidden}
.btns{margin-top:30px;display:flex;gap:10px;justify-content:center;flex-wrap:wrap}
.btn{padding:12px 24px;border-radius:50px;font-weight:700;text-decoration:none;font-size:12px}
.btn-primary{background:#00ff88;color:#000}
.btn-sec{background:rgba(255,255,255,0.06);color:#fff;border:1px solid rgba(255,255,255,0.2)}
.dot{width:6px;height:6px;background:#00ff88;border-radius:50%;display:inline-block;margin-right:6px}
</style>
</head>
<body>
<div class="hero">
<div class="content">
<div class="badge">● LIVE • LUBUMBASHI DRC • V9 ULTRA</div>
<h1>SCAMBUSTERAI<br><span>EMPIRE V9</span></h1>
<p class="sub">Real-time Fraud Defense + M-Pesa DRC + Banks + SWIFT Global • 150+ Countries</p>
<div class="stats">
<div class="stat"><div class="num">$12.4M</div><div class="label">USD TODAY</div></div>
<div class="stat"><div class="num">0.3s</div><div class="label">FRAUD SCAN</div></div>
<div class="stat"><div class="num">1,384</div><div class="label">ACTIVE FLOWS</div></div>
</div>
<div class="dashboard">
<div style="display:flex;justify-content:space-between;margin-bottom:10px"><span style="font-size:10px;letter-spacing:2px;font-weight:800">LIVE FEED</span><span style="color:#00ff88;font-size:10px"><span class="dot"></span>OPTIMAL • 12ms</span></div>
<div class="flows" id="flows"></div>
</div>
<div class="btns">
<a href="/docs" class="btn btn-primary">ENTER COMMAND CENTER →</a>
<a href="/docs" class="btn btn-sec">API DOCS</a>
</div>
<p style="margin-top:30px;color:#445;font-size:9px;letter-spacing:1px">RAWBANK • EQUITY BCDC • ACCESS • FBN • TMB • PAWAPAY • VISA DIRECT • SWIFT</p>
</div>
</div>
<script>
const flows=["MPESA +2,147,833 CDF • KINSHASA → LUBUMBASHI • SAFE","RAWBANK → +5.2M CDF • APPROVED • NOW","SWIFT → USD 42,300 LONDON • SETTLED","AI SCAN • +24381XXX • SCORE 94 BLOCKED FRAUD","BCDC → 1.8M CDF • SECURE CLEAR","MPESA +850K CDF KOLWEZI • SAFE","VISA DIRECT → EUR 18,900 PARIS ACTIVE","MPESA -120K CDF PAYOUT LUBUMBASHI"];
let i=0;
function addFlow(){
const el=document.getElementById('flows');
const div=document.createElement('div');
div.textContent='> '+flows[i%flows.length];
el.prepend(div);
if(el.children.length>7) el.removeChild(el.lastChild);
i++;
}
setInterval(addFlow,700);
addFlow();
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.get("/health")
def health():
    return {"status": "V9 ULTRA LIVE", "city": "Lubumbashi"}
