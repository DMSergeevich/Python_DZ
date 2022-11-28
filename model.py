import random


# ход бота
def second_bot(temp):
    if temp > 57:
        x = random.randrange(1, 29)
    elif 57 >= temp >= 30:
        x = temp-29
    elif temp == 29:
        x = random.randrange(1, 29)
    return x