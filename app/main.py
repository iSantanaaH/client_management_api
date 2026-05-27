from fastapi import FastAPI

# Database Connection
from app.database.connection import Base, engine

# Routes
from app.routes.webhook_routes import router as webhook_routes
from app.routes.client_routes import router as client_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Client Management API",
    version="1.0.0"
)

app.include_router(webhook_routes)
app.include_router(client_routes)

@app.get("/")
def home():
    return {"message": "Api online"}
