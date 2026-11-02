from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>🛡️ ScamBuster Empire V9 - LIVE!</h1><p>Deploy REUSSI! Empire en ligne!</p>"

@app.route("/health")
def health():
    return "OK"
