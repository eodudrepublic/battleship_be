# invite_router.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from random import choice
from uuid import uuid4

from schemas.game import GameStartRequest, GameStatusResponse, AttackStatusResponse, AttackRequest, DamageRequest
from schemas.invite import InviteStatusRequest, JoinRequest
from models.user import AppUser
from models.game import GameRoom, Attack
from database import get_db

router = APIRouter()

@router.post("/create")
def start_game(host_id: int=Query(...), db: Session = Depends(get_db)):
    """초대 링크 생성"""
    # 초대한 사람의 id가 app_users에 있는지 확인
    # is_appuser = db.query(AppUser).filter(AppUser.user_id == host_id).first()
    # if not is_appuser:
    #     raise HTTPException(status_code=400, detail="Unregistered User")

    # 이미 참여 중인 게임이 있는지 확인
    is_player1 = db.query(GameRoom).filter(GameRoom.player_first == host_id).first()
    is_player2 = db.query(GameRoom).filter(GameRoom.player_last == host_id).first()

    if (is_player1 or is_player2):
        return {"message": "already exists"}

    created_room_code = str(uuid4())[:8]

    new_room = GameRoom(
        room_code = created_room_code,
        status = "before",
        player_first = host_id,
        player_last = 0,
        first_board = [],
        last_board = []
    )

    new_attack = Attack(
        room_code = created_room_code,
        attacker = host_id,
        opponent = 0,
        attack_position = "",
        damage_status = 'not yet'
    )
    db.add(new_room)
    db.add(new_attack)
    db.commit()
    db.refresh(new_room)
    db.refresh(new_attack)

    return {"room_code": created_room_code}

@router.get("/join-room")
def join_room_via_link(room_code: str = Query(...), invited_id: int = Query(...), db:Session = Depends(get_db)):
    """초대 링크 통해 참가"""
    # 초대받은 사람의 id가 app_users에 있는지 확인
    # is_appuser = db.query(AppUser).filter(AppUser.user_id == invited_id).first()
    # if not is_appuser:
    #     raise HTTPException(status_code=400, detail="Unregistered User")

    # 이미 참여 중인 게임이 있는지 확인
    is_player1 = db.query(GameRoom).filter(GameRoom.player_first == invited_id).first()
    is_player2 = db.query(GameRoom).filter(GameRoom.player_last == invited_id).first()

    if (is_player1 or is_player2):
        return {"message": "already exists"}
    
    room = db.query(GameRoom).filter(GameRoom.room_code == room_code).first()
    attack = db.query(Attack).filter(Attack.room_code == room_code).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    if not attack:
        raise HTTPException(status_code=404, detail="Room not found")


    first_player = choice([room.player_first, invited_id])
    last_player = invited_id if first_player == room.player_first else room.player_first

    room.status = "in_progress"
    room.player_first = first_player
    room.player_last = last_player
    attack.attacker = first_player
    attack.opponent = last_player

    db.commit()
    db.refresh(room)
    
    if (invited_id == first_player):
        return {
            "is_matched": True,
            "room_code": room_code,
            "opponent": last_player,
            "is_first": True
        }
    elif (invited_id == last_player):
        return {
            "is_matched": True,
            "room_code": room_code,
            "opponent": first_player,
            "is_first": False
        }
    else:
        return {"message": "user not found"}

@router.get("/invitation-status")
def get_invitation_status(room_code: str = Query(...), host_id: int = Query(...), db: Session = Depends(get_db)):
    room = db.query(GameRoom).filter(GameRoom.room_code == room_code).first()
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
    
    
    if (room.status == "before"):
        return {
            "is_matched": False,
            "room_code": "",
            "opponent": 0,
            "is_first": False
        }
    else:
        if (host_id == room.player_first):
            return {
                "is_matched": True,
                "room_code": room_code,
                "opponent": room.player_last,
                "is_first": True
                }
        elif (host_id == room.player_last):
            return {
                "is_matched": True,
                "room_code": room_code,
                "opponent": room.player_first,
                "is_first": False
            }
        else:
            return {"message": "user not found"}