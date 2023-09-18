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


def main():
    game_title()
    print(dice(1))


main()
