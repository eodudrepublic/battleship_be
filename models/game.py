from sqlalchemy import Column, Integer, String, Enum, String
from models import Base

class GameRoom(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_code = Column(String(20), unique=True, nullable=False)
    status = Column(Enum('before', 'in_progress', 'completed'), nullable=False)
    player_first = Column(Integer, nullable=False)      # 현재 turn인 AppUser의 id
    player_last = Column(Integer, nullable=False)
    is_finished = False

class Attack(Base):
    __tablename__ = "attacks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    room_code = Column(String(20), unique=True, nullable=False) 
    attacker = Column(Integer, nullable=False)
    opponent = Column(Integer, nullable=False)
    attack_position_x = Column(String(1), nullable=False)
    attack_position_y = Column(Integer, nullable=False)
    is_attacked = Column(Enum('not yet', 'attacked', 'missed'))