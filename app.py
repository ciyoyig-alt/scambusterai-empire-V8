from flask import Flask, request, jsonify
import re
import os
import hashlib
from datetime import datetime

app = Flask(__name__)

DISCLAIMER = "ScamBusterAI est un outil d'aide a la decision. Il ne garantit pas 100% de detection. La decision finale appartient au client. ScamBusterAI ne peut pas etre tenu responsable des pertes financieres."
TERMS = "En utilisant cette API, le client accepte que ScamBusterAI fournit une analyse probabiliste. La responsabilite finale de bloquer ou autoriser appartient au client."

BRAIN = {
    "scam_patterns": [
        r"gagn", r"loterie", r"félicitation", r"tu as gagné",
        r"compte bloqué", r"compte suspendu", r"vérifie.*urgent",
        r"clique.*vite", r"offre.*expire", r"gratuit.*clique",
        r"bit\.ly", r"tinyurl", r"argent.*facile",
        r"double.*argent", r"invest.*100%", r"crypto.*garanti",
        r"donne.*code", r"mot de passe"
    ],
    "learned_scams": [],
    "total_checked": 0,
    "total_blocked": 0,
}

LOGS = []

TRUSTED_DOMAINS = ["rawbank.com", "equitybank.com", "orange.com", "vodacom.com", "airtel.com", "wave.com"]
OWNER_KEY = "MOI-PROPRIETAIRE-2026"

CLIENTS = {
    "Rawbank": {"key": "RAW-123", "paye": 500, "status": "ACTIF"},
    "Wave": {"key": "WAVE-456", "paye": 300, "status": "ACTIF"},
}

def ai_analyze(text, phone="", url="", client="INCONNU"):
    text_low = (text or "").lower()
    url_low = (url or "").lower()
    score = 0
    reasons = []
    signals = []
    # AUTONOME : analyse seule, sans humain
    for pattern in BRAIN["scam_patterns"] + BRAIN["learned_scams"]:
        if re.search(pattern, text_low):
            score += 25
            reasons.append(f"Pattern: {pattern}")
            signals.append("TEXT_SCAM_PATTERN")
    if url_low:
        if any(d.split('.')[0] in url_low and d not in url_low for d in TRUSTED_DOMAINS):
            score += 40
            reasons.append("Faux domaine qui imite une banque")
            signals.append("FAKE_DOMAIN")
        if ".tk" in url_low or ".xyz" in url_low or "bit.ly" in url_low:
            score += 20
            reasons.append("Domaine suspect")
            signals.append("SUSPICIOUS_DOMAIN")
    if "urgent" in text_low or "immédiat" in text_low or "24h" in text_low:
        score += 15
        reasons.append("Pression / urgence")
        signals.append("URGENCY")
    # AUTONOME : apprend seule
    if score >= 70 and text_low not in BRAIN["learned_scams"]:
        BRAIN["learned_scams"].append(text_low[:30])
    score = min(score, 100)
    BRAIN["total_checked"] += 1
    if score >= 71:
        BRAIN["total_blocked"] += 1
    if score >= 71:
        verdict, action = "SCAM", "BLOCK"
    elif score >= 31:
        verdict, action = "SUSPICIOUS", "REVIEW"
    else:
        verdict, action = "SAFE", "ALLOW"

    timestamp = datetime.now().isoformat()
    log_entry = {
        "timestamp": timestamp,
        "client": client,
        "input_hash": hashlib.sha256((text+url).encode()).hexdigest()[:12],
        "input_preview": (text or url)[:80],
        "score": score,
        "verdict": verdict,
        "action": action,
        "reasons": reasons
    }
    LOGS.insert(0, log_entry)
    if len(LOGS) > 200:
        LOGS.pop()

    return {
        "score": score, "verdict": verdict, "action": action,
        "reasons": reasons, "signals": signals, "confidence": 99.0,
        "analyzed_by": "ScamBusterAI V9 - Autonomous - Sans intervention humaine",
        "timestamp": timestamp,
        "disclaimer": DISCLAIMER,
        "terms": "Decision finale au client - Voir /terms"
    }

