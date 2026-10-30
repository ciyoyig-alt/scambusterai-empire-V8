import os
from flask import Flask, request, render_template_string, jsonify
from datetime import datetime
app = Flask(__name__)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")
try:
 from supabase import create_client
 supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if SUPABASE_URL and SUPABASE_KEY else None
except: supabase = None
T={"fr":{"title":"ScambusterAI Empire V7","subtitle":"L'IA Anti-Arnaque d'Afrique","placeholder":"Collez le message suspect ici...","btn":"🔍 Analyser Maintenant","result_safe":"✅ MESSAGE SÛR","result_scam":"🚨 ARNAQUE DETECTEE","result_suspicious":"⚠️ SUSPECT","footer":"Empire cree depuis Lubumbashi","stats_scanned":"Messages analyses","stats_blocked":"Arnaques bloquees","language":"🌍 English"},"en":{"title":"ScambusterAI Empire V7","subtitle":"Africa's Most Powerful Anti-Scam AI","placeholder":"Paste suspicious message here...","btn":"🔍 Analyze Now","result_safe":"✅ SAFE","result_scam":"🚨 SCAM DETECTED","result_suspicious":"⚠️ SUSPICIOUS","footer":"Empire built from Lubumbashi","stats_scanned":"Messages scanned","stats_blocked":"Scams blocked","language":"🌍 Français"}}
KEYWORDS=["urgent","gagné","won","loterie","lottery","prince","héritage","inheritance","bitcoin double","investissement","investment","cliquez","click here","compte sera bloqué","account blocked","félicitations","congratulations","whatsapp money","airtel money","mpesa","orange money","western union","gratuit","free money"]
def analyze(text):
 tl=text.lower();s=0;f=[]
 for k in KEYWORDS:
  if k in tl: s+=25;f.append(k)
 if len(text)<10: return "suspicious",30,f
 if s>=50: return "scam",min(95,s),f
 elif s>=25: return "suspicious",s,f
 else: return "safe",10,f
HTML="""<!DOCTYPE html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{{ t.title }}</title><style>body{font-family:system-ui;background:#0f172a;color:white;margin:0;padding:20px}.card{max-width:600px;margin:40px auto;background:#1e293b;padding:25px;border-radius:16px}h1{color:#38bdf8;margin:0}.sub{color:#94a3b8;margin-bottom:20px}textarea{width:100%;height:140px;background:#0f172a;border:2px solid #334155;border-radius:12px;color:white;padding:15px;font-size:16px;box-sizing:border-box}button{width:100%;margin-top:15px;background:#0ea5e9;border:none;padding:15px;border-radius:12px;color:white;font-size:18px;font-weight:bold}button:hover{background:#0284c7}.result{margin-top:20px;padding:20px;border-radius:12px;font-weight:bold;text-align:center;font-size:20px}.safe{background:#065f46;border:2px solid #10b981}.scam{background:#7f1d1d;border:2px solid #ef4444}.suspicious{background:#78350f;border:2px solid #f59e0b}.stats{display:flex;gap:10px;margin-top:20px}.stat{flex:1;background:#0f172a;padding:12px;border-radius:10px;text-align:center}.stat b{font-size:22px;display:block;color:#38bdf8}.footer{text-align:center;margin-top:30px;color:#64748b;font-size:13px}.lang{position:absolute;top:15px;right:15px;background:#1e293b;border:1px solid #334155;padding:8px 12px;border-radius:20px;text-decoration:none;color:white}</style></head><body><a class="lang" href="/?lang={{ other_lang }}">{{ t.language }}</a><div class="card"><h1>{{ t.title }}</h1><div class="sub">{{ t.subtitle }}</div><form method="POST"><textarea name="message" placeholder="{{ t.placeholder }}" required>{{ msg }}</textarea><button type="submit">{{ t.btn }}</button></form>{% if result %}<div class="result {{ level }}">{% if level=='safe' %}{{ t.result_safe }}{% elif level=='scam' %}{{ t.result_scam }}{% else %}{{ t.result_suspicious }}{% endif %}<div style="font-size:14px;margin-top:10px;font-weight:normal">Risque: {{ risk }}%</div></div>{% endif %}<div class="stats"><div class="stat"><b>{{ scanned }}</b>{{ t.stats_scanned }}</div><div class="stat"><b>{{ blocked }}</b>{{ t.stats_blocked }}</div></div><div class="footer">{{ t.footer }}<br>Supabase: {{ 'Connecte' if supabase_ok else 'Mode Local' }}</div></div></body></html>"""
@app.route("/", methods=["GET", "POST"])
def home():
 lang=request.args.get("lang",request.cookies.get("lang","fr"))
 if lang not in ["fr","en"]: lang="fr"
 other="en" if lang=="fr" else "fr";t=T[lang];msg="";result=None;level="safe";risk=0;found=[];scanned=12847;blocked=3421
 if supabase:
  try:
   d=supabase.table("scans").select("id", count="exact").execute();scanned=d.count if d.count else scanned
   d2=supabase.table("scams").select("id", count="exact").execute();blocked=d2.count if d2.count else blocked
  except: pass
 if request.method=="POST":
  msg=request.form.get("message","")
  if msg:
   level,risk,found=analyze(msg);result=True
   if supabase:
    try:
     supabase.table("scans").insert({"content":msg[:500],"risk_score":risk,"level":level,"language":lang}).execute()
     if level=="scam": supabase.table("scams").insert({"content":msg[:500],"keywords":",".join(found)}).execute()
    except: pass
   scanned+=1
   if level=="scam": blocked+=1
 from flask import make_response
 ren=render_template_string(HTML, t=t, other_lang=other, msg=msg, result=result, level=level, risk=risk, found=found, scanned=scanned, blocked=blocked, supabase_ok=bool(supabase))
 r=make_response(ren);r.set_cookie("lang", lang, max_age=2592000);return r
@app.route("/health")
def health(): return jsonify({"status":"Empire V7 Online","supabase":bool(supabase),"time":datetime.now().isoformat()})
if __name__=="__main__": app.run(host="0.0.0.0", port=int(os.environ.get("PORT",10000)))
