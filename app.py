import os, re, hashlib, datetime
from functools import wraps
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Text, DateTime, Boolean, select, insert, func
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["60/minute"])

# --- DB ---
DB_URL = os.environ.get("DATABASE_URL", "sqlite:///scambuster.db")
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DB_URL, pool_pre_ping=True)
md = MetaData()

scams = Table("scams", md,
    Column("id", Integer, primary_key=True),
    Column("text", Text, nullable=False),
    Column("hash", String(64), unique=True),
    Column("category", String(50)),
    Column("created_at", DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)))

reports = Table("reports", md,
    Column("id", Integer, primary_key=True),
    Column("text", Text, nullable=False),
    Column("category", String(50)),
    Column("score", Integer),
    Column("verdict", String(20)),
    Column("blocked", Boolean, default=False),
    Column("created_at", DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)))

md.create_all(engine)

API_KEYS = {k.strip() for k in os.environ.get("API_KEYS", "").split(",") if k.strip()}

def require_key(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if request.headers.get("X-API-Key") not in API_KEYS:
            return jsonify(error="invalid key"), 401
        return f(*a, **kw)
    return wrapper

# --- FILTRE MONDIAL V9 ---
BANKS = ["Rawbank","Equity BCDC","TMB","Ecobank","UBA","GTBank","Access Bank","First Bank","KCB","Equity Bank","Standard Chartered","HSBC","BNP Paribas","PayPal","Wise","Revolut","Venmo","Cash App","Zelle","Stripe","Payoneer","M-Pesa","Airtel Money","Orange Money","MTN MoMo","Wave","Binance","Coinbase","Trust Wallet","MetaMask","USDT","Tether"]

LOSS = ["perdu","perte","volé","vole","débité","debite","piraté","pirate","arnaque","escroquerie","fraude","hacked","stolen","lost money","scammed","fraud","unauthorized","compte bloqué","compte piraté","code otp","mot de passe","verify your account","vérifiez votre compte","suspended"]

URGENCE = ["urgent","immédiatement","maintenant","dans 24h","24 heures","sinon","act now","verify now","cliquez ici","click here"]

def global_filter(txt):
    low = txt.lower()
    score = 0
    reasons = []
    banks = []
    for b in BANKS:
        if b.lower() in low:
            score += 25
            banks.append(b)
            reasons.append(f"banque/fintech: {b}")
    for w in LOSS:
        if w in low:
            score += 25
            reasons.append(f"perte argent: {w}")
            break
    for w in URGENCE:
        if w in low:
            score += 15
            reasons.append(f"urgence: {w}")
            break
    if "http" in low or "bit.ly" in low or "t.me" in low or "wa.me" in low:
        score += 15
        reasons.append("contient un lien")
    score = min(score, 99)
    if score >= 65:
        return score, "SCAM", True, "BANK_FINTECH_FRAUD", banks, reasons
    if score >= 30:
        return score, "SUSPECT", False, "SUSPECT", banks, reasons
    return score, "SAFE", False, "SAFE", banks, reasons

def get_text():
    d = request.get_json(silent=True) or {}
    return (d.get("text") or "").strip()[:2000]

@app.get("/")
def home():
    return jsonify(status="ScamBusterAI V9 LIVE", filter="GLOBAL_FILTER_V9", version="V9")

@app.get("/health")
def health():
    return "OK"

@app.post("/v1/analyze")
@require_key
def analyze():
    txt = get_text()
    if len(txt) < 5:
        return jsonify(error="text min 5"), 400
    s, v, b, c, banks, reasons = global_filter(txt)
    return jsonify(score=s, verdict=v, blocked=b, category=c, banks=banks, reasons=reasons)

@app.post("/v1/report")
@require_key
@limiter.limit("30/minute")
def report():
    txt = get_text()
    if len(txt) < 10:
        return jsonify(error="text min 10"), 400
    s, v, b, c, banks, reasons = global_filter(txt)
    h = hashlib.sha256(txt.lower().encode()).hexdigest()
    try:
        with engine.begin() as conn:
            conn.execute(insert(scams).values(text=txt, hash=h, category=c))
            conn.execute(insert(reports).values(text=txt, category=c, score=s, verdict=v, blocked=b))
    except IntegrityError:
        return jsonify(status="duplicate", score=s, verdict=v, blocked=b), 200
    return jsonify(status="reported", score=s, verdict=v, blocked=b, category=c), 201

@app.get("/v1/blocked")
@require_key
def blocked_list():
    limit = min(int(request.args.get("limit", 20)), 100)
    with engine.connect() as conn:
        rows = conn.execute(select(reports).where(reports.c.blocked == True).order_by(reports.c.id.desc()).limit(limit)).mappings().all()
    return jsonify(blocked=[{"id": r["id"], "text": r["text"][:200], "score": r["score"], "category": r["category"]} for r in rows])

@app.get("/v1/stats")
@require_key
def stats():
    with engine.connect() as conn:
        n = conn.execute(select(func.count()).select_from(scams)).scalar()
        r = conn.execute(select(func.count()).select_from(reports)).scalar()
        b = conn.execute(select(func.count()).select_from(reports).where(reports.c.blocked == True)).scalar()
    return jsonify(scams=n, reports=r, blocked=b, banks=len(BANKS))
