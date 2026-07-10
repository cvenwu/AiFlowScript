from fastapi import FastAPI

app = FastAPI(title="FastAPI Demo", version="0.1.0")


@app.get("/")
def read_root():
    return {"message": "Hello FastAPI"}


@app.get("/healthz")
def health_check():
    return {"status": "ok"}