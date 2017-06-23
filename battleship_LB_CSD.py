#!/usr/bin/env python3
import os
import random

BOLD = "\033[1m"
RESET = "\033[0;0m"
RED = "\033[91m"
BLUE = "\033[34m"
ORANGE = "\033[93m"
GREEN = "\033[32m"


def generate_board():
    # generates a board
    board = []
    for x in range(10):
        board.append(["~"]*10)
    return board

# ------------------------------------------------------------------------------


def print_board(board, u):
    # prints the board in a human-readable fashion
    color = ""
    if u == "Player1" or u == "Player":
        color = RED
    elif u == "Player2" or u == "AI":
        color = BLUE
    print("This is " + BOLD + color + u + RESET + "'s board")
    for x in range(10):
        if x == 0:
            print("     " + BOLD + str(x+1) + RESET, end="")
        else:
            print("     " + BOLD + str(x+1) + RESET, end="")
    print("\n")
    for i in range(10):
        row = "     ".join(board[i]).replace("0", BOLD + color + "0" + RESET).replace("X", BOLD + ORANGE + "X" + RESET)
        print(BOLD + "{0:<2d}".format(i+1) + RESET + "   {}".format(row))
        print("\n")
    print(" ")

# ------------------------------------------------------------------------------


def print_placement(board, u):
    # prints the board in a human-readable fashion
    color = ""
    if u == "Player1" or u == "Player":
        color = RED
    elif u == "Player2" or u == "AI":
        color = BLUE
    print("This is " + BOLD + color + u + RESET + "'s board")
    for x in range(10):
        if x == 0:
            print("     " + BOLD + str(x+1) + RESET, end="")
        else:
            print("     " + BOLD + str(x+1) + RESET, end="")
    print("\n")
    for i in range(10):
        row = "     ".join(board[i]).replace(
            "Y", BOLD + GREEN + "Y" + RESET).replace(
            "P", BOLD + GREEN + "P" + RESET).replace(
            "A", BOLD + GREEN + "A" + RESET).replace(
            "L", BOLD + GREEN + "L" + RESET).replace(
            "G", BOLD + GREEN + "G" + RESET)
        print(BOLD + "{0:<2d}".format(i+1) + RESET + "   {}".format(row))
        print("\n")
    print(" ")

# ------------------------------------------------------------------------------


def get_coordinate():
    # gets the coordinates of the starting point of the ship from the player
    while True:
        user_input = input("Enter coordinates (row,col) or 'exit' to quit game: ")
        if user_input == "exit":
            quit()
        else:
            try:
                coordinate = user_input.split(",")
                if len(coordinate) != 2:
                    raise Exception("Too many or too few coordinates.")
                # converts coordinates to intigers and to represent indicies
                coordinate[0] = int(coordinate[0])-1
                coordinate[1] = int(coordinate[1])-1
                if coordinate[0] > 9 or coordinate[0] < 0 or coordinate[1] > 9 or coordinate[1] < 0:
                    raise Exception("Invalid entry. Your coordinate should be between 1-10.")
                return coordinate
            except ValueError:
                print("Only numeric values are accepted as coordinates.")
            except Exception as e:
                print(e)

# ------------------------------------------------------------------------------


def vertical_or_horizontal():
    # gets the orientation of the ship
    while True:
        user_input = input("Vertical or horizontal (v/h)?: ")
        if user_input.lower() == "v" or user_input.lower() == "h":
            return user_input.lower()
        else:
            print("Invalid input. Please only enter v or h.")

# ------------------------------------------------------------------------------


def validate_ship_position(board, length, orientation, x, y):
    # Checks that the ship can be placed on the board at the given coordinates
    # i.e. it doesn't hang out from the board or being placed on another ship
    if orientation == "h" and y+length > 10:
        print("It's not even in the ocean!")
        return False
    elif orientation == "v" and x+length > 10:
        print("It's not even in the ocean!")
        return False
    elif orientation == "h":
        for i in range(length):
            if board[x][y+i] != "~":
                print("There's already a ship there! Choose another place.")
                return False
    elif orientation == "v":
        for i in range(length):
            if board[x+i][y] != "~":
                print("There's already a ship there! Choose another place.")
                return False
    return True


def validate_ship_position_ai(board, length, orientation, x, y):
    # Checks that the ship can be placed on the board at the given coordinates
    # i.e. it doesn't hang out from the board or being placed on another ship
    if orientation == "h" and y+length > 10:
        return False
    elif orientation == "v" and x+length > 10:
        return False
    elif orientation == "h":
        for i in range(length):
            if board[x][y+i] != "~":
                return False
    elif orientation == "v":
        for i in range(length):
            if board[x+i][y] != "~":
                return False
    return True

# ------------------------------------------------------------------------------


def ship_placement(board, ship, s, orientation, x, y):
    # places the ship on the board at the given coordinates and in the given orientation
    if orientation == "v":
        for i in range(ship):
            board[x+i][y] = s
    if orientation == "h":
        for i in range(ship):
            board[x][y+i] = s
    return board

