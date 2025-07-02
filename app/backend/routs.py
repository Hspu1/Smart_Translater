from typing import Annotated

from fastapi import APIRouter, Request, Depends
from sqlalchemy import insert
from deep_translator import GoogleTranslator
from sqlalchemy.exc import IntegrityError

from app.backend.schemas import TranslatedRequest
from app.core import async_session_maker, UserModel, TranslationModel
from app.utils import logger

generate_user_id_router = APIRouter()
translater_router = APIRouter()


@generate_user_id_router.post(path="/generate_user_id", status_code=201)
async def generate_user_id():
    async with async_session_maker() as session:
        async with session.begin():
            stmt = insert(UserModel).returning(UserModel.id)

            result = await session.execute(stmt)
            user_id = result.scalar_one()
            return {
                "user_id": user_id
            }


@translater_router.post(path="/translater", status_code=201)
async def translater(
        input_data: Annotated[TranslatedRequest, Depends()], request: Request
):
    redis = request.app.state.redis  # берём redis клиент из lifespan
    key = (
        f"translate:{input_data.user_id}:"
        f"{input_data.original_text}"
    )

    cached_data = await redis.get(key)
    if cached_data is not None:
        return {
            "translated_text": cached_data,
            "cached": True
        }

    translated = (
        GoogleTranslator(source='auto', target="ru").translate(
            input_data.original_text)
    )

    await redis.set(key, translated, ex=86400)

    translated_data = TranslationModel(
        user_id=input_data.user_id, original_word=input_data.original_text,
        translated_word=translated
    )
    if len(input_data.original_text) <= 25:
        try:
            async with async_session_maker() as session:
                async with session.begin():
                    session.add(translated_data)

        except IntegrityError as e:
            # при написании таблиц был добавлен уникальный констрейнт
            logger.warning(f"IntegrityError при сохранении перевода: {e}")

    return {
        "translated_text": translated,
        "cached": False
    }
