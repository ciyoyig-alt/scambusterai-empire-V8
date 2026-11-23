from flask import Flask, request, jsonify
import re
from datetime import datetime

app = Flask(__name__)

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

TRUSTED_DOMAINS = ["rawbank.com", "equitybank.com", "orange.com", "vodacom.com", "airtel.com", "wave.com"]
OWNER_KEY = "MOI-PROPRIETAIRE-2026"

CLIENTS = {
    "Rawbank": {"key": "RAW-123", "paye": 500, "status": "ACTIF"},
    "Wave": {"key": "WAVE-456", "paye": 300, "status": "ACTIF"},
}

def ai_analyze(text, phone="", url=""):
    text_low = (text or "").lower()
    url_low = (url or "").lower()
    score = 0
    reasons = []
    signals = []
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
    return {"score": score, "verdict": verdict, "action": action, "reasons": reasons, "signals": signals, "confidence": 99.0, "analyzed_by": "ScamBusterAI V9 - Autonomous", "timestamp": datetime.now().isoformat()}

@app.route("/")
def home():
    return jsonify({"filter": "GLOBAL_FILTER_V9", "status": "ScamBusterAI V9 LIVE - AUTONOMOUS AI", "version": "V9-AUTONOMOUS", "mode": "FULLY_AUTONOMOUS_NO_HUMAN", "stats": {"total_checked": BRAIN["total_checked"], "total_blocked": BRAIN["total_blocked"], "learned_patterns": len(BRAIN["learned_scams"])}})

@app.route("/api/v9/check", methods=["POST"])
def check_universal():
    data = request.get_json() or {}
    return jsonify(ai_analyze(data.get("text",""), data.get("phone",""), data.get("url","")))

@app.route("/api/v9/check-sms", methods=["POST"])
def check_sms():
    data = request.get_json() or {}
    r = ai_analyze(data.get("message","") or data.get("text",""))
    r["sector"] = "MOBILE_NETWORK"
    return jsonify(r)

@app.route("/api/v9/check-payment", methods=["POST"])
def check_payment():
    data = request.get_json() or {}
    r = ai_analyze(data.get("text",""), data.get("phone",""), data.get("link","") or data.get("url",""))
    r["sector"] = "FINTECH"
    return jsonify(r)

@app.route("/api/v9/check-url", methods=["POST"])
def check_url():
    data = request.get_json() or {}
    r = ai_analyze("", "", data.get("url",""))
    r["sector"] = "BANK"
    return jsonify(r)

@app.route("/owner")
def owner_dashboard():
    key = request.args.get("key")
    if key != OWNER_KEY:
        return jsonify({"error": "ACCES REFUSE - Seule la proprietaire entre ici"}), 403
    total_revenu = sum(c["paye"] for c in CLIENTS.values())
    return jsonify({"message": "Bienvenue Proprietaire, tu es au coeur de la machine", "proprietaire": "TOI - Fondatrice de ScamBusterAI V9", "ton_revenu_mensuel": f"{total_revenu}$ / mois", "total_verifies": BRAIN["total_checked"], "total_bloques": BRAIN["total_blocked"], "tes_clients": CLIENTS, "ta_machine": "Elle travaille pour TOI 24h/24"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)# ===== TON COEUR - SEULE TOI Y ENTRES =====
OWNER_KEY = "MOI-PROPRIETAIRE-2026"
CLIENTS = {
    "Rawbank": {"key": "RAW-123", "paye": 500, "status": "ACTIF"},
    "Wave": {"key": "WAVE-456", "paye": 300, "status": "ACTIF"},
}

@app.route("/owner")
def owner_dashboard():
    key = request.args.get("key")
    if key != OWNER_KEY:
        return jsonify({"error": "ACCES REFUSE - Seule la propriétaire entre ici"}), 403
    
    total_revenu = sum(c["paye"] for c in CLIENTS.values())
    return jsonify({
        "message": "Bienvenue Propriétaire, tu es au coeur de la machine",
        "proprietaire": "TOI - Fondatrice de ScamBusterAI V9",
        "ton_revenu_mensuel": f"{total_revenu}$ / mois",
        "total_verifies": BRAIN["total_checked"],
        "total_bloques": BRAIN["total_blocked"],
        "tes_clients": CLIENTS,
        "ta_machine": "Elle travaille pour TOI 24h/24",
        "ton_pouvoir": [
            "Tu peux bloquer une banque",
            "Tu peux changer le prix",
            "Tu peux voir toutes les arnaques",
            "Tu es la seule à décider"
        ]
    })
