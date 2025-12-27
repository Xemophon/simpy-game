#Libs
from random import randint
#Colors
RED = '\033[91m'
GREEN = '\033[92m'
ORANGE = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m' 
CYAN = '\033[96m'
BOLD = '\033[1m'
RESET = '\033[0m'

#Controllable template
class Cont():
    def __init__(self, name, max_health, max_mana, health, damage, shield, mana, crit_chance, dodge_chance, isStunned = False, money = 150):
         self.name = name
         self.max_health = max_health
         self.max_mana = max_mana
         self.health = health
         self.damage = damage
         self.shield = shield
         self.mana = mana
         self.crit_chance = crit_chance
         self.dodge_chance = dodge_chance
         self.isStunned = isStunned
         self.money = money

    def refund_money(self, cont):
        self.money += round((cont.max_health - cont.health) / 2)

    def attack(self, cont, isSpell = False, magic_attack = 0):
        # Header for the action
        if not isSpell:
            print(f"\n {RED}⚔️  {self.name} attacks {cont.name}!{RESET}")

        roll_chance = randint(0, 100)
        
        # --- EVADE CHECK ---
        if roll_chance <= self.dodge_chance * 100:
             print(f" {CYAN}[🛡️ EVADE] {cont.name} dodged the attack!{RESET}")
             return

        # --- HIT CALCULATION ---
        is_crit = False
        if isSpell == False:
            if randint(1, 100) <= self.crit_chance * 100:
                is_crit = True
                attack = int(self.damage * 1.5)
            else:
                attack = randint(int(self.damage * 0.8), self.damage)
        else:
            attack = magic_attack

        # --- DAMAGE RESOLUTION ---
        if self.damage <= 0:
            print(f" {CYAN}[💨 MISS] The attack was too weak!{RESET}")
        
        # Direct Hit (No Shield or Magic Penetration)
        elif cont.shield == 0 or isSpell == True:
            if is_crit:
                print(f" {ORANGE}[💥 CRIT] {cont.name} takes {BOLD}{attack}{RESET}{ORANGE} dmg!{RESET}")
            else:
                print(f" {RED}[⚔️ HIT ] {cont.name} takes {BOLD}{round(attack)}{RESET}{RED} dmg.{RESET}")
            cont.health -= attack
        
        # Shield Mitigation
        else:
            mitigation_percent = min(0.80, cont.shield * 0.04)
            damage_multiplier = 1 - mitigation_percent
            damage_taken = attack * damage_multiplier
            
            cont.health -= damage_taken
            
            shield_loss = 2 if attack > 30 else 1
            cont.shield = max(0, cont.shield - shield_loss)
            
            block_amt = int(mitigation_percent * 100)
            print(f" {BLUE}[🛡️ BLOCK] Shield absorbed {block_amt}% damage.{RESET}")
            print(f"           {cont.name} takes {RED}{round(damage_taken)} dmg{RESET} (Shield -{shield_loss})")
    
    def spell(self, spell, cont):
        # Spell Header
        print(f"\n {BLUE}✨ {self.name} casts {spell.name}!{RESET}")
        
        if isinstance(cont, Monster):
            if spell.type == cont.weakness:
                print(f" {ORANGE}[🔥 WEAKNESS] It's super effective!{RESET}")
                mattack = spell.atpower + round(spell.atpower * 0.5)
            else:
                mattack = randint(spell.atpower - 10, spell.atpower)
        else:
            mattack = randint(spell.atpower - 10, spell.atpower)
            
        self.mana -= spell.exhaust
        # Pass to attack function for final processing
        self.attack(cont, True, mattack)

    def debuff(self, inflict):
        print(f" {MAGENTA}[☠️ DEBUFF] {self.name} is affected by {inflict.effect}!{RESET}")
        if inflict.effect == "Poison":
            self.health -= inflict.atpower
            print(f"           Took {RED}{inflict.atpower} poison damage.{RESET}")
        elif inflict.effect == "Stun":
            self.isStunned = True
            print(f"           {ORANGE}Stunned for 1 turn.{RESET}")
        elif inflict.effect == "Weakness":
            self.damage -= inflict.atpower
            print(f"           Damage reduced by {inflict.atpower}.{RESET}")
        elif inflict.effect == "Break":
            self.shield = 0
            print(f"           {RED}Shield BROKEN!{RESET}")

    def buff(self, rebound):
        print(f" {GREEN}[✨ BUFF] {self.name} uses {rebound.effect}!{RESET}")
        if rebound.effect == "Heal":
            self.health += rebound.atpower
            if self.health > self.max_health:
                self.health = self.max_health
                print(f"           {GREEN}Healed to MAX HP.{RESET}")
            else:
                print(f"           {GREEN}Restored {rebound.atpower} HP.{RESET}")
        elif rebound.effect == "Remana":
            self.mana += rebound.atpower
            if self.mana > self.max_mana:
                self.mana = self.max_mana
                print(f"           {BLUE}Restored to MAX MANA.{RESET}")
            else:
                print(f"           {BLUE}Restored {rebound.atpower} Mana.{RESET}")
        elif rebound.effect == "Strength":
            self.damage += rebound.atpower
            print(f"           {RED}Damage increased by {rebound.atpower}.{RESET}")
        elif rebound.effect == "Resistance":
            self.shield += rebound.atpower
            print(f"           {CYAN}Shield reinforced by {rebound.atpower}.{RESET}")

    def drink(self, potion):
        self.health += potion.heal
        self.mana += potion.remana
    
    def shielding(self, shielding):
        self.shield += shielding.armor
    
    def equip(self, itemj):
        if itemj.power > 0:
            self.damage += itemj.power
        elif itemj.armor > 0:
            self.shield += itemj.armor

