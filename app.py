from flask import Flask, request, jsonify
import re
from datetime import datetime
import os

app = Flask(__name__)

HTML = """<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0"><title>SCAMBUSTER AI V7</title><style>*{margin:0;padding:0;box-sizing:border-box}body{font-family:system-ui;background:#0a0a0f;color:#fff;min-height:100vh;padding:15px}.container{max-width:600px;margin:0 auto}.header{text-align:center;margin:20px 0}.logo{font-size:50px}h1{font-size:26px;background:linear-gradient(90deg,#00ff88,#00d4ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-weight:900}.subtitle{color:#888;margin-top:5px;font-size:12px}.card{background:#15151f;border:1px solid #222;border-radius:20px;padding:20px;margin:15px 0}label{color:#aaa;font-size:11px;text-transform:uppercase;display:block;margin-bottom:6px}textarea,input{width:100%;background:#0a0a0f;border:1px solid #333;border-radius:12px;padding:12px;color:#fff;font-size:15px;outline:none}textarea{height:110px;resize:none}.btn{width:100%;background:linear-gradient(90deg,#00ff88,#00d4ff);color:#000;border:none;border-radius:12px;padding:14px;font-size:17px;font-weight:900;cursor:pointer;margin-top:10px}.result{display:none;margin-top:20px}.result.show{display:block}.score-circle{width:110px;height:110px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:32px;font-weight:900;margin:0 auto 15px;border:4px solid}.score-red{border-color:#ff3344;background:rgba(255,51,68,.1);color:#ff3344}.score-orange{border-color:#ffaa00;background:rgba(255,170,0,.1);color:#ffaa00}.score-yellow{border-color:#ffdd00;background:rgba(255,221,0,.1);color:#ffdd00}.score-green{border-color:#00ff88;background:rgba(0,255,136,.1);color:#00ff88}.risk-text{text-align:center;font-size:20px;font-weight:800;margin-bottom:12px}.flags{display:flex;flex-wrap:wrap;gap:6px;justify-content:center;margin:12px 0}.flag{background:#222;border:1px solid #333;padding:5px 10px;border-radius:20px;font-size:10px;color:#aaa}.details{background:#0a0a0f;border-radius:12px;padding:12px;margin:12px 0}.detail-item{padding:6px 0;border-bottom:1px solid #1a1a2a;font-size:13px;color:#ccc}.advice{border-radius:12px;padding:12px;font-weight:600;text-align:center;margin-top:12px}.advice.red{background:rgba(255,51,68,.15);border:1px solid #ff3344;color:#ff8888}.advice.orange{background:rgba(255,170,0,.15);border:1px solid #ffaa00;color:#ffcc66}.advice.green{background:rgba(0,255,136,.15);border:1px solid #00ff88;color:#88ffaa}.footer{text-align:center;margin:30px 0;color:#555;font-size:11px}.examples{display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-top:10px}.example-btn{background:#1a1a2a;border:1px solid #333;color:#888;padding:8px;border-radius:8px;font-size:11px;cursor:pointer}</style></head><body><div class="container"><div class="header"><div class="logo">🛡️</div><h1>SCAMBUSTER AI V7</h1><div class="subtitle">🟢 LIVE • Empire Lubumbashi • Anti-Scam</div></div><div class="card"><div><label>📩 Message Suspect</label><textarea id="text" placeholder="Colle message ici... Ex: Félicitations vous avez gagné 5000$!"></textarea></div><div style="margin-top:12px"><label>🔗 Lien</label><input id="url" type="text" placeholder="https://..."></div><button class="btn" id="btn" onclick="analyze()">🔍 ANALYSER</button><div class="examples"><button class="example-btn" onclick="loadEx(0)">💰 Prince</button><button class="example-btn" onclick="loadEx(1)">🏦 Banque</button><button class="example-btn" onclick="loadEx(2)">🎰 Loterie</button><button class="example-btn" onclick="loadEx(3)">💘 Romance</button></div><div class="result" id="result"><div class="score-circle" id="circle">0%</div><div class="risk-text" id="risk"></div><div class="flags" id="flags"></div><div class="details" id="details"></div><div class="advice" id="advice"></div></div></div><div class="footer">SCAMBUSTER AI V7 © 2026 • ciyoyig-alt • Render LIVE</div></div><script>const ex=["Bonjour cher ami, Je suis Prince N'Golo du Mali, j'ai 15 Millions $ bloqués. Envoie ton compte IMMEDIATEMENT!!!","ALERTE: Votre compte Rawbank suspendu! Cliquez http://rawbank-secure.tk/verify - URGENT sinon blocage!","FELICITATIONS!!! Vous avez GAGNE 5000$ loterie WhatsApp! Cliquez bit.ly/win5000 - Offre expire AUJOURD'HUI!!!","Salut bébé c'est Jessica, soldat américain en Syrie, je t'aime. Besoin de 500$ via Western Union stp chéri ❤️"];function loadEx(i){document.getElementById('text').value=ex[i];}async function analyze(){const text=document.getElementById('text').value;const url=document.getElementById('url').value;if(!text&&!url){alert('Colle un message!');return;}const btn=document.getElementById('btn');btn.textContent='⏳ ANALYSE...';try{const res=await fetch('/api/analyze',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text,url})});const d=await res.json();const r=document.getElementById('result');r.classList.add('show');const c=document.getElementById('circle');c.textContent=d.score+'%';c.className='score-circle score-'+d.color;document.getElementById('risk').textContent=d.risk;document.getElementById('flags').innerHTML=d.flags.map(f=>`<span class=flag>🚩 ${f}</span>`).join('')||'✅ Aucun';document.getElementById('details').innerHTML=d.details.map(x=>`<div class=detail-item>• ${x}</div>`).join('');const a=document.getElementById('advice');a.textContent=d.advice;a.className='advice '+d.color;r.scrollIntoView({behavior:'smooth'});}catch(e){alert('Erreur');}btn.textContent='🔍 ANALYSER';}</script></body></html>"""

