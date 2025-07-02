from pydantic import BaseModel, constr


class TranslatedRequest(BaseModel):
    user_id: int
    original_text: constr(
        strip_whitespace=True, min_length=1, max_length=500
    )  # strip_whitespace убирает пробелы с начала и с конца
