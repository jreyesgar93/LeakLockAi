from fastapi import FastAPI, HTTPException
from leak_lock_ai.utils.settings import Settings
from leak_lock_ai.routers import predictions, sensors, chatgpt


app = FastAPI()
settings = Settings()


@app.get("/")
async def root():
    return {"message": f"Hello to LeakLock Ai API in {settings.mode}"}


app.include_router(predictions.router, prefix="/api/v1")
app.include_router(chatgpt.router, prefix="/api/v1")
app.include_router(sensors.router, prefix="/api/v1")
