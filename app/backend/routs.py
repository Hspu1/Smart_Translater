from fastapi import APIRouter
from sqlalchemy import insert

from app.core import async_session_maker, UserModel

generate_user_id_router = APIRouter()


@generate_user_id_router.post("/generate_user_id", status_code=201)
async def generate_user_id():
    async with async_session_maker() as session:
        async with session.begin():
            stmt = insert(UserModel).returning(UserModel.id)

            result = await session.execute(stmt)
            user_id = result.scalar_one()
            return {
                "user_id": user_id
            }
