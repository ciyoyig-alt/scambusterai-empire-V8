from flask import Flask, request
import re
from collections import Counter
app = Flask(__name__)

# ===== V10.2 BASE - 37 GLOBAL BANKS =====
GLOBAL_BANKS_FINTECHS = [
    {"name": "JPMorgan Chase", "type": "Banque Globale", "region": "USA", "risk": "🔴 Très Ciblé"},
    {"name": "Bank of America", "type": "Banque Globale", "region": "USA", "risk": "🔴 Très Ciblé"},
    {"name": "HSBC", "type": "Banque Globale", "region": "UK/World", "risk": "🔴 Très Ciblé"},
    {"name": "Barclays", "type": "Banque Globale", "region": "UK", "risk": "🟠 Ciblé"},
    {"name": "BNP Paribas", "type": "Banque Globale", "region": "France/EU", "risk": "🟠 Ciblé"},
    {"name": "Deutsche Bank", "type": "Banque Globale", "region": "Germany", "risk": "🟠 Ciblé"},
    {"name": "Santander", "type": "Banque Globale", "region": "Spain/Latam", "risk": "🟠 Ciblé"},
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
    {"name": "Skrill", "type": "Fintech", "region": "World", "risk": "🟠 Ciblé"},
    {"name": "Neteller", "type": "Fintech", "region": "World", "risk": "🟠 Ciblé"},
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
    {"name": "KuCoin", "type": "Crypto Exchange", "region": "World", "risk": "🟠 Ciblé"},
    {"name": "Tether USDT", "type": "Crypto Stablecoin", "region": "World", "risk": "🔴 Fake Airdrops"},
]

# ===== V11 AUTO-LEARNING MEMORY - Le cerveau qui grandit tout seul =====
LEARNED_SCAMS = []  # Le monde va enseigner à ton AI
PATTERN_WEIGHTS = Counter()  # Poids auto-appris

def learn_from_text(text, is_scam=True):
    """AUTO-LEARNING: Quand le monde signale un scam, l'AI apprend"""
    words = re.findall(r'\b\w+\b', text.lower())
    # Mots suspects auto-appris
    for w in words:
        if len(w) > 3 and is_scam:
            PATTERN_WEIGHTS[w] += 1
    if is_scam and len(text) > 10:
        LEARNED_SCAMS.append(text[:200])
        if len(LEARNED_SCAMS) > 100:  # Garde les 100 derniers
            LEARNED_SCAMS.pop(0)

def scan_engine_v11(text):
    text_low = text.lower()
    score = 0
    reasons = []
    
    # 1. Base 37 banques mondiales (V10.2)
    for bank in GLOBAL_BANKS_FINTECHS:
        if bank["name"].lower() in text_low and "🔴" in bank["risk"]:
            score += 25
            reasons.append(f"Impersonation: {bank['name']}")

    # 2. AUTO-LEARNING - Mots que le monde a appris à l'AI
    for word, weight in PATTERN_WEIGHTS.most_common(50):
        if word in text_low and weight >= 2:
            score += min(weight * 2, 15)
            if f"Learned: {word}" not in reasons:
                reasons.append(f"Learned: {word} (x{weight})")

    # 3. Patterns classiques
    classic = ["urgent", "compte bloqué", "gagnez", "double", "bit.ly", "http://", "cliquez ici", "airdrop gratuit"]
    for w in classic:
        if w in text_low:
            score += 10

    score = min(score, 99)
    if score >= 70: verdict, color = "SCAM DETECTED", "#ff2a2a"
    elif score >= 40: verdict, color = "SUSPECT - AI Learning", "#ffaa00"
    else: verdict, color = "SAFE - AI Vérifié", "#00ff88"
    return score, verdict, color, reasons

