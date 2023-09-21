"""
Handles the API calls and csv reads
"""
import gspread
from google.oauth2.service_account import Credentials
from print_functions import text_center

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive",
]

CREDS = Credentials.from_service_account_file("creds.json")
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
ENEMY = GSPREAD_CLIENT.open("enemy").sheet1
MOREENEMIES = GSPREAD_CLIENT.open("reset").sheet1
LEADER_BOARD = GSPREAD_CLIENT.open("leaderboard").sheet1


def read_enemy_csv():
    """
    Reads the google sheet file and stores it in the variable enemy_lst.
    enemy_lst variable is passed along during the game.
    """
    enemy_lst = ENEMY.get_all_values()[1:]
    return enemy_lst


def read_leader_board_csv():
    """
    Reads sorts and prints the leaderboard based on the score element
    """
    leader_board = LEADER_BOARD.get_all_values()[1:]
    sorted_list = sorted(leader_board, key=lambda x: int(x[6]), reverse=True)
    leader_board = sorted_list

    return leader_board


def upload_to_leader_board(player, leader_board):
    """
    Adds the player to the Leader Board CSV file if player has a
    minimum of 5 in Score.
    """
    player_row = [
        player.char_type,
        player.name,
        player.strength_points,
        player.health_points,
        player.skill_points,
        player.armor,
        player.score,
    ]
    if player.score > 4:
        LEADER_BOARD.append_row(player_row)
    else:
        text_center("You need a minimum of 5 in score to enter list")

    return leader_board


def download(enemy_lst):
    """
    Updates the enemy_lst with new enemies. The addenemy_lst list is crosschecked against enemy_lst
    and duplicates are removed. The enemy_lst is added to the bottom of addenemy_lst and then
    redefined to equal the updated addenemy_lst before returned.
    """
    addenemy_lst = MOREENEMIES.get_all_values()[1:]
    list_num = 0
    for row in addenemy_lst:
        list_num += 1
        if row[1] in [sublist[1] for sublist in enemy_lst]:
            addenemy_lst.pop(list_num - 1)
    list_num = 0
    for row in enemy_lst:
        list_num += 1
        if row[1] not in [sublist[1] for sublist in addenemy_lst]:
            addenemy_lst.append(row)
    enemy_lst = addenemy_lst
    return enemy_lst
