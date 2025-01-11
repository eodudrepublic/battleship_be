from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from random import choice
from uuid import uuid4


from schemas.game import AttackStatusResponse, AttackRequest, BoardInfo
from models.game import GameRoom, Attack
from database import get_db
from sologame_service import create_board, create_attack_coordinate



router = APIRouter()

@router.post("/create-sologame")
def create_sologame(user_id: int, db: Session = Depends(get_db)):
    is_player1 = db.query(GameRoom).filter(GameRoom.player_first == user_id).first()
    is_player2 = db.query(GameRoom).filter(GameRoom.player_last == user_id).first()

    if (is_player1 or is_player2):
        return {"message": "already exists"}

    created_room_code = str(uuid4())[:8]

    computer_id = 0
    first_player = choice([user_id, computer_id])
    last_player = user_id if first_player == computer_id else computer_id

    new_room = GameRoom(
        room_code = created_room_code,
        status = "in_progress",
        player_first = first_player,
        player_last = last_player,
        first_board = [],
        last_board = []
    )

    if (computer_id == first_player):
        new_room.first_board = create_board()
    else:
        new_room.last_board = create_board()

    new_attack = Attack(
        room_code = created_room_code,
        attacker = first_player,
        opponent = last_player,
        attack_position = "",
        damage_status = 'not yet'
    )
    db.add(new_room)
    db.add(new_attack)
    db.commit()
    db.refresh(new_room)
    db.refresh(new_attack)

    if (user_id == first_player):
        return {
            "is_matched": True,
            "room_code": created_room_code,
            "opponent": last_player,
            "is_first": True
            }
    elif (user_id == last_player):
        return {
            "is_matched": True,
            "room_code": created_room_code,
            "opponent": first_player,
            "is_first": False
        }
    else:
        return {"message": "user not found"}


@router.post("/board")
def post_board_status(board_info: BoardInfo, db: Session = Depends(get_db)):
    current_room = db.query(GameRoom).filter(GameRoom.room_code == board_info.room_code).first()
    if not current_room:
        raise HTTPException(status_code=404, detail="Game room not found")
    
    if (board_info.user_id == current_room.player_first):
        current_room.first_board = board_info.board
    elif (board_info.user_id == current_room.player_last):
        current_room.last_board = board_info.board
    else:
        raise HTTPException(status_code=400, detail="Invalid user")
    
    db.commit()


@router.post("/attack", response_model=AttackStatusResponse)
def attack(attack_info: AttackRequest, db: Session = Depends(get_db)):
    current_room = db.query(GameRoom).filter(GameRoom.room_code == attack_info.room_code).first()
    if not current_room:
        raise HTTPException(status_code=404, detail="Game room not found")

    current_attack = db.query(Attack).filter(Attack.room_code == attack_info.room_code).first()
    if not current_attack:
        new_attack = Attack(
            room_code = attack_info.room_code,
            attacker = attack_info.attacker,
            opponent = attack_info.opponent,
            attack_position = attack_info.attack_position,
            attack_status = "not yet",
            damage_status = "not yet"        
        )
        db.add(new_attack)
        db.commit()
        db.refresh(new_attack)
        return new_attack
    
    # 공격자, 수비자가 유효한지 확인
    if attack_info.attacker not in [current_room.player_first, current_room.player_last] or \
        attack_info.opponent not in [current_room.player_first, current_room.player_last]:
        if (attack_info.attacker != 0 and attack_info.opponent != 0):
            raise HTTPException(status_code=400, detail="Invalid attacker or opponent")

    # 현재 턴 확인
    if current_attack.attacker != attack_info.attacker:
        raise HTTPException(status_code=400, detail="Not your turn")
    
    current_attack.attacker= attack_info.attacker
    current_attack.opponent = attack_info.opponent
    current_attack.attack_position = attack_info.attack_position

    # 공격 성공 여부 확인
    if (attack_info.opponent == current_room.player_first):
        target_board = current_room.first_board.copy()
    else:
        target_board = current_room.last_board.copy()

    if (attack_info.attack_position in target_board):
        current_attack.damage_status = 'damaged'
        target_board.remove(attack_info.attack_position)
    else:
        current_attack.damage_status = 'missed'

    # 수정된 보드 상태를 다시 저장
    if attack_info.opponent == current_room.player_first:
        current_room.first_board = target_board
    else:
        current_room.last_board = target_board
        
    #  게임 종료 여부 확인
    if len(target_board) == 0:
        current_room.status = 'completed'

    db.commit()
    db.refresh(current_attack)
    db.refresh(current_room)

    return {
        "room_code": current_attack.room_code,
        "attacker": current_attack.attacker,
        "opponent": current_attack.opponent,
        "attack_position": current_attack.attack_position,
        "damage_status": current_attack.damage_status,
        "game_status": current_room.status,
    }


