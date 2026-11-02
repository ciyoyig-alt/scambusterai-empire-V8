from flask import Flask, request
app = Flask(__name__)

# ====== SCAMBUSTER AI WORLD - GLOBAL DATABASE ======
# Toutes les banques & fintechs les plus utilisées au MONDE - Cibles #1 des scammers
GLOBAL_BANKS_FINTECHS = [
    # --- GLOBAL BANKS ---
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

    # --- GLOBAL FINTECHS - Le coeur des scams 2026 ---
    {"name": "PayPal", "type": "Fintech Paiement", "region": "World", "risk": "🔴 #1 Phishing Mondial"},
    {"name": "Wise (ex TransferWise)", "type": "Fintech Transfert", "region": "World", "risk": "🔴 Très Ciblé"},
    {"name": "Revolut", "type": "Fintech Néobanque", "region": "EU/World", "risk": "🔴 Très Ciblé"},
    {"name": "Venmo", "type": "Fintech Paiement", "region": "USA", "risk": "🟠 Ciblé"},
    {"name": "Cash App", "type": "Fintech Paiement", "region": "USA", "risk": "🔴 Très Ciblé"},
    {"name": "Zelle", "type": "Fintech Paiement", "region": "USA", "risk": "🔴 Très Ciblé"},
    {"name": "Skrill", "type": "Fintech", "region": "World", "risk": "🟠 Ciblé"},
    {"name": "Neteller", "type": "Fintech", "region": "World", "risk": "🟠 Ciblé"},
    {"name": "Payoneer", "type": "Fintech Freelance", "region": "World", "risk": "🔴 Très Ciblé"},

    # --- MOBILE MONEY WORLD ---
    {"name": "M-Pesa", "type": "Mobile Money", "region": "Kenya/Africa", "risk": "🔴 #1 Scam Africa"},
    {"name": "Airtel Money", "type": "Mobile Money", "region": "Africa/India", "risk": "🔴 Très Ciblé"},
    {"name": "Orange Money", "type": "Mobile Money", "region": "Africa/EU", "risk": "🔴 Très Ciblé"},
    {"name": "MTN MoMo", "type": "Mobile Money", "region": "Africa", "risk": "🔴 Très Ciblé"},
    {"name": "Wave", "type": "Mobile Money", "region": "West Africa", "risk": "🟠 Ciblé"},
    {"name": "GCash", "type": "Mobile Money", "region": "Philippines", "risk": "🔴 Très Ciblé"},
    {"name": "Paytm", "type": "Mobile Money", "region": "India", "risk": "🔴 Très Ciblé"},

    # --- CRYPTO FINTECHS - La mine d'or des scammers ---
    {"name": "Binance", "type": "Crypto Exchange", "region": "World", "risk": "🔴 #1 Fake Apps"},
    {"name": "Coinbase", "type": "Crypto Exchange", "region": "World", "risk": "🔴 Très Ciblé"},
    {"name": "Trust Wallet", "type": "Crypto Wallet", "region": "World", "risk": "🔴 Fake Versions"},
    {"name": "MetaMask", "type": "Crypto Wallet", "region": "World", "risk": "🔴 Très Ciblé"},
    {"name": "Kraken", "type": "Crypto Exchange", "region": "World", "risk": "🟠 Ciblé"},
    {"name": "KuCoin", "type": "Crypto Exchange", "region": "World", "risk": "🟠 Ciblé"},
    {"name": "Tether USDT", "type": "Crypto Stablecoin", "region": "World", "risk": "🔴 Fake Airdrops"},
]

def scan_engine(text):
    text_low = text.lower()
    score = 0
    reasons = []
    # ScamBuster AI connait toutes ces marques mondiales
    for bank in GLOBAL_BANKS_FINTECHS:
        if bank["name"].lower() in text_low and "🔴" in bank["risk"]:
            score += 25
            reasons.append(f"Impersonation: {bank['name']}")
    
    extra = ["urgent", "compte bloqué", "gagnez", "double", "bit.ly", "http://", "vérifiez"]
    for w in extra:
        if w in text_low:
            score += 10
    
    score = min(score, 99)
    if score >= 70: verdict, color = "SCAM DETECTED", "#ff2a2a"
    elif score >= 40: verdict, color = "SUSPECT - Vérifiez Banque", "#ffaa00"
    else: verdict, color = "SAFE", "#00ff88"
    return score, verdict, color, reasons

