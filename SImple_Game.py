#Simple Game
from time import sleep

#Modules
from actions import *
from objects import *
from items import *

#Game Loop
print_splash_screen()
sleep(2)
clean_up()
while player.health > 0 and monster.health > 0:
    try:
        if game.player.isStunned == False:
            print_banner(f"BATTLE ROUND {bround}", color=BLUE, separator='=')
            debuff_effect(game.player)
            buff_effect(game.player)
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
            choice_f(player, choice_p)
            sleep(2)
        elif game.player.isStunned == True:
            debuff_effect(game.player)
            buff_effect(game.player)
            print_banner("PLAYER STUNNED", color=ORANGE, separator='~')
        if monster.health <= 0:
            print_banner("YOU WON", color=GREEN, separator='*')
            break
        print_banner("MONSTER TURN", color=RED, separator='#')
        debuff_effect(game.monster)
        buff_effect(game.monster)
        if game.monster.isStunned == False:
            choice_m = randint(1, 2)
            choice_f(monster, choice_m)
        elif game.monster.isStunned == True:
            print_banner("MONSTER STUNNED", color=ORANGE, separator='~')
            display_battle_status(monster,player)
            sleep(2)
        if player.health <= 0:
            print_banner("YOU LOST", color=RED, separator='*')
            break
        sleep(3)
        clean_up()        
        display_battle_status(monster,player)
        sleep(2)
        game.player.refund_money(game.monster)
        bround += 1

    #Error Handling
    except ValueError:
        clean_up()
        print_banner("Inputted wrong number, dummy", color=RED, separator='#')
        display_battle_status(monster,player)
    except TypeError as e :
        print_banner("The dev butchered the code", color=RED, separator='#')
        print(e)
        break
    except IndexError:
        clean_up()
        print_banner("NAUGHTY NAUGHTY - YOU DID SOMETHING ILLEGAL", color=RED, separator='#')
        display_battle_status(monster,player)

#TODO Monster magic