from sqlalchemy import Column, Integer, String, Enum, String, Boolean, BigInteger, JSON
from models import Base

class GameRoom(Base):
    __tablename__ = "games"

    room_code = Column(String(20), primary_key=True, unique=True, nullable=False)
    status = Column(Enum('before', 'in_progress', 'completed'), nullable=False)
    player_first = Column(BigInteger, nullable=False)
    player_last = Column(BigInteger, nullable=False)
    first_board = Column(JSON, nullable=False)
    last_board = Column(JSON, nullable=False)


class Attack(Base):
    __tablename__ = "attacks"

    room_code = Column(String(20), primary_key=True, unique=True, nullable=False) 
    attacker = Column(BigInteger, nullable=False)
    opponent = Column(BigInteger, nullable=False)
    attack_position = Column(String(3), nullable=True)
    damage_status = Column(Enum('not yet', 'damaged', 'missed'))