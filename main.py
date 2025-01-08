# main.py
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import game_router
import user_router
import invite_router


from database import init_db

init_db()
app = FastAPI()

app.include_router(user_router.router, prefix="/users", tags=["Users"])
app.include_router(game_router.router, prefix="/games", tags=["Games"])
app.include_router(invite_router.router, prefix="/invite", tags=["Invite"])

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 모든 도메인 허용. 보안이 중요하다면 특정 도메인으로 제한.
    allow_credentials=True,  # 쿠키를 포함한 자격 증명 허용
    allow_methods=["*"],  # 모든 HTTP 메서드 허용 (GET, POST, PUT 등)
    allow_headers=["*"],  # 모든 헤더 허용
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the BattleShip API"}

@app.get("/hello")
def hello():
    return {"message" : "Hello World!"}