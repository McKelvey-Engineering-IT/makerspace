from pydantic import BaseModel


class Settings(BaseModel):
    MESSAGE_STREAM_DELAY: int = 10
    MESSAGE_STREAM_RETRY_TIMEOUT: int = 15000
