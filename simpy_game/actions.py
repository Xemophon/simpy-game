#Libs
from random import randint
import items as game
import objects as temp
from misc_actions import *

global_potions = {}
store_potions = {}
for potion in game.potions:
    global_potions.update({potion.name : potion.quantity})
    store_potions.update({potion.name : potion.price})

store_items = {}
for item in game.items_u:
    store_items.update({item.name : item.quantity})

global_spells_l = []
for spell in game.spells:
    global_spells_l.append(spell.name)

#Active Buffs and Debuffs
active_debuffs_m = {}
active_buffs_m = {}
player_potions_2 = global_potions.copy()

active_debuffs_p = {}
active_buffs_p = {}
player_potions_1 = global_potions.copy()

def choice_f(cont, contr , choice_f):
        if choice_f == 1:
            atks_func(cont, contr)
        elif choice_f == 2:
            potion_func(cont)

def atks_func(cont, contr):
    if isinstance(cont, temp.Player):
        print_banner("COMBAT MENU", color=GREEN, separator='-')
        print(f"  {RED}1. ⚔️  PHYSICAL ATTACK{RESET}")
        print(f"  {BLUE}2. ✨  SPELLBOOK{RESET}")
        
        try:
            atks = int(input(f"\n{BOLD}Select Action (1-2): {RESET}"))
        except ValueError:
            atks = 1

        # --- OPTION 1: ATTACK ---
        if atks == 1 or cont.mana <= 0:
            if cont.mana <= 0 and atks == 2:
                print(f"{RED}Not enough Mana! Forced to attack.{RESET}")
            cont.attack(contr)

        # --- OPTION 2: SPELLS ---
        elif atks == 2 and cont.mana > 0:
            print("\n")
            # Table Header
            print(f" {BOLD}{'No.':<4} {'Name':<18} {'Cost':<8} {'Effect / Damage'}{RESET}")
            print(f" {CYAN}{'-'*55}{RESET}")

            for i, spell in enumerate(game.spells):
                idx = i + 1
                spell_name = spell.name
                exhaust = f"{spell.exhaust} MP"
                
                # Dynamic formatting based on spell type
                if isinstance(spell, temp.Debuff):
                    effect_desc = f"{spell.effect} ({spell.duration} trn)"
                    row_color = MAGENTA
                    icon = "☠️"
                elif isinstance(spell, temp.Buff):
                    effect_desc = f"{spell.effect} ({spell.duration} trn)"
                    row_color = GREEN
                    icon = "✨"
                else: # Damage Spell
                    effect_desc = f"{spell.atpower} Dmg"
                    row_color = BLUE
                    icon = "🔥"

                # Print aligned row
                print(f" [{idx:<2}] {icon} {row_color}{spell_name:<18}{RESET} {BLUE}{exhaust:<8}{RESET} {row_color}{effect_desc}{RESET}")

            print("\n")
            try:
                spellc = int(input(f"{BOLD}Cast Spell (Enter No.): {RESET}"))
                selected_spell = game.spells[spellc - 1]
            except (ValueError, IndexError):
                print(f"{RED}Invalid spell selection.{RESET}")
                return

            # Execute Spell
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
                cont.spell(selected_spell, contr)

    # --- MONSTER AI ---
    elif isinstance(cont, temp.Monster):
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
    
    # Identify Inventory based on Player
    if isinstance(cont, temp.Player):
        if hasattr(game, 'player_2') and cont == game.player_2:
            potion_l = player_potions_2
        else:
            potion_l = player_potions_1
        
        # New Table Layout
        print_banner("POTION SATCHEL", color=CYAN, separator='*')
        print(f" {BOLD}{'No.':<4} {'Potion Name':<18} {'Qty':<5} {'Recovery Effect'}{RESET}")
        print(f" {CYAN}{'-'*55}{RESET}")

        for i, potion_name in enumerate(potion_l.keys()):
            stats = game.potions[i]
            qty = potion_l[potion_name]
            
            # Build recovery string (e.g., "+50 HP  +20 MP")
            recovery = ""
            if stats.heal > 0:
                recovery += f"{GREEN}💚 +{stats.heal:<4} HP{RESET} "
            if stats.remana > 0:
                recovery += f"{BLUE}💧 +{stats.remana:<4} MP{RESET}"
                
            print(f" [{i+1:<2}] {CYAN}{potion_name:<18}{RESET} x{qty:<4} | {recovery}")

        print("\n")
        try:
            potionc = int(input(f"{BOLD}Drink Potion (Enter No.): {RESET}"))
            selected_p = game.potions[potionc - 1]
            
            # Check Quantity
            if potion_l[selected_p.name] > 0:
                selected_p.quantity -= 1
                potion_l[selected_p.name] -= 1
                
                # Remove if empty
                if potion_l[selected_p.name] == 0:
                    potion_l.pop(selected_p.name)
                    game.potions.pop(potionc - 1)
            else:
                print("Empty!")
                raise IndexError

        except (ValueError, IndexError):
            print(f"{RED}Invalid selection.{RESET}")
            return
            
    elif isinstance(cont, temp.Monster):
        print_banner("HEAL ACTION", color=GREEN, separator='-')
        potionc = randint(1,3)
        if potionc > len(game.potions): potionc = 1 

    # Execute Drink
    cont.drink(game.potions[potionc - 1] if isinstance(cont, temp.Monster) else selected_p)
    
    # Feedback
    used_p = game.potions[potionc - 1] if isinstance(cont, temp.Monster) else selected_p
    
    print(f"\n {GREEN}{'='*15} RECOVERY {'='*15}{RESET}")
    print(f"  Action: {CYAN}Drank {used_p.name}{RESET}")
    print(f"  Result: {GREEN}💚 +{used_p.heal} HP{RESET}  {BLUE}💧 +{used_p.remana} MP{RESET}")
    print(f" {GREEN}{'='*40}{RESET}\n")

    # Cap Logic
    if cont.health >= cont.max_health:
        cont.health = cont.max_health
        print(f"  {ORANGE}(Health capped at {int(cont.max_health)}){RESET}")
    if cont.mana >= cont.max_mana:
        cont.mana = cont.max_mana
        print(f"  {ORANGE}(Mana capped at {int(cont.max_mana)}){RESET}")

