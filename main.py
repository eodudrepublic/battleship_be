# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import engine
from models import Base

import controllers

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(controllers.router)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용. 보안이 중요하다면 특정 도메인으로 제한.
    allow_credentials=True,  # 쿠키를 포함한 자격 증명 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT 등)
    allow_headers=["*"],  # 모든 헤더 허용
)