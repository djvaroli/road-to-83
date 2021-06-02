from typing import *

from pydantic import BaseModel


class ResponseContent(BaseModel):
    data: Any
    status: str
    error_message: Optional[Union[str, None]] = None

