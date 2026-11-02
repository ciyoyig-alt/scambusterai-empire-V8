from flask import Flask, request, jsonify
import re, json, os
from collections import Counter
try: import requests
except: requests=None
app = Flask(__name__)

BRAIN_FILE="brain.json"
CLOUD_URL=os.environ.get("BRAIN_CLOUD_URL","")
# 45 BANQUES + FINTECHS + MOBILE MONEY V12.3
BANKS=["JPMorgan Chase","Bank of America","HSBC","Barclays","BNP Paribas","Deutsche Bank","Standard Chartered","Ecobank","UBA","GTBank","First Bank Nigeria","Access Bank","KCB Bank","Equity Bank","Rawbank","Equity BCDC","TMB","PayPal","Wise","Revolut","Venmo","Cash App","Zelle","Payoneer","Stripe","Skrill","Neteller","M-Pesa","Airtel Money","Orange Money","MTN MoMo","Wave","GCash","Paytm","MoMo","Binance","Coinbase","Trust Wallet","MetaMask","Kraken","Tether USDT","Bybit","Zwa Cash","U-Reporter","Afrimoney"]

def load_brain():
 if CLOUD_URL and requests:
  try:
   r=requests.get(CLOUD_URL,timeout=5)
   if r.status_code==200:
    d=r.json()
    # npoint wrap
    if "scams" in d: return d.get("scams",[]),Counter(d.get("patterns",{}))
    if "content" in d and isinstance(d["content"],dict): return d["content"].get("scams",[]),Counter(d["content"].get("patterns",{}))
  except: pass
 if os.path.exists(BRAIN_FILE):
  try:
   with open(BRAIN_FILE,"r",encoding="utf-8") as f: d=json.load(f); return d.get("scams",[]),Counter(d.get("patterns",{}))
  except: pass
 return [],Counter()

def save_brain():
 data={"scams":SCAMS,"patterns":dict(PATTERNS),"version":"V12.3 CLOUD 45","banks":len(BANKS)}
 try:
  with open(BRAIN_FILE,"w",encoding="utf-8") as f: json.dump(data,f,ensure_ascii=False)
 except: pass
 if CLOUD_URL and requests:
  try: requests.post(CLOUD_URL,json=data,timeout=5)
  except: pass

SCAMS,PATTERNS=load_brain()
STOP={"avec","pour","vous","votre","dans","les","des","une","est","sont"}

def learn(txt):
 ws=re.findall(r'\w{3,}',txt.lower())
 for w in ws:
  if w not in STOP: PATTERNS[w]+=1
 if txt not in SCAMS and len(txt)>10: SCAMS.append(txt[:250])
 save_brain()

def scan(txt):
 low=txt.lower(); s=0; r=[]
 for b in BANKS:
  if b.lower() in low: s+=18; r.append(b)
 for w,c in PATTERNS.most_common(50):
  if w in low: s+=min(c*3,15)
 if "http" in low or "bit.ly" in low: s+=10
 s=min(s,99)
 v="SCAM DETECTED" if s>=65 else "SUSPECT" if s>=30 else "SAFE"
 return s,v,r

@app.route("/")
def home():
 cloud="☁️ CLOUD CONNECTÉ - IMMORTEL" if CLOUD_URL else "💾 LOCAL - Retombera à 0 au deploy - Active /setup"
 return f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#000;color:#fff;text-align:center;font-family:Arial;padding:20px}} .b{{background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;padding:12px 20px;border-radius:30px;text-decoration:none;font-weight:900;display:inline-block;margin:5px}} .ok{{color:#00ff88;border:1px solid #00ff88;border-radius:30px;padding:10px;display:inline-block;font-size:11px}}</style></head><body><h1>SCAMBUSTER <span style='color:#00ff88'>AI</span></h1><div class='ok'>✅ V12.3 CLOUD 45 - {len(BANKS)} BANQUES+FINTECHS - {len(SCAMS)} SCAMS - {cloud}</div><p>ORIGIN: LUBUMBASHI | MINE: THE WORLD</p><p style='font-size:10px;color:#888'>{', '.join(BANKS[:7])}... +{len(BANKS)-7} Fintechs</p><a href='/scan' class='b'>SCANNER</a> <a href='/banks' class='b'>{len(BANKS)} BANQUES</a> <a href='/learned' class='b'>CERVEAU {len(SCAMS)}</a> <a href='/setup' class='b'>SETUP CLOUD</a><br><br><p style='color:#555;font-size:10px'>V12.3 CLOUD 45 - brain.json + cloud</p></body></html>"

