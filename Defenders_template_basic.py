import random

# Game variables
game_vars = {
    'turn': 0,                      # Current Turn
    'monster_kill_target': 20,      # Number of kills needed to win
    'monsters_killed': 0,           # Number of monsters killed so far
    'num_monsters': 0,              # Number of monsters in the field
    'gold': 10,                     # Gold for purchasing units
    }

archer = {'shortform' : 'ARCHR',
          'name': 'Archer',
          'maxHP': 5,
          'min_damage': 1,
          'max_damage': 4,
          'price': 5
          }
             
wall = {'shortform': 'WALL',
        'name': 'Wall',
        'maxHP': 20,
        'min_damage': 0,
        'max_damage': 0,
        'price': 3
        }

zombie = {'shortform': 'ZOMBI',
          'name': 'Zombie',
          'maxHP': 15,
          'min_damage': 3,
          'max_damage': 6,
          'moves' : 1,
          'reward': 2
          }

field = [ [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None],
          [None, None, None, None, None, None, None] ]


#----------------------------------------------------------------------
# draw_field()
#
#    Draws the field of play
#    The column numbers only go to 3 since players can only place units
#      in the first 3 columns
#----------------------------------------------------------------------

def draw_field():
    rows = len(field)
    columns = len(field[0])

    print("{:^2}{:^6}{:^6}{:^6}".format(" ","1","2","3"))

    print(" ", end = "")
    for column in range(columns):
        print("+-----", end = "")
    print("+")

    for row in range(rows):
        print(chr(ord("A")+row), end = "")
        for column in field[row]:
            if column != None:
                print("|{:5}".format(str(column)), end = "")
            else:
                print("|{:5}".format(" "), end = "")
        print("|")
        print(" ", end = "")
        for column in field[row]:
            if column != None:
                print("|{:5}".format(str(column)), end = "")
            else:
                print("|{:5}".format(" "), end = "")
        print("|")
        print(" ", end = "")
        for column in range(columns):
            print("+-----", end = "")
        print("+")

    return

#----------------------------
# show_combat_menu()
#
#    Displays the combat menu
#----------------------------
def show_combat_menu(game_vars):
    print("1. Buy unit     2. End turn")
    print("3. Save game    4. Quit")

#----------------------------
# show_main_menu()
#
#    Displays the main menu
#----------------------------
def show_main_menu():
    print("1. Start new game")
    print("2. Load saved game")
    print("3. Quit")

#-----------------------------------------------------
# place_unit()
#
#    Places a unit at the given position
#    This function works for both defender and monster
#    Returns False if the position is invalid
#       - Position is not on the field of play
#       - Position is occupied
#       - Defender is placed past the first 3 columns
#    Returns True if placement is successful
#-----------------------------------------------------

def place_unit(field, position, unit_name):       
    return True

#-------------------------------------------------------------------
# buy_unit()
#
#    Allows player to buy a unit and place it using place_unit()
#-------------------------------------------------------------------
def buy_unit(field, game_vars):                                    
    return

#-----------------------------------------------------------
# defender_attack()
#
#    Defender unit attacks.
#
#-----------------------------------------------------------
def defender_attack(defender_name, field, row, column):
    return

#-----------------------------------------------------------
# monster_advance()
#
#    Monster unit advances.
#       - If it lands on a defender, it deals damage
#       - If it lands on a monster, it does nothing
#       - If it goes out of the field, player loses
#-----------------------------------------------------------
def monster_advance(monster_name, field, row, column):
    return

#---------------------------------------------------------------------
# spawn_monster()
#
#    Spawns a monster in a random lane on the right side of the field.
#    Assumes you will never place more than 5 monsters in one turn.
#---------------------------------------------------------------------
def spawn_monster(field, monster_list):
    return

#-----------------------------------------
# save_game()
#
#    Saves the game in the file 'save.txt'
#-----------------------------------------
def save_game():
    print("Game saved.")

#-----------------------------------------
# load_game()
#
#    Loads the game from 'save.txt'
#-----------------------------------------
def load_game(game_vars):
    return

#-----------------------------------------------------
# initialize_game()
#
#    Initializes all the game variables for a new game
#-----------------------------------------------------
def initialize_game():
    game_vars['turn'] = 0
    game_vars['monster_kill_target'] = 20
    game_vars['monsters_killed'] = 0
    game_vars['num_monsters'] = 0
    game_vars['gold'] = 10
    

#-----------------------------------------
#               MAIN GAME
#-----------------------------------------

print("Desperate Defenders")
print("-------------------")
print("Defend the city from undead monsters!")
print()

# TO DO: ADD YOUR CODE FOR THE MAIN GAME HERE!
show_main_menu()
choice = int(input("Your Choice? "))
if choice == 1:
    play_game = True
    initialize_game()
elif chocie == 2:
    play_game = True
    pass
else:
    play_game = False

while play_game == True:
    draw_field()
    show_combat_menu(game_vars)
    choice = int(input("Your Choice?"))

    
    
