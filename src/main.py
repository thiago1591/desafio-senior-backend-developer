from fastapi import FastAPI
from src.database import init_tortoise
from src.otel_setup import configure_tracer
from src.routes import api_router

app = FastAPI()
configure_tracer(app)

init_tortoise(app)

app.include_router(api_router)

@app.get("/")
def read_root():
    return {"message": "API FastAPI iniciada com sucesso!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
