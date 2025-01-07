from pydantic import BaseModel

class JoinRequest(BaseModel):
    invited_id: int
    room_code: str

    class Config:
        from_attributes = True
        
class InviteStatusRequest(BaseModel):
    host_id: int
    room_code: str

    class Config:
        from_attributes = True