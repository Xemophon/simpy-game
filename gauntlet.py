#Simple Game
from time import sleep

#Modules
from actions import *
from objects import *
from items import *

#Game Loop
selected = 0
floor = 0
game.monster = game.beasts[floor]
print_splash_screen()
while selected == 0:
    try:
        print_banner("SELECT CLASS", color=RED, separator='/')
        ind = 0
        for clas in game.classes:
            ind += 1
            print(f"{ind}. {clas.role}")
        role_choice = int(input("Choice: "))
        game.player = game.classes[role_choice - 1]
        selected = 1
        show_stats(game.player)
    except Exception:
        print_banner("CHOOSE PLEASE", color=CYAN, separator='/')
sleep(2)
clean_up()

temp_health_1 = game.player.health
temp_health_2 = game.monster.health

while game.player.health > 0 and game.monster.health > 0:
    try:
        animated_banner(f"BATTLE ROUND {bround}", color=BLUE, separator='=')
        debuff_effect(game.player, active_debuffs_p)
        buff_effect(game.player, active_buffs_p)
        if game.player.isStunned == False:
            print_banner("ACTION PHASE", color=BLUE, separator='-')
            print(
                f"1. {RED}⚔️  ATTACK{RESET}     — Deal Damage\n"
                f"2. {GREEN}🧪  HEAL{RESET}       — Restore HP/Mana\n"
                f"3. {ORANGE}🏳️  SURRENDER{RESET}  — End Game"
            )
            print("-" * 45)
            choice_p = int(input("Choose action: "))
            if choice_p not in [1, 2]:
                if choice_p == 3:
                    animated_banner("ACTION: SURRENDERED", color=ORANGE, separator='~', time = 0.02)
                    break
                else:
                    raise ValueError
            choice_f(game.player, game.monster, choice_p)
            sleep(3)
            clean_up()
            status = health_check(game.player, game.monster, temp_health_1)
            stats_pulsate(game.player, status, game.monster, game.player)
            sleep(2)
        elif game.player.isStunned == True:
            print_banner("PLAYER STUNNED", color=ORANGE, separator='~')
        if game.monster.health <= 0:
            floor += 1
            if floor == 4:
                print_banner("YOU WON", color=GREEN, separator='*')
                sleep(3)
                break
            store(game.player, player_potions_1)
            animated_banner("NEXT FLOOR", color=GREEN, separator='*')
            game.monster = game.beasts[floor]
            print("\n")
            print_banner(f"{game.monster.name} aproaches", color=RED, separator='=')
            print("\n")
            bround = 1
            sleep(3)
            continue
        print_banner("MONSTER TURN", color=RED, separator='#')
        debuff_effect(game.monster, active_debuffs_m)
        buff_effect(game.monster, active_buffs_m)
        if game.monster.isStunned == False:
            choice_m = randint(1, 2)
            choice_f(game.monster, game.player, choice_m)
            sleep(3)
            clean_up()
            status = health_check(game.monster, game.player, temp_health_2)
            stats_pulsate(game.monster, status, game.monster, game.player)
            sleep(2)
        elif game.monster.isStunned == True:
            print_banner("MONSTER STUNNED", color=ORANGE, separator='~')
            sleep(2)
        if game.player.health <= 0:
            print_banner("YOU LOST", color=RED, separator='*')
            sleep(3)
            break
        game.player.refund_money(game.monster)
        bround += 1

    #Error Handling
    except ValueError:
        clean_up()
        print_banner("INPUTTED WRONG NUMBER, DUMMY", color=RED, separator='#')
        display_battle_status(game.monster, game.player)
    except TypeError as e :
        print_banner("DEV BUTCHERED --- EXITING", color=RED, separator='#')
        print(e)
        break
    except IndexError:
        clean_up()
        print_banner("NAUGHTY NAUGHTY - YOU DID SOMETHING ILLEGAL", color=RED, separator='#')
        display_battle_status(game.monster, game.player)