from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/')
def index():
    with open("web/index.html") as f:
        return HTMLResponse(f.read())
