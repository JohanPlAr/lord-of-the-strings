import time

from google_spreads import (
    read_enemy_csv,
    read_leader_board_csv,
    upload_to_leader_board,
    download,
)
from dice_funcs import dice, battle_dice
from print_functions import (
    clear_screen,
    text_center,
    game_title,
    input_center,
    leave,
    long_text,
)
from ai_storyteller import configure, story


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
        player_string = f"{player_title}\n\n{abilities}"
        return player_string


def game_menu(player, enemy_lst, leader_board):
    """
    Holds the Game Menu which allows user to choose activities
    """
    menu = {}
    menu["\t\t1."] = "Create New Hero"
    menu["\t\t2."] = "Choose Opponent"
    menu["\t\t3."] = "Leader Board"
    menu["\t\t4."] = "View Stats"
    menu["\t\t5."] = "Download New Opponents"
    menu["\t\t6."] = "View Wins"
    menu["\t\t7."] = "Rules"
    menu["\t\t8."] = "Quit Game"

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
            character_input(player, enemy_lst, leader_board)
        elif selection == "2":
            if player != "Hero has not been created":
                while True:
                    game_title()
                    list_num = 0
                    player, enemy_lst, num = opponents_lst(
                        player, enemy_lst, leader_board, list_num
                    )
                    enemy, num = get_enemy(enemy_lst, num)
                    game_title()
                    print(enemy)
                    print()
                    text_center("1. Fight or 2.Flight?")
                    challenge = input_center("Choose wisely:")
                    if challenge.lower() == "fight" or challenge == "1":
                        story(player, enemy)
                        sword_battle(player, enemy_lst, enemy, num, leader_board)
                        break
                    elif challenge.lower() == "flight" or challenge == "2":
                        continue
                    else:
                        text_center('Wrong input, Please choose "1" or "2" to continue')
                        time.sleep(3)
            else:
                game_title()
                text_center(player)
                leave()
                game_menu(player, enemy_lst, leader_board)
        elif selection == "3":
            while True:
                game_title()
                if player != "Hero has not been created":
                    list_num = 1
                    opponents_lst(player, enemy_lst, leader_board, list_num)
                    player, enemy_lst, num = opponents_lst(
                        player, enemy_lst, leader_board, list_num
                    )
                    enemy, num = get_enemy(leader_board, num)
                    game_title()
                    print(enemy)
                    print()
                    text_center("1. Fight or 2.Flight?")
                    challenge = input_center("Choose wisely:")
                    if challenge.lower() == "fight" or challenge == "1":
                        story(player, enemy)
                        sword_battle(player, enemy_lst, enemy, num, leader_board)
                    elif challenge.lower() == "flight" or challenge == "2":
                        continue
                    else:
                        text_center("Wrong input, Please choose 1 or 2 to continue")
                        time.sleep(3)
                else:
                    game_title()
                    text_center(player)
                    leave()
                    break

        elif selection == "4":
            game_title()
            if player != "Hero has not been created":
                print(player)
                leave()
            else:
                text_center(player)
                leave()

        elif selection == "5":
            new_enemy_lst = download(enemy_lst)
            if len(new_enemy_lst) > len(enemy_lst):
                enemy_lst = new_enemy_lst
                text_center("New Opponents Successfully Downloaded")
                leave()
            else:
                text_center("No new enemies available")
                leave()
        elif selection == "6":
            game_title()
            wins_lst(enemy_lst)
            leave()
        elif selection == "7":
            game_title()
            text_center(RULES)

        elif selection == "8":
            upload_to_leader_board(player, leader_board)
            print(player)
            text_center("Successful upload to Leader Board")
            text_center("GOOD BYE!")
            exit()
        else:
            text_center("Invalid option selected. Please try again.")
            leave()


def opponents_lst(player, enemy_lst, leader_board, list_num):
    """
    Displays the enemies available for battle. Zip is used to display the list
    in two columns.
    """
    if list_num == 1:
        print_list = leader_board
    else:
        print_list = enemy_lst
    while True:
        game_title()
        two_col_lst = []
        x_num = 1
        columns = 2
        text_center("  NAME\t\tSCORE\t   NAME\t\tSCORE")
        for row in print_list:
            if row[3] != 0:
                two_col_lst.append(f"{x_num}. {row[1].upper()} \t{row[6]}")
                x_num += 1

        for first, second in zip(two_col_lst[::columns], two_col_lst[1::columns]):
            print(f"\t\t{first: <13} \t{second: <13}")

        undef_opponent_lst = []
        for row in print_list:
            if row[3] != 0:
                undef_opponent_lst.append(row)
        x_num = 0

        print()
        opponent = input_center("Please select an opponent or 'M' for back to menu: ")
        if opponent.lower() == "m":
            game_menu(player, enemy_lst, leader_board)
        try:
            opponent = int(opponent)
            if opponent - 1 in range(len(undef_opponent_lst)):
                num = opponent - 1
                for row in undef_opponent_lst:
                    x_num += 1
                    if opponent == x_num:
                        return player, enemy_lst, num

            else:
                game_title()
                text_center("Pick a number from the list or 'M' menu.")
                input_center(f"You entered '{opponent}'")

        except ValueError:
            game_title()
            text_center("Pick a number from the list or 'M' menu.")
            input_center(f"You entered '{opponent}'")

        else:
            game_title()
            print()

            text_center(player)
            leave()
            game_menu(player, enemy_lst, leader_board)
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


