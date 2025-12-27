#Libs
import items as game
import objects as temp
from time import sleep
from os import system
import re

#Colors
RED = '\033[91m'
GREEN = '\033[92m'
DARKCYAN = '\033[36m'
ORANGE = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m' 
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

temp_health_1 = 0
temp_health_2 = 0

def clean_up():
    """Clears the console"""
    system('cls')

def health_check(cont, contr, temp):
    """Checks health to determine what attack color to push for animation"""
    status = "" # Default
    if cont.health == temp:
        status = "evaded"
    elif (temp - cont.health) >= (contr.damage * 1.5): 
        status = "crit"
    elif cont.health < temp:
        status = "atk"
    return status, cont.health
    
def strip_ansi(text):
    """Clears the format"""
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)

def show_stats(self):
    """Shows starting stats"""
    animated_banner(f"SELECTED {self.name} as {self.role}", color=RED, separator='/')
    print_banner(f"Health: {self.max_health}, Mana: {self.max_mana}, Damage:{self.damage}, Shield:{self.shield}", color=GREEN, separator='/')

def _generate_stat_line(cont):
    """Generates battle stats"""
    health_coef = cont.health / cont.max_health
    mana_coef = cont.mana / cont.max_mana
    bar_length = 20
    if isinstance(cont, temp.Player):
        pl_label = f"{CYAN} {cont.name} {RESET} " 
        health_color = GREEN if health_coef > 0.5 else ORANGE if health_coef > 0.25 else RED
        mana_color = BLUE
    else:
        pl_label = f"{MAGENTA}{cont.name}{RESET}"
        health_color = GREEN if health_coef > 0.5 else ORANGE if health_coef > 0.25 else RED
        mana_color = BLUE
    health_bar_filled = health_color + '█' * int(bar_length * health_coef) + RESET
    health_bar_empty = '░' * (bar_length - int(bar_length * health_coef))
    health_part = (
        f"{pl_label} Health: "
        f"{health_bar_filled}{health_bar_empty} "
        f"{int(cont.health):>3}/{cont.max_health:<3}"
    )
    mana_bar_filled = mana_color + '█' * int(bar_length * mana_coef) + RESET
    mana_bar_empty = '░' * (bar_length - int(bar_length * mana_coef))
    mana_part = (
        f"| Mana: {mana_bar_filled}{mana_bar_empty} "
        f"{int(cont.mana):>3}/{cont.max_mana}"
    )
    return health_part + " " + mana_part


def display_status(cont):
    """Displays controllable stats"""
    cont_line = _generate_stat_line(cont)
    cont_extra_stats = f"{RED}Damage: {cont.damage:<4} | Shield: {CYAN}{cont.shield}{RESET} | Assets: {ORANGE}{cont.money}{RESET}"
    return cont_line + f" {cont_extra_stats}"

def display_battle_status(cont_1, cont_2):
    """Displays battle stats"""
    print_banner("BATTLE STATS", color=BLUE, separator='~', length = 120)
    print(display_status(cont_1))
    print(display_status(cont_2))
    print(CYAN + "=" * 120 + RESET)
    print("\n")

def stats_pulsate(actor, status, cont_1, cont_2):
    """Animates the console output of the stats according to the changes"""
    frames = 6
    color_1 = ""
    color_2 = ""
    if actor == cont_2:
        if status == "atk": color_1 = RED # Player 1 takes damage
        elif status == "crit" : color_1 = ORANGE
        elif status == "evaded" : color_1 = CYAN
        elif status == "heal": color_2 = GREEN # Player 2 heals
    elif actor == cont_1:
        if status == "atk": color_2 = RED  
        elif status == "crit" : color_2 = ORANGE
        elif status == "evaded" : color_2 = CYAN
        elif status == "heal": color_1 = GREEN # Player 1 heals

    for _ in range(frames):
        clean_up()
        print_banner("BATTLE STATS", color=BLUE, separator='~', length=120)
        
        line_1 = display_status(cont_1)
        if color_1:
            print(f"{color_1}{strip_ansi(line_1)}{RESET}")
        else:
            print(line_1)
        line_2 = display_status(cont_2)
        if color_2:
            print(f"{color_2}{strip_ansi(line_2)}{RESET}")
        else:
            print(line_2)
        print(CYAN + "=" * 120 + RESET)
        print("\n")
        sleep(0.1) 
        clean_up()
        display_battle_status(cont_1, cont_2)
        sleep(0.1)
    clean_up()
    display_battle_status(cont_1, cont_2)

def print_banner(text, color=BLUE, separator="=", length = 45):
    """Prints a centered, colorized banner."""
    fill = separator * ((length - len(text) - 2) // 2)
    print(f"{color}{fill} {text} {fill}{RESET}")

def animated_banner(text, color=BLUE, separator="=", length = 45, time = 0.03):
    fill = separator * ((length - len(text) - 2) // 2)
    content = f"{color}{fill} {text} {fill}{RESET}"
    content_lst = list(content)
    output = ""
    for letter in content_lst:
        output += "".join(letter)
        print(f"{color} {output} {RESET}")
        sleep(time)
        clean_up()
    print(f"{color}{output}{RESET}")

def print_splash_screen():
    """Prints a centered, colorized main screen."""
    print(CYAN + "=" * 50 + RESET)
    print(f"{CYAN}       {MAGENTA}SIMPLE CONSOLE RPG - BATTLE COMMENCE!{RESET}")
    print(CYAN + "=" * 50 + RESET)
    print(f"{RED}{game.monster.name} appears...{RESET}")
    sleep(1)