@app.route("/scan",methods=["GET","POST"])
def sp():
 res=""
 if request.method=="POST":
  txt=request.form.get("text",""); fb=request.form.get("fb","")
  if fb=="scam" and txt: learn(txt); res=f"<div style='border:2px solid #00ff88;padding:15px;margin:15px;border-radius:12px'><h2 style='color:#00ff88'>☁️ GRAVÉ! TOTAL {len(SCAMS)}</h2><p>{'CLOUD' if CLOUD_URL else 'LOCAL'} - {len(PATTERNS)} patterns</p></div>"
  else:
   s,v,r=scan(txt); res=f"<div style='border:2px solid #ffaa00;padding:15px;margin:15px;border-radius:12px'><h2>{v} {s}%</h2><p>{' | '.join(r[:5])}</p><form method='POST'><input type='hidden' name='text' value='{txt}'><button name='fb' value='scam' style='background:#ff2a2a;color:#fff;padding:10px 20px;border:none;border-radius:20px;font-weight:900'>☁️ OUI GRAVE DANS LE CLOUD!</button></form></div>"
 return f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#000;color:#fff;text-align:center;padding:15px;font-family:Arial}} textarea{{width:90%;max-width:500px;height:100px;background:#111;color:#fff;border:1px solid #00ff88;border-radius:10px;padding:10px}}</style></head><body><a href='/' style='color:#00ccff'>← WORLD</a><h1>SCAN V12.3 CLOUD 45</h1><form method='POST'><textarea name='text' placeholder='Colle scam...'></textarea><br><button style='background:#00ff88;padding:12px 25px;border-radius:30px;border:none;font-weight:900;margin-top:10px'>ANALYSER</button></form>{res}</body></html>"

@app.route("/banks")
def bp():
 rows="".join([f"<tr><td>{i+1}</td><td>{b}</td><td>{'BANQUE' if i<17 else 'FINTECH' if i<27 else 'MOBILE MONEY' if i<37 else 'CRYPTO' if i<43 else 'DRC FINTECH'}</td><td>🔴</td></tr>" for i,b in enumerate(BANKS)])
 return f"<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{{background:#000;color:#fff;text-align:center;font-family:Arial;padding:15px}} table{{width:98%;max-width:800px;margin:auto;border-collapse:collapse;background:#111;border-radius:10px;overflow:hidden;font-size:11px}} th{{background:#00ff88;color:#000;padding:8px}} td{{padding:7px;border-bottom:1px solid #222}}</style></head><body><a href='/' style='color:#00ccff'>← WORLD</a><h1>🏦 {len(BANKS)} BANQUES + FINTECHS + MOBILE MONEY</h1><table><tr><th>#</th><th>Nom</th><th>Type</th><th>Risque</th></tr>{rows}</table></body></html>"

@app.route("/learned")
def lp():
 top=PATTERNS.most_common(30); pat="".join([f"<div>{w}-{c}</div>" for w,c in top]); scams="".join([f"<div style='background:#111;padding:10px;margin:5px;border-radius:8px;text-align:left'>🔴 {s}</div>" for s in SCAMS[-10:][::-1]])
 return f"<html><body style='background:#000;color:#fff;text-align:center;font-family:Arial;padding:20px'><a href='/' style='color:#00ccff'>← WORLD</a><h1>CERVEAU {len(SCAMS)} - {len(BANKS)} BANKS CLOUD={'ON' if CLOUD_URL else 'OFF'}</h1>{scams}<h3>PATTERNS {len(PATTERNS)}</h3>{pat}</body></html>"

@app.route("/setup")
def setup():
 return "<html><head><meta name='viewport' content='width=device-width,initial-scale=1'><style>body{background:#000;color:#fff;font-family:Arial;padding:20px;line-height:1.7} a{color:#00ccff} .box{background:#111;border:1px solid #00ff88;border-radius:12px;padding:15px;margin:15px auto;max-width:600px} code{background:#222;padding:3px 6px;border-radius:4px;color:#00ff88}</style></head><body><a href='/'>← WORLD</a><h1>☁️ SETUP CLOUD 45 - 20 SECONDES</h1><div class='box'><h3>Pour ne PLUS JAMAIS retomber à 0:</h3><p>1. Va sur <a href='https://www.npoint.io/' target='_blank'>npoint.io</a> → Create → colle <code>{\"scams\":[],\"patterns\":{}}</code> → Create</p><p>2. Copie le lien genre <code>https://api.npoint.io/xxxxxx</code></p><p>3. Sur Render.com → pire-v7 → Environment → Add Variable<br>Name: <code>BRAIN_CLOUD_URL</code><br>Value: ton lien npoint</p><p>4. Save → Deploy → Ton site affichera ☁️ CLOUD CONNECTÉ - IMMORTEL</p><p>5. Après, même 100 deploys, tes scams restent!</p></div></body></html>"

@app.route("/health")
def hl(): return f"V12.3 CLOUD 45 OK {len(BANKS)} BANKS {len(SCAMS)} SCAMS CLOUD={bool(CLOUD_URL)}"
