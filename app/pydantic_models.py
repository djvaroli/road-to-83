from typing import *

from pydantic import BaseModel


class ResponseContent(BaseModel):
    data: Any
    status: str
    error_message: Optional[Union[str, None]] = None


class NewCalorieEntry(BaseModel):
    calories: int


class EditEntry(BaseModel):
    document_id: str
    updatedDocument: Dict
    index: str = "road83-metric-logs"


class DeleteEntry(BaseModel):
    document_id: str
    index: str = "road83-metric-logs"