@app.route("/")
def home():
    count = len(GLOBAL_BANKS_FINTECHS)
    return f"""
<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<title>ScamBuster V10.2 GLOBAL</title>
<style>body{{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding:20px}}
h1{{font-size:38px}}h1 span{{color:#00ff88}}.sub{{color:#00ccff;letter-spacing:3px;font-size:12px}}
.badge{{margin:12px auto;background:rgba(0,255,136,0.1);border:1px solid #00ff88;border-radius:50px;padding:8px 20px;display:inline-block;font-size:11px}}
.grid{{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;padding:10px;max-width:1100px;margin:auto}}
.card{{background:#111;border:1px solid #222;border-radius:12px;padding:12px;width:250px;font-size:12px}}
.card h3{{color:#00ff88;margin:5px 0;font-size:14px}}.btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:11px 22px;border-radius:50px;font-weight:900;text-decoration:none;display:inline-block;margin:6px;font-size:12px}}
.footer{{margin-top:30px;padding:12px;color:#444;font-size:9px;border-top:1px solid #111;letter-spacing:1px}}
</style></head><body>
<h1>SCAM<span>BUSTER</span> AI</h1>
<div class="sub">EMPIRE V10.2 - GLOBAL BANKS & FINTECHS SHIELD</div>
<div class="badge">🌍 {count} BANQUES & FINTECHS MONDIALES PROTÉGÉES - SYSTEM ONLINE</div>
<div class="grid">
<div class="card"><h3>🏦 {len([b for b in GLOBAL_BANKS_FINTECHS if 'Banque' in b['type']])} Banques Mondiales</h3><p>USA, EU, Africa, Asia</p></div>
<div class="card"><h3>💳 {len([b for b in GLOBAL_BANKS_FINTECHS if 'Fintech' in b['type'] or 'Mobile' in b['type']])} Fintechs & Mobile Money</h3><p>PayPal, Wise, M-Pesa, Orange...</p></div>
<div class="card"><h3>₿ {len([b for b in GLOBAL_BANKS_FINTECHS if 'Crypto' in b['type']])} Crypto Exchanges</h3><p>Binance, Coinbase, Trust...</p></div>
<div class="card" style="border-color:#00ccff"><h3>🧠 AI GLOBAL</h3><p>ScamBuster connait toutes les marques que le monde utilise</p></div>
</div>
<a href="/scan" class="btn">SCANNER MESSAGE</a>
<a href="/banks" class="btn" style="background:linear-gradient(90deg,#00ccff,#aa88ff)">VOIR LES {count} BANQUES</a>
<div style="max-width:600px;margin:20px auto;color:#666;font-size:11px;line-height:1.6">ORIGIN: LUBUMBASHI, DRC<br>MINE: THE WORLD<br><b style="color:#fff">ScamBuster AI doit toucher toutes les banques que les gens utilisent - Tu as raison Chef, c'est fait!</b></div>
<div class="footer">ORIGIN: LUBUMBASHI | MINE: THE WORLD | V10.2 GLOBAL REGISTRY - {count} INSTITUTIONS<br>pire-v7.onrender.com</div>
</body></html>
    """

@app.route("/banks")
def banks_page():
    rows = "".join([f'<tr><td>{b["name"]}</td><td>{b["type"]}</td><td>{b["region"]}</td><td>{b["risk"]}</td></tr>' for b in GLOBAL_BANKS_FINTECHS])
    return f"""<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1">
<style>body{{background:#000;color:#fff;font-family:Arial;text-align:center;padding:15px}} table{{width:98%;max-width:900px;margin:15px auto;border-collapse:collapse;background:#111;border-radius:10px;overflow:hidden;font-size:12px}} th{{background:#00ff88;color:#000;padding:8px}} td{{padding:8px;border-bottom:1px solid #222}} a{{color:#00ccff;text-decoration:none}} .btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:10px 20px;border-radius:50px;font-weight:900;text-decoration:none;display:inline-block;margin:5px}}</style>
</head><body><a href="/">← WORLD</a> | <a href="/scan">Scan →</a>
<h1>🏦 GLOBAL BANKS & FINTECHS - {len(GLOBAL_BANKS_FINTECHS)} INSTITUTIONS</h1>
<p style="color:#888;font-size:11px">Toutes les banques et fintechs que le monde utilise - Base ScamBuster AI WORLD</p>
<table><tr><th>Nom</th><th>Type</th><th>Région</th><th>Risque Scam</th></tr>{rows}</table>
<a href="/" class="btn">RETOUR WORLD</a>
<div style="margin-top:20px;color:#444;font-size:9px">ORIGIN: LUBUMBASHI | MINE: THE WORLD | V10.2</div>
</body></html>"""

@app.route("/scan", methods=["GET", "POST"])
def scan_page():
    result_html = ""
    if request.method == "POST":
        user_text = request.form.get("text", "")
        score, verdict, color, reasons = scan_engine(user_text)
        result_html = f'<div style="background:#111;border:2px solid {color};border-radius:15px;padding:15px;margin:15px auto;max-width:500px"><h2 style="color:{color}">{verdict}</h2><p style="font-size:50px;margin:5px">{score}%</p><p style="font-size:11px">{"<br>".join(reasons) if reasons else "Aucune marque usurpée détectée"}</p></div>'
    return f'<!DOCTYPE html><html><head><meta name="viewport" content="width=device-width, initial-scale=1"><style>body{{background:#000;color:#fff;text-align:center;padding:20px;font-family:Arial}} textarea{{width:90%;max-width:500px;height:100px;background:#111;color:#fff;border:1px solid #00ff88;border-radius:10px;padding:10px}} .btn{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:12px 30px;border-radius:50px;font-weight:900;cursor:pointer;margin-top:10px}} a{{color:#00ccff;text-decoration:none}}</style></head><body><a href="/">← WORLD</a> | <a href="/banks">Banks ({len(GLOBAL_BANKS_FINTECHS)}) →</a><h1>🛡️ SCAN AI - GLOBAL BRANDS</h1><p style="font-size:12px;color:#888">Colle un message qui usurpe une banque mondiale</p><form method="POST"><textarea name="text" placeholder="Ex: Votre compte PayPal bloqué, cliquez ici http://... ou Votre Rawbank suspendu..."></textarea><br><button class="btn" type="submit">ANALYSER GLOBAL</button></form>{result_html}</body></html>'

@app.route("/health")
def health():
    return f"V10.2 GLOBAL {len(GLOBAL_BANKS_FINTECHS)} BANKS ONLINE"
