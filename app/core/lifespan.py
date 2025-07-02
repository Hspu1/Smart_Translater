from fastapi import FastAPI
from redis.asyncio import Redis

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = Redis(host="127.0.0.1", port=6379, decode_responses=True)
    yield

    await app.state.redis.aclose()