@app.route("/")
def home():
    learned_count = len(LEARNED_SCAMS)
    total_patterns = len(PATTERN_WEIGHTS)
    return f"""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ScamBuster V11 AUTO-LEARNING</title>
<style>body{{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding:20px}}
h1{{font-size:38px}}h1 span{{color:#00ff88}}.sub{{color:#00ccff;letter-spacing:3px;font-size:11px}}
.badge{{margin:10px auto;background:linear-gradient(90deg,rgba(0,255,136,0.15),rgba(0,204,255,0.15));border:1px solid #00ff88;border-radius:50px;padding:10px 20px;display:inline-block;font-size:11px;animation:pulse 2s infinite}}@keyframes pulse{{0%,100%{{box-shadow:0 0 10px #00ff88}}50%{{box-shadow:0 0 25px #00ff88}}}}
.grid{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;padding:10px;max-width:1100px;margin:auto}}
.card{{background:#111;border:1px solid #222;border-radius:12px;padding:12px;width:250px;font-size:12px}}.card h3{{color:#00ff88;margin:5px 0;font-size:13px}}.btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:11px 20px;border-radius:50px;font-weight:900;text-decoration:none;display:inline-block;margin:5px;font-size:11px}}
.footer{{margin-top:30px;padding:12px;color:#444;font-size:9px;border-top:1px solid #111}}
</style></head><body>
<h1>SCAM<span>BUSTER</span> AI</h1>
<div class="sub">EMPIRE V11 - WORLD AUTO-LEARNING ENGINE</div>
<div class="badge">🧠 AUTO-LEARNING ACTIVE - {learned_count} SCAMS APPRIS - {total_patterns} PATTERNS - SYSTEM EVOLVING</div>
<div class="grid">
<div class="card"><h3>🏦 37 Banques Mondiales</h3><p>Base V10.2 conservée</p></div>
<div class="card"><h3>💳 Fintechs & Mobile Money</h3><p>PayPal, M-Pesa, Binance...</p></div>
<div class="card" style="border-color:#00ff88"><h3>🧠 {learned_count} Scams Appris</h3><p>Le monde enseigne à l'AI</p></div>
<div class="card" style="border-color:#aa88ff"><h3>⚡ {total_patterns} Patterns Auto</h3><p>L'AI apprend tout seul</p></div>
</div>
<a href="/scan" class="btn">SCANNER + APPRENDRE</a>
<a href="/banks" class="btn" style="background:linear-gradient(90deg,#00ccff,#aa88ff)">37 BANQUES</a>
<a href="/learned" class="btn" style="background:linear-gradient(90deg,#ffaa00,#ff5500)">CERVEAU AI ({learned_count})</a>
<div style="max-width:600px;margin:20px auto;color:#666;font-size:11px;line-height:1.6">V9 = Châssis WORLD<br>V10.2 = 37 Banques Mondiales<br><b style="color:#00ff88">V11 = AUTO-LEARNING - L'AI apprend tout seul des signalements du monde entier!</b><br>ORIGIN: LUBUMBASHI | MINE: THE WORLD</div>
<div class="footer">ORIGIN: LUBUMBASHI, DRC | MINE: THE WORLD | V11 AUTO-LEARNING - {learned_count} LEARNED<br>pire-v7.onrender.com</div>
</body></html>
    """

