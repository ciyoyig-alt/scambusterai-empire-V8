from flask import Flask, request, jsonify
import re
from urllib.parse import urlparse

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>SCAMBUSTER AI V7</title>
<style>
body{background:#080810;color:#fff;font-family:system-ui;margin:0;padding:15px}
.header{text-align:center;padding:20px 0}
.logo{font-size:50px}
h1{color:#00ff88;margin:5px}
.card{background:#151520;border:1px solid #222;border-radius:22px;padding:20px;max-width:520px;margin:0 auto}
label{opacity:.7;font-size:13px}
textarea,input{width:100%;background:#0c0c14;border:1px solid #333;color:#fff;padding:15px;border-radius:14px;margin:8px 0 15px 0;box-sizing:border-box;font-size:16px}
.btn{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;font-weight:900;padding:16px;border-radius:14px;width:100%;border:none;font-size:19px}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:15px 0}
.small{background:#1e1e30;border:1px solid #333;color:#aaa;padding:12px;border-radius:12px;font-size:14px}
.circle{width:130px;height:130px;border-radius:50%;display:flex;align-items:center;justify-content:center;margin:25px auto;font-size:38px;font-weight:900;border:5px solid}
.flags{text-align:left;background:#0c0c14;padding:15px;border-radius:14px;border:1px solid #222;margin:10px 0}
.advice{margin-top:15px;padding:16px;border-radius:14px;font-weight:800;text-align:center;border:2px solid}
</style>
</head>
<body>
<div class="header">
<div class="logo">🛡️</div>
<h1>SCAMBUSTER AI V7</h1>
<div style="color:#00ff88;font-size:13px">🟢 LIVE • Empire Lubumbashi • Anti-Scam</div>
</div>
<div class="card">
<label>📩 MESSAGE SUSPECT</label>
<textarea id="msg" rows="3" placeholder="Colle message ici..."></textarea>
<label>🔗 LIEN</label>
<input id="link" placeholder="https://...">
<button class="btn" onclick="analyser()">🔍 ANALYSER</button>
<div class="grid">
<button class="small" onclick="setM('Je suis un prince nigerian heritage 2 millions $')">💰 Prince</button>
<button class="small" onclick="setM('Votre compte bancaire est bloque cliquez ici')">🏦 Banque</button>
<button class="small" onclick="setM('Felicitations vous avez gagne loterie 5000$!')">🎰 Loterie</button>
<button class="small" onclick="setM('Mon amour envoie moi argent urgent')">💘 Romance</button>
</div>
<div id="res" style="display:none;text-align:center">
<div id="circle" class="circle">0%</div>
<h2 id="status"></h2>
<div class="flags" id="flags"></div>
<div class="advice" id="advice"></div>
</div>
</div>
<script>
function setM(t){document.getElementById('msg').value=t}
async function analyser(){
 const m=document.getElementById('msg').value;
 const l=document.getElementById('link').value;
 const r=await fetch('/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m,link:l})});
 const d=await r.json();
 document.getElementById('res').style.display='block';
 const c=document.getElementById('circle');
 c.innerText=d.score+'%';
 if(d.score<30){c.style.borderColor='#00ff88';c.style.color='#00ff88'}
 else if(d.score<65){c.style.borderColor='orange';c.style.color='orange'}
 else{c.style.borderColor='#ff3b3b';c.style.color='#ff3b3b'}
 document.getElementById('status').innerText=d.status;
 document.getElementById('flags').innerHTML=d.flags.map(f=>'• '+f).join('<br>');
 document.getElementById('advice').innerText=d.advice;
 window.scrollTo(0,9999);
}
</script>
</body>
</html>
"""

def analyze_logic(message, link):
    msg = (message or "").lower()
    lnk = (link or "").lower()
    combined = msg + " " + lnk
    score = 7
    flags = []
    if any(x in combined for x in ["5000","10000","gagné","gagne","félicitations","felicitations","loterie","loto"]):
        score += 45; flags.append("Gain / Loterie: promesse d'argent facile")
    if any(x in combined for x in ["prince","nigeria","héritage","heritage","million"]):
        score += 55; flags.append("Arnaque Prince Nigérian")
    if any(x in combined for x in ["banque","bloqué","bloque","vérifiez","cliquez ici"]):
        score += 40; flags.append("Phishing bancaire")
    if any(x in combined for x in ["amour","chéri","envoie argent","romance"]):
        score += 35; flags.append("Arnaque sentimentale")
    if any(x in combined for x in ["crypto","bitcoin","usdt","investir"]):
        score += 30; flags.append("Escroquerie Crypto")
    if any(x in combined for x in ["urgent","24h","dernière chance"]):
        score += 15; flags.append("Pression urgence")
    if lnk:
        if any(s in lnk for s in ["vt.tiktok.com","bit.ly","tinyurl","t.me","wa.me"]):
            score += 35; flags.append(f"Lien raccourci: {lnk[:35]}")
        if len(lnk)>40: score+=10; flags.append("Lien long suspect")
    score = min(95, max(7, score))
    if score < 30:
        status="🟢 SÉCURISÉ"; badge="LOW"; advice="✅ Semble OK mais reste vigilant."
    elif score < 65:
        status="🟠 SUSPECT"; badge="SUSPECT"; advice="⚠️ Méfiance! Vérifie avant."
    else:
        status="🔴 DANGER ARNAQUE"; badge="HIGH"; advice="🚨 ARNAQUE probable! Ne clique PAS!"
    if not flags: flags=["Aucun mot-clé d'arnaque"]
    return score, status, badge, flags, advice

@app.route("/")
def home():
    return HTML_PAGE

@app.route("/analyze", methods=["POST"])
def api_analyze():
    data = request.get_json() or {}
    score, status, badge, flags, advice = analyze_logic(data.get("message",""), data.get("link",""))
    return jsonify({"score":score,"status":status,"badge":badge,"flags":flags,"advice":advice})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)