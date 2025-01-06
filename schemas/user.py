import datetime
from pydantic import BaseModel

class AppUserRequest(BaseModel):
    user_id: str
    nickname: str
    profile_image_url: str

    class Config:
        from_attributes = True