from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return "<h1 style='background:black;color:#00ff88;padding:100px;text-align:center'>SCAMBUSTERAI V9 ULTRA IS COMING...<br><br>Deploy SUCCESS! Maintenant on met l'ecran geant!</h1>"

@app.get("/health")
def health():
    return {"status": "OK"}
