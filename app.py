# ===== TON COEUR - SEULE TOI Y ENTRES =====
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
