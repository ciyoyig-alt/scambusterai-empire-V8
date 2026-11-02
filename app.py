from flask import Flask, request, jsonify
import re, json, os
from collections import Counter
app = Flask(__name__)

BRAIN_FILE = "brain.json"
BANKS = ["PayPal","Wise","Revolut","M-Pesa","Orange Money","Airtel Money","MTN MoMo","Binance","Coinbase","Rawbank","Equity BCDC","JPMorgan","HSBC","Ecobank","Zwa Cash","U-Reporter"]

def load_brain():
    if os.path.exists(BRAIN_FILE):
        try:
            with open(BRAIN_FILE,"r",encoding="utf-8") as f:
                d=json.load(f)
                return d.get("scams",[]), Counter(d.get("patterns",{}))
        except: pass
    return [], Counter()

def save_brain():
    try:
        with open(BRAIN_FILE,"w",encoding="utf-8") as f:
            json.dump({"scams":SCAMS,"patterns":dict(PATTERNS)},f,ensure_ascii=False)
    except: pass

SCAMS, PATTERNS = load_brain()
STOP = {"avec","pour","vous","votre","dans","les","des","une","est","sont","merci"}

def learn(txt):
    ws=re.findall(r'\w{3,}',txt.lower())
    for w in ws:
        if w not in STOP:
            PATTERNS[w]+=1
    if txt not in SCAMS and len(txt)>10:
        SCAMS.append(txt[:250])
    save_brain()

def scan(txt):
    low=txt.lower()
    score=0
    rs=[]
    for b in BANKS:
        if b.lower() in low:
            score+=20
            rs.append(b)
    for w,c in PATTERNS.most_common(50):
        if w in low:
            score+= min(c*3,15)
            if len(rs)<5: rs.append(f"{w}x{c}")
    if "http" in low: score+=10
    score=min(score,99)
    if score>=65: v="SCAM DETECTED"
    elif score>=30: v="SUSPECT"
    else: v="SAFE"
    return score,v,rs

@app.route("/")
def home():
    return f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#000;color:#fff;text-align:center;font-family:Arial;padding:20px}} .b{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;padding:12px 20px;border-radius:30px;text-decoration:none;font-weight:900;display:inline-block;margin:5px}}</style></head><body><h1>SCAMBUSTER <span style='color:#00ff88'>AI</span></h1><p>V12.1 FIX - CLOUD READY - {len(SCAMS)} SCAMS - {len(PATTERNS)} PATTERNS - {len(BANKS)} BANKS</p><p>ORIGIN: LUBUMBASHI | MINE: THE WORLD</p><a href='/scan' class='b'>SCANNER</a> <a href='/banks' class='b'>BANQUES</a> <a href='/learned' class='b'>CERVEAU {len(SCAMS)}</a><br><br><p style='color:#666;font-size:11px'>Fichier: {BRAIN_FILE} - Deploy FIX du 2 Nov 2026</p></body></html>"

@app.route("/scan",methods=["GET","POST"])
def scan_page():
    res=""
    if request.method=="POST":
        txt=request.form.get("text","")
        fb=request.form.get("fb","")
        if fb=="scam" and txt:
            learn(txt)
            res=f"<div style='border:2px solid #00ff88;padding:15px;margin:15px;border-radius:12px'><h2 style='color:#00ff88'>GRAVÉ! {len(SCAMS)} SCAMS</h2><p>{len(PATTERNS)} PATTERNS</p></div>"
        else:
            s,v,r=scan(txt)
            res=f"<div style='border:2px solid #ffaa00;padding:15px;margin:15px;border-radius:12px'><h2>{v} - {s}%</h2><p>{' | '.join(r)}</p><form method='POST'><input type='hidden' name='text' value='{txt}'><button name='fb' value='scam' style='background:#ff2a2a;color:#fff;padding:10px 20px;border:none;border-radius:20px;font-weight:900'>OUI GRAVE CE SCAM!</button></form></div>"
    return f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#000;color:#fff;text-align:center;padding:15px;font-family:Arial}} textarea{{width:90%;max-width:500px;height:100px;background:#111;color:#fff;border:1px solid #00ff88;border-radius:10px;padding:10px}}</style></head><body><a href='/' style='color:#00ccff'>← WORLD</a><h1>SCAN V12.1 FIX</h1><form method='POST'><textarea name='text' placeholder='Colle scam ici...'></textarea><br><button style='background:#00ff88;padding:12px 25px;border-radius:30px;border:none;font-weight:900;margin-top:10px'>ANALYSER</button></form>{res}</body></html>"

@app.route("/banks")
def banks_page():
    rows="".join([f"<div style='background:#111;margin:5px;padding:10px;border-radius:8px'>{b}</div>" for b in BANKS])
    return f"<html><body style='background:#000;color:#fff;text-align:center;font-family:Arial;padding:20px'><a href='/' style='color:#00ccff'>← WORLD</a><h1>{len(BANKS)} BANQUES</h1>{rows}</body></html>"

@app.route("/learned")
def learned_page():
    top=PATTERNS.most_common(30)
    pat="".join([f"<div>{w} - {c}</div>" for w,c in top])
    scams="".join([f"<div style='background:#111;padding:10px;margin:5px;border-radius:8px;text-align:left'>🔴 {s}</div>" for s in SCAMS[-10:][::-1]])
    return f"<html><body style='background:#000;color:#fff;text-align:center;font-family:Arial;padding:20px'><a href='/' style='color:#00ccff'>← WORLD</a><h1>CERVEAU {len(SCAMS)} SCAMS - {len(PATTERNS)} PATTERNS</h1><h3>SCAMS GRAVÉS</h3>{scams}<h3>PATTERNS</h3>{pat}</body></html>"

@app.route("/export")
def export_b():
    return jsonify({"scams":SCAMS,"patterns":dict(PATTERNS),"version":"V12.1 FIX"})

@app.route("/health")
def health():
    return f"V12.1 FIX OK {len(SCAMS)} SCAMS {len(PATTERNS)} PATTERNS"
