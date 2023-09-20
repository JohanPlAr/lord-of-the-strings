"""Providing random number functions."""
import random
import os
import time
import textwrap
import gspread
from google.oauth2.service_account import Credentials
import openai
from dotenv import load_dotenv


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


def configure():
    """
    Fetches the API KEY from the .env file
    """
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")


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


def input_center(text):
    """
    Placing input label in center of 62 Characters line
    """
    txt = f"{text}".upper()
    num = round(len(txt) / 2)
    center_input = input(txt.rjust(62 // 2 + num))
    return center_input


def game_title():
    """
    Clears the screen and prints the game title
    """
    clear_screen()
    text_center("⚔⚔⚔---LORD OF THE STRINGS---⚔⚔⚔")
    print()


def leave():
    """
    Input used to pause program before user is leaving function.
    Asking the user to interact with enter before leaving.
    """
    input_center("MENU press Enter: ")
    if input_center is True:
        clear_screen()


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
    increase serendipity and allow higher uncertainty in the battles.
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
    enemy_lst = ENEMY.get_all_values()[1:]
    return enemy_lst


def read_leader_board_csv():
    leader_board = LEADER_BOARD.get_all_values()[1:]
    sorted_list = sorted(leader_board, key=lambda x: x[6])
    leader_board = sorted_list
    return leader_board


def upload_to_leader_board(player, leader_board):
    player_row = [
        player.char_type,
        player.name,
        player.strength_points,
        player.health_points,
        player.skill_points,
        player.armor,
        player.score,
    ]
    if player.score >= 0:
        LEADER_BOARD.append_row(player_row)
    else:
        text_center("You need a minimum of 5 score to enter list")

    return leader_board


class CharacterStats:
    """
    Object collects the character and selected enemy stats. __str__ used to make
    the print of the object prettier.
    """

    def __init__(
        self,
        char_type,
        name,
        strength_points,
        health_points,
        skill_points,
        armor,
        score,
    ):
        self.char_type = char_type
        self.name = name
        self.strength_points = strength_points
        self.health_points = health_points
        self.skill_points = skill_points
        self.armor = armor
        self.score = score

    def __str__(self):
        player_title = (
            f"---{self.name.upper()} THE MIGHTY {self.char_type.upper()}---".center(62)
        )
        abilities = f"""\t\t\t ⚔-SCORE-⚔:\t{self.score}
        \t\t1. STRENGTH:\t{self.strength_points}
        \t\t2. HEALTH:\t{self.health_points}
        \t\t3. SWORD SKILL:\t{self.skill_points}
        \t\t4. ARMOR:\t{self.armor}"""
        player_string = f"{player_title}\n{self.score}\n{abilities}"
        return player_string


def game_menu(player, enemy_lst):
    """
    Holds the Game Menu which allows user to choose activities
    """
    menu = {}
    menu["\t\t1."] = "Create New Hero"
    menu["\t\t2."] = "View Stats"
    menu["\t\t3."] = "Choose Opponent"
    menu["\t\t4."] = "View Wins"
    menu["\t\t5."] = "Download New Opponents"
    menu["\t\t6."] = "Leader Board"
    menu["\t\t7."] = "Quit Game"

    while True:
        game_title()
        text_center("GAME MENU:")
        print()
        options = menu.keys()
        options = sorted(options)
        for entry in options:
            print(entry, menu[entry])
        print()
        selection = input_center("Please select an option: ")
        if selection == "1":
            character_input(player, enemy_lst)
        elif selection == "2":
            game_title()
            if player != "Hero has not been created":
                print(player)
            else:
                text_center(player)
            leave()
        elif selection == "3":
            game_title()
            player, enemy_lst, num = opponents_lst(player, enemy_lst)
            enemy, num = get_enemy(enemy_lst, num)
            story(player, enemy)
            sword_battle(player, enemy_lst, enemy, num)
        elif selection == "4":
            game_title()
            wins_lst(enemy_lst)
            leave()
        elif selection == "5":
            enemy_lst = download(enemy_lst)
            print("New Opponents Successfully Downloaded")

        elif selection == "6":
            leader_board = read_leader_board_csv()
            upload_to_leader_board(player, leader_board)
            player, enemy_lst, num = opponents_lst(player, leader_board)
            enemy, num = get_enemy(enemy_lst, num)
            story(player, enemy)
            sword_battle(player, enemy_lst, enemy, num)
            #    enemy_lst = read_enemy_csv()
        elif selection == "7":
            print("Goodbye!")
            exit()
        else:
            print("Invalid option selected. Please try again.")


def opponents_lst(player, enemy_lst):
    """
    Displays the undefeated enemies available for battle. zip is used to display the list
    in two columns.
    """
    while True:
        two_col_lst = []
        x_num = 1
        columns = 2
        for row in enemy_lst:
            if row[3] != 0:
                two_col_lst.append(f"\t\t{x_num}. {row[1].upper()}")
                x_num += 1

        for first, second in zip(two_col_lst[::columns], two_col_lst[1::columns]):
            print(f"{first: <13}{second: <13}")

        if player != "Hero has not been created":
            print()
            opponent = input_center(
                "Please select an opponent or 'M' for back to menu: "
            )
            x_num = 0
            undef_opponent_lst = []
            for row in enemy_lst:
                if row[3] != 0:
                    undef_opponent_lst.append(row)
            if opponent.lower() == "m":
                game_menu(player, enemy_lst)
            try:
                if int(opponent) - 1 in range(len(undef_opponent_lst)):
                    for row in undef_opponent_lst:
                        x_num += 1
                        if int(opponent) == x_num:
                            num = int(opponent) - 1
                            return player, enemy_lst, num
            except ValueError:
                game_title()
                text_center("Pick a number from the list or 'M' menu.")
                text_center(f"You entered '{opponent}'")
            else:
                game_title()
                text_center("Pick a number from the list or 'M' menu.")
                text_center(f"You entered '{opponent}'")

        else:
            game_title()
            print()
            text_center(player)
            leave()
            game_menu(player, enemy_lst)
            break


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
    score = int(enemy_vals[6])
    enemy = CharacterStats(
        char_type, name, strength_points, health_points, skill_points, armor, score
    )
    return enemy, num


def wins_lst(enemy_lst):
    """
    Displays a list of the defeated enemies. Checks for health_points 0
    """
    text_center("DEFEATED OPPONENTS:")
    lst_num = 1
    for row in enemy_lst:
        if row[3] == 0:
            print(f"\t\t{lst_num}. {row[1]}")
            lst_num += 1
        else:
            lst_num = 1


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
    print(enemy_lst)
    return enemy_lst


def character_input(player, enemy_lst):
    """
    Handles the user input to create the player character. Automates unique
    stats for the types human/elf/dwarf/orc.
    """
    game_title()
    if player != "Hero has not been created":
        text_center(f" WARNING! Creating a new character will erase {player.name}")
        continue_create = input_center("Do you still wish to continue y/n?")
        if continue_create.lower() != "y":
            game_menu(player, enemy_lst)

    text_center("CREATE A NEW CHARACTER")
    while True:
        print()
        name = input("\t\tNAME: ")
        if name == "":
            print("\t\t Please enter a NAME before next step")
        else:
            break
        clear_screen
    time.sleep(1)
    while True:
        type_choice = input(
            "\t\t1. Human\n\t\t2. Elf\n\t\t3. Dwarf\n\t\t4. Orc\n\n\t\tTYPE: "
        ).lower()
        time.sleep(1)
        clear_screen()
        if type_choice == "1" or type_choice == "human":
            char_type = "human"
            strength_points = 2 + dice(1)
            health_points = 3 + dice(2)
            skill_points = 4 + dice(1)
            armor = 0
            stat_points = dice(2)
            score = 0
            player = CharacterStats(
                char_type,
                name,
                strength_points,
                health_points,
                skill_points,
                armor,
                score,
            )
            break
        elif type_choice == "2" or type_choice == "elf":
            char_type = "elf"
            strength_points = 2 + dice(1)
            health_points = 2 + dice(1)
            skill_points = 4 + dice(1)
            armor = 0
            stat_points = dice(3)
            score = 0
            player = CharacterStats(
                char_type,
                name,
                strength_points,
                health_points,
                skill_points,
                armor,
                score,
            )
            break
        elif type_choice == "3" or type_choice == "dwarf":
            char_type = "dwarf"
            strength_points = 3 + dice(2)
            health_points = 3 + dice(1)
            skill_points = 2 + dice(1)
            armor = dice(1)
            stat_points = dice(1)
            score = 0
            player = CharacterStats(
                char_type,
                name,
                strength_points,
                health_points,
                skill_points,
                armor,
                score,
            )
            break
        elif type_choice == "4" or type_choice == "orc":
            char_type = "orc"
            strength_points = 2 + dice(2)
            health_points = 2 + dice(1)
            skill_points = dice(1)
            armor = 3
            stat_points = dice(2)
            score = 0
            player = CharacterStats(
                char_type,
                name,
                strength_points,
                health_points,
                skill_points,
                armor,
                score,
            )
            break
        else:
            text_center(
                f"Choices available are Human/Elf/Dwarf/Orc\nYou entered '{type_choice}'"
            )
    add_stat_points(player, stat_points, enemy_lst)
    return player


def stat_points_input(stat_points):
    """
    Handles ValueError for int(input())
    """
    while True:
        try:
            activate_stat_points = int(
                input_center("How many points do you wish to add: ")
            )
            if activate_stat_points > stat_points:
                text_center(f"Please choose a number 1-{stat_points}")
        except ValueError:
            text_center(f"Please choose a number 1-{stat_points}")
            continue
        return int(activate_stat_points)


def add_stat_points(player, stat_points, enemy_lst):
    """
    The final stage of the character creation which let's the user place stat_points
    of their choice.
    """
    while True:
        game_title()
        if stat_points < 1:
            text_center(f"You have {stat_points} points to add to your stats")
            print(player)
            leave()
            game_menu(player, enemy_lst)
        text_center(f"You have {stat_points} points to add to your abilities")
        print(player)
        if stat_points > 0:
            select_attribute = input_center("Choose ability: ")

        if select_attribute == "1":
            activate_stat_points = stat_points_input(stat_points)
            if activate_stat_points <= stat_points:
                player.strength_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                not_enough_points(player, stat_points, enemy_lst)
        elif select_attribute == "2":
            activate_stat_points = stat_points_input(stat_points)
            if activate_stat_points <= stat_points:
                player.health_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                not_enough_points(player, stat_points, enemy_lst)
        elif select_attribute == "3":
            activate_stat_points = stat_points_input(stat_points)
            if activate_stat_points <= stat_points:
                player.skill_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                not_enough_points(player, stat_points, enemy_lst)
        elif select_attribute == "4":
          activate_stat_points = stat_points_input(stat_points)
            if activate_stat_points <= stat_points:
                player.armor += activate_stat_points
                stat_points -= activate_stat_points
            else:
                not_enough_points(player, stat_points, enemy_lst)
        else:
            print(f"Choices available are 1,2,3,4\nYou entered '{select_attribute}'")


def not_enough_points(player, stat_points, enemy_lst):
    """
    Reduces repetition of code in add_stat_points.
    """
    text_center(f"Not enough points left\nYou have {stat_points} left")
    add_stat_points(player, stat_points, enemy_lst)


def sword_battle(player, enemy_lst, enemy, num):
    """
    handles the battle logic between player and selected opponent.
    """
    total = 0
    clear_screen()
    text_center("⚔⚔⚔---Battle---⚔⚔⚔")
    player_dice = 5 + round(player.score / 10)
    enemy_dice = 5 + round(enemy.score / 10)

    while True:
        attack = (player.skill_points + battle_dice(player_dice, total)) - (
            enemy.skill_points + battle_dice(enemy_dice, total)
        )
        time.sleep(1)
        if attack == 0:
            text_center("The swords clash and no damage is dealt to either opponent")
            time.sleep(2)
        if attack > 0:
            damage = (player.strength_points + dice(1)) - round(
                enemy.armor + dice(1) + (enemy.skill_points / 2)
            )
            if damage < 1:
                damage = 1
            text_center(
                f"{player.name.upper()} strikes {enemy.name.upper()} who looses {damage} HP"
            )
            enemy.health_points -= damage
            text_center(f"{enemy.name.upper()} has {enemy.health_points} HP left")
            time.sleep(2)
            if enemy.health_points < 1:
                game_title()
                text_center(f"{enemy.name.upper()} recieves a final blow.")
                text_center(f"{player.name.upper()} lifts the sword in triumph")
                text_center(f"{enemy.name.upper()} is defeated.")

                input_center("Press enter to continue the quest:")
                time.sleep(1)
                dead = enemy_lst[num]
                dead[3] = 0
                enemy_lst.pop(num)
                enemy_lst.append(dead)
                player.score += 1
                stat_points = 3
                add_stat_points(player, stat_points, enemy_lst)
        if attack < 0:
            damage = (enemy.strength_points + dice(1)) - round(
                (player.armor + dice(1) + (player.skill_points / 2))
            )
            if damage < 1:
                damage = 1
            text_center(
                f"{enemy.name.upper()} strikes {player.name.upper()} who looses {damage} HP"
            )
            player.health_points -= damage
            text_center(f"{player.name.upper()} has {player.health_points} HP left")
            if player.health_points < 1:
                text_center(f"{player.name.upper()} recieves a final blow.")
                text_center(f"{enemy.name.upper()} lifts sword in triumph")
                input_center("The fight is over. Press enter: ")
                clear_screen()
                player.score -= 1
                player.health_points = 0
                stat_points = 3
                add_stat_points(player, stat_points, enemy_lst)
                leave()
                game_menu()
                break


def story(player, enemy):
    """
    Api call to chat-gpt asking it to reply to a string prepared with type and name.
    Length limit of the reply is included in the string
    """
    clear_screen()
    messages = [
        {"role": "system", "content": "You are a Storyteller"},
    ]
    message = f"""Set up with dialouge that leads to {player.name} the {player.char_type}
               and {enemy.name} the {enemy.char_type} drawing their weapons and comencing
               a sword_battle against eachother. 
               Maximum length 70 words"""
    if message:
        messages.append(
            {"role": "user", "content": message},
        )
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

    reply = chat.choices[0].message.content
    wrapped_reply = textwrap.wrap(reply, width=62)
    game_title()
    print("\n".join(wrapped_reply))
    messages.append({"role": "assistant", "content": reply})
    print()
    input_center("Press Enter to start the battle")


def main():
    """
    Controls calls for the api and game functions. Prints the "title-page"
    """
    configure()
    enemy_lst = ENEMY.get_all_values()[1:]
    game_title()
    text_center("A RPG-adventure game powered by the story-telling of chat-gpt")
    text_center("Now enter the realm")
    leave()
    clear_screen()
    player = "Hero has not been created"
    time.sleep(1)

    game_menu(player, enemy_lst)


main()
