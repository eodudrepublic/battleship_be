import random

# 배 배치 함수
def place_ship(board, width, height, count):
    for _ in range(count):
        while True:
            direction = random.choice(["H", "V"])
            if direction == "H":
                row, col = random.randint(0, 10-height), random.randint(0, 10 - width)
                if all(board[row][col + i] == "-" for i in range(width)) \
                    and all(board[row+height-1][col + i] == "-" for i in range(width)):
                    for i in range(width):
                        board[row][col + i] = "S"
                        board[row+height-1][col + i] = "S"
                    break
            else:  # Vertical
                row, col = random.randint(0, 10 - width), random.randint(0, 8)
                if all(board[row + i][col] == "-" for i in range(width)) \
                    and all(board[row + i][col+height-1] == "-" for i in range(width)):
                    for i in range(width):
                        board[row + i][col] = "S"
                        board[row + i][col+height-1] = "S"
                    break

# 좌표 변환 함수
def board_to_coordinates(board):
    coordinates = []
    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell == "S":
                # 행을 A-J로 변환, 열은 1부터 시작
                coordinate = f"{chr(65 + row_idx)}{col_idx + 1}"
                coordinates.append(coordinate)
    return coordinates

def create_board():
    # 10x10 보드 생성
    board = [["-" for _ in range(10)] for _ in range(10)]
    
    # 배 배치
    place_ship(board, 3, 2, 1)  # 3x2
    place_ship(board, 4, 1, 2)  # 4x1
    place_ship(board, 2, 1, 3)  # 2x1

    coordinates = board_to_coordinates(board)
    return coordinates

def create_attack_coordinate():
    row = random.choice("ABCDEFGHIJ")
    col = random.randint(1, 10)
    coordinate = f"{row}{col}"

    return coordinate
