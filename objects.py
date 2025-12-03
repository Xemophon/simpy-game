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
    def __init__(self, health, damage, shield, mana):
         self.health = health
         self.damage = damage
         self.shield = shield
         self.mana = mana

    def _tdamage(self, attack, isSpell = False):
        if self.shield == 0 or isSpell == True:
            self.health -= attack
            print(f"  {RED}💥 Direct Hit! Took {round(attack)} damage.{RESET}")
        else:
            self.health -= attack * 0.4
            self.shield -= 1
            print(f"  {CYAN}🛡️ Shield Active! Took {round(attack * 0.4)} damage. Shield: {self.shield}{RESET}")

    def debuff(self, inflict):
        self.damage -= inflict.atpower
        print(f"  {GREEN}💥 Monster afflicted by {inflict.effect}. Took {round(inflict.atpower)} damage.{RESET}")

    def heal(self, potion):
        self.health += potion.heal
    
    def remana(self,potion):
        self.mana += potion.remana
    
    def shielding(self, shielding):
        self.shield += shielding.armor
    
    def equip(self, itemj):
        if itemj.power > 0:
            self.damage += itemj.power
        elif itemj.armor > 0:
            self.shield += itemj.armor

class Player(Cont):
    def __init__(self, health, damage, shield, mana):
        super().__init__(health, damage, shield, mana)
        self.max_health = 100

    def attack(self, cont):
        attack = randint(self.damage - 15, self.damage)
        cont._tdamage(attack)
        print(f"  {GREEN}⚔️ You dealt {attack} damage.{RESET}")
    
    def spell(self, spell, cont):
        mattack = randint(spell.atpower - 10, spell.atpower)
        cont._tdamage(mattack, isSpell = True)
        self.mana -= spell.exhaust
        print(f"{BLUE}✨ {spell.name} CAST!{RESET} The monster is struck by arcane energy!")
        print(f"  {RED}⚡ Damage Dealt: {mattack}{RESET} | Cost: {BLUE}{spell.exhaust} Mana{RESET}")

class Monster(Cont):
    def __init__(self, health, damage, shield, mana):
        super().__init__(health, damage, shield, mana)
        self.max_health = 150
    
    def attack(self,cont):
        attack = randint(self.damage - 15, self.damage)
        cont._tdamage(attack)
        print(f"  {RED}⚔️ Monster dealt {attack} damage.{RESET}")

#Item templates
class Item():
    def __init__(self, name, power, quantity, heal, armor, remana):
         self.name = name
         self.power = power
         self.heal = heal
         self.armor = armor
         self.remana = remana
         self.quantity = quantity

class Weapon(Item):
    def __init__(self,name, power, quantity, heal = 0, armor = 0, remana = 0):
        super().__init__(name, power, quantity, heal, armor, remana)
        self.durability = 50

class Potions(Item):
    def __init__(self, name, heal, remana, quantity = 10, power = 0, armor = 0):
        super().__init__(name, power, quantity, heal, armor, remana)

class Armor(Item):
    def __init__(self, name, armor, quantity, remana = 0, power = 0, heal = 0):
        super().__init__(name, power, quantity, heal, armor, remana)

class Spell():
    def __init__(self, name, atpower, exhaust):
        self.name = name
        self.atpower = atpower
        self.exhaust = exhaust

class Debuff(Spell):
    def __init__(self, name, atpower, exhaust, effect, duration):
        super().__init__(name, atpower, exhaust)
        self.effect = effect
        self.duration = duration