from flask import Flask, render_template_string, request, jsonify
import re
from urllib.parse import urlparse

app = Flask(__name__)

HTML = """ [ton HTML actuel - garde le] """

def analyze_scam(message, link):
    score = 0
    flags = []
    
    msg = (message or "").lower()
    link_low = (link or "").lower()
    
    # 1. ANALYSE MESSAGE - mots clés arnaque
    scam_keywords = {
        "gagné": 25, "gagne":25, "5000$":30, "félicitations":20, "felicitations":20,
        "prince":35, "héritage":30, "banque":15, "loterie":30, "urgence":20,
        "cliquez ici":25, "virement":20, "whatsapp":10, "crypto":15,
        "amour":15, "romance":15, "aide moi":20
    }
    for word, pts in scam_keywords.items():
        if word in msg:
            score += pts
            flags.append(f"Mot suspect: {word}")
    
    # 2. ANALYSE LIEN
    if link:
        try:
            parsed = urlparse(link if link.startswith("http") else "https://"+link)
            domain = parsed.netloc.lower()
            # liens raccourcis = suspect
            shorteners = ["vt.tiktok.com", "bit.ly", "tinyurl", "t.me", "wa.me", "goo.gl"]
            if any(s in domain for s in shorteners):
                score += 40
                flags.append(f"Lien raccourci: {domain}")
            if domain.count("-") >= 3 or len(domain) > 30:
                score += 20
                flags.append("Domaine suspect long")
            if re.search(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", domain):
                score += 50
                flags.append("IP directe")
        except:
            score += 10
    else:
        if not msg:
            return 0, "VIDE", [], "Entre un message!"
    
    # Plafonne 0-95%
    score = min(95, max(5, score))
    
    if score < 25:
        status = "SÉCURISÉ"
        color = "green"
        advice = "✅ Semble OK mais reste vigilant."
    elif score < 55:
        status = "SUSPECT"
        color = "orange"
        advice = "⚠️ Méfiance - vérifie l'expéditeur."
    else:
        status = "DANGER ARNAQUE"
        color = "red"
        advice = "🚨 ARNAQUE probable - ne clique pas, ne paie pas!"
    
    return score, status, flags, advice

@app.route("/")
def home():
    return render_template_string(HTML_TEMPLATE) # garde ton template

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json()
    msg = data.get("message","")
    link = data.get("link","")
    score, status, flags, advice = analyze_scam(msg, link)
    return jsonify({"score":score,"status":status,"flags":flags,"advice":advice})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
