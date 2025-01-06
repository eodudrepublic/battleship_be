waiting_list = []

def add_user_to_waiting_list(user_id: int):
    """대기 리스트에 사용자 추가"""
    if user_id in waiting_list:
        raise ValueError("User already in waiting list")
    waiting_list.append(user_id)
    return waiting_list

def remove_user_from_waiting_list(user_id: int):
    """대기 리스트에서 사용자 제거"""
    if user_id not in waiting_list:
        raise ValueError("User not in waiting list")
    waiting_list.remove(user_id)
    return waiting_list

def get_waiting_list():
    """대기 리스트 조회"""
    return waiting_list

def match_users():
    """대기 리스트에서 두 명 매칭"""
    if len(waiting_list) < 2:
        return []
    matched_users = waiting_list[:2]
    for user in matched_users:
        waiting_list.remove(user)
    return matched_users