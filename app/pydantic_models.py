from typing import *
import datetime
from dateutil import parser

from pydantic import BaseModel, validator


class ResponseContent(BaseModel):
    data: Any
    status: str
    error_message: Optional[Union[str, None]] = None


class NewCalorieEntry(BaseModel):
    calories: int
    timestamp: int

    @validator("timestamp")
    def validate_and_convert_date(cls, v):
        if not isinstance(v, int):
            if isinstance(v, str):
                v = int(parser.parse(v).timestamp())
            else:
                v = int(v)
        return v


class EditEntry(BaseModel):
    document_id: str
    updatedDocument: Dict
    index: str = "road83-metric-logs"


class DeleteEntry(BaseModel):
    document_id: str
    index: str = "road83-metric-logs"

