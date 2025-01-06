import json
import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SECRET_FILE = os.path.join(BASE_DIR, 'secrets.json')

try:
    with open(SECRET_FILE, 'r') as file:
        secrets = json.load(file)
except (FileNotFoundError, json.JSONDecodeError) as e:
    raise Exception(f"Error loading secrets.json: {e}")

db_info = secrets.get("DB", {})
if not db_info:
    raise Exception("Database configuration not found in secrets.json")

DATABASE_URL = f"mysql+pymysql://{db_info.get('user')}:{db_info.get('password')}@{db_info.get('host')}:{db_info.get('port')}/{db_info.get('database')}?charset=utf8"

# echo=True -> SQLAlchemy가 실행하는 실제 SQL 쿼리를 콘솔에 출력
engine = create_engine(DATABASE_URL, echo=True)

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    """데이터베이스 초기화"""
    from models.game import Base  # 모델 임포트
    Base.metadata.create_all(bind=engine)

def get_db():
    """FastAPI의 Dependency로 사용할 DB 세션 스코프 함수"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()