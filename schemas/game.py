import datetime
from pydantic import BaseModel

class GameStartRequest(BaseModel):
    room_code: str
    player1_id: int 
    player2_id: int

    class Config:
        from_attributes = True

class GameStatusResponse(BaseModel):
    id: int
    room_code: str
    status: str
    attacker: int
    opponent: int
    attack_position_x: str
    attack_position_y: int

    class Config:
        from_attributes = True

class AttackStatusResponse(BaseModel):
    id: int
    room_code: str
    attacker: int
    opponent: int
    attack_position_x: str
    attack_position_y: int
    is_attacked: str

class AttackRequest(BaseModel):
    room_code: str
    attacker: int
    opponent: int
    attack_position_x: str
    attack_position_y: int

    class Config:
        from_attributes = True

class DamageRequest(BaseModel):
    room_code: str
    attack_position_x: str
    attack_position_y: int
    is_attacked: str
    is_finished: bool

    class Config:
        from_attributes = True
