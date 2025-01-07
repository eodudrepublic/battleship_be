from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from random import choice

from waiting_list_service import (
    add_user_to_waiting_list,
    remove_user_from_waiting_list,
    get_waiting_list,
    match_users,
)
from uuid import uuid4
from models.game import GameRoom, Attack
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
def match_users_route(user_id: int, db: Session = Depends(get_db)):
    matched_users = match_users()
    # 두번째로 호출하면 이게 실행됨
    # if len(matched_users) < 2: 
    #     return {
    #         "is_matched": False,
    #         "room_code": "",
    #         "opponent": 0,
    #         "is_first": False
    #     }
    created_room_code = str(uuid4())[:8]

    existing_room = db.query(GameRoom).filter(GameRoom.room_code == created_room_code).first()
    if existing_room:
        room_first = db.query(GameRoom).filter(GameRoom.player_first == user_id).first()
        if room_first:
            return {
                "is_matched": True,
                "room_code": room_first.room_code,
                "opponent": room_first.player_last,
                "is_first": True
            }
        room_last = db.query(GameRoom).filter(GameRoom.player_last == user_id).first()
        if room_last:
            return {
                "is_matched": True,
                "room_code": room_last.room_code,
                "opponent": room_last.player_first,
                "is_first": False
            }
    
    random_first = choice(matched_users)
    random_later = matched_users[1] if random_first == matched_users[0] else matched_users[0]

    new_game = GameRoom(
        room_code = created_room_code,
        status = 'in_progress',
        player_first = random_first,
        player_last = random_later,
        is_finished = False
    )

    new_attack = Attack(
        room_code = created_room_code,
        opponent = random_later,
        attacker = random_first,
        attack_position_x = "",
        attack_position_y = 0,
        attack_status = "not yet",
        damage_status = "not yet"
    )

    db.add(new_attack)
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    db.refresh(new_attack)

    room_first = db.query(GameRoom).filter(GameRoom.player_first == user_id).first()
    if room_first:
        return {
            "is_matched": True,
            "room_code": room_first.room_code,
            "opponent": room_first.player_last,
            "is_first": True
        }
    room_last = db.query(GameRoom).filter(GameRoom.player_last == user_id).first()
    if room_last:
        return {
            "is_matched": True,
            "room_code": room_last.room_code,
            "opponent": room_last.player_first,
            "is_first": False
        }
    
    return {"message" : "Added"}
