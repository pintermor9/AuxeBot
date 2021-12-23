from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def index():
    with open("web/index.html") as f:
        return f.read()
