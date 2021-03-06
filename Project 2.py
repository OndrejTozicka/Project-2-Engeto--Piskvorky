# Autor Ondřej Tožička

import random

def create_dict_guess(board_size):
    for i in range(1,board_size**2+1):
        guesses[i] =" "
    return guesses

def print_board(board_size):
    print("-"*(board_size*4-1))
    for pole in guesses:
        if pole % board_size ==0:
            print(" " + guesses[pole])
            print("-"*(board_size*4-1))
        else:
            print(" " +guesses[pole]+ " |",end="")

def check_choice(choice):
    if choice.isnumeric() == False:
        print("Nezadal jsi cislo!")
        return False
    elif int(choice) > board_size**2 or int(choice) == 0:
        print("Zadal jsi číslo větší než je hrací pole nebo 0!")
        return False
    elif guesses[int(choice)] != " ":
        if game_type == "m" or (game_type == "s" and switch == "player1"):
            print("Toto pole je již zabráno! Zvol jiné.")
        return False
    else:
        return True


def create_all_winning_comb(board_size):
    winning_rows = []
    winning_columns = {}
    winning_diag_up = []
    winning_diag_down = []

    for pole in guesses.keys():
        winning_rows.append(pole)
        if pole%board_size == 0 :
            all_winning_comb.append(winning_rows)
            winning_rows = []
        zbytek = pole%board_size
        if zbytek in winning_columns:
            winning_columns[zbytek].append(pole)
        else:
            winning_columns[zbytek] = [pole]

    diagnumberup =1
    diagnumberdown = board_size
    for i in range(board_size):
        winning_diag_up.append(diagnumberup)
        winning_diag_down.append(diagnumberdown)
        diagnumberup += board_size + 1
        diagnumberdown += board_size -1

    all_winning_comb.append(winning_diag_up)
    all_winning_comb.append(winning_diag_down)
    for key in winning_columns.keys():
        all_winning_comb.append(winning_columns[key])

    return all_winning_comb


def check_finish(player):
    tool = players_tools[player]
    for winning_comb in all_winning_comb:
        checked_guess = []
        for pole in winning_comb:
            checked_guess.append(guesses[pole]==tool)
        if all(checked_guess):
            return (True, "win")

    check_no_winner = []
    for winning_comb in all_winning_comb:
        checked_guess = []
        for pole in winning_comb:
            checked_guess.append(guesses[pole])
        if (players_tools["player1"] in checked_guess) and (players_tools["player2"] in checked_guess):
            check_no_winner.append(True)
        else:
            check_no_winner.append(False)
    if all(check_no_winner):
        return (True, "draw")
    return (False,"No end yet")


players_tools = {"player1":"X","player2":"O"}
players = {}
guesses = {}
game_type = ""
finish = False
switch = ""
pocet_tahu = 0
all_winning_comb = []
result = ()


print("Vítejte v jednoduché hře PIŠKVORKY. \n")
print("Vaším cílem je zkompletovat celou řadu, sloupec nebo diagonalu na hracím poli o velikosti, kterou si zvolíte.")
print("Hodně štěstí!\n")

while not (game_type == "m" or game_type == "s"):
    game_type = input("Chceš hrát mulitplayer pro dva hráče nebo singleplyer proti Bobovi? Zvol M (Multiplayer) nebo S (Singleplayer)").lower()

if game_type == "m":
    players["player1"] = input("Zadej jméno hráče č.1: ").upper()
    players["player2"] = input("zadej jméno hráče č.2: ").upper()
else:
    players["player1"] = input("Zadej své jméno: ").upper()
    players["player2"] = "BOB"

test_number = True
while test_number:
    board_size = input("Zadej velikost hracícho pole. Minimální velikost je 3x3. "
                       "Doporučujici menší než 10x10 pro lepší přehlednost: ")
    try:
        board_size = int(board_size)
    except:
        print("Musíš zadat číslo!")
    else:
        if board_size <3:
            print("Hrací pole musí být minimálně 3x3. Zadej velikost znovu")
        else:
            test_number = False

input("Zmáčkni ENTER pro zahájení hry.")
print("Tohle je vaše hrací pole: \n")

create_dict_guess(board_size)
create_all_winning_comb(board_size)


while finish != True:
    print_board(board_size)
    print("=" * 40)
    if pocet_tahu%2 == 0:
        switch = "player1"
    else:
        switch = "player2"
    player = players[switch]
    if game_type == "s":
        if switch == "player1":
            choice = input("Hráči {}, napiš svůj tip. Musí to být číslo "
                               "menší nebo rovno velikosti hracího pole ( =< {} ) :".format(player,board_size**2))
        else:
            choice = str(random.randint(1,board_size**2))
    else:
        choice = input("Hráči {}, napiš svůj tip. Musí to být číslo "
                       "menší nebo rovno velikosti hracího pole ( =< {} ) :".format(player, board_size ** 2))

    while check_choice(choice) != True:
        if game_type == "m" or switch == "player1":
            choice = input("Hráči {}, napiš svůj opravený tip.".format(player))
        else:
            choice = str(random.randint(1, board_size **2))
    guesses[int(choice)] = players_tools[switch]
    pocet_tahu +=1
    result = check_finish(switch)
    finish = result[0]
    if game_type == "s" and switch == "player2":
        print("BOB si vybral políčko {}".format(choice))
    print("="*40)


if result[1] == "win":
    print("Gratuluji, vyhrál hráč {} po {} odehraných tipech.".format(players[switch],pocet_tahu))
    print_board(board_size)
else:
    print("Remiza! Už ani jeden z hráčů nemůže vyhrát")
    print_board(board_size)

