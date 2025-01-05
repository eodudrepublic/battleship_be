# models.py
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

class AppUser(Base):
    __tablename__ = "app_users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String(20), nullable=False)
    nickname = Column(String(20), nullable=False)
    profile_image_url = Column(String(100), nullable=True)