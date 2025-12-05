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
    def __init__(self, name, max_health, health, damage, shield, mana, isStunned = False, money = 150):
         self.name = name
         self.max_health = max_health
         self.health = health
         self.damage = damage
         self.shield = shield
         self.mana = mana
         self.isStunned = isStunned
         self.money = money

    def refund_money(self, cont):
        self.money += round((cont.max_health - cont.health) / 2)

    def attack(self, cont, isSpell = False, mattack = 0):
        if isSpell == False:
            attack = randint(self.damage-5, self.damage)
        else:
            attack = mattack
        if cont.shield == 0 or isSpell == True:
            cont.health -= attack
            print(f"  {RED}💥 Direct Hit! {cont.name} took {round(attack)} damage.{RESET}")
        else:
            mitigation_percent = min(0.80, cont.shield * 0.04)
            damage_multiplier = 1 - mitigation_percent
            damage_taken = attack * damage_multiplier
            cont.health -= damage_taken
            shield_loss = 2 if attack > 30 else 1
            cont.shield = max(0, cont.shield - shield_loss)
            print(f"  {CYAN}🛡️ Shield Absorbs {int(mitigation_percent*100)}%! {cont.name} took {round(damage_taken)} dmg. (Shield -{shield_loss}){RESET}")
    
    def spell(self, spell, cont):
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
            if self.mana > 200:
                self.mana = 200
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
    def __init__(self, name, atpower, exhaust):
        self.name = name
        self.atpower = atpower
        self.exhaust = exhaust

class Debuff(Spell):
    def __init__(self, name, atpower, exhaust, effect, duration):
        super().__init__(name, atpower, exhaust)
        self.effect = effect
        self.duration = duration

class Buff(Spell):
    def __init__(self, name, atpower, exhaust, effect, duration):
        super().__init__(name, atpower, exhaust)
        self.effect = effect
        self.duration = duration