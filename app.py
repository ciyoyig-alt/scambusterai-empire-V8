from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ScamBuster Empire V9 WORLD</title>
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=Inter:wght@400;700&display=swap');
body{background:#000;color:#fff;font-family:'Inter',sans-serif;text-align:center;margin:0;padding:0;overflow-x:hidden}
.hero{padding:60px 20px 30px}
h1{font-family:'Orbitron',sans-serif;font-size:48px;color:#fff;letter-spacing:3px;margin:0;text-shadow:0 0 30px #00ff88}
h1 span{color:#00ff88}
.subtitle{font-size:18px;color:#00ccff;letter-spacing:6px;margin-top:10px;text-transform:uppercase}
.badge{margin:30px auto;background:rgba(0,255,136,0.1);border:1px solid #00ff88;border-radius:50px;padding:10px 25px;display:inline-block}
.dot{display:inline-block;width:10px;height:10px;background:#00ff88;border-radius:50%;box-shadow:0 0 10px #00ff88;animation:blink 1.5s infinite;margin-right:8px}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0}}
.grid{display:flex;flex-wrap:wrap;justify-content:center;gap:20px;padding:20px;max-width:1000px;margin:auto}
.card{background:linear-gradient(180deg,#111,#0a0a0a);border:1px solid #222;border-radius:20px;padding:25px;width:300px;transition:0.3s}
.card:hover{border-color:#00ff88;box-shadow:0 0 30px rgba(0,255,136,0.2);transform:translateY(-5px)}
.card h3{color:#00ff88;margin-top:0}
.btn{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:none;padding:16px 40px;border-radius:50px;font-weight:900;font-size:16px;letter-spacing:1px;cursor:pointer;box-shadow:0 0 20px rgba(0,255,136,0.5)}
.footer{margin-top:50px;padding:20px;color:#444;font-size:12px;letter-spacing:2px;border-top:1px solid #111}
.footer strong{color:#666}
</style>
</head>
<body>
<div class="hero">
<h1>SCAM<span>BUSTER</span></h1>
<div class="subtitle">Empire V9 World Edition</div>
<div class="badge"><span class="dot"></span> GLOBAL SYSTEM ONLINE - WORLDWIDE SHIELD ACTIVE</div>
</div>

<div class="grid">
<div class="card">
<h3>🌍 Global Engine</h3>
<p>Detecting scams across WhatsApp, Crypto, Phishing, Investments in 100+ countries.</p>
</div>
<div class="card">
<h3>🛡️ V9 Ultra Core</h3>
<p>Real-time AI analysis. No more fake links. No more stolen money. Protection for everyone.</p>
</div>
<div class="card">
<h3>⚡ Empire Protocol</h3>
<p>Built to scale. From one server to global infrastructure. Like Facebook, like Google.</p>
</div>
</div>

<div style="margin:40px 0">
<button class="btn" onclick="document.getElementById('mission').scrollIntoView({behavior:'smooth'})">ENTER THE EMPIRE</button>
</div>

<div id="mission" style="max-width:700px;margin:60px auto;padding:0 20px;color:#888;line-height:1.8">
<h2 style="color:#fff;letter-spacing:3px">THE MISSION</h2>
<p>We do not build for a city. We build for the world.<br>
Every day, millions lose money to digital scams.<br>
<strong style="color:#fff">ScamBuster is the shield.</strong></p>
</div>

<div class="footer">
ORIGIN: <strong>LUBUMBASHI, DRC</strong> &nbsp;|&nbsp; MINE: <strong>THE WORLD</strong><br><br>
Built by The Founder - 2026<br>
pire-v7.onrender.com
</div>
</body>
</html>
    """

@app.route("/health")
def health():
    return "WORLD ONLINE"
