#Libs
from random import randint
from time import sleep
import items as game
import objects as temp

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

global_potions = {}
for potion in game.potions:
    global_potions.update({potion.name : potion.quantity})

global_items_dic = {}
for item in game.items_u:
    global_items_dic.update({item.name : item.quantity})

global_spells_l = []
for spell in game.spells:
    global_spells_l.append(spell.name)

active_debuffs = {}
active_buffs = {}

def choice_f(cont, choice_f):
        if choice_f == 1:
            atks_func(cont)
        elif choice_f == 2:
            potion_func(cont)
        elif choice_f == 3:
            item_func(cont)

def atks_func(cont):
    if cont == game.player:
        print_banner("PLAYER ATTACK", color=GREEN, separator='-')
        print(f"  {RED}1. ⚔️ PHYSICAL ATTACK{RESET}")
        print(f"  {BLUE}2. ✨ MAGICAL SPELL{RESET}")
        atks = int(input("Select type (1 or 2): "))
        if atks == 1 or cont.mana <= 0:
            cont.attack(game.monster)
        elif atks == 2 and cont.mana > 0:
            spells_l = global_spells_l
            for spell in game.spells:
                print(
                f"{MAGENTA}{BOLD}✧ Arcane Spell:{RESET} {MAGENTA}{spell.name}{RESET} "
                f"(Use {BLUE}{spell.exhaust}{RESET} Mana) — "
                f"Hits for {ORANGE}{spell.atpower} Damage{RESET}"
                    )
            spellc = int(input("Choose spell: "))
            cont.spell(game.spells[spellc - 1], game.monster)
            if isinstance(game.spells[spellc - 1], temp.Debuff):
                active_debuffs.update({(game.spells[spellc - 1]) : (game.spells[spellc - 1]).duration})
    elif cont == game.monster:
        print_banner("MONSTER SLASH", color=RED, separator='-')
        cont.attack(game.player)

def potion_func(cont):
    potion_l = global_potions
    if cont == game.player:
        print_banner("POTION INVENTORY", color=CYAN, separator='*')
        ind = 0
        for potion in potion_l.keys():
            print(
                f"{CYAN}{BOLD}✧ Potion :{RESET} {CYAN}{potion}{RESET} | {potion_l[potion]} left | "
                f"Returns {BLUE}{game.potions[ind].remana}{RESET} Mana | "
                f"Rejuvanates {GREEN}{game.potions[ind].heal} Health{RESET} |"
                )
            ind += 1
        potionc = int(input("Choose potion with number: "))
        print_banner("HEAL ACTION", color=GREEN, separator='-')
        (game.potions[potionc - 1]).quantity -= 1
        potion_l[(game.potions[potionc - 1]).name] -= 1
    elif cont == game.monster:
        print_banner("HEAL ACTION", color=GREEN, separator='-')
        potionc = randint(1,3)
    cont.heal(game.potions[potionc - 1])
    print(f"{GREEN}💚 REGENERATION SUCCESS!{RESET}")
    print(f"  {game.potions[potionc - 1].name} restored:")
    print(f"  ✨ {GREEN}+{game.potions[potionc - 1].heal} Health{RESET} | {BLUE}💧 +{game.potions[potionc - 1].remana} Mana{RESET}")
    if cont.health >= cont.max_health:
        cont.health = cont.max_health
        print(f"{ORANGE}🛡️ Health already MAXED ({int(cont.max_health)} HP)! Regeneration capped.{RESET}")
    for name in potion_l.keys():
        if potion_l[name] == 0:
            potion_l.pop(name)
            game.potions.pop(potionc - 1)
            break

def item_func(cont):
    print_banner("EQUIPMENT/ITEM USE", color=MAGENTA, separator='^')
    items_dic = global_items_dic
    for item in items_dic.keys():
        print(f"{ORANGE}{BOLD}✧ Item :{RESET} {ORANGE}{item}{RESET} | {items_dic[item]} left |")
    itemsc = int(input("Choose item with number: "))
    cont.equip(game.items_u[itemsc - 1])
    (game.items_u[itemsc - 1]).quantity -= 1
    items_dic[(game.items_u[itemsc - 1]).name] -= 1
    print(f"{GREEN}Equipped!{RESET}")
    for name in items_dic.keys():
        if items_dic[name] == 0:
            items_dic.pop(name)
            game.items_u.pop(itemsc - 1)
            break

def debuff_effect():
    if active_debuffs:
        for element in list(active_debuffs.keys()):
            active_debuffs[element] -= 1
            if active_debuffs[element] <= 0:
                print(f"The effect of {element.effect} has worn off!")
                if element.effect == "Stun":
                    game.stunned = False                    
                del active_debuffs[element]
                continue 

            if element.effect == "Poison":
                game.monster.debuff(element) 
                print(f"{RED}☠️ Poison deals damage!{RESET}")
            elif element.effect == "Stun":
                game.stunned = True

def _generate_stat_line(cont):
    health_coef = cont.health / cont.max_health
    mana_coef = cont.mana / 200
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
        f"{int(cont.mana):>3}/200"
    )
    return health_part + " " + mana_part

def display_battle_status(monster,player):
    print(MONSTER_ART) 
    print_banner("BATTLE STATS", color=BLUE, separator='~')
    monster_line = _generate_stat_line(monster)
    player_line = _generate_stat_line(player)
    monster_extra_stats = f"{RED}Damage: {monster.damage:<4} | Shield: {CYAN}{monster.shield}{RESET}"
    player_extra_stats = f"{GREEN}Damage: {player.damage:<4} | Shield: {CYAN}{player.shield}{RESET}"
    print(monster_line + f" {monster_extra_stats}")
    print(player_line + f" {player_extra_stats}")
    
    print(CYAN + "=" * 90 + RESET)

def print_banner(text, color=BLUE, separator="="):
    """Prints a centered, colorized banner."""
    length = 45
    fill = separator * ((length - len(text) - 2) // 2)
    print(f"{color}{fill} {text} {fill}{RESET}")

def print_splash_screen():
    print(CYAN + "=" * 50 + RESET)
    print(f"{CYAN}       {MAGENTA}SIMPLE CONSOLE RPG - BATTLE COMMENCE!{RESET}")
    print(CYAN + "=" * 50 + RESET)
    print(f"{RED}Your enemy appears...{RESET}")
    print(MONSTER_ART)
    sleep(1)