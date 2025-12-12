#Template
from objects import *

#Classes
warrior = Player("Warrior", "Faruko", 200, 50, 200, 35, 15, 50, 0.3, 0.2)
mage = Player("Mage", "Kaputio", 120, 200, 120, 20, 10, 200, 0.2, 0.1)
rogue = Player("Rogue", "Harpun", 90, 100, 90, 25, 8, 100, 0.6, 0.3)

#Monster Types
boss = Monster(None, "Boss", "Govnior", 150, 200, 150, 30, 10, 200, 0.4, 0.1, False, float('inf'))
slime = Monster("Fire", "Minion", "Sticky Slime", 50, 20, 50, 8, 0, 20, 0.1, 0.3, False, 20)
goblin = Monster("Ice", "Scout", "Goblin Raider", 90, 50, 90, 15, 5, 50, 0.2, 0.1, False, 45)
orc = Monster(None, "Tank", "Orc Warlord", 140, 40, 140, 25, 20, 40, 0.1, 0.05, False, 80)
lich = Monster("Holy", "Mage", "Dark Lich", 80, 200, 80, 40, 2, 200, 0.3, 0.1, False, 100)

#Weapons
dagger = Weapon("Rusty Dagger", 15, 5, 1)
club = Weapon("Wooden Club", 10, 3, 1)
axe = Weapon("Battle Axe", 45, 15, 1)
spear = Weapon("Steel Spear", 40, 12, 1)
excalibur = Weapon("Excalibur", 150, 45, 1)
mjolnir = Weapon("Thunder Hammer", 120, 35, 1)
djin = Item("Jin Jitnq", 250, float("inf"), 1, float("inf"), float("inf"), float("inf"))

# --- ARMOR ---
leather = Armor("Leather Tunic", 15, 4, 1)
buckler = Armor("Wooden Buckler", 10, 2, 1)
chainmail = Armor("Chainmail Vest", 50, 14, 1)
kite_shield = Armor("Knight's Shield", 45, 12, 1)
dragon = Armor("Dragon Scale", 130, 35, 1)
aegis = Armor("Aegis of Immortality", 200, 50, 1)

# --- POTIONS ---
sip_hp = Potions("Sip of Health", 3, 5, 0, 10)
sip_mana = Potions("Sip of Mana", 3, 0, 5, 10)
elixir = Potions("Grand Elixir", 50, 50, 50, 3) # Full restore
panacea = Potions("Panacea", 30, 100, 0, 2) # Massive Heal, no mana
spirit_water = Potions("Spirit Water", 30, 0, 100, 2) # Massive Mana


#Spells
fblas = Spell("Flaming Blast", "Fire", 40, 40)
iblas = Spell("Icicle", "Ice", 25, 15)
lighty = Spell("Flying Crucifix", "Holy", 30, 20)
strike = Spell("Southern Gust", "Wind", 20, 10)
maxdop = Spell("Meteo Strike", "Physical", 100, 150)
poison = Debuff("Deadly Mist", "Witchery", 15, 35, "Poison", 3)
poweak = Debuff("Enchaining Smite", "Witchery", 10, 35, "Weakness", 2)
strip = Debuff("Buldozer", "Degrade", 10, 80, "Break", 1)
stun_1 = Debuff("Mirage","Physical", 5, 45, "Stun", 3)
barding = Buff("Bard Healing", None, 20, 50, "Heal", 4)
remaning = Buff("Mana Extraction", None, 15, 30, "Remana", 4)
berserk = Buff("Berserker Fury", None, 40, 80, "Strength", 2)
protec = Buff("Earth's Protection", None, 50, 80, "Resistance", 2)
cleanse = Buff("Soul Retribution", "Holy", 0, 50, "Cleanse", 1)

#Assigning Inventories
classes = [warrior, mage, rogue]

beasts = [slime, goblin, orc, lich, boss]

items_u = [dagger, club, axe, spear, excalibur, mjolnir, djin, leather, buckler, chainmail, kite_shield, dragon, aegis]

potions = [sip_hp, sip_mana, elixir, panacea, spirit_water]

spells = [fblas, iblas, lighty, strike, maxdop, poison, poweak, strip, stun_1, barding, remaning, berserk, protec, cleanse]

#Round and statuses
bround = 1
stunned = False