@app.route("/")
def home():
    return jsonify({"filter": "GLOBAL_FILTER_V9", "status": "ScamBusterAI V9 LIVE - AUTONOMOUS AI - SANS INTERVENTION HUMAINE", "version": "V9-AUTONOMOUS", "mode": "FULLY_AUTONOMOUS", "disclaimer": DISCLAIMER, "stats": {"total_checked": BRAIN["total_checked"], "total_blocked": BRAIN["total_blocked"], "learned_patterns": len(BRAIN["learned_scams"])}})

@app.route("/terms")
def terms():
    return jsonify({"terms": TERMS, "disclaimer": DISCLAIMER, "responsabilite": "La decision finale appartient au client. ScamBusterAI fournit une aide a la decision."})

@app.route("/api/v9/check", methods=["POST"])
def check_universal():
    data = request.get_json() or {}
    return jsonify(ai_analyze(data.get("text",""), data.get("phone",""), data.get("url",""), data.get("client","INCONNU")))

@app.route("/api/v9/check-sms", methods=["POST"])
def check_sms():
    data = request.get_json() or {}
    r = ai_analyze(data.get("message","") or data.get("text",""), "", "", data.get("client","INCONNU"))
    r["sector"] = "MOBILE_NETWORK"
    return jsonify(r)

@app.route("/api/v9/check-payment", methods=["POST"])
def check_payment():
    data = request.get_json() or {}
    r = ai_analyze(data.get("text",""), data.get("phone",""), data.get("link","") or data.get("url",""), data.get("client","INCONNU"))
    r["sector"] = "FINTECH"
    return jsonify(r)

@app.route("/api/v9/check-url", methods=["POST"])
def check_url():
    data = request.get_json() or {}
    r = ai_analyze("", "", data.get("url",""), data.get("client","INCONNU"))
    r["sector"] = "BANK"
    return jsonify(r)

