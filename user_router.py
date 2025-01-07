from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from schemas.user import AppUserRequest
from models.user import AppUser
from models.game import GameRoom


router = APIRouter()

@router.get("/hello")
def hello():
    return {"message" : "Hello World!"}
    
@router.post("/user")
def manage_user(user: AppUserRequest, db: Session = Depends(get_db)):
    existing_user = db.query(AppUser).filter(AppUser.user_id == user.user_id).first()
    if existing_user:
        return {
            "message": "User exists",
            "user": {
                "user_id": existing_user.user_id,
                "nickname": existing_user.nickname,
                "profile_image_url": existing_user.profile_image_url,
            },
        }
    else:
        new_user = AppUser(
            user_id = user.user_id,
            nickname = user.nickname,
            profile_image_url = user.profile_image_url,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "message": "User added",
            "user": {
                "user_id": new_user.user_id,
                "nickname": new_user.nickname,
                "profile_image_url": new_user.profile_image_url,
            },
        }
    
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    """모든 유저 조회"""
    users = db.query(AppUser).all()  # 동기 쿼리
    return users

# @router.get("/room-status")
# def get_user_rooms(user_id: int, db: Session = Depends(get_db)):
#     """유저가 참가 중인 방 정보 보기"""
#     is_first_player = db.query(GameRoom).filter(GameRoom.player_first == user_id).first()
#     if is_first_player:
#         return is_first_player

#     is_last_player = db.query(GameRoom).filter(GameRoom.player_last == user_id).first()
#     if is_last_player:
#         return is_last_player