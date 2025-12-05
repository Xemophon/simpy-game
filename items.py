#Template
from objects import *

#Classes
warrior = Player("Warrior", "Faruko", 200, 50, 200, 35, 15, 50)
mage = Player("Mage", "Kaputio", 100, 200, 100, 20, 10, 200)

boss = Cont("Govnior", 150, 200, 150, 30, 10, 200, False, float('inf'))

dagger = Weapon("Rusty Dagger", 15, 5, 1)
club = Weapon("Wooden Club", 10, 3, 1)

# Mid-Tier
axe = Weapon("Battle Axe", 45, 15, 1)
spear = Weapon("Steel Spear", 40, 12, 1)

# End-Game (High Cost, High Power)
excalibur = Weapon("Excalibur", 150, 45, 1)
mjolnir = Weapon("Thunder Hammer", 120, 35, 1)

# --- ARMOR ---
# Starter
leather = Armor("Leather Tunic", 15, 4, 1)
buckler = Armor("Wooden Buckler", 10, 2, 1)

# Mid-Tier
chainmail = Armor("Chainmail Vest", 50, 14, 1)
kite_shield = Armor("Knight's Shield", 45, 12, 1)

# End-Game
dragon = Armor("Dragon Scale", 130, 35, 1)
aegis = Armor("Aegis of Immortality", 200, 50, 1)

# --- POTIONS ---
# Budget / Small
sip_hp = Potions("Sip of Health", 3, 5, 0, 10)
sip_mana = Potions("Sip of Mana", 3, 0, 5, 10)

# High Tier
elixir = Potions("Grand Elixir", 50, 50, 50, 3) # Full restore
panacea = Potions("Panacea", 30, 100, 0, 2) # Massive Heal, no mana
spirit_water = Potions("Spirit Water", 30, 0, 100, 2) # Massive Mana


#Spells
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
classes = [warrior, mage]

items_u = [dagger, club, axe, spear, excalibur, mjolnir, leather, buckler, chainmail, kite_shield, dragon, aegis]

potions = [sip_hp, sip_mana, elixir, panacea, spirit_water]

spells = [fblas, iblas, maxdop, poison, stun_1, barding, remaning, berserk, protec]

#Round and statuses
bround = 1
stunned = False