@router.post("/damage", response_model=AttackStatusResponse)
def damage(room_code: str, db: Session = Depends(get_db)):
    current_room = db.query(GameRoom).filter(GameRoom.room_code == room_code).first()
    if not current_room:
        raise HTTPException(status_code=404, detail="Game room not found")

    current_attack = db.query(Attack).filter(Attack.room_code == room_code).first()
    if not current_attack:
        raise HTTPException(status_code=404, detail="Attack not found")
    
    if (current_attack.attacker == 0 or current_attack.opponent == 0):
        current_attack.attacker = 0
        current_attack.opponent = current_room.player_first if current_room.player_last == 0 else current_room.player_last
        current_attack.attack_position = create_attack_coordinate()

        # 공격 성공 여부 확인
        if (current_attack.opponent == current_room.player_first):
            target_board = current_room.first_board.copy()
        else:
            target_board = current_room.last_board.copy()

        if (current_attack.attack_position in target_board):
            current_attack.damage_status = 'damaged'
            target_board.remove(current_attack.attack_position)
        else:
            current_attack.damage_status = 'missed'

        # 수정된 보드 상태를 다시 저장
        if current_attack.opponent == current_room.player_first:
            current_room.first_board = target_board
        else:
            current_room.last_board = target_board
        
        db.commit()

    response = {
        "room_code": current_attack.room_code,
        "attacker": current_attack.attacker,
        "opponent": current_attack.opponent,
        "attack_position": current_attack.attack_position,
        "damage_status": current_attack.damage_status,
        "game_status": current_room.status,
    }

    if current_room.status == "completed":
        db.delete(current_room)
        db.delete(current_attack)
        db.commit()

    return response



@router.post("/end-turn")
def end_turn(room_code: str, db: Session = Depends(get_db)):
    current_attack = db.query(Attack).filter(Attack.room_code == room_code).first()
    if not current_attack:
        raise HTTPException(status_code=404, detail="Attack info doesn't exist")
    pre_attacker = current_attack.attacker
    pre_opponent = current_attack.opponent

    current_attack.attacker = pre_opponent
    current_attack.opponent = pre_attacker
    current_attack.attack_position = ""
    current_attack.damage_status = 'not yet'
    db.commit()
    
@router.get("/status")
def get_status(room_code: str, db: Session = Depends(get_db)):
    current_game = db.query(GameRoom).filter(GameRoom.room_code == room_code).first()
    if not current_game:
        raise HTTPException(status_code=400, detail="Game doesn't exist")
    return current_game
    

@router.get("/")
def get_rooms(db: Session = Depends(get_db)):
    """진행 중인 모든 게임 조회"""
    rooms = db.query(GameRoom).all()
    return rooms

@router.delete("/delete")
def delete_room(room_code: str, db: Session = Depends(get_db)):
    """삭제"""
    current_game = db.query(GameRoom).filter(GameRoom.room_code == room_code).first()
    if not current_game:
        raise HTTPException(status_code=400, detail="Game doesn't exist")

    db.delete(current_game)
    db.commit()
    
    return {"message": "room deleted"}
