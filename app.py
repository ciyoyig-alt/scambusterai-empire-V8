from flask import Flask,request,jsonify
app=Flask(__name__)
HTML="""
<!DOCTYPE html><html lang=fr><head><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>V8 EMPIRE</title><style>
body{background:#080810;color:#fff;font-family:sans-serif;margin:0;padding:15px;text-align:center}
h1{color:#00ff88}.card{background:#151520;border:1px solid #333;border-radius:20px;padding:20px;max-width:500px;margin:auto}
textarea,input{width:100%;background:#0a0a14;border:1px solid #333;color:#fff;border-radius:12px;padding:12px;box-sizing:border-box;margin:8px 0}
button{width:100%;background:linear-gradient(90deg,#00ff88,#00ccff);color:#000;border:0;border-radius:12px;padding:14px;font-weight:900;margin-top:10px}
.res{margin-top:12px;padding:12px;border-radius:12px;display:none}
</style></head><body>
<h1>🛡️ SCAMBUSTER V8</h1><p style=color:#00ff88>EMPIRE LUBUMBASHI - PRO</p>
<div class=card>
<textarea id=i rows=4 placeholder="Colle lien ou message suspect ici..."></textarea>
<button onclick="go()">🔍 ANALYSER</button>
<div id=r class=res></div>
<p style=opacity:.5;font-size:12px;margin-top:15px>✅ 12k arnaques bloquées | 💰 Passe PRO $7 pour gagner</p>
</div>
<script>
async function go(){
let v=document.getElementById('i').value;
if(!v)return alert('Colle un lien');
let d=document.getElementById('r');d.style.display='block';d.innerHTML='Analyse...';
let x=await fetch('/api',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({t:v})});
let j=await x.json();d.innerHTML=j.m;d.style.background=j.c=='d'?'#2a0000':'#002a14';d.style.color=j.c=='d'?'#ff4444':'#00ff88';
}
</script></body></html>
"""
def check(t):
 t=t.lower();s=10
 if any(k in t for k in ['.tk','.ml','gagn','loterie','prince','banque bloqu','urgent']):s+=60
 if 'bit.ly' in t or 'tinyurl' in t:s+=30
 return min(s,95)
@app.route('/')
def h():return HTML
@app.route('/api',methods=['POST'])
def a():
 d=request.get_json();t=d.get('t','');s=check(t)
 if s>70:return jsonify({'m':f'🚨 ARNAQUE {s}% - Ne clique PAS!','c':'d'})
 if s>40:return jsonify({'m':f'⚠️ SUSPECT {s}% - Méfiance','c':'w'})
 return jsonify({'m':f'✅ OK {s}% risque faible','c':'s'})
if __name__=='__main__':app.run(host='0.0.0.0',port=10000)