# ------------------------------------------------------------------------------


def user_place_ships(board, ships, u, color):
    # Player places his/her ships on his/her board
    for ship, length in ships.items():
        print("Placement phase")
        print_placement(board, u)
        print("Placing " + ship + " ({} long)".format(length))
        valid = False
        while not valid:
            x, y = get_coordinate()
            orientation = vertical_or_horizontal()
            valid = validate_ship_position(board, length, orientation, x, y)
        board = ship_placement(board, length, ship[0], orientation, x, y)
        os.system("tput reset")


def list_of_position(board):
    # saves the position of the ships placed by the player
    galley_pos = []
    yacht_pos = []
    pirate_ship_pos = []
    longship_pos = []
    armored_cruiser_pos = []
    for i_x, x in enumerate(board):
        for i_y, y in enumerate(x):
            if "G" in y:
                galley_pos.append([i_x, i_y])
            if "Y" in y:
                yacht_pos.append([i_x, i_y])
            if "P" in y:
                pirate_ship_pos.append([i_x, i_y])
            if "L" in y:
                longship_pos.append([i_x, i_y])
            if "A" in y:
                armored_cruiser_pos.append([i_x, i_y])
    return galley_pos, yacht_pos, pirate_ship_pos, longship_pos, armored_cruiser_pos

# ------------------------------------------------------------------------------


def ai_place_ships(board, ships, u):
    # AI places its ships on its board
    for ship, length in ships.items():
        print("AI placing " + ship + "({} long)..".format(length))
        valid = False
        while not valid:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            orientation = random.randint(0, 1)
            if orientation == 0:
                orientation = "v"
            else:
                orientation = "h"
            valid = validate_ship_position_ai(board, length, orientation, x, y)
        board = ship_placement(board, length, ship[0], orientation, x, y)

# ------------------------------------------------------------------------------


def hit_check(board, x, y, letter=None):
    # Check if the given coordinates hit target or miss
    if board[x][y] == "~":
        return "miss", letter
    elif board[x][y] == "X" or board[x][y] == "0":
        return "try again", letter
    else:
        letter = board[x][y]
        return "hit", letter

# ------------------------------------------------------------------------------


def player_move(board, showboard, u, ships):
    while True:
        x, y = get_coordinate()
        res, letter = hit_check(board, x, y)
        if res == "hit":
            os.system("tput reset")
            print("It's a hit.")
            check_sink(board, x, y)
            board[x][y] = "X"
            showboard[x][y] = "X"
            print_board(showboard, u)
            input("Hit ENTER to continue.")
            os.system("tput reset")
            break
        elif res == "try again":
            print("This coordinate has been hit already.")
            continue
        else:
            os.system("tput reset")
            board[x][y] = "0"
            showboard[x][y] = "0"
            print("It's a miss.")
            print_board(showboard, u)
            input("Hit ENTER to continue.")
            os.system("tput reset")
            break
    print("\n")
    return board, showboard

# ------------------------------------------------------------------------------


def ai_move(board, showboard, u, ships, color):
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        res, letter = hit_check(board, x, y)
        if res == "hit":
            previous_hit_x = x
            previous_hit_y = y
            check_sink(board, x, y)
            board[x][y] = "X"
            showboard[x][y] = "X"
            print("AI hit " + str(x+1) + ", " + str(y+1) + ".")
            print("It's a hit.")
            print_board(showboard, u)
            break
        elif res == "try again":
            continue
        else:
            previous_hit_x = None
            previous_hit_y = None
            board[x][y] = "0"
            showboard[x][y] = "0"
            print("AI targeted " + str(x+1) + ", " + str(y+1) + ".")
            print("It's a miss.")
            print_board(showboard, u)
            break
    input("Hit ENTER to continue.")
    return board, showboard, previous_hit_x, previous_hit_y, letter


def smart_ai_move(board, showboard, u, ships, previous_hit_x, previous_hit_y, letter, color,
                  galley_pos, armored_cruiser_pos, pirate_ship_pos, longship_pos, yacht_pos):
    if "G" in letter:
        hit_ship = galley_pos
    if "A" in letter:
        hit_ship = armored_cruiser_pos
    if "P" in letter:
        hit_ship = pirate_ship_pos
    if "L" in letter:
        hit_ship = longship_pos
    if "Y" in letter:
        hit_ship = yacht_pos
    hit_ship.remove([previous_hit_x, previous_hit_y])
    if hit_ship:
        hit_coordinate_x = hit_ship[0][0]
        hit_coordinate_y = hit_ship[0][1]
        board[hit_coordinate_x][hit_coordinate_y] = "X"
        showboard[hit_coordinate_x][hit_coordinate_y] = "X"
        print("AI targeted " + str(hit_coordinate_x+1) + ", " + str(hit_coordinate_y+1) + ".")
        print("It's a hit.")
        print_board(showboard, u)
    else:
        hit_coordinate_x = None
        hit_coordinate_y = None
        letter = ""
        ai_move(board, showboard, u, ships, BLUE)
    input("Hit ENTER to continue.")
    return board, showboard, hit_coordinate_x, hit_coordinate_y, letter
