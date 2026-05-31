from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routers.task import router as tasks_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Tasks API")

app.include_router(tasks_router, prefix="/tasks", tags=["Tasks"])


@app.get("/")
def root():
    return {"message": "Tasks API is running"}
