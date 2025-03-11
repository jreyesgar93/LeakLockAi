from os import getenv
from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "LeakLock AI"
    mode: str
    dbpath: str

    class Config:
        env_file = f"leak_lock_ai/envs/{getenv('MODE')}.env"

