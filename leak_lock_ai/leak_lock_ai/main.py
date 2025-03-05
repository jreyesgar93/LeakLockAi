from fastapi import FastAPI
from leak_lock_ai.utils.settings import Settings


app = FastAPI()
settings = Settings()


@app.get("/")
async def root():
    return {"message": f"Hello World, {settings.mode}"}
