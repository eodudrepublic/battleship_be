import datetime
from pydantic import BaseModel
from typing import List

class GameStartRequest(BaseModel):
    room_code: str
    player1_id: int 
    player2_id: int

    class Config:
        from_attributes = True

class GameStatusResponse(BaseModel):
    room_code: str
    status: str
    attacker: int
    opponent: int
    attack_position: str

    class Config:
        from_attributes = True


class AttackRequest(BaseModel):
    room_code: str
    attacker: int
    opponent: int
    attack_position: str

    class Config:
        from_attributes = True

class AttackStatusResponse(BaseModel):
    room_code: str
    attacker: int
    opponent: int
    attack_position: str
    damage_status: str
    game_status: str
    
    class Config:
        from_attributes = True

class DamageRequest(BaseModel):
    room_code: str
    attack_position: str
    damage_status: str
    is_finished: bool

    class Config:
        from_attributes = True

class BoardInfo(BaseModel):
    room_code: str
    user_id: int
    board: List[str]    
    
    class Config:
        from_attributes = True