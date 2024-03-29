from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routes import blockchain

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(blockchain.router)


@app.get("/health")
def home():
    return {"status": "healthy"}
