# models.py
from models import Base
from sqlalchemy import Column, BigInteger, String

class AppUser(Base):
    __tablename__ = "app_users"

    user_id = Column(BigInteger, primary_key=True, nullable=False)
    nickname = Column(String(20), nullable=False)
    profile_image_url = Column(String(100), nullable=True)