def item_func(cont):
    clean_up()
    print_banner("AVIALABLE EQUIPMENT", color=MAGENTA, separator='^')
    items_dic = store_items
    ind = 0
    for item in items_dic.keys():
        print(f"{ORANGE}{BOLD}✧ Item :{RESET} {ORANGE}{item}{RESET} | {items_dic[item]} left | Costs {game.items_u[ind].price}")
        if isinstance(game.items_u[ind], temp.Weapon):
            print(f"     {RED}└── ⚔️  Power: {game.items_u[ind].power}{RESET}")
        elif isinstance(game.items_u[ind], temp.Armor):
            print(f"     {CYAN}└── 🛡️  Block: {game.items_u[ind].armor}{RESET}")
        ind += 1
    itemsc = int(input("Choose item with number: "))
    bitem = (game.items_u[itemsc - 1])
    if cont.money >= bitem.price:
        cont.money -= bitem.price
        cont.equip(bitem)
        bitem.quantity -= 1
        items_dic[bitem.name] -= 1
        animated_banner(f"SUCCSESSFULLY BOUGHT {bitem.name}", GREEN)
        for name in list(items_dic.keys()):
            if items_dic[name] == 0:
                items_dic.pop(name)
                game.items_u.pop(itemsc - 1)
                break
    else:
        raise IndexError

def store(cont, potion_list):
    ready = False
    potions = game.potions
    animated_banner("WANDERING TRADER", color=BLUE, separator='=')
    while ready == False:
        try:
            print_banner("STORE PHASE", color=ORANGE, separator='-')
            print(
                f"1. {MAGENTA}⚔️  EQUIPMENT{RESET}     — Buy Equipment\n"
                f"2. {GREEN}🧪  POTIONS{RESET}       — Buy Potions\n"
                f"3. {CYAN}🏳️ EXIT{RESET}  — Exit Store"
            )
            print("-" * 45)
            choice_p = int(input("Choose action: "))
            if choice_p == 1:
                item_func(cont)
                clean_up()
            elif choice_p == 2:
                for i, potion in enumerate(store_potions.keys()):
                    print(
                        f"{CYAN}{BOLD}✧ Potion :{RESET} {CYAN}{potion}{RESET}"
                        f"Returns {BLUE}{game.potions[i].remana}{RESET} Mana | "
                        f"Rejuvanates {GREEN}{game.potions[i].heal} Health{RESET} |"
                        f"Costs {ORANGE}{game.potions[i].price} Money{RESET} |"
                        )
                    sleep(2)
                potionc = int(input("Choose potion with number: "))
                bpotion = potions[potionc - 1]
                if cont.money >= bpotion.price:
                    animated_banner("SUCCSESSFULLY BOUGHT POTION", GREEN)
                    cont.money -= bpotion.price
                    if bpotion.name not in list(potion_list.keys()):
                        potion_list.update({bpotion.name : 1})
                    else:
                        potion_list[bpotion.name] += 1
                    sleep(1)
                    clean_up()
            elif choice_p == 3:
                ready = True
                clean_up()
            else:
                raise ValueError
            
        except ValueError:
            clean_up()
            print_banner("INPUTTED WRONG NUMBER, DUMMY", color=RED, separator='#')
        except TypeError:
            clean_up()
            print_banner("NOT ENOUGH ASSETS", RED)

def debuff_effect(cont, debuff_list):
    if debuff_list:
        for element in list(debuff_list.keys()):
            debuff_list[element] -= 1
            if debuff_list[element] < 0:
                print(f"The effect of {element.effect} has worn off!")
                if element.effect == "Stun":
                    cont.isStunned = False
                if element.effect == "Weakness":
                    cont.damage += element.atpower*element.duration            
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
                if element.effect == "Cleanse":
                    cleanse(active_debuffs_m if cont == game.monster or cont == game.player_2 else active_buffs_p)
                del buff_list[element]
                continue 
            cont.buff(element)

def cleanse(debuff_list):
    for item in list(debuff_list.keys()):
        del debuff_list[item]