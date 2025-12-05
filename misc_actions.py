#Libs
import items as game
from time import sleep
from os import system

#Colors
RED = '\033[91m'
GREEN = '\033[92m'
ORANGE = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m' 
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'
MONSTER_ART = r"""
    __/\__
   ( O  O )
  ( \ -- / )
  \ \__/\ / /
   \ )  ( /
   /______\
  |________|         
"""

def clean_up():
    system('cls')

def show_stats(self):
    print_banner(f"SELECTED {self.role}", color=RED, separator='/')
    print_banner(f"Health: {self.max_health}, Mana: {self.max_mana}, Damage:{self.damage}, Shield:{self.shield}", color=GREEN, separator='/')

def _generate_stat_line(cont):
    health_coef = cont.health / cont.max_health
    mana_coef = cont.mana / cont.max_mana
    bar_length = 20
    if cont == game.player:
        pl_label = f"{GREEN}Player{RESET} " 
        health_color = GREEN if health_coef > 0.5 else ORANGE if health_coef > 0.25 else RED
        mana_color = BLUE
    else: # Monster
        pl_label = f"{RED}Monster{RESET}"
        health_color = GREEN if health_coef > 0.5 else ORANGE if health_coef > 0.25 else RED
        mana_color = BLUE
    # 1. Health Bar
    health_bar_filled = health_color + '█' * int(bar_length * health_coef) + RESET
    health_bar_empty = '░' * (bar_length - int(bar_length * health_coef))
    health_part = (
        f"{pl_label} Health: "
        f"{health_bar_filled}{health_bar_empty} "
        f"{int(cont.health):>3}/{cont.max_health:<3}"
    )
    # 2. Mana Bar
    mana_bar_filled = mana_color + '█' * int(bar_length * mana_coef) + RESET
    mana_bar_empty = '░' * (bar_length - int(bar_length * mana_coef))
    mana_part = (
        f"| Mana: {mana_bar_filled}{mana_bar_empty} "
        f"{int(cont.mana):>3}/{cont.max_mana}"
    )
    return health_part + " " + mana_part

def display_battle_status(monster,player):
    print_banner("BATTLE STATS", color=BLUE, separator='~', length = 120)
    monster_line = _generate_stat_line(monster)
    player_line = _generate_stat_line(player)
    monster_extra_stats = f"{RED}Damage: {monster.damage:<4} | Shield: {CYAN}{monster.shield}{RESET} | Assets: {ORANGE}inf{RESET}"
    player_extra_stats = f"{GREEN}Damage: {player.damage:<4} | Shield: {CYAN}{player.shield}{RESET} | Assets: {ORANGE}{player.money}{RESET}"
    print(monster_line + f" {monster_extra_stats}")
    print(player_line + f" {player_extra_stats}")
    print(CYAN + "=" * 120 + RESET)

def print_banner(text, color=BLUE, separator="=", length = 45):
    """Prints a centered, colorized banner."""
    fill = separator * ((length - len(text) - 2) // 2)
    print(f"{color}{fill} {text} {fill}{RESET}")

def print_splash_screen():
    print(CYAN + "=" * 50 + RESET)
    print(f"{CYAN}       {MAGENTA}SIMPLE CONSOLE RPG - BATTLE COMMENCE!{RESET}")
    print(CYAN + "=" * 50 + RESET)
    print(f"{RED}Your enemy appears...{RESET}")
    print(MONSTER_ART)
    sleep(1)