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
while game.player.health > 0 and game.monster.health > 0:
    try:
        print_banner(f"BATTLE ROUND {bround}", color=BLUE, separator='=')
        print("\n")
        debuff_effect(game.player, active_debuffs_p)
        buff_effect(game.player, active_buffs_p)
        if game.player.isStunned == False:
            print_banner("ACTION PHASE", color=BLUE, separator='-')
            print(
                f"1. {RED}⚔️  ATTACK{RESET}     — Deal Damage\n"
                f"2. {GREEN}🧪  HEAL{RESET}       — Restore HP/Mana\n"
                f"3. {MAGENTA}🛡️  EQUIP/ITEM{RESET} — Gain Stats/Shield\n"
                f"4. {ORANGE}🏳️  SURRENDER{RESET}  — End Game"
            )
            print("-" * 45)
            choice_p = int(input("Choose action: "))
            if choice_p not in [1, 2, 3]:
                print_banner("ACTION: SURRENDERED", color=ORANGE, separator='~')
                break
            choice_f(game.player, choice_p)
            sleep(2)
        elif game.player.isStunned == True:
            print_banner("PLAYER STUNNED", color=ORANGE, separator='~')
        if game.monster.health <= 0:
            floor += 1
            if floor == 4:
                print_banner("YOU WON", color=GREEN, separator='*')
                sleep(3)
                break
            clean_up()
            print_banner("NEXT FLOOR", color=GREEN, separator='*')
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
            choice_f(game.monster, choice_m)
        elif game.monster.isStunned == True:
            print_banner("MONSTER STUNNED", color=ORANGE, separator='~')
            sleep(2)
        if game.player.health <= 0:
            print_banner("YOU LOST", color=RED, separator='*')
            sleep(3)
            break
        sleep(3)
        clean_up()        
        display_battle_status(game.monster, game.player)
        sleep(2)
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