from sqlalchemy import Column, Integer, String, Enum, String, Boolean, BigInteger
from models import Base

class GameRoom(Base):
    __tablename__ = "games"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    room_code = Column(String(20), unique=True, nullable=False)
    status = Column(Enum('before', 'in_progress', 'completed'), nullable=False)
    player_first = Column(BigInteger, nullable=False)      # 현재 turn인 AppUser의 id
    player_last = Column(BigInteger, nullable=False)
    is_finished = False

class Attack(Base):
    __tablename__ = "attacks"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    room_code = Column(String(20), unique=True, nullable=False) 
    attacker = Column(BigInteger, nullable=False)
    opponent = Column(BigInteger, nullable=False)
    attack_position_x = Column(String(1), nullable=True)
    attack_position_y = Column(BigInteger, nullable=True)
    attack_status = Column(Enum('not yet', 'attack'))
    damage_status = Column(Enum('not yet', 'damaged', 'missed'))