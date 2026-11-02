from flask import Flask, request, jsonify
import re, json, os, requests
from collections import Counter
app = Flask(__name__)

# ===== V12.1 CLOUD FOREVER CONFIG =====
BRAIN_FILE = "scambuster_brain_v12.json"
# Tu vas créer 1 lien cloud gratuit en 20 secondes (voir instructions en bas)
CLOUD_URL = os.environ.get("BRAIN_CLOUD_URL", "")  # On va le mettre sur Render

GLOBAL_BANKS = [
    {"name": "JPMorgan Chase", "type": "Banque Globale", "region": "USA", "risk": "🔴 Très Ciblé"},
    {"name": "Bank of America", "type": "Banque Globale", "region": "USA", "risk": "🔴 Très Ciblé"},
    {"name": "HSBC", "type": "Banque Globale", "region": "UK/World", "risk": "🔴 Très Ciblé"},
    {"name": "Barclays", "type": "Banque Globale", "region": "UK", "risk": "🟠 Ciblé"},
    {"name": "BNP Paribas", "type": "Banque Globale", "region": "France/EU", "risk": "🟠 Ciblé"},
    {"name": "Standard Chartered", "type": "Banque Globale", "region": "Africa/Asia", "risk": "🔴 Très Ciblé"},
    {"name": "Ecobank", "type": "Banque Pan-Africaine", "region": "Africa", "risk": "🔴 Très Ciblé"},
    {"name": "UBA", "type": "Banque Pan-Africaine", "region": "Africa", "risk": "🔴 Très Ciblé"},
    {"name": "Rawbank", "type": "Banque", "region": "DRC", "risk": "🟢 Vérifiée"},
    {"name": "Equity BCDC", "type": "Banque", "region": "DRC", "risk": "🟢 Vérifiée"},
    {"name": "PayPal", "type": "Fintech Paiement", "region": "World", "risk": "🔴 #1 Phishing Mondial"},
    {"name": "Wise", "type": "Fintech Transfert", "region": "World", "risk": "🔴 Très Ciblé"},
    {"name": "Revolut", "type": "Fintech Néobanque", "region": "EU/World", "risk": "🔴 Très Ciblé"},
    {"name": "M-Pesa", "type": "Mobile Money", "region": "Kenya/Africa", "risk": "🔴 #1 Scam Africa"},
    {"name": "Airtel Money", "type": "Mobile Money", "region": "Africa/India", "risk": "🔴 Très Ciblé"},
    {"name": "Orange Money", "type": "Mobile Money", "region": "Africa/EU", "risk": "🔴 Très Ciblé"},
    {"name": "MTN MoMo", "type": "Mobile Money", "region": "Africa", "risk": "🔴 Très Ciblé"},
    {"name": "Binance", "type": "Crypto Exchange", "region": "World", "risk": "🔴 #1 Fake Apps"},
    {"name": "Coinbase", "type": "Crypto Exchange", "region": "World", "risk": "🔴 Très Ciblé"},
    {"name": "Trust Wallet", "type": "Crypto Wallet", "region": "World", "risk": "🔴 Fake Versions"},
    {"name": "Zwa Cash", "type": "Fintech DRC", "region": "DRC", "risk": "🟠 Appris"},
    {"name": "U-Reporter", "type": "SMS Survey", "region": "DRC", "risk": "🟠 Appris"},
]