@app.route("/scan", methods=["GET", "POST"])
def scan_page():
    result_html = ""
    if request.method == "POST":
        user_text = request.form.get("text", "")
        feedback = request.form.get("feedback", "")
        score, verdict, color, reasons = scan_engine_v11(user_text)
        
        # AUTO-LEARNING: Si l'utilisateur dit c'est un scam, on apprend!
        if feedback == "scam":
            learn_from_text(user_text, is_scam=True)
            result_html = f'<div style="background:#111;border:2px solid {color};border-radius:15px;padding:15px;margin:15px auto;max-width:500px"><h2 style="color:{color}">{verdict}</h2><p style="font-size:50px;margin:5px">{score}%</p><p style="font-size:11px">{", ".join(reasons) if reasons else "Analyse en cours..."}</p><p style="color:#00ff88;margin-top:10px">✅ MERCI! L AI A APPRIS! Total appris: {len(LEARNED_SCAMS)}</p></div>'
        else:
            result_html = f'<div style="background:#111;border:2px solid {color};border-radius:15px;padding:15px;margin:15px auto;max-width:500px"><h2 style="color:{color}">{verdict}</h2><p style="font-size:50px;margin:5px">{score}%</p><p style="font-size:11px">{", ".join(reasons) if reasons else "Aucune menace connue"}</p><form method="POST" style="margin-top:15px"><input type="hidden" name="text" value="{user_text}"><p style="font-size:12px;color:#888">C etait vraiment un scam?</p><button name="feedback" value="scam" style="background:#ff2a2a;color:#fff;border:none;padding:8px 15px;border-radius:20px;cursor:pointer">OUI, C ETAIT UN SCAM - APPRENDS!</button> <button name="feedback" value="safe" style="background:#222;color:#fff;border:1px solid #444;padding:8px 15px;border-radius:20px;cursor:pointer">Non, safe</button></form></div>'

    return f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{background:#000;color:#fff;text-align:center;padding:15px;font-family:Arial}} textarea{{width:90%;max-width:500px;height:100px;background:#111;color:#fff;border:1px solid #00ff88;border-radius:10px;padding:10px}} .btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:12px 25px;border-radius:50px;font-weight:900;cursor:pointer;margin-top:10px}} a{{color:#00ccff;text-decoration:none;font-size:12px}}</style></head><body><a href="/">← WORLD</a> | <a href="/banks">Banks</a> | <a href="/learned">Cerveau</a><h1>🧠 SCAN V11 AUTO-LEARNING</h1><p style="font-size:11px;color:#888">Colle un message suspect, l AI apprend de toi!</p><form method="POST"><textarea name="text" placeholder="Ex: Votre compte Binance bloqué..."></textarea><br><button class="btn" type="submit">ANALYSER AVEC AI</button></form>{result_html}</body></html>'

@app.route("/banks")
def banks_page():
    rows = "".join([f'<tr><td>{b["name"]}</td><td>{b["type"]}</td><td>{b["region"]}</td><td>{b["risk"]}</td></tr>' for b in GLOBAL_BANKS_FINTECHS])
    return f"""<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{background:#000;color:#fff;font-family:Arial;text-align:center;padding:15px}} table{{width:98%;max-width:900px;margin:15px auto;border-collapse:collapse;background:#111;border-radius:10px;overflow:hidden;font-size:11px}} th{{background:#00ff88;color:#000;padding:8px}} td{{padding:8px;border-bottom:1px solid #222}} a{{color:#00ccff;text-decoration:none}} .btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:10px 20px;border-radius:50px;font-weight:900;text-decoration:none;display:inline-block;margin:5px}}</style></head><body><a href="/">← WORLD</a> | <a href="/scan">Scan</a> | <a href="/learned">Cerveau</a><h1>🏦 37 GLOBAL BANKS & FINTECHS</h1><table><tr><th>Nom</th><th>Type</th><th>Région</th><th>Risque</th></tr>{rows}</table><a href="/" class="btn">RETOUR WORLD</a></body></html>"""

@app.route("/learned")
def learned_page():
    top_patterns = PATTERN_WEIGHTS.most_common(20)
    patterns_html = "".join([f'<tr><td>{w}</td><td>{c} fois</td></tr>' for w,c in top_patterns]) if top_patterns else '<tr><td colspan="2">Aucun pattern encore, commence à scanner!</td></tr>'
    scams_html = "".join([f'<div style="background:#111;border:1px solid #222;border-radius:8px;padding:10px;margin:8px auto;max-width:600px;font-size:11px;text-align:left">🔴 {s}</div>' for s in LEARNED_SCAMS[-10:][::-1]]) if LEARNED_SCAMS else '<p style="color:#666">Aucun scam appris encore</p>'
    return f"""<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{background:#000;color:#fff;font-family:Arial;text-align:center;padding:15px}} table{{width:90%;max-width:500px;margin:15px auto;border-collapse:collapse;background:#111;border-radius:10px;overflow:hidden;font-size:11px}} th{{background:#ffaa00;color:#000;padding:8px}} td{{padding:6px;border-bottom:1px solid #222}} a{{color:#00ccff;text-decoration:none}} .btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:10px 20px;border-radius:50px;font-weight:900;text-decoration:none;display:inline-block;margin:5px}}</style></head><body><a href="/">← WORLD</a> | <a href="/scan">Scan</a> | <a href="/banks">Banks</a><h1>🧠 CERVEAU AUTO-LEARNING V11</h1><p style="color:#888;font-size:11px">L AI apprend tout seul des signalements mondiaux</p><h3 style="color:#ffaa00">{len(LEARNED_SCAMS)} Scams Appris par le Monde</h3>{scams_html}<h3 style="color:#00ff88;margin-top:30px">{len(PATTERN_WEIGHTS)} Patterns Auto-Détectés</h3><table><tr><th>Mot Suspect Appris</th><th>Poids</th></tr>{patterns_html}</table><p style="color:#444;font-size:10px;margin-top:20px">ORIGIN: LUBUMBASHI | MINE: THE WORLD | V11 AUTO-LEARNING</p><a href="/" class="btn">RETOUR WORLD</a></body></html>"""

@app.route("/health")
def health():
    return f"V11 AUTO-LEARNING {len(LEARNED_SCAMS)} LEARNED {len(GLOBAL_BANKS_FINTECHS)} BANKS ONLINE"
