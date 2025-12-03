#Template
from objects import *

#Objects of game
player = Cont("Faruko", 100, 100, 20, 10, 200)
monster = Cont("Govnior", 150, 150, 30, 10, 200, False, float('inf'))

potion1 = Potions("Balanced Rejuvenation", 7, 10, 10, 5)
potion2 = Potions("FulHeal", 15, 25, 0, 3)
potion3 = Potions("Remana", 15, 0, 25, 3)

sword = Weapon("GodSword", 60, 20, 2)
shield = Armor("Shield of Paladin", 25, 8, 1)
armor = Armor("Yielding Armor", 40, 10, 4 )

fblas = Spell("Blast", 40, 30)
iblas = Spell("Icicle", 25, 10)
maxdop = Spell("Meteo Strike", 100, 150)
poison = Debuff("Deadly Mist", 15, 35, "Poison", 3)
stun_1 = Debuff("Mirage", 5, 45, "Stun", 3)
barding = Buff("Bard Healing", 20, 50, "Heal", 4)
remaning = Buff("Mana Extraction", 15, 30, "Remana", 4)
berserk = Buff("Berserker Fury", 40, 80, "Strength", 2)
protec = Buff("Earth's Protection", 50, 80, "Resistance", 2)

#Assigning Inventories
potions = [potion1, potion2, potion3]

items_u = [shield, armor, sword]

spells = [fblas, iblas, maxdop, poison, stun_1, barding, remaning, berserk, protec]

bround = 1
stunned = False