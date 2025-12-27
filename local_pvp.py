#Simple Game
from time import sleep
from copy import deepcopy
from random import choice

#Modules
from actions import *
from objects import *
from items import *

#Game Loop
names_list = ["Kael", "Thorne", "Elara", "Verrick", "Lyra", "Grom"]
selected = 0
while selected == 0:
    try:
        print_banner("SELECT CLASS", color=RED, separator='/')
        ind = 0
        for clas in game.classes:
            ind += 1
            print(f"{ind}. {clas.role}")
        role_choice_1 = int(input("Choice P1: "))
        role_choice_2 = int(input("Choice P2: "))
        game.player_1 = deepcopy(game.classes[role_choice_1 - 1])
        game.player_1.name = choice(names_list)
        names_list.remove(game.player_1.name)
        game.player_2 = deepcopy(game.classes[role_choice_2 - 1])
        game.player_2.name = choice(names_list)
        selected = 1
        show_stats(game.player_1)
        show_stats(game.player_2)
    except Exception as e:
        print_banner("CHOOSE PLEASE", color=CYAN, separator='/')
        print(e)
sleep(2)
clean_up()
while game.player_1.health > 0 and game.player_2.health > 0:
    try:
        print_banner(f"BATTLE ROUND {bround}", color=BLUE, separator='=')
        debuff_effect(game.player_1, active_debuffs_p)
        buff_effect(game.player_1, active_buffs_p)
        if game.player_1.isStunned == False:
            print_banner("ACTION PHASE P1", color=BLUE, separator='-')
            print(
                f"1. {RED}⚔️  ATTACK{RESET}     — Deal Damage\n"
                f"2. {GREEN}🧪  HEAL{RESET}       — Restore HP/Mana\n"
                f"3. {MAGENTA}🛡️  VISIT STORE{RESET} — Buy equipment and refill potions\n"
                f"4. {ORANGE}🏳️  SURRENDER{RESET}  — End Game"
            )
            print("-" * 45)
            choice_p = int(input("Choose action: "))
            if choice_p not in [1, 2]:
                if choice_p == 3:
                    store(game.player_1, player_potions_1)
                else:
                    print_banner("ACTION: SURRENDERED", color=RED, separator='~')
                    break
            else:
                choice_f(game.player_1, game.player_2, choice_p)
            sleep(2)
        elif game.player_1.isStunned == True:
            print_banner("P1 STUNNED", color=ORANGE, separator='~')
        if game.player_2.health <= 0:
            print_banner("P1 WON", color=ORANGE, separator='*')
            sleep(3)
            break
        print_banner("P2 TURN", color=RED, separator='#')
        debuff_effect(game.player_2, active_debuffs_m)
        buff_effect(game.player_2, active_buffs_m)
        if game.player_2.isStunned == False:
            print_banner("ACTION PHASE P2", color=ORANGE, separator='-')
            print(
                f"1. {RED}⚔️  ATTACK{RESET}     — Deal Damage\n"
                f"2. {GREEN}🧪  HEAL{RESET}       — Restore HP/Mana\n"
                f"3. {MAGENTA}🛡️  VISIT STORE{RESET} — Buy equipment and refill potions\n"
                f"4. {ORANGE}🏳️  SURRENDER{RESET}  — End Game"
            )
            print("-" * 45)
            choice_m = int(input("Choose action: "))
            if choice_m not in [1, 2]:
                if choice_m == 3:
                    store(game.player_2, player_potions_2)
                else:
                    print_banner("ACTION: SURRENDERED", color=RED, separator='~')
                    break
            else:
                choice_f(game.player_2, game.player_1, choice_m)
            sleep(2)
        elif game.player_2.isStunned == True:
            print_banner("P2 STUNNED", color=ORANGE, separator='~')
            sleep(2)
        if game.player_1.health <= 0:
            print_banner("P2 WON", color=CYAN, separator='*')
            sleep(3)
            break
        sleep(3)
        clean_up()        
        display_battle_status(game.player_2, game.player_1)
        sleep(2)
        game.player_1.refund_money(game.player_2)
        game.player_2.refund_money(game.player_1)
        bround += 1

    #Error Handling
    except ValueError:
        clean_up()
        print_banner("INPUTTED WRONG NUMBER, DUMMY", color=RED, separator='#')
        display_battle_status(game.player_2, game.player_1)
    except TypeError as e :
        print_banner("DEV BUTCHERED --- EXITING", color=RED, separator='#')
        print(e)
        break
    except IndexError:
        clean_up()
        print_banner("NAUGHTY NAUGHTY - YOU DID SOMETHING ILLEGAL", color=RED, separator='#')
        display_battle_status(game.player_2, game.player_1)