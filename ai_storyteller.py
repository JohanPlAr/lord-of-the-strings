"""
"""
import os
import textwrap
import openai
from dotenv import load_dotenv
from print_functions import game_title, clear_screen, input_center


def configure():
    """
    Fetches the API KEY from the .env file
    """
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")


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
