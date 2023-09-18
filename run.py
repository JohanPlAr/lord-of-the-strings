import random
import os
import time
import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open("enemy").sheet1
MOREENEMIES = GSPREAD_CLIENT.open("reset").sheet1


def clear_screen():
    """
    Clears the screen, cover the commands for Windows "nt" with "cls" and clear for else
    """
    os.system("cls" if os.name == "nt" else "clear")


def text_center(text):
    """
    Placing text in center of 62 Character line
    """
    txt = f"{text}"
    center_txt = txt.center(62)
    print(center_txt)


def game_title():
    """
    Prints the game title
    """
    text_center("⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔")


def dice(num):
    """
    Simulates a six sided dice roll. The num parameter describes number of rolls
    being called
    """
    result = 0
    total = 0
    for _ in range(num):
        result = random.randint(1, 6)
        total += result
    return total


def battle_dice(num, total):
    """
    Simulates a six sided dice with the addition that all sixes generates two new
    rolls of dice. This function is only used in the sword_battle function to
    increase serendipity and allow higher uncertanty in the battles.
    """
    result = 0
    sixes = []
    for _ in range(num):
        result = random.randint(1, 6)
        total += result
        if result != 6:
            result += total
            num -= 1
        else:
            sixes.append(result)
    if len(sixes) > 0:
        battle_dice(num, total)
    return total


def read_enemy_csv():
    """
    Reads the google sheet file and storing it in the variable enemy_lst.
    enemy_lst variable is passed along during the game and only reset to restart
    the settings
    """
    enemy_lst = SHEET.get_all_values()[1:]
    return enemy_lst


class CharacterStats:
    """
    Object collects the character and selected enemy stats. __str__ used to make
    the print of the object prettier.
    """

    def __init__(
        self, char_type, name, strength_points, health_points, skill_points, armor
    ):
        self.char_type = char_type
        self.name = name
        self.strength_points = strength_points
        self.health_points = health_points
        self.skill_points = skill_points
        self.armor = armor

    def __str__(self):
        return f"""{self.name.upper()} THE MIGHTY {self.char_type.upper()}\n
        STRENGTH:\t{self.strength_points}\n
        HEALTH:\t\t{self.health_points}\n
        SWORD SKILL:\t{self.skill_points}\n
        ARMOR:\t\t{self.armor}"""


def game_menu():
    """
    Holds the Game Menu which allows user to choose activities
    """
    menu = {}
    menu["\t\t\t1."] = "Create New Hero"
    menu["\t\t\t2."] = "View Stats"
    menu["\t\t\t3."] = "Choose Opponent"
    menu["\t\t\t4."] = "View Wins"
    menu["\t\t\t5."] = "Download New Opponents"
    menu["\t\t\t6."] = "Reset Opponents To Start Settings"
    menu["\t\t\t7."] = "Quit Game"

    while True:
        clear_screen()
        game_title()
        print("\t\t\tGAME MENU:")
        options = menu.keys()
        options = sorted(options)
        for entry in options:
            print(entry, menu[entry])
        selection = input("\t\t\tPlease select an option: ")
        if selection == "1":
            character_input()
        elif selection == "2":
            clear_screen()
        elif selection == "3":
            clear_screen()
            game_title()
        elif selection == "4":
            clear_screen()
            game_title()
        elif selection == "5":
            clear_screen()
            game_title()
        elif selection == "6":
            enemy_lst = read_enemy_csv()
        elif selection == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option selected. Please try again.")


def opponents_lst(enemy_lst):
    """
    Displays enemies available for battle. zip is used to display the list
    in two columns.
    """
    while True:
        two_col_lst = []
        x_num = 1
        columns = 2
        for row in enemy_lst:
            if row[3] != 0:
                two_col_lst.append(f"{x_num}. {row[1].upper()}")
                x_num += 1

        for first, second in zip(two_col_lst[::columns], two_col_lst[1::columns]):
            print(f"{first: <13}\t\t{second: <13}")


def get_enemy(enemy_lst, num):
    """
    Creates an "enemy"-instance from CharacterStats object
    """
    enemy_vals = enemy_lst[num]
    char_type = enemy_vals[0]
    name = enemy_vals[1]
    strength_points = int(enemy_vals[2])
    health_points = int(enemy_vals[3])
    skill_points = int(enemy_vals[4])
    armor = int(enemy_vals[5])
    enemy = CharacterStats(
        char_type, name, strength_points, health_points, skill_points, armor
    )
    return enemy, num


