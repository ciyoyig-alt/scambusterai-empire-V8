from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

ULTRA_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ScambusterAI Empire V9 ULTRA | Lubumbashi DRC</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#020208;color:#fff;font-family:system-ui;overflow-x:hidden}
.hero{min-height:100vh;position:relative;background:radial-gradient(ellipse at center,#0a1930 0%,#020208 70%);display:flex;align-items:center;justify-content:center}
.content{position:relative;z-index:2;text-align:center;max-width:1200px;padding:20px}
.badge{display:inline-block;padding:8px 20px;border:1px solid #00ff88;border-radius:50px;color:#00ff88;font-size:11px;letter-spacing:2px;margin-bottom:20px;box-shadow:0 0 20px rgba(0,255,136,0.3)}
h1{font-size:clamp(32px,6vw,84px);font-weight:900;line-height:0.9;letter-spacing:-2px;margin-bottom:20px}
h1 span{background:linear-gradient(90deg,#00ff88,#00aaff);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.sub{font-size:clamp(14px,2vw,18px);color:#8892a0;margin-bottom:30px}
.stats{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:30px 0}
.stat{background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.1);border-radius:16px;padding:18px}
.stat .num{font-size:24px;font-weight:800;color:#00ff88}
.stat .label{font-size:10px;color:#8892a0;letter-spacing:1px;margin-top:4px}
.dashboard{margin-top:40px;background:rgba(10,10,20,0.8);border:1px solid rgba(0,255,136,0.2);border-radius:20px;padding:16px;text-align:left}
.flows{font-family:monospace;font-size:12px;line-height:2;color:#00ff88;height:140px;overflow:hidden}
.flow{margin-bottom:2px}
.btns{display:flex;gap:12px;justify-content:center;margin-top:30px;flex-wrap:wrap}
.btn{padding:14px 28px;border-radius:50px;font-weight:700;text-decoration:none;font-size:13px}
.btn-primary{background:#00ff88;color:#000;box-shadow:0 0 30px rgba(0,255,136,0.4)}
.btn-sec{background:rgba(255,255,255,0.06);color:#fff;border:1px solid rgba(255,255,255,0.2)}
.live{color:#00ff88;display:flex;align-items:center;gap:6px;font-size:11px}
.dot{width:7px;height:7px;background:#00ff88;border-radius:50%;animation:blink 1s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}
</style>
</head>
<body>
<div class="hero">
<div class="content">
<div class="badge">● LIVE • LUBUMBASHI DRC • V9 ULTRA • ONLINE</div>
<h1>SCAMBUSTERAI<br><span>EMPIRE V9</span></h1>
<p class="sub">Real-time Fraud Defense + M-Pesa DRC + 5 Banks + SWIFT Global<br>150+ Countries • Built in Lubumbashi</p>
<div class="stats">
<div class="stat"><div class="num" id="t1">$12.4M</div><div class="label">USD TODAY</div></div>
<div class="stat"><div class="num">0.3s</div><div class="label">FRAUD SCAN</div></div>
<div class="stat"><div class="num">1,384</div><div class="label">ACTIVE FLOWS</div></div>
</div>
<div class="dashboard">
<div style="display:flex;justify-content:space-between;margin-bottom:12px"><span style="font-weight:800;font-size:11px;letter-spacing:2px">LIVE FEED</span><span class="live"><span class="dot"></span>OPTIMAL • 12ms</span></div>
<div class="flows" id="flows"></div>
</div>
<div class="btns">
<a href="/docs" class="btn btn-primary">ENTER COMMAND CENTER →</a>
<a href="/docs" class="btn btn-sec">API DOCS</a>
</div>
<p style="margin-top:40px;color:#445;font-size:10px;letter-spacing:2px">RAWBANK • EQUITY BCDC • ACCESS • FBN • TMB • PAWAPAY • VISA DIRECT • SWIFT</p>
<p style="margin-top:10px;color:#223;font-size:9px">scambusterai-empire-v7.onrender.com • EST. 2024 LUBUMBASHI</p>
</div>
</div>
<script>
const flows=["MPESA +2,147,833 CDF • KINSHASA → LUBUMBASHI • 0.2s AGO • SAFE","RAWBANK → +5.2M CDF • COMMERCIAL • APPROVED • NOW","SWIFT → USD 42,300 • LONDON • SETTLED","AI SCAN • +24381XXXXXXX • SCORE 94/100 • BLOCKED • FRAUD","BCDC → 1.8M CDF • SECURE • 0.3s SCAN: CLEAR","MPESA +850K CDF • KOLWEZI • 0.5s AGO • SAFE","VISA DIRECT → EUR 18,900 PARIS • ACTIVE","MPESA -120K CDF • PAYOUT • LUBUMBASHI • 1.1s AGO"];
let i=0;
function addFlow(){
const el=document.getElementById('flows');
const div=document.createElement('div');
div.className='flow';
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
    return ULTRA_HTML

@app.get("/health")
def health():
    return {"status": "V9 ULTRA LIVE", "location": "Lubumbashi DRC", "flows": 1384}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=10000)
