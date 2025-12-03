#Libs
from random import randint
import items as game
import objects as temp
from misc_actions import *

global_potions = {}
for potion in game.potions:
    global_potions.update({potion.name : potion.quantity})

global_items_dic = {}
for item in game.items_u:
    global_items_dic.update({item.name : item.quantity})

global_spells_l = []
for spell in game.spells:
    global_spells_l.append(spell.name)

#Active Buffs and Debuffs
active_debuffs_m = {}
active_buffs_m = {}

active_debuffs_p = {}
active_buffs_p = {}

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
            game.player.attack(game.monster)
        elif atks == 2 and cont.mana > 0:
            spells_l = global_spells_l
            for spell in game.spells:
                if isinstance(spell, temp.Debuff):
                    print(
                    f"{CYAN}{BOLD}✧ Debuff Spell:{RESET} {CYAN}{spell.name}{RESET} "
                    f"(Use {BLUE}{spell.exhaust}{RESET} Mana) — "
                    f"Hits for {ORANGE}{spell.atpower} Damage{RESET}"
                    f" | Has {CYAN}{spell.effect} Effect for {spell.duration} turns{RESET}"
                        )
                elif isinstance(spell, temp.Buff):
                    print(
                    f"{GREEN}{BOLD}✧ Buff Spell:{RESET} {GREEN}{spell.name}{RESET} "
                    f"(Use {BLUE}{spell.exhaust}{RESET} Mana) — "
                    f"Has {CYAN}{spell.effect} Effect for {spell.duration} turns{RESET}"
                        )
                else:
                    print(
                    f"{MAGENTA}{BOLD}✧ Arcane Spell:{RESET} {MAGENTA}{spell.name}{RESET} "
                    f"(Use {BLUE}{spell.exhaust}{RESET} Mana) — "
                    f"Hits for {ORANGE}{spell.atpower} Damage{RESET}"
                        )
            spellc = int(input("Choose spell: "))
            if isinstance(game.spells[spellc - 1], temp.Debuff):
                active_debuffs_m.update({(game.spells[spellc - 1]) : (game.spells[spellc - 1]).duration})
                game.player.mana -= game.spells[spellc - 1].exhaust
            elif isinstance(game.spells[spellc - 1], temp.Buff):
                active_buffs_p.update({(game.spells[spellc - 1]) : (game.spells[spellc - 1]).duration})
                game.player.mana -= game.spells[spellc - 1].exhaust
            else:
                game.player.spell(game.spells[spellc - 1], game.monster)
    elif cont == game.monster:
        print_banner("MONSTER SLASH", color=RED, separator='-')
        game.monster.attack(game.player)

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
                f"Costs {ORANGE}{game.potions[ind].price} money{RESET} |"
                )
            ind += 1
        potionc = int(input("Choose potion with number: "))
        if cont.money >= (game.potions[potionc - 1]).price:
            print_banner("HEAL ACTION", color=GREEN, separator='-')
            (game.potions[potionc - 1]).quantity -= 1
            potion_l[(game.potions[potionc - 1]).name] -= 1
            cont.money -= (game.potions[potionc - 1]).price
        else:
            print("Not enough assets")
            raise IndexError
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
    ind = 0
    for item in items_dic.keys():
        print(f"{ORANGE}{BOLD}✧ Item :{RESET} {ORANGE}{item}{RESET} | {items_dic[item]} left | Costs {game.items_u[ind].price}")
        ind += 1
    itemsc = int(input("Choose item with number: "))
    if cont.money >= game.items_u[itemsc - 1].price:
        cont.money -= game.items_u[itemsc - 1].price
        cont.equip(game.items_u[itemsc - 1])
        (game.items_u[itemsc - 1]).quantity -= 1
        items_dic[(game.items_u[itemsc - 1]).name] -= 1
        print(f"{GREEN}Equipped!{RESET}")
        for name in items_dic.keys():
            if items_dic[name] == 0:
                items_dic.pop(name)
                game.items_u.pop(itemsc - 1)
                break
    else:
        print(f"{RED}Not enough assets{RESET}")
        raise IndexError

def debuff_effect(cont):
    if active_debuffs_m and cont == game.monster:
        for element in list(active_debuffs_m.keys()):
            active_debuffs_m[element] -= 1
            if active_debuffs_m[element] < 0:
                print(f"The effect of {element.effect} has worn off!")
                if element.effect == "Stun":
                    cont.isStunned = False                    
                del active_debuffs_m[element]
                continue 

            if element.effect == "Poison":
                cont.debuff(element)
            elif element.effect == "Stun":
                cont.isStunned = True

    elif active_debuffs_p and cont == game.player:
        for element in list(active_debuffs_p.keys()):
            active_debuffs_p[element] -= 1
            if active_debuffs_p[element] < 0:
                print(f"The effect of {element.effect} has worn off!")
                if element.effect == "Stun":
                    cont.isStunned = False                    
                del active_debuffs_p[element]
                continue 

            if element.effect == "Poison":
                cont.debuff(element)
            elif element.effect == "Stun":
                cont.isStunned = True

def buff_effect(cont):
    if active_buffs_m and cont == game.monster:
        for element in list(active_buffs_m.keys()):
            active_buffs_m[element] -= 1
            if active_buffs_m[element] < 0:
                print(f"The effect of {element.effect} has worn off!")
                if element.effect == "Strength":
                    cont.damage -= element.atpower*element.duration
                if element.effect == "Resistance":
                    cont.shield -= element.atpower*element.duration       
                del active_buffs_m[element]
                continue 
            cont.buff(element)

    elif active_buffs_p and cont == game.player:
        for element in list(active_buffs_p.keys()):
            active_buffs_p[element] -= 1
            if active_buffs_p[element] < 0:
                print(f"The effect of {element.effect} has worn off!")
                if element.effect == "Strength":
                    cont.damage -= element.atpower*element.duration
                if element.effect == "Resistance":
                    cont.shield -= element.atpower*element.duration       
                del active_buffs_p[element]
                continue 
            cont.buff(element)