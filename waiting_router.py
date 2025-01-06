from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from waiting_list_service import (
    add_user_to_waiting_list,
    remove_user_from_waiting_list,
    get_waiting_list,
    match_users,
)
from uuid import uuid4
from models.game import GameRoom
from database import get_db

router = APIRouter()

@router.post("/add")
def add_to_waiting_list(user_id: int):
    try:
        updated_list = add_user_to_waiting_list(user_id)
        return {"message": "User added", "waiting_list": updated_list}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.delete("/remove/{user_id}")
def remove_from_waiting_list(user_id: int):
    try:
        updated_list = remove_user_from_waiting_list(user_id)
        return {"message": "User removed", "waiting_list": updated_list}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/")
def get_waiting_list_route():
    return {"waiting_list": get_waiting_list()}

@router.get("/match")
def match_users_route(db: Session = Depends(get_db)):
    matched_users = match_users()
    room_code = str(uuid4())[:8]
    while (db.query(GameRoom).filter(GameRoom.room_code==room_code).first()):
        room_code = str(uuid4())[:8]
    return {
        "room_code": room_code,
        "matched_users": matched_users
    }