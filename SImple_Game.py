#Simple Game

#Modules
from actions import *
from objects import *
from items import *

#Game Loop
print_splash_screen()
while player.health > 0 and monster.health > 0:
    try:
        print_banner(f"BATTLE ROUND {bround}", color=BLUE, separator='=')
        print_banner("ACTION PHASE", color=BLUE, separator='-')
        print(
            f"1. {RED}⚔️ ATTACK{RESET}     — Deal Damage\n"
            f"2. {GREEN}🧪 HEAL{RESET}       — Restore HP/Mana\n"
            f"3. {MAGENTA}🛡️ EQUIP/ITEM{RESET} — Gain Stats/Shield\n"
            f"4. {ORANGE}🏳️ SURRENDER{RESET}  — End Game"
        )
        print("-" * 45)
        choice_p = int(input("Choose action: "))
        if choice_p not in [1, 2, 3] :
            print_banner("ACTION: SURRENDERED", color=ORANGE, separator='~')
            break
        else:
            choice_f(player, choice_p)
            sleep(2)
            if monster.health <= 0:
                print_banner("YOU WON", color=GREEN, separator='*')
                break
            print_banner("MONSTER TURN", color=RED, separator='#')
            debuff_effect()
            if game.stunned == False:
                choice_m = randint(1, 2)
                choice_f(monster, choice_m)
                display_battle_status(monster,player)
                sleep(2)
            elif game.stunned == True:
                print_banner("MONSTER STUNNED", color=ORANGE, separator='~')
                display_battle_status(monster,player)
            if player.health <= 0:
                print_banner("YOU LOST", color=RED, separator='*')
                break
            bround += 1

    #Error Handling
    except ValueError:
        print("Inputted wrong number, retard")
    # except TypeError:
    #     print("The dev butchered the code")
    except IndexError:
        print("Naughty naughty, no such item there")

#TODO Buffs and Monster magic