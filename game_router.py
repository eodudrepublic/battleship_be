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
    
    random_first = choice([game.player1_id, game.player2_id])
    random_later = game.player2_id if random_first == game.player1_id else game.player1_id

    new_game = GameRoom(
        room_code = game.room_code,
        status = 'in_progress',
        player_first = random_first,
        player_last = random_later,
        is_finished = False
    )

    new_attack = Attack(
        room_code = game.room_code,
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
            attack_status = "not yet",
            damage_status = "not yet"        
        )
        db.add(new_attack)
        db.commit()
        db.refresh(new_attack)
        return new_attack
    
    if current_attack.attacker != attack_info.attacker:
        raise HTTPException(status_code=400, detail="Not your turn")
    
    # user 정보가 app_users에 있는지 확인
    current_attack.attacker= attack_info.attacker
    current_attack.opponent = attack_info.opponent
    current_attack.attack_position_x = attack_info.attack_position_x
    current_attack.attack_position_y = attack_info.attack_position_y
    current_attack.attack_status = "attack"
    current_attack.damage_status = "not yet"
        
    db.commit()
    db.refresh(current_attack)

    return current_attack


@router.get("/attack_status", response_model=AttackStatusResponse)
def attack_status(room_code: str, db: Session = Depends(get_db)):
    current_attack = db.query(Attack).filter(Attack.room_code == room_code).first()
    if not current_attack:
        raise HTTPException(status_code=404, detail="No attack found")
    return current_attack


@router.post("/damage")
def damage(damage_info: DamageRequest, db: Session = Depends(get_db)):
    current_attack = db.query(Attack).filter(Attack.room_code == damage_info.room_code).first()
    if not current_attack:
        raise HTTPException(status_code=404, detail="No attack found")
    
    current_attack.damage_status = damage_info.damage_status
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

@router.post("/end-turn", response_model=AttackStatusResponse)
def end_turn(room_code: str, db: Session = Depends(get_db)):
    current_attack = db.query(Attack).filter(Attack.room_code == room_code).first()
    if not current_attack:
        raise HTTPException(status_code=404, detail="Attack info doesn't exist")
    pre_attacker = current_attack.attacker
    pre_opponent = current_attack.opponent

    current_attack.attacker = pre_opponent
    current_attack.opponent = pre_attacker
    current_attack.attack_position_x = ""
    current_attack.attack_position_y = 0
    current_attack.attack_status = 'not yet'
    current_attack.damage_status = 'not yet'
    db.commit()
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