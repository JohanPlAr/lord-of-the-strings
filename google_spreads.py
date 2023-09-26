"""
Handles the API calls and csv reads and uploads
"""
import gspread
from google.oauth2.service_account import Credentials
from print_functions import text_center, game_title

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
    Adds the player to the Leader Board CSV file if player
    reaches the top 20. Only adds to the csv if player has
    a top 20 score.
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
    leader_board.append(player_row)
    sorted_list = sorted(leader_board, key=lambda x: int(x[6]), reverse=True)
    leader_board = sorted_list
    num = 0
    if len(sorted_list) > 19:
        for row in range(19):
            row = sorted_list[num]
            num += 1
            if player.score > int(row[6]):
                game_title()
                LEADER_BOARD.append_row(player_row)
                text_center(f"Congratulations you reached number {num-1}!")
                break
    else:
        for row in range(len(sorted_list)):
            row = sorted_list[num]
            num += 1
            if player.score > int(row[6]):
                game_title()
                LEADER_BOARD.append_row(player_row)
                text_center(f"Congratulations you reached number {num}!")
                break
            else:
                text_center(f'Score: "{player.score}" is too low for Leader Board')
                text_center("Better luck next time")
                break

    return leader_board


def download(enemy_lst):
    """
    Updates the enemy_lst with new enemies. The addenemy_lst list is crosschecked against enemy_lst
    and duplicates are removed. The enemy_lst is added to the bottom of addenemy_lst and then
    redefined to equal the updated addenemy_lst before returned.
    """
    addenemy_lst = MOREENEMIES.get_all_values()[1:]
    list_num = 0
    new_lst = [*enemy_lst]
    for row in addenemy_lst:
        list_num += 1
        if row[1] not in [sublist[1] for sublist in new_lst]:
            new_lst.append(row)
    return new_lst
