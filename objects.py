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
        roll_chance = randint(0, 100)
        if roll_chance > self.dodge_chance * 100:
            is_crit = False
            if isSpell == False:
                if randint(1, 100) <= self.crit_chance * 100:
                    is_crit = True
                    attack = int(self.damage * 1.5)
                else:
                    attack = randint(int(self.damage * 0.8), self.damage)
            else:
                attack = magic_attack
            if self.damage <= 0:
                print(f"  {CYAN}🛡️ {cont.name} evaded the attack.{RESET}")
            elif cont.shield == 0 or isSpell == True:
                if is_crit:
                    print(f"  {RED}💥💥 Critical Hit! {cont.name} took {attack} damage.{RESET}")
                else:
                    print(f"  {RED}💥 Direct Hit! {cont.name} took {round(attack)} damage.{RESET}")
                cont.health -= attack
            else:
                mitigation_percent = min(0.80, cont.shield * 0.04)
                damage_multiplier = 1 - mitigation_percent
                damage_taken = attack * damage_multiplier
                cont.health -= damage_taken
                shield_loss = 2 if attack > 30 else 1
                cont.shield = max(0, cont.shield - shield_loss)
                print(f"  {CYAN}🛡️ Shield Absorbs {int(mitigation_percent*100)}%! {cont.name} took {round(damage_taken)} dmg. (Shield -{shield_loss}){RESET}")
        else:
            print(f"  {CYAN}🛡️ {cont.name} evaded the attack.{RESET}")
    
    def spell(self, spell, cont):
        if isinstance(cont, Monster):
            if spell.type == cont.weakness:
                mattack = spell.atpower + round(spell.atpower * 0.5)
            else:
                mattack = randint(spell.atpower - 10, spell.atpower)
        else:
            mattack = randint(spell.atpower - 10, spell.atpower)
        self.mana -= spell.exhaust
        print(f"{BLUE}✨ {spell.name} CAST!{RESET} {cont.name} is struck by arcane energy!")
        print(f"  {RED}⚡ Damage Dealt: {mattack}{RESET} | Cost: {BLUE}{spell.exhaust} Mana{RESET}")
        self.attack(cont, True, mattack)

    def debuff(self, inflict):
        if inflict.effect == "Poison":
            self.health -= inflict.atpower
        elif inflict.effect == "Stun":
            self.isStunned = True
        elif inflict.effect == "Weakness":
            self.damage -= inflict.atpower
        elif inflict.effect == "Break":
            self.shield = 0
        print(f"  {GREEN}💥 {self.name} afflicted by {inflict.effect}. Took {round(inflict.atpower)} damage.{RESET}")

    def buff(self, rebound):
        if rebound.effect == "Heal":
            self.health += rebound.atpower
            if self.health > self.max_health:
                self.health = self.max_health
                print(f"  {GREEN}💚 {self.name} has {rebound.effect}. Healed to max health this turn.{RESET}")
            else:
                print(f"  {GREEN}💚 {self.name} has {rebound.effect}. Healed for {round(rebound.atpower)} this turn.{RESET}")
        elif rebound.effect == "Remana":
            self.mana += rebound.atpower
            if self.mana > self.max_mana:
                self.mana = self.max_mana
                print(f"  {BLUE}💙 {self.name} has {rebound.effect}. Returned to max mana this turn.{RESET}")
            else:
                print(f"  {BLUE}💙 {self.name} has {rebound.effect}. Returned {round(rebound.atpower)} mana this turn.{RESET}")
        elif rebound.effect == "Strength":
            self.damage += rebound.atpower
            print(f"  {RED}⚔️ {self.name} has {rebound.effect}. Buffed damage with {round(rebound.atpower)} this turn.{RESET}")
        elif rebound.effect == "Resistance":
            self.shield += rebound.atpower
            print(f"  {CYAN}🛡️ {self.name} has {rebound.effect}. Buffed shield with {round(rebound.atpower)} this turn.{RESET}")

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