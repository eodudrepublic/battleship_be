# models.py
from models import Base
from sqlalchemy import Column, Integer, String

class AppUser(Base):
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(20), nullable=False)
    nickname = Column(String(20), nullable=False)
    profile_image_url = Column(String(100), nullable=True)