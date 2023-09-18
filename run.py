import random
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

    return player


def main():
    game_title()
    print(dice(1))
    character_input()
    print(read_enemy_csv())


main()
