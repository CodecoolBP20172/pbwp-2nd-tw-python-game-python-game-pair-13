#!/usr/bin/env python3
import os
import random


def generate_board():
    # generates a board
    board = []
    for x in range(10):
        board.append(["~"]*10)
    return board

# ------------------------------------------------------------------------------


def print_board(board, u):
    # prints the board in a human-readable fashion
    print ("This is " + u + "'s board")
    bold = "\033[1m"
    reset = "\033[0;0m"
    for x in range(10):
        if x == 0:
            print ("       " + bold + str(x+1) + reset, end="")
        else:
            print ("     " + bold + str(x+1) + reset, end="")
    print ("\n")

    for i in range(10):
        row = board[i]
        print (bold + "{:<2d}".format(i+1) + reset, *row, sep="     ")
        print ("\n")
    print (" ")
    return board

# ------------------------------------------------------------------------------


def get_coordinate():
    # gets the coordinates of the starting point of the ship from the player
    while True:
        user_input = input("Enter a coordinates (row,col): ")
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
    if orientation == "v":
        for i in range(ship):
            board[x+i][y] = s
    if orientation == "h":
        for i in range(ship):
            board[x][y+i] = s
    return board

# ------------------------------------------------------------------------------


def user_place_ships(board, ships, u):
    # Player places his/her ships on his/her board
    for ship, length in ships.items():
        print ("Placement phase")
        print_board(board, u)
        print ("Placing " + ship + " ({} long)".format(length))
        valid = False
        while not valid:
            x, y = get_coordinate()
            orientation = vertical_or_horizontal()
            valid = validate_ship_position(board, length, orientation, x, y)
        board = ship_placement(board, length, ship[0], orientation, x, y)
        os.system("tput reset")

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


def hit_check(board, x, y):
    # Check if the given coordinates hit target or miss
    if board[x][y] == "~":
        return "miss"
    elif board[x][y] == "X" or board[x][y] == "0":
        return "try again"
    else:
        return "hit"

# ------------------------------------------------------------------------------


def player_move(board, showboard, u, ships):
    while True:
        x, y = get_coordinate()
        res = hit_check(board, x, y)
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
    print ("\n")
    return board, showboard

# ------------------------------------------------------------------------------


def ai_move(board, showboard, u, ships):
    while True:
        x = random.randint(0, 9)
        y = random.randint(0, 9)
        res = hit_check(board, x, y)
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

    user_place_ships(user1_board, ships, "Player1")
    print_board(user1_board, "Player1")
    input("Hit ENTER to continue.")
    os.system("tput reset")

    user_place_ships(user2_board, ships, "Player2")
    print_board(user2_board, "Player2")
    input("Hit ENTER to continue.")
    os.system("tput reset")

    win_condition = False
    while not win_condition:
        os.system("tput reset")
        print ("Player1's turn")
        print_board(user2_board_show, "Player2")
        user2_board, user2_board_show = player_move(user2_board, user2_board_show, "Player2", ships)
        win_condition = check_win(user2_board)
        if win_condition is True:
            winner = "Player1"
            break
        os.system("tput reset")
        print ("Player2's turn")
        print_board(user1_board_show, "Player1")
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

    user_place_ships(user1_board, ships, "Player")
    print_board(user1_board, "Player")
    input("Hit ENTER to continue.")
    os.system("tput reset")
    ai_place_ships(ai_board, ships, "AI")
    input("Hit ENTER to continue.")
    os.system("tput reset")

    win_condition = False
    while not win_condition:
        os.system("tput reset")
        print("Player's turn")
        print_board(ai_board_show, "AI")
        ai_board, ai_board_show = player_move(ai_board, ai_board_show, "AI", ships)
        win_condition = check_win(ai_board)
        if win_condition is True:
            winner = "Player1"
            break
        os.system("tput reset")
        print("AI's turn")
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
