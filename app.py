from flask import Flask, request, jsonify
import re, json, os
from collections import Counter
app = Flask(__name__)

# ===== FICHIER CERVEAU PERMANENT V12 =====
BRAIN_FILE = "scambuster_brain_v12.json"

GLOBAL_BANKS = [
    {"name": "JPMorgan Chase", "type": "Banque Globale", "region": "USA", "risk": "🔴 Très Ciblé"},
    {"name": "Bank of America", "type": "Banque Globale", "region": "USA", "risk": "🔴 Très Ciblé"},
    {"name": "HSBC", "type": "Banque Globale", "region": "UK/World", "risk": "🔴 Très Ciblé"},
    {"name": "Barclays", "type": "Banque Globale", "region": "UK", "risk": "🟠 Ciblé"},
    {"name": "BNP Paribas", "type": "Banque Globale", "region": "France/EU", "risk": "🟠 Ciblé"},
    {"name": "Deutsche Bank", "type": "Banque Globale", "region": "Germany", "risk": "🟠 Ciblé"},
    {"name": "Standard Chartered", "type": "Banque Globale", "region": "Africa/Asia", "risk": "🔴 Très Ciblé"},
    {"name": "Ecobank", "type": "Banque Pan-Africaine", "region": "Africa", "risk": "🔴 Très Ciblé"},
    {"name": "UBA", "type": "Banque Pan-Africaine", "region": "Africa", "risk": "🔴 Très Ciblé"},
    {"name": "Rawbank", "type": "Banque", "region": "DRC", "risk": "🟢 Vérifiée"},
    {"name": "Equity BCDC", "type": "Banque", "region": "DRC", "risk": "🟢 Vérifiée"},
    {"name": "KCB Bank", "type": "Banque", "region": "East Africa", "risk": "🟠 Ciblé"},
    {"name": "First Bank Nigeria", "type": "Banque", "region": "Nigeria", "risk": "🔴 Très Ciblé"},
    {"name": "PayPal", "type": "Fintech Paiement", "region": "World", "risk": "🔴 #1 Phishing Mondial"},
    {"name": "Wise", "type": "Fintech Transfert", "region": "World", "risk": "🔴 Très Ciblé"},
    {"name": "Revolut", "type": "Fintech Néobanque", "region": "EU/World", "risk": "🔴 Très Ciblé"},
    {"name": "Venmo", "type": "Fintech Paiement", "region": "USA", "risk": "🟠 Ciblé"},
    {"name": "Cash App", "type": "Fintech Paiement", "region": "USA", "risk": "🔴 Très Ciblé"},
    {"name": "Zelle", "type": "Fintech Paiement", "region": "USA", "risk": "🔴 Très Ciblé"},
    {"name": "Payoneer", "type": "Fintech Freelance", "region": "World", "risk": "🔴 Très Ciblé"},
    {"name": "M-Pesa", "type": "Mobile Money", "region": "Kenya/Africa", "risk": "🔴 #1 Scam Africa"},
    {"name": "Airtel Money", "type": "Mobile Money", "region": "Africa/India", "risk": "🔴 Très Ciblé"},
    {"name": "Orange Money", "type": "Mobile Money", "region": "Africa/EU", "risk": "🔴 Très Ciblé"},
    {"name": "MTN MoMo", "type": "Mobile Money", "region": "Africa", "risk": "🔴 Très Ciblé"},
    {"name": "Wave", "type": "Mobile Money", "region": "West Africa", "risk": "🟠 Ciblé"},
    {"name": "GCash", "type": "Mobile Money", "region": "Philippines", "risk": "🔴 Très Ciblé"},
    {"name": "Paytm", "type": "Mobile Money", "region": "India", "risk": "🔴 Très Ciblé"},
    {"name": "Binance", "type": "Crypto Exchange", "region": "World", "risk": "🔴 #1 Fake Apps"},
    {"name": "Coinbase", "type": "Crypto Exchange", "region": "World", "risk": "🔴 Très Ciblé"},
    {"name": "Trust Wallet", "type": "Crypto Wallet", "region": "World", "risk": "🔴 Fake Versions"},
    {"name": "MetaMask", "type": "Crypto Wallet", "region": "World", "risk": "🔴 Très Ciblé"},
    {"name": "Kraken", "type": "Crypto Exchange", "region": "World", "risk": "🟠 Ciblé"},
    {"name": "Tether USDT", "type": "Crypto Stablecoin", "region": "World", "risk": "🔴 Fake Airdrops"},
    {"name": "Zwa Cash", "type": "Fintech DRC", "region": "DRC", "risk": "🟠 Nouveau - Appris"},
    {"name": "U-Reporter", "type": "SMS Survey", "region": "DRC", "risk": "🟠 Nouveau - Appris"},
]

