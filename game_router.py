from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from random import choice

from schemas.game import GameStartRequest, GameStatusResponse, AttackStatusResponse, AttackRequest, DamageRequest
from models.game import GameRoom, Attack
from database import get_db

router = APIRouter()

@router.post("/start")
def start_game(game: GameStartRequest, db: Session = Depends(get_db)):
    existing_room = db.query(GameRoom).filter(GameRoom.room_code == game.room_code).first()
    if existing_room:
        raise HTTPException(status_code=400, detail="Game already exists")
    
    random_turn = choice([game.player1_id, game.player2_id])

    new_game = GameRoom(
        room_code = game.room_code,
        status = 'in_progress',
        player_first = random_turn,
        player_last = game.player2_id if random_turn == game.player1_id else game.player1_id,
        is_finished = False
    )
    db.add(new_game)
    db.commit()
    db.refresh(new_game)
    return new_game

@router.post("/attack", response_model=AttackStatusResponse)
def attack(attack_info: AttackRequest, db: Session = Depends(get_db)):
    current_attack = db.query(Attack).filter(Attack.room_code == attack_info.room_code).first()
    if not current_attack:
        new_attack = Attack(
            room_code = attack_info.room_code,
            attacker = attack_info.attacker,
            opponent = attack_info.opponent,
            attack_position_x = attack_info.attack_position_x,
            attack_position_y = attack_info.attack_position_y,
            is_attacked = "not yet"
        )
        db.add(new_attack)
        db.commit()
        db.refresh(new_attack)
        return new_attack
    
    if current_attack.attacker == attack_info.attacker:
        raise HTTPException(status_code=400, detail="Not your turn")
    
    current_attack.attacker= attack_info.attacker
    current_attack.opponent = attack_info.opponent
    current_attack.attack_position_x = attack_info.attack_position_x
    current_attack.attack_position_y = attack_info.attack_position_y
    current_attack.is_attacked = "not yet"
        
    db.commit()
    db.refresh(current_attack)

    return current_attack


@router.get("/attack_status", response_model=AttackStatusResponse)
def attack_status(room_code: str, db: Session = Depends(get_db)):
    current_attack = db.query(Attack).filter(Attack.room_code == room_code).first()
    return current_attack


@router.post("/damage")
def damage(damage_info: DamageRequest, db: Session = Depends(get_db)):
    current_attack = db.query(Attack).filter(Attack.room_code == damage_info.room_code).first()
    if not current_attack:
        raise HTTPException(status_code=404, detail="No attack found")
    
    current_attack.is_attacked = damage_info.is_attacked
    db.commit()

    if damage_info.is_finished:
        current_game = db.query(GameRoom).filter(GameRoom.room_code == damage_info.room_code).first()
        # current_game.is_finished = True
        db.delete(current_game)
        db.commit()
        return {"message": "finished"}

    return current_attack

@router.get("/damage_status", response_model=AttackStatusResponse)
def damage_status(room_code: str, db: Session = Depends(get_db)):
    current_attack = db.query(Attack).filter(Attack.room_code == room_code).first()
    if not current_attack:
        raise HTTPException(status_code=404, detail="Damage info doesn't exist")
    return current_attack


@router.get("/status", response_model=GameStatusResponse)
def get_status(room_code: str, db: Session = Depends(get_db)):
    current_game = db.query(GameRoom).filter(GameRoom.room_code == room_code).first()
    if not current_game:
        raise HTTPException(status_code=400, detail="Game doesn't exist")
    return current_game 
    
    

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    """진행 중인 모든 게임 조회"""
    users = db.query(GameRoom).all()  # 동기 쿼리
    return users