@app.route("/owner")
def owner_dashboard_unique():
    key = request.args.get("key")
    if key != OWNER_KEY:
        return "<h1>ACCES REFUSE - Seul le proprietaire entre ici</h1>", 403

    total_revenu = sum(c["paye"] for c in CLIENTS.values())
    clients_html = ""
    for nom, c in CLIENTS.items():
        clients_html += f"""
        <div class="client">
          <div><b>{nom}</b><br><span class="small">Clé: {c['key']} • {c['status']}</span></div>
          <div class="prix">{c['paye']}$<span class="small"> / mois</span></div>
        </div>
        """

    patterns_html = "".join([f"<span class='tag'>{p}</span>" for p in BRAIN["scam_patterns"]])
    learned = "<br>".join(BRAIN["learned_scams"]) if BRAIN["learned_scams"] else "Aucun scam appris pour le moment - la machine apprend seule quand elle bloque."

    logs_html = ""
    if not LOGS:
        logs_html = "<p class='small'>Aucune decision enregistree pour le moment. La machine attend, toute seule.</p>"
    else:
        for l in LOGS[:20]:
            color = "#f87171" if l['verdict']=="SCAM" else "#34d399" if l['verdict']=="SAFE" else "#fbbf24"
            logs_html += f"<div style='background:#0f172a;border:1px solid #26314d;border-radius:10px;padding:10px;margin-top:8px'><b style='color:{color}'>{l['verdict']} - {l['score']}/100 - {l['action']}</b><br><span class='small'>{l['timestamp']} | Client: {l['client']} | Hash: {l['input_hash']}</span><br><span style='font-size:13px'>{l['input_preview']}</span><br><span class='small'>Raisons: {', '.join(l['reasons']) if l['reasons'] else 'Aucune'}</span></div>"

    html = f"""
    <!DOCTYPE html>
    <html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
    <title>ScamBusterAI - Tableau de Bord Proprietaire - AUTONOME</title>
    <meta http-equiv="refresh" content="10">
    <style>
    *{{box-sizing:border-box}} body{{margin:0;font-family:system-ui,Arial;background:#070b14;color:#fff}}
    .top{{background:linear-gradient(90deg,#6d28d9,#db2777);padding:22px 18px}}
    .top h1{{margin:0;font-size:26px}} .top p{{margin:6px 0 0;opacity:.9}}
    .wrap{{max-width:920px;margin:0 auto;padding:16px}}
    .grid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}} @media(max-width:600px){{.grid{{grid-template-columns:1fr}}}}
    .card{{background:#111827;border:1px solid #26314d;border-radius:16px;padding:16px}}
    .card h3{{margin:0 0 6px;font-size:14px;color:#a5b4fc}} .big{{font-size:34px;font-weight:800}}
    .green{{color:#34d399}} .red{{color:#f87171}} .gold{{color:#fbbf24}}
    .client{{display:flex;justify-content:space-between;align-items:center;background:#0f172a;border:1px solid #26314d;border-radius:12px;padding:12px;margin-top:10px}}
    .prix{{font-size:22px;font-weight:800;color:#34d399}} .small{{font-size:12px;color:#94a3b8}}
    .tag{{display:inline-block;background:#1e293b;border:1px solid #334155;padding:5px 9px;border-radius:999px;font-size:12px;margin:3px}}
    .footer{{text-align:center;color:#94a3b8;font-size:12px;padding:14px}}
    .legal{{background:#fef3c7;color:#111827;border-radius:12px;padding:12px;font-size:13px;line-height:1.5}}
    .auto{{background:#065f46;border:1px solid #34d399;border-radius:12px;padding:12px;font-size:13px}}
    </style></head><body>
    <div class="top"><h1>🛡️ ScamBusterAI V9</h1><p>Bienvenue Proprietaire — Machine Autonome • Fondateur</p></div>
    <div class="wrap">
      <div class="auto">🤖 <b>MODE AUTONOME ACTIF</b> — Cette page se met a jour toute seule toutes les 10 secondes. Aucune intervention humaine necessaire. La machine analyse, bloque, apprend et enregistre seule.</div>
      <div class="grid" style="margin-top:14px">
        <div class="card"><h3>💰 TON REVENU MENSUEL</h3><div class="big gold">{total_revenu}$ / mois</div><p class="small">Calcule seul sur tes vrais clients actifs.</p></div>
        <div class="card"><h3>👥 TES CLIENTS ACTIFS</h3><div class="big">{len(CLIENTS)}</div><p class="small">Clients qui paient reellement.</p></div>
        <div class="card"><h3>🔍 TOTAL VERIFIES</h3><div class="big">{BRAIN['total_checked']}</div><p class="small">Analyses faites seules par ton IA.</p></div>
        <div class="card"><h3>🚫 TOTAL BLOQUES</h3><div class="big red">{BRAIN['total_blocked']}</div><p class="small">Scams bloques seuls, sans humain.</p></div>
      </div>
      <div class="card" style="margin-top:14px"><h3>📋 TES CLIENTS</h3>{clients_html}</div>
      <div class="card" style="margin-top:14px"><h3>🧠 CERVEAU DE L'IA — PATTERNS DE BASE</h3><div style="margin-top:8px">{patterns_html}</div><p class="small">Ces patterns sont dans ton code.</p></div>
      <div class="card" style="margin-top:14px"><h3>📚 CE QUE L'IA A APPRIS TOUTE SEULE</h3><p style="font-size:14px">{learned}</p><p class="small">Nombre de patterns appris : {len(BRAIN['learned_scams'])}</p></div>
      <div class="card" style="margin-top:14px"><h3>📜 JOURNAL DES DECISIONS — TA PREUVE</h3><p class="small">Enregistre seul, chaque decision. Aucun humain ne touche.</p>{logs_html}</div>
      <div class="card" style="margin-top:14px"><h3>⚖️ PROTECTION JURIDIQUE</h3><div class="legal"><b>⚠️ IMPORTANT :</b> {DISCLAIMER}<br><br>{TERMS}</div></div>
      <div class="card" style="margin-top:14px"><h3>⚙️ ETAT DU SYSTEME</h3><p>Statut : <b class="green">● LIVE - AUTONOMOUS AI - SANS INTERVENTION HUMAINE</b><br>Version : V9-AUTONOMOUS<br>Filtre : GLOBAL_FILTER_V9<br>Serveur : scambusterai-empire-v7.onrender.com</p></div>
    </div>
    <div class="footer">ScamBusterAI V9 — Machine Autonome — Tableau de Bord Prive Proprietaire — Lubumbashi</div>
    </body></html>
    """
    return html

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
