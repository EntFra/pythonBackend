from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return "Hola"

@app.get("/url")
async def root():
    return {"url_curso":"https://www.google.es"}