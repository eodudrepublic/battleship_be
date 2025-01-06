from fastapi import APIRouter, Depends, HTTPException
from waiting_list_service import (
    add_user_to_waiting_list,
    remove_user_from_waiting_list,
    get_waiting_list,
    match_users,
)
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
def match_users_route():
    matched_users = match_users()
    return matched_users