"""
The functions in this file handles printing operations
"""
import os
import textwrap


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


def long_text(txt):
    """
    Breaks text line after 62 characters. Used for longer text prints.
    """
    wrapped_txt = textwrap.wrap(txt, width=62)
    print("\n".join(wrapped_txt))


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
