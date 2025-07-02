from fastapi.responses import ORJSONResponse
from uvicorn import run
from fastapi import FastAPI

from app.core import lifespan
from app.backend import generate_user_id_router, translater_router


app = FastAPI(
    title="Smart Translater",
    default_response_class=ORJSONResponse,
    lifespan=lifespan
)
app.include_router(generate_user_id_router)
app.include_router(translater_router)


if __name__ == '__main__':
    run(
        app="app.main:app", port=8000, host="127.0.0.1",
        reload=False, use_colors=True
    )
