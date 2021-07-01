
from fastapi import FastAPI
app = FastAPI()

@app.get('/')
def index():
    return {"status": "online"}

import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8080)