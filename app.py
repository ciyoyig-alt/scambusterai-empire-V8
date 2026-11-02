from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ScamBuster Empire V9</title>
<style>
body{background:#000;color:#fff;font-family:Arial;text-align:center;margin:0;padding:20px}
h1{font-size:50px;color:#00ff88;text-shadow:0 0 20px #00ff88;animation:glow 2s infinite}
@keyframes glow{0%{text-shadow:0 0 20px #00ff88}50%{text-shadow:0 0 40px #00ff88,0 0 60px #00ff88}100%{text-shadow:0 0 20px #00ff88}}
.card{background:#111;border:2px solid #00ff88;border-radius:20px;padding:20px;margin:20px auto;max-width:400px;box-shadow:0 0 30px #00ff8866}
.btn{background:linear-gradient(45deg,#00ff88,#00ccff);color:#000;border:none;padding:15px 30px;border-radius:50px;font-size:18px;font-weight:bold;cursor:pointer}
.live{display:inline-block;width:15px;height:15px;background:#00ff88;border-radius:50%;animation:blink 1s infinite}
@keyframes blink{0%{opacity:1}50%{opacity:0}100%{opacity:1}}
</style>
</head>
<body>
<h1>🛡️ SCAMBUSTER</h1>
<h2 style="color:#00ccff">EMPIRE V9 ULTRA - LIVE</h2>
<div class="card">
<div class="live"></div> SYSTEM ONLINE<br><br>
<strong style="font-size:30px">pire-v7.onrender.com</strong><br><br>
✅ Build: FIXED<br>
✅ Flask + Gunicorn<br>
✅ LIVE VERT
</div>
<div class="card">
<h3>🔥 EMPIRE STATUS 🔥</h3>
<p>🚀 Deploy: SUCCESS</p>
<p>💎 Version: V9 ULTRA</p>
<p>🌍 Global: ACTIVE</p>
<button class="btn" onclick="alert('EMPIRE V9 ULTRA READY CHEF!')">ACTIVER EMPIRE</button>
</div>
<p style="color:#555">Built by Chef Empire 2026</p>
</body>
</html>
    """

@app.route("/health")
def health():
    return "OK"
