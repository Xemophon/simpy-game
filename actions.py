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
        try:
            atks = int(input("Select type (1 or 2): "))
        except ValueError:
            atks = 1
        if atks == 1 or cont.mana <= 0:
            game.player.attack(game.monster)
        elif atks == 2 and cont.mana > 0:
            for i, spell in enumerate(game.spells):
                idx = i + 1
                if isinstance(spell, temp.Debuff):
                    print(
                    f"{idx}. {MAGENTA}{BOLD}Debuff:{RESET} {MAGENTA}{spell.name}{RESET} "
                    f"({BLUE}{spell.exhaust} Mana{RESET}) — "
                    f"{CYAN}{spell.effect} ({spell.duration} turns){RESET}"
                        )
                elif isinstance(spell, temp.Buff):
                    print(
                    f"{idx}. {GREEN}{BOLD}Buff:{RESET} {GREEN}{spell.name}{RESET} "
                    f"({BLUE}{spell.exhaust} Mana{RESET}) — "
                    f"{CYAN}{spell.effect} ({spell.duration} turns){RESET}"
                        )
                else:
                    print(
                    f"{idx}. {CYAN}{BOLD}Arcane:{RESET} {CYAN}{spell.name}{RESET} "
                    f"({BLUE}{spell.exhaust} Mana{RESET}) — "
                    f"Hits for {ORANGE}{spell.atpower} Dmg{RESET}"
                        )
            spellc = int(input("Choose spell: "))
            selected_spell = game.spells[spellc - 1]
            if cont.mana < selected_spell.exhaust:
                print(f"{RED}Not enough Mana! Cast failed.{RESET}")
                return
            if isinstance(selected_spell, temp.Debuff):
                cont.mana -= selected_spell.exhaust
                active_debuffs_m.update({selected_spell : selected_spell.duration})
                print(f"{GREEN}Cast Successful! {selected_spell.name} applied to Monster.{RESET}")
            elif isinstance(selected_spell, temp.Buff):
                cont.mana -= selected_spell.exhaust
                active_buffs_p.update({selected_spell : selected_spell.duration})
                print(f"{GREEN}Cast Successful! {selected_spell.name} applied to Player.{RESET}")
            else:
                game.player.spell(selected_spell, game.monster)
    elif cont == game.monster:
        magic_chance = randint(1, 10)
        spell_choice = game.spells[randint(0, len(game.spells) - 1)]
        if magic_chance > 7 and cont.mana >= spell_choice.exhaust:
            print_banner("MONSTER CASTING", color=MAGENTA, separator='*')
            if isinstance(spell_choice, temp.Buff):
                cont.mana -= spell_choice.exhaust
                active_buffs_m.update({spell_choice : spell_choice.duration})
                print(f"{RED}The Monster casts {MAGENTA}{spell_choice.name}{RED}!{RESET}")
                print(f"  {CYAN}Effect: {spell_choice.effect} applied to self for {spell_choice.duration} turns.{RESET}")
            elif isinstance(spell_choice, temp.Debuff):
                cont.mana -= spell_choice.exhaust
                active_debuffs_p.update({spell_choice : spell_choice.duration})
                print(f"{RED}The Monster casts {MAGENTA}{spell_choice.name}{RED}!{RESET}")
                print(f"  {CYAN}Effect: {spell_choice.effect} cast on Player for {spell_choice.duration} turns.{RESET}")
            else:
                cont.spell(spell_choice, game.player)
        else:
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
    cont.drink(game.potions[potionc - 1])
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
        if isinstance(game.items_u[ind], temp.Weapon):
            print(f"     {RED}└── ⚔️  Power: {game.items_u[ind].power}{RESET}")
        elif isinstance(game.items_u[ind], temp.Armor):
            print(f"     {CYAN}└── 🛡️  Block: {game.items_u[ind].armor}{RESET}")
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

def debuff_effect(cont, debuff_list):
    if debuff_list:
        for element in list(debuff_list.keys()):
            debuff_list[element] -= 1
            if debuff_list[element] < 0:
                print(f"The effect of {element.effect} has worn off!")
                if element.effect == "Stun":
                    cont.isStunned = False                    
                del debuff_list[element]
                continue
            cont.debuff(element)

def buff_effect(cont, buff_list):
    if buff_list:
        for element in list(buff_list.keys()):
            buff_list[element] -= 1
            if buff_list[element] < 0:
                print(f"The effect of {element.effect} has worn off!")
                if element.effect == "Strength":
                    cont.damage -= element.atpower*element.duration
                if element.effect == "Resistance":
                    cont.shield -= element.atpower*element.duration       
                del buff_list[element]
                continue 
            cont.buff(element)