#Template
from objects import *

#Objects of game
player = Player(100, 20, 10, 200)

monster = Monster(150, 30, 10, 200)

potion1 = Potions("Balanced Rejuvenation", 10, 10, 15)
potion2 = Potions("FulHeal", 25, 0, 5)
potion3 = Potions("Remana", 0, 25, 5)

sword = Weapon("GodSword", 20, 2)
shield = Armor("Shield of Paladin", 15, 1)
armor = Armor("Yielding Armor", 40, 5)

fblas = Spell("Blast", 40, 30)
iblas = Spell("Icicle", 25, 10)
maxdop = Spell("Meteo Strike", 100, 150)
poison = Debuff("Deadly Mist", 15, 35, "Poison", 3)
stun_1 = Debuff("Mirage", 20, 5, "Stun", 3)

#Assigning Inventories
potions = [potion1, potion2, potion3]

items_u = [shield, armor, sword]

spells = [fblas, iblas, maxdop, poison, stun_1]

bround = 1
stunned = False