def character_input():
    """
    Handles the user input to create the player character. Automates unique
    stats for the types human/elf/dwarf/orc.
    """
    clear_screen()
    game_title()
    print("HERO")
    name = input("NAME: ")
    time.sleep(1)
    while True:
        type_choice = input("1. Human\n2. Elf\n3. Dwarf\n4. Orc\n\nTYPE: ").lower()
        time.sleep(1)
        clear_screen()
        if type_choice == "1" or type_choice == "human":
            char_type = "human"
            strength_points = 2 + dice(1)
            health_points = 3 + dice(2)
            skill_points = 4 + dice(1)
            armor = 0
            stat_points = dice(2)
            player = CharacterStats(
                char_type, name, strength_points, health_points, skill_points, armor
            )
            break
        elif type_choice == "2" or type_choice == "elf":
            char_type = "elf"
            strength_points = 2 + dice(1)
            health_points = 2 + dice(1)
            skill_points = 4 + dice(1)
            armor = 0
            stat_points = dice(3)
            player = CharacterStats(
                char_type, name, strength_points, health_points, skill_points, armor
            )
            break
        elif type_choice == "3" or type_choice == "dwarf":
            char_type = "dwarf"
            strength_points = 3 + dice(2)
            health_points = 3 + dice(1)
            skill_points = 2 + dice(1)
            armor = dice(1)
            stat_points = dice(1)
            player = CharacterStats(
                char_type, name, strength_points, health_points, skill_points, armor
            )
            break
        elif type_choice == "4" or type_choice == "orc":
            char_type = "orc"
            strength_points = 2 + dice(2)
            health_points = 2 + dice(1)
            skill_points = dice(1)
            armor = 3
            stat_points = dice(2)
            player = CharacterStats(
                char_type, name, strength_points, health_points, skill_points, armor
            )
            break
        else:
            print(
                f"Choices available are Human/Elf/Dwarf/Orc\nYou entered '{type_choice}'"
            )
    add_stat_points(player, stat_points)
    return player


def add_stat_points(player, stat_points, enemy_lst):
    """
    The final stage of the character creation which let's the user place stat_points
    of their choice.
    """
    while True:
        clear_screen()
        game_title()
        if stat_points < 1:
            clear_screen()
            game_title()
            print(f"You have {stat_points} points to add to your stats")
            print(player)
            leave()
            game_menu()
        print(f"You have {stat_points} points to add to your abilities")
        print(player)
        if stat_points > 0:
            select_attribute = input("Choose attribute: ")

        if select_attribute == "1":
            activate_stat_points = int(input("How many points do you wish to add: "))

            if activate_stat_points <= stat_points:
                player.strength_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                print(f"Not enough points left\nYou have {stat_points} left")
                add_stat_points(player, stat_points, enemy_lst)
        elif select_attribute == "2":
            activate_stat_points = int(input("How many points do you wish to add: "))
            if activate_stat_points <= stat_points:
                player.health_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                print(f"Not enough points left\nYou have {stat_points} left")
                add_stat_points(player, stat_points, enemy_lst)
        elif select_attribute == "3":
            activate_stat_points = int(input("How many points do you wish to add: "))
            if activate_stat_points <= stat_points:
                player.skill_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                print(f"Not enough points left\nYou have {stat_points} left")
                add_stat_points(player, stat_points, enemy_lst)
        elif select_attribute == "4":
            activate_stat_points = int(input("How many points do you wish to add: "))
            if activate_stat_points <= stat_points:
                player.armor += activate_stat_points
                stat_points -= activate_stat_points
            else:
                print(f"Not enough points left\nYou have {stat_points} left")
                add_stat_points(player, stat_points, enemy_lst)
        else:
            print(f"Choices available are 1,2,3,4\nYou entered '{select_attribute}'")


def main():
    player = "Player has not been created"
    clear_screen()
    game_title()
    opponents_lst(read_enemy_csv)
    game_menu()
    print(dice(1))
    character_input()
    print(read_enemy_csv())


main()