SCAM_PATTERNS = {
    'urgency': ['urgent','immediatement','immediate','now','asap','dernière chance','expire','bloqué','suspendu'],
    'money': ['gagné','won','lottery','loterie','héritage','inheritance','million','prince','donation','transfer','western union'],
    'phishing': ['cliquez','click here','verify','vérifiez','compte','password','banque','bank','paypal','binance'],
    'romance': ['amour','bébé','chéri','love you','military','soldat'],
    'crypto': ['invest','investissement','doubler','bitcoin','usdt','trading','profit garanti'],
}

def analyze_text(text):
    tl = text.lower()
    score = 0; flags=[]; details=[]
    if len(text) < 5:
        return {"score":0,"risk":"🟢 SÉCURISÉ","color":"green","flags":[],"details":["Trop court"]}
    for cat,kws in SCAM_PATTERNS.items():
        found=[k for k in kws if k in tl]
        if found:
            score+=len(found)*15; flags.append(cat.upper()); details.append(f"{cat}: {', '.join(found[:2])}")
    if re.search(r'\$\s?\d+|\d+\s?\$', text): score+=20; details.append("Montant $ détecté")
    if 'http' in tl or 'www.' in tl or 'bit.ly' in tl: score+=15; flags.append("LINK"); details.append("Lien suspect")
    score=min(score,100)
    if score>=75: risk,color="🔴 ARNAQUE ÉLEVÉE","red"
    elif score>=45: risk,color="🟠 SUSPECT","orange"
    elif score>=20: risk,color="🟡 ATTENTION","yellow"
    else: risk,color="🟢 SÉCURISÉ","green"
    return {"score":score,"risk":risk,"color":color,"flags":list(set(flags)),"details":details}

@app.route('/')
def index(): return HTML

@app.route('/api/analyze', methods=['POST'])
def analyze():
    data=request.get_json() or {}
    txt=data.get('text','')+' '+data.get('url','')
    r=analyze_text(txt)
    r['advice']="🚨 NE CLIQUE PAS! Bloque et signale." if r['score']>=75 else "⚠️ Méfie-toi, vérifie l'expéditeur." if r['score']>=45 else "✅ Semble OK mais reste vigilant."
    return jsonify(r)

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