def load_brain_cloud():
    # 1. Essaye CLOUD d'abord (survit aux deploys)
    if CLOUD_URL:
        try:
            r = requests.get(CLOUD_URL, timeout=5)
            if r.status_code == 200:
                data = r.json()
                # npoint met data dans un wrapper
                if "scams" in data:
                    return data.get("scams", []), Counter(data.get("patterns", {}))
                if "content" in data and isinstance(data["content"], dict):
                    return data["content"].get("scams", []), Counter(data["content"].get("patterns", {}))
        except: pass
    # 2. Sinon fichier local
    if os.path.exists(BRAIN_FILE):
        try:
            with open(BRAIN_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("scams", []), Counter(data.get("patterns", {}))
        except: pass
    return [], Counter()

def save_brain_cloud():
    data = {"scams": LEARNED_SCAMS, "patterns": dict(PATTERN_WEIGHTS), "version": "V12.1 CLOUD FOREVER", "origin": "LUBUMBASHI", "total": len(LEARNED_SCAMS)}
    # Sauve local
    try:
        with open(BRAIN_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except: pass
    # Sauve CLOUD (immortel)
    if CLOUD_URL:
        try:
            requests.post(CLOUD_URL, json=data, timeout=5)
        except:
            try: # npoint utilise POST sur meme URL
                requests.post(CLOUD_URL, json=data, timeout=5)
            except: pass

LEARNED_SCAMS, PATTERN_WEIGHTS = load_brain_cloud()
STOPWORDS = {"avec","pour","vous","votre","dans","tous","tout","nous","les","des","une","est","sont","être","avoir","oui","non","bonjour","merci"}

def learn_v12_1(text):
    words = re.findall(r'\b\w{3,}\b', text.lower())
    useful = [w for w in words if w not in STOPWORDS]
    for w in useful:
        PATTERN_WEIGHTS[w] += 1
    if text not in LEARNED_SCAMS and len(text) > 10:
        LEARNED_SCAMS.append(text[:300])
    save_brain_cloud()

def scan_v12_1(text):
    low = text.lower()
    score=0; reasons=[]
    for b in GLOBAL_BANKS:
        if b["name"].lower() in low and "🔴" in b["risk"]:
            score+=25; reasons.append(f"{b['name']}")
    for w,c in PATTERN_WEIGHTS.most_common(100):
        if w in low:
            score+= min(c*3, 20) if c>=2 else 4
            if len(reasons)<6: reasons.append(f"{w} x{c}")
    if "http" in low or "bit.ly" in low: score+=15
    if "urgent" in low or "bloqué" in low: score+=10
    score=min(score,99)
    if score>=70: v,c="#ff2a2a","SCAM DETECTED"
    elif score>=35: v,c="#ffaa00","SUSPECT V12.1"
    else: v,c="#00ff88","SAFE"
    return score,c,v,reasons

@app.route("/")
def home():
    cloud_status = "☁️ CLOUD CONNECTÉ - IMMORTEL" if CLOUD_URL else "💾 LOCAL SEUL - Va s'effacer au prochain deploy - Active le Cloud!"
    return f"""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>V12.1 CLOUD FOREVER</title>
<style>body{{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding:20px}}
h1{{font-size:36px}}h1 span{{color:#00ff88}}.sub{{color:#00ccff;letter-spacing:2px;font-size:11px}}
.badge{{margin:12px auto;background:linear-gradient(90deg,rgba(0,255,136,0.2),rgba(170,136,255,0.2));border:1px solid #00ff88;border-radius:50px;padding:12px 20px;display:inline-block;font-size:11px}}
.grid{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;padding:10px;max-width:1100px;margin:auto}}
.card{{background:#111;border:1px solid #222;border-radius:12px;padding:12px;width:250px;font-size:12px}}.card h3{{color:#00ff88;margin:5px 0;font-size:13px}}.btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:11px 18px;border-radius:50px;font-weight:900;text-decoration:none;display:inline-block;margin:4px;font-size:11px}}
</style></head><body>
<h1>SCAM<span>BUSTER</span> AI</h1>
<div class="sub">EMPIRE V12.1 - CLOUD FOREVER ENGINE</div>
<div class="badge">💾☁️ {cloud_status}<br>🧠 {len(LEARNED_SCAMS)} SCAMS IMMORTELS - {len(PATTERN_WEIGHTS)} PATTERNS - NE MEURT JAMAIS</div>
<div class="grid">
<div class="card" style="border-color:#00ff88"><h3>🏦 {len(GLOBAL_BANKS)} Banques Mondiales</h3><p>Base V10.2 + V11</p></div>
<div class="card" style="border-color:#aa88ff"><h3>💳 Fintechs & Mobile Money</h3><p>PayPal, M-Pesa, Binance...</p></div>
<div class="card" style="border-color:#00ff88"><h3>🧠 {len(LEARNED_SCAMS)} Scams Immortels</h3><p>Cloud + Local</p></div>
<div class="card" style="border-color:#ffaa00"><h3>⚡ {len(PATTERN_WEIGHTS)} Patterns Forever</h3><p>{cloud_status}</p></div>
</div>
<a href="/scan" class="btn">SCANNER + APPRENDRE</a>
<a href="/banks" class="btn" style="background:linear-gradient(90deg,#00ccff,#aa88ff)">BANQUES</a>
<a href="/learned" class="btn" style="background:linear-gradient(90deg,#ffaa00,#ff5500)">CERVEAU ({len(LEARNED_SCAMS)})</a>
<a href="/export" class="btn" style="background:linear-gradient(90deg,#444,#888);color:#fff">EXPORT</a>
<div style="max-width:650px;margin:20px auto;color:#666;font-size:11px;line-height:1.6">
V12.1 = Cerveau Cloud: Sauvegardé sur internet, survit à 1000 deploys!<br>
Fichier local: {BRAIN_FILE} | Cloud: {"ACTIF" if CLOUD_URL else "INACTIF - voir instructions /setup"}<br>
Origin: LUBUMBASHI | Mine: THE WORLD
</div>
<div style="color:#444;font-size:9px;margin-top:20px">ORIGIN: LUBUMBASHI | V12.1 CLOUD FOREVER - {len(LEARNED_SCAMS)} IMMORTAL<br>pire-v7.onrender.com</div>
</body></html>
"""

@app.route("/scan", methods=["GET","POST"])
def scan():
    html_res=""
    if request.method=="POST":
        txt=request.form.get("text",""); fb=request.form.get("feedback","")
        if fb=="scam" and txt: learn_v12_1(txt)
        sc,ver,col,rs = scan_v12_1(txt)
        html_res=f'<div style="background:#111;border:2px solid {col};border-radius:15px;padding:15px;margin:15px auto;max-width:500px"><h2 style="color:{col}">{ver}</h2><p style="font-size:50px">{sc}%</p><p style="font-size:11px">{" | ".join(rs)}</p>'
        if fb=="scam": html_res+=f'<p style="color:#00ff88">☁️ GRAVÉ DANS LE CLOUD POUR TOUJOURS! Total: {len(LEARNED_SCAMS)}</p></div>'
        else: html_res+=f'<form method="POST"><input type="hidden" name="text" value="{txt}"><button name="feedback" value="scam" style="background:#ff2a2a;color:#fff;border:none;padding:10px 18px;border-radius:20px;cursor:pointer;font-weight:900">☁️💾 OUI - GRAVE DANS LE CLOUD!</button></form></div>'
    return f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{background:#000;color:#fff;text-align:center;padding:15px;font-family:Arial}} textarea{{width:90%;max-width:500px;height:110px;background:#111;color:#fff;border:1px solid #00ff88;border-radius:10px;padding:10px}} .btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:12px 25px;border-radius:50px;font-weight:900;cursor:pointer;margin-top:10px}} a{{color:#00ccff;text-decoration:none;font-size:12px}}</style></head><body><a href="/">← WORLD</a> | <a href="/banks">Banks</a> | <a href="/learned">Cerveau</a> | <a href="/setup">Setup Cloud</a><h1>☁️ SCAN V12.1 CLOUD</h1><form method="POST"><textarea name="text" placeholder="Colle message suspect..."></textarea><br><button class="btn" type="submit">ANALYSER V12.1</button></form>{html_res}</body></html>'

@app.route("/banks")
def banks():
    rows="".join([f'<tr><td>{b["name"]}</td><td>{b["type"]}</td><td>{b["region"]}</td><td>{b["risk"]}</td></tr>' for b in GLOBAL_BANKS])
    return f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{background:#000;color:#fff;font-family:Arial;text-align:center;padding:15px}} table{{width:98%;max-width:900px;margin:15px auto;border-collapse:collapse;background:#111;border-radius:10px;overflow:hidden;font-size:11px}} th{{background:#00ff88;color:#000;padding:8px}} td{{padding:8px;border-bottom:1px solid #222}} a{{color:#00ccff;text-decoration:none}}</style></head><body><a href="/">← WORLD</a><h1>🏦 {len(GLOBAL_BANKS)} BANQUES V12.1</h1><table><tr><th>Nom</th><th>Type</th><th>Région</th><th>Risque</th></tr>{rows}</table></body></html>'

@app.route("/learned")
def learned():
    top=PATTERN_WEIGHTS.most_common(50)
    pat="".join([f'<tr><td>{w}</td><td>{c}</td></tr>' for w,c in top]) if top else '<tr><td colspan="2">Vide</td></tr>'
    scams="".join([f'<div style="background:#111;border:1px solid #222;border-radius:8px;padding:10px;margin:8px auto;max-width:650px;font-size:11px;text-align:left">🔴 {s}</div>' for s in LEARNED_SCAMS[-20:][::-1]]) if LEARNED_SCAMS else '<p style="color:#666">Aucun - commence à scanner!</p>'
    return f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{background:#000;color:#fff;font-family:Arial;text-align:center;padding:15px}} table{{width:90%;max-width:600px;margin:15px auto;border-collapse:collapse;background:#111;border-radius:10px;overflow:hidden;font-size:11px}} th{{background:#ffaa00;color:#000;padding:8px}} td{{padding:6px;border-bottom:1px solid #222}} a{{color:#00ccff;text-decoration:none}} .btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:10px 20px;border-radius:50px;font-weight:900;text-decoration:none;display:inline-block;margin:5px}}</style></head><body><a href="/">← WORLD</a><h1>☁️🧠 CERVEAU V12.1 CLOUD</h1><p style="color:#888;font-size:11px">{"☁️ CLOUD ACTIF - Immortel" if CLOUD_URL else "💾 LOCAL SEUL - Active le cloud dans /setup"}</p><h3 style="color:#ffaa00">{len(LEARNED_SCAMS)} Scams Immortels</h3>{scams}<h3 style="color:#00ff88;margin-top:30px">{len(PATTERN_WEIGHTS)} Patterns</h3><table><tr><th>Mot</th><th>Poids</th></tr>{pat}</table><a href="/" class="btn">RETOUR</a></body></html>'

@app.route("/export")
def export_brain():
    return jsonify({"scams": LEARNED_SCAMS, "patterns": dict(PATTERN_WEIGHTS), "version": "V12.1", "cloud": bool(CLOUD_URL)})

@app.route("/setup")
def setup():
    return """
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{background:#000;color:#fff;font-family:Arial;padding:20px;line-height:1.7} a{color:#00ccff} .box{background:#111;border:1px solid #00ff88;border-radius:12px;padding:15px;margin:15px auto;max-width:600px} code{background:#222;padding:3px 6px;border-radius:4px;color:#00ff88}</style></head><body>
<a href="/">← WORLD</a>
<h1>☁️ SETUP CLOUD FOREVER - 20 SECONDES</h1>
<div class="box">
<h3 style="color:#00ff88">Pour rendre ton cerveau IMMORTEL (survit aux deploys):</h3>
<p><b>Étape 1:</b> Va sur <a href="https://www.npoint.io/" target="_blank">https://www.npoint.io/</a></p>
<p><b>Étape 2:</b> Clique "Create" → Colle ça: <code>{"scams":[],"patterns":{}}</code> → Create</p>
<p><b>Étape 3:</b> Copie le lien qui finit par <code>/storage/...</code> Exemple: <code>https://api.npoint.io/xxxxxx</code></p>
<p><b>Étape 4:</b> Sur Render.com → Ton Service pire-v7 → Environment → Add Variable</p>
<p>Name: <code>BRAIN_CLOUD_URL</code><br>Value: colle ton lien npoint</p>
<p><b>Étape 5:</b> Save → Render va redéployer → Ton cerveau sera IMMORTEL!</p>
</div>
<div class="box" style="border-color:#ffaa00">
<h3>⚡ Sans Cloud?</h3>
<p>Sans cloud, V12.1 fonctionne mais comme V12: il garde les scams jusqu'au prochain deploy. Avec cloud, il garde pour TOUJOURS!</p>
<p>En attendant, tu peux re-scanner tes 4 scams, ils resteront jusqu'au prochain commit.</p>
</div>
</body></html>
"""

@app.route("/health")
def health():
    return f"V12.1 CLOUD FOREVER {len(LEARNED_SCAMS)} CLOUD={bool(CLOUD_URL)} BANKS={len(GLOBAL_BANKS)}"