class Player(Cont):
    def __init__(self, role, name, max_health, max_mana, health, damage, shield, mana, crit_chance, dodge_chance, isStunned = False, money = 150):
        super().__init__(name, max_health, max_mana, health, damage, shield, mana, crit_chance, dodge_chance, isStunned, money)
        self.role = role

class Monster(Cont):
    def __init__(self, weakness, role, name, max_health, max_mana, health, damage, shield, mana, crit_chance, dodge_chance, isStunned = False, money = 150):
        super().__init__(name, max_health, max_mana, health, damage, shield, mana, crit_chance, dodge_chance, isStunned, money)
        self.role = role
        self.weakness = weakness

#Item templates
class Item():
    def __init__(self, name, price, power, quantity, heal, armor, remana):
         self.name = name
         self.price = price
         self.power = power
         self.heal = heal
         self.armor = armor
         self.remana = remana
         self.quantity = quantity

class Weapon(Item):
    def __init__(self, name, price, power, quantity, heal = 0, armor = 0, remana = 0):
        super().__init__(name, price, power, quantity, heal, armor, remana)
        self.durability = 50

class Potions(Item):
    def __init__(self, name, price, heal, remana, quantity = 10, power = 0, armor = 0):
        super().__init__(name, price, power, quantity, heal, armor, remana)

class Armor(Item):
    def __init__(self, name, price, armor, quantity, remana = 0, power = 0, heal = 0):
        super().__init__(name, price, power, quantity, heal, armor, remana)

class Spell():
    def __init__(self, name, type, atpower, exhaust):
        self.name = name
        self.type = type
        self.atpower = atpower
        self.exhaust = exhaust

class Debuff(Spell):
    def __init__(self, name, type, atpower, exhaust, effect, duration):
        super().__init__(name, type, atpower, exhaust)
        self.effect = effect
        self.duration = duration

class Buff(Spell):
    def __init__(self, name, type, atpower, exhaust, effect, duration):
        super().__init__(name, type, atpower, exhaust)
        self.effect = effect
        self.duration = duration