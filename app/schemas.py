from typing import Optional

from pydantic import BaseModel


class WikiUrl(BaseModel):
    url: Optional[str] = 'https://en.wikipedia.org/wiki/Artificial_intelligence'


class Message(BaseModel):
    message: str