# ===== V12 CERVEAU PERMANENT =====
def load_brain():
    if os.path.exists(BRAIN_FILE):
        try:
            with open(BRAIN_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("scams", []), Counter(data.get("patterns", {}))
        except: pass
    return [], Counter()

def save_brain():
    try:
        with open(BRAIN_FILE, "w", encoding="utf-8") as f:
            json.dump({"scams": LEARNED_SCAMS, "patterns": dict(PATTERN_WEIGHTS)}, f, ensure_ascii=False, indent=2)
    except: pass

LEARNED_SCAMS, PATTERN_WEIGHTS = load_brain()

STOPWORDS = {"avec","pour","vous","votre","dans","tous","tout","nous","les","des","une","est","sont","être","avoir","oui","non","bonjour","merci","veuillez"}

def learn_v12(text):
    words = re.findall(r'\b\w{3,}\b', text.lower())
    useful = [w for w in words if w not in STOPWORDS and len(w) > 2]
    for w in useful:
        PATTERN_WEIGHTS[w] += 1
    if text not in LEARNED_SCAMS and len(text) > 10:
        LEARNED_SCAMS.append(text[:300])
    save_brain()

def scan_v12(text):
    low = text.lower()
    score = 0
    reasons = []
    for b in GLOBAL_BANKS:
        if b["name"].lower() in low:
            if "🔴" in b["risk"]:
                score += 25
                reasons.append(f"{b['name']} impersonation")
    for w, c in PATTERN_WEIGHTS.most_common(100):
        if w in low and c >= 1:
            add = min(c*3, 20) if c>=2 else 5
            score += add
            if len(reasons) < 5:
                reasons.append(f"Learned: {w} x{c}")
    if "http://" in low or "bit.ly" in low or "t.me" in low: score+=15; reasons.append("Lien suspect")
    if "urgent" in low or "bloqué" in low or "remboursez" in low: score+=10
    score = min(score, 99)
    if score >= 70: verdict, color = "SCAM DETECTED", "#ff2a2a"
    elif score >= 35: verdict, color = "SUSPECT - AI V12", "#ffaa00"
    else: verdict, color = "SAFE - AI Vérifié", "#00ff88"
    return score, verdict, color, reasons

@app.route("/")
def home():
    return f"""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>V12 MEMORY FOREVER</title>
<style>body{{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding:20px}}
h1{{font-size:36px}}h1 span{{color:#00ff88}}.sub{{color:#00ccff;letter-spacing:2px;font-size:11px}}
.badge{{margin:12px auto;background:linear-gradient(90deg,rgba(0,255,136,0.2),rgba(170,136,255,0.2));border:1px solid #00ff88;border-radius:50px;padding:12px 20px;display:inline-block;font-size:11px;animation:pulse 2s infinite}}@keyframes pulse{{0%,100%{{box-shadow:0 0 15px #00ff88}}50%{{box-shadow:0 0 30px #aa88ff}}}}
.grid{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;padding:10px;max-width:1100px;margin:auto}}
.card{{background:#111;border:1px solid #222;border-radius:12px;padding:12px;width:250px;font-size:12px}}.card h3{{color:#00ff88;margin:5px 0;font-size:13px}}.btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:11px 18px;border-radius:50px;font-weight:900;text-decoration:none;display:inline-block;margin:4px;font-size:11px}}
.footer{{margin-top:30px;padding:12px;color:#444;font-size:9px;border-top:1px solid #111}}
</style></head><body>
<h1>SCAM<span>BUSTER</span> AI</h1>
<div class="sub">EMPIRE V12 - MEMORY FOREVER ENGINE</div>
<div class="badge">💾🧠 MEMORY FOREVER - {len(LEARNED_SCAMS)} SCAMS GRAVÉS - {len(PATTERN_WEIGHTS)} PATTERNS - N'OUBLIE JAMAIS</div>
<div class="grid">
<div class="card" style="border-color:#00ff88"><h3>🏦 {len(GLOBAL_BANKS)} Banques Mondiales</h3><p>Base V10.2 + V11</p></div>
<div class="card" style="border-color:#aa88ff"><h3>💳 Fintechs & Mobile Money</h3><p>PayPal, M-Pesa, Binance...</p></div>
<div class="card" style="border-color:#00ff88"><h3>🧠 {len(LEARNED_SCAMS)} Scams Gravés</h3><p>Mémoire permanente</p></div>
<div class="card" style="border-color:#ffaa00"><h3>⚡ {len(PATTERN_WEIGHTS)} Patterns Forever</h3><p>Sauvegardé sur disque</p></div>
</div>
<a href="/scan" class="btn">SCANNER + APPRENDRE</a>
<a href="/banks" class="btn" style="background:linear-gradient(90deg,#00ccff,#aa88ff)">BANQUES</a>
<a href="/learned" class="btn" style="background:linear-gradient(90deg,#ffaa00,#ff5500)">CERVEAU ({len(LEARNED_SCAMS)})</a>
<a href="/export" class="btn" style="background:linear-gradient(90deg,#444,#888);color:#fff">EXPORT CERVEAU</a>
<div style="max-width:650px;margin:20px auto;color:#666;font-size:11px;line-height:1.6">
V9 WORLD → V10.2 37 Banks → V11 Auto-Learning → <b style="color:#00ff88">V12 MEMORY FOREVER - Le cerveau est gravé dans un fichier et ne meurt jamais!</b><br>
Fichier: {BRAIN_FILE} | Origin: LUBUMBASHI | Mine: THE WORLD
</div>
<div class="footer">ORIGIN: LUBUMBASHI, DRC | MINE: THE WORLD | V12 MEMORY FOREVER - {len(LEARNED_SCAMS)} PERMANENT<br>pire-v7.onrender.com</div>
</body></html>
"""

@app.route("/scan", methods=["GET","POST"])
def scan():
    html_res=""
    if request.method=="POST":
        txt=request.form.get("text","")
        fb=request.form.get("feedback","")
        if fb=="scam" and txt:
            learn_v12(txt)
        sc, ver, col, rs = scan_v12(txt)
        html_res=f'<div style="background:#111;border:2px solid {col};border-radius:15px;padding:15px;margin:15px auto;max-width:500px"><h2 style="color:{col}">{ver}</h2><p style="font-size:50px;margin:5px">{sc}%</p><p style="font-size:11px">{" | ".join(rs) if rs else "Analyse V12"}</p>'
        if fb=="scam":
            html_res+=f'<p style="color:#00ff88">💾 GRAVÉ POUR TOUJOURS! Total: {len(LEARNED_SCAMS)} | Patterns: {len(PATTERN_WEIGHTS)}</p></div>'
        else:
            html_res+=f'<form method="POST"><input type="hidden" name="text" value="{txt}"><p style="font-size:12px;color:#888">C etait un scam? Grave le pour toujours!</p><button name="feedback" value="scam" style="background:#ff2a2a;color:#fff;border:none;padding:10px 18px;border-radius:20px;cursor:pointer;font-weight:900">💾 OUI - GRAVE DANS LE CERVEAU!</button> <button name="feedback" value="safe" style="background:#222;color:#fff;border:1px solid #444;padding:8px 15px;border-radius:20px">Non</button></form></div>'
    return f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{background:#000;color:#fff;text-align:center;padding:15px;font-family:Arial}} textarea{{width:90%;max-width:500px;height:110px;background:#111;color:#fff;border:1px solid #00ff88;border-radius:10px;padding:10px}} .btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:12px 25px;border-radius:50px;font-weight:900;cursor:pointer;margin-top:10px}} a{{color:#00ccff;text-decoration:none;font-size:12px}}</style></head><body><a href="/">← WORLD</a> | <a href="/banks">Banks</a> | <a href="/learned">Cerveau</a><h1>💾 SCAN V12 FOREVER</h1><p style="font-size:11px;color:#888">Scanne et grave pour toujours dans le cerveau</p><form method="POST"><textarea name="text" placeholder="Colle message suspect..."></textarea><br><button class="btn" type="submit">ANALYSER V12</button></form>{html_res}</body></html>'

@app.route("/banks")
def banks():
    rows="".join([f'<tr><td>{b["name"]}</td><td>{b["type"]}</td><td>{b["region"]}</td><td>{b["risk"]}</td></tr>' for b in GLOBAL_BANKS])
    return f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{background:#000;color:#fff;font-family:Arial;text-align:center;padding:15px}} table{{width:98%;max-width:900px;margin:15px auto;border-collapse:collapse;background:#111;border-radius:10px;overflow:hidden;font-size:11px}} th{{background:#00ff88;color:#000;padding:8px}} td{{padding:8px;border-bottom:1px solid #222}} a{{color:#00ccff;text-decoration:none}} .btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:10px 20px;border-radius:50px;font-weight:900;text-decoration:none;display:inline-block;margin:5px}}</style></head><body><a href="/">← WORLD</a><h1>🏦 {len(GLOBAL_BANKS)} BANQUES + FINTECHS V12</h1><table><tr><th>Nom</th><th>Type</th><th>Région</th><th>Risque</th></tr>{rows}</table><a href="/" class="btn">RETOUR WORLD</a></body></html>'

@app.route("/learned")
def learned():
    top=PATTERN_WEIGHTS.most_common(50)
    pat="".join([f'<tr><td>{w}</td><td>{c} fois</td></tr>' for w,c in top]) if top else '<tr><td colspan="2">Cerveau vide - commence!</td></tr>'
    scams="".join([f'<div style="background:#111;border:1px solid #222;border-radius:8px;padding:10px;margin:8px auto;max-width:650px;font-size:11px;text-align:left">🔴 {s}</div>' for s in LEARNED_SCAMS[-20:][::-1]]) if LEARNED_SCAMS else '<p style="color:#666">Aucun scam gravé</p>'
    return f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{background:#000;color:#fff;font-family:Arial;text-align:center;padding:15px}} table{{width:90%;max-width:600px;margin:15px auto;border-collapse:collapse;background:#111;border-radius:10px;overflow:hidden;font-size:11px}} th{{background:#ffaa00;color:#000;padding:8px}} td{{padding:6px;border-bottom:1px solid #222}} a{{color:#00ccff;text-decoration:none}} .btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:10px 20px;border-radius:50px;font-weight:900;text-decoration:none;display:inline-block;margin:5px}}</style></head><body><a href="/">← WORLD</a> | <a href="/scan">Scan</a> | <a href="/banks">Banks</a><h1>💾🧠 CERVEAU V12 FOREVER</h1><p style="color:#888;font-size:11px">Mémoire permanente - Fichier: {BRAIN_FILE}</p><h3 style="color:#ffaa00">{len(LEARNED_SCAMS)} Scams Gravés pour Toujours</h3>{scams}<h3 style="color:#00ff88;margin-top:30px">{len(PATTERN_WEIGHTS)} Patterns Forever</h3><table><tr><th>Mot Suspect Gravé</th><th>Poids</th></tr>{pat}</table><p style="color:#444;font-size:10px;margin-top:20px">ORIGIN: LUBUMBASHI | MINE: THE WORLD | V12 MEMORY FOREVER</p><a href="/" class="btn">RETOUR WORLD</a></body></html>'

@app.route("/export")
def export_brain():
    return jsonify({"scams": LEARNED_SCAMS, "patterns": dict(PATTERN_WEIGHTS), "total_banks": len(GLOBAL_BANKS), "version": "V12 MEMORY FOREVER", "origin": "LUBUMBASHI"})

@app.route("/health")
def health():
    return f"V12 MEMORY FOREVER {len(LEARNED_SCAMS)} PERMANENT {len(PATTERN_WEIGHTS)} PATTERNS {len(GLOBAL_BANKS)} BANKS"
