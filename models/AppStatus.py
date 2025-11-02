from pydantic import BaseModel
import fastapi_pagination

class AppStatus(BaseModel):
    status: str
