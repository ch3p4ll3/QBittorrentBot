from pydantic import BaseModel, field_validator


class Telegram(BaseModel):
    bot_token: str
    api_id: int
    api_hash: str

    @field_validator('bot_token')
    def bot_token_validator(cls, v):
        if not v or not v.strip():
            raise ValueError('Bot token cannot be empty')
        return v

    @field_validator('api_hash')
    def api_hash_validator(cls, v):
        if not v or not v.strip():
            raise ValueError('API HASH cannot be empty')
        return v
