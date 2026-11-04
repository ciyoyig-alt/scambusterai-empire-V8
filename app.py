@app.get("/")
def home():
    return jsonify(status="ScamBusterAI Empire V8 is LIVE", health="/health", version="V8")import os, re, hashlib, datetime
from functools import wraps
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from sqlalchemy import (create_engine, MetaData, Table, Column, Integer, String,
                        Text, DateTime, select, insert, update, func)
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
limiter = Limiter(get_remote_address, app=app, default_limits=["60/minute"])

# --- Base de données (PostgreSQL sur Render, SQLite en local) ---
DB_URL = os.environ.get("DATABASE_URL", "sqlite:///scambuster.db")
if DB_URL.startswith("postgres://"):
    DB_URL = DB_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DB_URL, pool_pre_ping=True)
md = MetaData()
scams = Table("scams", md,
    Column("id", Integer, primary_key=True),
    Column("text", Text, nullable=False),
    Column("hash", String(64), unique=True, index=True),
    Column("category", String(50), index=True),
    Column("created_at", DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc)))
patterns = Table("patterns", md,
    Column("word", String(60), primary_key=True),
    Column("count", Integer, default=1, index=True))
md.create_all(engine)

# --- Clés API : variable d'environnement API_KEYS="cle1,cle2" ---
API_KEYS = {k.strip() for k in os.environ.get("API_KEYS", "").split(",") if k.strip()}

def require_key(f):
    @wraps(f)
    def wrapper(*a, **kw):
        if request.headers.get("X-API-Key") not in API_KEYS:
            return jsonify(error="invalid or missing API key"), 401
        return f(*a, **kw)
    return wrapper

BANKS = ["JPMorgan Chase","Bank of America","HSBC","Barclays","BNP Paribas","Deutsche Bank",
 "Standard Chartered","Ecobank","UBA","GTBank","First Bank Nigeria","Access Bank","KCB Bank",
 "Equity Bank","Rawbank","Equity BCDC","TMB","PayPal","Wise","Revolut","Venmo","Cash App","Zelle",
 "Payoneer","Stripe","Skrill","Neteller","M-Pesa","Airtel Money","Orange Money","MTN MoMo","Wave",
 "GCash","Paytm","MoMo","Binance","Coinbase","Trust Wallet","MetaMask","Kraken","Tether USDT",
 "Bybit","Zwa Cash","U-Reporter","Afrimoney"]
STOP = {"avec","pour","vous","votre","dans","les","des","une","est","sont"}

def analyze(txt):
    low = txt.lower(); score = 0; reasons = []
    for b in BANKS:
        if b.lower() in low:
            score += 18; reasons.append(f"mentions {b}")
    with engine.connect() as c:
        top = c.execute(select(patterns.c.word, patterns.c.count)
                        .order_by(patterns.c.count.desc()).limit(50)).all()
    for w, n in top:
        if w in low:
            score += min(n * 3, 15)
    if "http" in low or "bit.ly" in low:
        score += 10; reasons.append("contains link")
    score = min(score, 99)
    verdict = "SCAM" if score >= 65 else "SUSPECT" if score >= 30 else "SAFE"
    return score, verdict, reasons

def get_text():
    data = request.get_json(silent=True) or {}
    txt = (data.get("text") or "").strip()
    return txt[:2000], (data.get("category") or "other")[:50]

@app.post("/v1/analyze")
@require_key
def api_analyze():
    txt, _ = get_text()
    if len(txt) < 5:
        return jsonify(error="'text' is required (min 5 chars)"), 400
    score, verdict, reasons = analyze(txt)
    return jsonify(score=score, verdict=verdict, reasons=reasons)

@app.post("/v1/scams")
@require_key
@limiter.limit("30/minute")
def api_add():
    txt, cat = get_text()
    if len(txt) < 10:
        return jsonify(error="'text' is required (min 10 chars)"), 400
    h = hashlib.sha256(txt.lower().encode()).hexdigest()
    try:
        with engine.begin() as c:
            c.execute(insert(scams).values(text=txt, hash=h, category=cat))
            for w in set(re.findall(r"\w{3,60}", txt.lower())) - STOP:
                r = c.execute(update(patterns).where(patterns.c.word == w)
                              .values(count=patterns.c.count + 1))
                if r.rowcount == 0:
                    c.execute(insert(patterns).values(word=w, count=1))
    except IntegrityError:
        return jsonify(status="duplicate"), 200
    return jsonify(status="stored"), 201

@app.get("/v1/scams")
@require_key
def api_list():
    limit = min(int(request.args.get("limit", 20)), 100)
    offset = int(request.args.get("offset", 0))
    with engine.connect() as c:
        rows = c.execute(select(scams).order_by(scams.c.id.desc())
                         .limit(limit).offset(offset)).mappings().all()
    return jsonify(items=[{"id": r["id"], "text": r["text"], "category": r["category"],
                           "created_at": r["created_at"].isoformat()} for r in rows])

@app.get("/v1/stats")
@require_key
def api_stats():
    with engine.connect() as c:
        n = c.execute(select(func.count()).select_from(scams)).scalar()
        p = c.execute(select(func.count()).select_from(patterns)).scalar()
    return jsonify(scams=n, patterns=p, capacity=1_000_000, banks=len(BANKS))

@app.get("/health")
def health():
    return "OK"