def character_input(player, enemy_lst, leader_board):
    """
    Handles the user input to create the player character. Automates unique
    stats for the types human/elf/dwarf/orc.
    """
    game_title()
    if player != "Hero has not been created":
        text_center(f" WARNING! Creating a new character will erase {player.name}")
        continue_create = input_center("Do you still wish to continue y/n?")
        if continue_create.lower() != "y":
            game_menu(player, enemy_lst, leader_board)

    text_center("CREATE A NEW CHARACTER")
    while True:
        print()
        name = input("\t\tNAME: ")
        print()
        if name == "":
            print("\t\t Please enter a NAME before next step")
        else:
            break
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
    add_stat_points(player, stat_points, enemy_lst, leader_board)
    return player


def stat_points_input(player, stat_points):
    """
    Handles ValueError for int(input())
    """
    while True:
        try:
            activate_stat_points = int(
                input_center("How many points do you wish to add: ")
            )
            if activate_stat_points > stat_points or activate_stat_points < 0:
                game_title()
                text_center(f"You have {stat_points} points to improve your stats")
                print(player)
                text_center(f"Please choose a number 0-{stat_points}")
        except ValueError:
            game_title()
            text_center(f"You have {stat_points} points to improve your stats")
            print(player)
            text_center(f"Please choose a number 0-{stat_points}")
            continue
        return int(activate_stat_points)


def add_stat_points(player, stat_points, enemy_lst, leader_board):
    """
    The final stage of the character creation which let's the user place stat_points
    of their choice. Also stat points are added after a battle
    """
    while True:
        game_title()
        if stat_points < 1:
            text_center(f"You have {stat_points} points to add to your stats")
            print(player)
            leave()
            game_menu(player, enemy_lst, leader_board)
        text_center(f"You have {stat_points} points to add to your abilities")
        print(player)
        if stat_points > 0:
            select_attribute = input_center("Choose ability: ")

        if select_attribute == "1":
            activate_stat_points = stat_points_input(player, stat_points)
            if activate_stat_points <= stat_points:
                player.strength_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                not_enough_points(player, stat_points, enemy_lst, leader_board)
        elif select_attribute == "2":
            activate_stat_points = stat_points_input(player, stat_points)
            if activate_stat_points <= stat_points:
                player.health_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                not_enough_points(player, stat_points, enemy_lst, leader_board)
        elif select_attribute == "3":
            activate_stat_points = stat_points_input(player, stat_points)
            if activate_stat_points <= stat_points:
                player.skill_points += activate_stat_points
                stat_points -= activate_stat_points
            else:
                not_enough_points(player, stat_points, enemy_lst, leader_board)
        elif select_attribute == "4":
            activate_stat_points = stat_points_input(player, stat_points)
            if activate_stat_points <= stat_points:
                player.armor += activate_stat_points
                stat_points -= activate_stat_points
            else:
                not_enough_points(player, stat_points, enemy_lst, leader_board)
        else:
            print(f"Choices available are 1,2,3,4\nYou entered '{select_attribute}'")


def not_enough_points(player, stat_points, enemy_lst, leader_board):
    """
    Reduces repetition of code in add_stat_points.
    """
    text_center(f"Not enough points left\nYou have {stat_points} left")
    add_stat_points(player, stat_points, enemy_lst, leader_board)


def sword_battle(player, enemy_lst, enemy, num, leader_board):
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
                add_stat_points(player, stat_points, enemy_lst, leader_board)
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
                add_stat_points(player, stat_points, enemy_lst, leader_board)
                leave()
                break


def main():
    """
    Controls calls for the api and game functions. Prints the "title-page"
    """
    configure()
    enemy_lst = read_enemy_csv()
    leader_board = read_leader_board_csv()
    game_title()
    text_center("A RPG-adventure game")
    text_center("Powered by the story-telling of chat-gpt\n")
    text_center("Now enter the realm")
    leave()
    clear_screen()
    player = "Hero has not been created"
    time.sleep(1)

    game_menu(player, enemy_lst, leader_board)


main()