# ------------------------------------------------------------------------------


def check_win(board):
    # checks if one of the players already hit all of the other players ships
    for row in board:
        for i in row:
            if i == "~" or i == "0" or i == "X":
                continue
            else:
                return False
    return True

# ------------------------------------------------------------------------------


def check_sink(board, x, y):
    # checks if a boat is fully sunk
    first_letter = board[x][y]
    counter = 0
    if first_letter in ("Y", "P", "A", "G", "L"):
        if first_letter == "Y":
            ship = "Yacht"
        elif first_letter == "P":
            ship = "Pirate ship"
        elif first_letter == "A":
            ship = "Armored cruiser"
        elif first_letter == "G":
            ship = "Galley"
        elif first_letter == "L":
            ship = "Longship"
        for row in board:
            counter += row.count(first_letter)
        if counter == 1:
            return print(ship, "sunk.")
# -----------------------------------------------------------------------------


def main():
    os.system("tput reset")
    user1_board = generate_board()
    user2_board = generate_board()
    user1_board_show = generate_board()
    user2_board_show = generate_board()

    ships = {
            "Yacht": 1,
            "Pirate ship": 2,
            "Armored cruiser": 3,
            "Galley": 4,
            "Longship": 5
            }

    user_place_ships(user1_board, ships, "Player1", RED)
    print_placement(user1_board, "Player1")
    input("Hit ENTER to continue.")
    os.system("tput reset")

    user_place_ships(user2_board, ships, "Player2", BLUE)
    print_placement(user2_board, "Player2")
    input("Hit ENTER to continue.")
    os.system("tput reset")

    win_condition = False
    while not win_condition:
        os.system("tput reset")
        print(RED + BOLD + "Player1's turn" + RESET)
        print_board(user2_board_show, "Player2")
        user2_board, user2_board_show = player_move(user2_board, user2_board_show, "Player2", ships)
        win_condition = check_win(user2_board)
        if win_condition is True:
            winner = "Player1"
            break
        os.system("tput reset")
        print(BLUE + BOLD + "Player2's turn" + RESET)
        print_board(user1_board_show, "Player1")
        user1_board, user1_board_show = player_move(user1_board, user1_board_show, "Player1", ships)
        win_condition = check_win(user1_board)
        if win_condition is True:
            winner = "Player2"
            break
    print("GAME OVER")
    print("The winner is ", winner + "!")


def vs_ai():
    os.system("tput reset")
    user1_board = generate_board()
    ai_board = generate_board()
    user1_board_show = generate_board()
    ai_board_show = generate_board()

    ships = {
            "Yacht": 1,
            "Pirate ship": 2,
            "Armored cruiser": 3,
            "Galley": 4,
            "Longship": 5
            }

    user_place_ships(user1_board, ships, "Player", RED)
    galley_pos, yacht_pos, pirate_ship_pos, longship_pos, armored_cruiser_pos = list_of_position(user1_board)
    print_placement(user1_board, "Player")
    input("Hit ENTER to continue.")
    os.system("tput reset")
    ai_place_ships(ai_board, ships, "AI")
    input("Hit ENTER to continue.")
    os.system("tput reset")
    win_condition = False
    hit_coordinate_x = None
    hit_coordinate_y = None
    letter = ""
    while not win_condition:
        os.system("tput reset")
        print(RED + BOLD + "Player's turn" + RESET)
        print_board(ai_board_show, "AI")
        ai_board, ai_board_show = player_move(ai_board, ai_board_show, "AI", ships)
        win_condition = check_win(ai_board)
        if win_condition is True:
            winner = "Player1"
            break
        os.system("tput reset")
        print(BLUE + BOLD + "AI's turn" + RESET)
        if hit_coordinate_x is None:
            user1_board, user1_board_show, hit_coordinate_x, hit_coordinate_y, letter = ai_move(
                user1_board, user1_board_show, "Player", ships, BLUE)
        else:
            user1_board, user1_board_show, hit_coordinate_x, hit_coordinate_y, letter = smart_ai_move(
                user1_board, user1_board_show, "Player", ships, hit_coordinate_x, hit_coordinate_y,
                letter, BLUE, galley_pos, armored_cruiser_pos, pirate_ship_pos, longship_pos, yacht_pos)
        win_condition = check_win(user1_board)
        if win_condition is True:
            winner = "AI"
            break
    print("GAME OVER")
    print("The winner is ", winner + "!")

# -----------------------------------------------------------------------------


if __name__ == "__main__":
    while True:
        user_input = input("Two player game or versus AI?('2p' or 'ai') Type exit to quit: ")
        if user_input == "2p":
            main()
        elif user_input == "ai":
            vs_ai()
        elif user_input == "exit":
            exit()
        else:
            print("Invalid input.")
            continue
