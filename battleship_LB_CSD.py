#!/usr/bin/env python3
import os
import random

BOLD = "\033[1m"
RESET = "\033[0;0m"
RED = "\033[91m"
BLUE = "\033[34m"


def generate_board():
    # generates a board
    board = []
    for x in range(10):
        board.append(["~"]*10)
    return board

# ------------------------------------------------------------------------------


def print_board(board, u, color):
    # prints the board in a human-readable fashion
    def colouring_board(color):
        print ("This is " + BOLD + color + u + RESET + "'s board")
        for x in range(10):
            if x == 0:
                print ("       " + BOLD + str(x+1) + RESET, end="")
            else:
                print ("     " + BOLD + str(x+1) + RESET, end="")
        print ("\n")

        for i in range(10):
            row = board[i]
            print (BOLD + "{:<2d}".format(i+1) + RESET, *row, sep="     ")
            print ("\n")
        print (" ")
        return board
    if u == "Player1" or u == "Player":
        colouring_board(RED)
    elif u == "Player2" or u == "AI":
        colouring_board(BLUE)

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
        print ("It's not even in the ocean!")
        return False
    elif orientation == "v" and x+length > 10:
        print ("It's not even in the ocean!")
        return False
    elif orientation == "h":
        for i in range(length):
            if board[x][y+i] != "~":
                print ("There's already a ship there! Choose another place.")
                return False
    elif orientation == "v":
        for i in range(length):
            if board[x+i][y] != "~":
                print ("There's already a ship there! Choose another place.")
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
    color = "\033[32m"
    if orientation == "v":
        for i in range(ship):
            board[x+i][y] = color + BOLD + s + RESET
    if orientation == "h":
        for i in range(ship):
            board[x][y+i] = color + BOLD + s + RESET
    return board

# ------------------------------------------------------------------------------


def user_place_ships(board, ships, u, color):
    # Player places his/her ships on his/her board
    for ship, length in ships.items():
        print ("Placement phase")
        print_board(board, u, color)
        print ("Placing " + ship + " ({} long)".format(length))
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
            if y == "G":
                galley_pos.append([i_x, i_y])
            if y == "Y":
                yacht_pos.append([i_x, i_y])
            if y == "P":
                pirate_ship_pos.append([i_x, i_y])
            if y == "L":
                longship_pos.append([i_x, i_y])
            if y == "A":
                armored_cruiser_pos.append([i_x, i_y])
    return galley_pos, yacht_pos, pirate_ship_pos, longship_pos, armored_cruiser_pos

# ------------------------------------------------------------------------------


def ai_place_ships(board, ships, u):
    # AI places its ships on its board
    for ship, length in ships.items():
        print ("AI placing " + ship + "({} long)..".format(length))
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
        orange = "\033[93m"
        hit_color = ""
        miss_color = ""
        if u == "Player1" or u == "Player":
            hit_color = orange
            miss_color = RED
        elif u == "Player2":
            hit_color = orange
            miss_color = BLUE
        x, y = get_coordinate()
        res = hit_check(board, x, y)
        if res == "hit":
            os.system("tput reset")
            print("It's a hit.")
            check_sink(board, x, y)
            board[x][y] = "X"
            showboard[x][y] = hit_color + BOLD + "X" + RESET
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
            showboard[x][y] = miss_color + BOLD + "0" + RESET
            print("It's a miss.")
            print_board(showboard, u)
            input("Hit ENTER to continue.")
            os.system("tput reset")
            break
    print ("\n")
    return board, showboard

# ------------------------------------------------------------------------------


def ai_move(board, showboard, u, ships):
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        res, letter = hit_check(board, x, y)
        if res == "hit":
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
            board[x][y] = "0"
            showboard[x][y] = "0"
            print("AI hit " + str(x+1) + ", " + str(y+1) + ".")
            print("It's a miss.")
            print_board(showboard, u)
            break
    input("Hit ENTER to continue.")
    return board, showboard


def smart_ai_move(board, previous_hit_x, previous_hit_y, ships, s): # s will be "letter"
    hit_ship = []
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
            ship = "ArmoRED cruiser"
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
    print_board(user1_board, "Player1", RED)
    input("Hit ENTER to continue.")
    os.system("tput reset")

    user_place_ships(user2_board, ships, "Player2", BLUE)
    print_board(user2_board, "Player2", BLUE)
    input("Hit ENTER to continue.")
    os.system("tput reset")

    win_condition = False
    while not win_condition:
        os.system("tput reset")
        print (RED + BOLD + "Player1's turn" + RESET)
        print_board(user2_board_show, "Player2", BLUE)
        user2_board, user2_board_show = player_move(user2_board, user2_board_show, "Player2", ships)
        win_condition = check_win(user2_board)
        if win_condition is True:
            winner = "Player1"
            break
        os.system("tput reset")
        print (BLUE + BOLD + "Player2's turn" + RESET)
        print_board(user1_board_show, "Player1", RED)
        user1_board, user1_board_show = player_move(user1_board, user1_board_show, "Player1", ships)
        win_condition = check_win(user1_board)
        if win_condition is True:
            winner = "Player2"
            break
    print ("GAME OVER")
    print ("The winner is ", winner + "!")


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
    print_board(user1_board, "Player", RED)
    input("Hit ENTER to continue.")
    os.system("tput reset")
    ai_place_ships(ai_board, ships, "AI")
    input("Hit ENTER to continue.")
    os.system("tput reset")

    win_condition = False
    while not win_condition:
        os.system("tput reset")
        print(RED + BOLD + "Player's turn" + RESET)
        print_board(ai_board_show, "AI", BLUE)
        ai_board, ai_board_show = player_move(ai_board, ai_board_show, "AI", ships)
        win_condition = check_win(ai_board)
        if win_condition is True:
            winner = "Player1"
            break
        os.system("tput reset")
        print(BLUE + BOLD + "AI's turn" + RESET)
        user1_board, user1_board_show = ai_move(user1_board, user1_board_show, "Player", ships)
        win_condition = check_win(user1_board)
        if win_condition is True:
            winner = "AI"
            break
    print ("GAME OVER")
    print ("The winner is ", winner + "!")

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
