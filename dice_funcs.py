"""
Functions handles the dice operations
"""
import random


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
