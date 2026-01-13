import pygame
import sys
from random import randint

# --- CONSTANTS & CONFIG ---
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 60)
GREEN = (34, 139, 34)
BLUE = (30, 144, 255)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (50, 50, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

# Fonts
FONT_SIZE_MAIN = 24
FONT_SIZE_TITLE = 48
FONT_SIZE_SMALL = 18

# States
STATE_MENU = "MENU"
STATE_CLASS_SELECTION = "CLASS_SELECTION"
STATE_BATTLE = "BATTLE"
STATE_STORE = "STORE"
STATE_GAME_OVER = "GAME_OVER"
STATE_VICTORY = "VICTORY"

# --- ASSET MANAGEMENT ---
class AssetManager:
    def __init__(self):
        self.images = {}
        self.load_assets()

    def load_assets(self):
        # Define paths to expected images.
        # If file exists, load it. If not, we will use fallback colors.
        asset_list = {
            "player": "assets/player.png",
            "monster": "assets/monster.png",
            "background": "assets/background.png",
            "title": "assets/title.png"
        }

        for name, path in asset_list.items():
            try:
                img = pygame.image.load(path)
                self.images[name] = pygame.transform.scale(img, (100, 150)) if name in ["player", "monster"] else img
            except (FileNotFoundError, pygame.error):
                self.images[name] = None # Fallback to None

assets = None # Initialized in GameManager

class GameLogger:
    def __init__(self):
        self.messages = []
        self.max_messages = 7  # How many lines to show in the log box

    def log(self, text, color=WHITE):
        """Adds a message to the log."""
        # Clean ANSI codes if any (though we shouldn't introduce them)
        # We will store (text, color) tuples
        self.messages.append((text, color))
        if len(self.messages) > 50: # Keep history but display limited
             self.messages.pop(0)

    def get_recent(self):
        return self.messages[-self.max_messages:]

    def clear(self):
        self.messages = []

# Global Logger instance
logger = GameLogger()

class Cont:
    def __init__(self, name, max_health, max_mana, health, damage, shield, mana, crit_chance, dodge_chance, isStunned=False, money=150):
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
        self.active_buffs = {} # Map object -> duration
        self.active_debuffs = {} # Map object -> duration

    def refund_money(self, cont):
        gain = round((cont.max_health - cont.health) / 2)
        self.money += gain
        logger.log(f"Looted {gain} gold from {cont.name}.", YELLOW)

    def attack(self, cont, isSpell=False, magic_attack=0):
        if not isSpell:
            logger.log(f"{self.name} attacks {cont.name}!", RED)

        roll_chance = randint(0, 100)

        # --- EVADE CHECK ---
        if roll_chance <= self.dodge_chance * 100:
             logger.log(f"[EVADE] {cont.name} dodged the attack!", CYAN)
             return

        # --- HIT CALCULATION ---
        is_crit = False
        if isSpell == False:
            if randint(1, 100) <= self.crit_chance * 100:
                is_crit = True
                attack_val = int(self.damage * 1.5)
            else:
                attack_val = randint(int(self.damage * 0.8), self.damage)
        else:
            attack_val = magic_attack

        # --- DAMAGE RESOLUTION ---
        if self.damage <= 0: # This logic from original seems odd if magic_attack is high but self.damage is 0?
             # Original: if self.damage <= 0: print miss.
             # But if isSpell is true, we passed magic_attack.
             # Let's trust existing logic but adapt for spell context if needed.
             if not isSpell:
                 logger.log(f"[MISS] The attack was too weak!", GRAY)
                 return
             elif magic_attack <= 0:
                 logger.log(f"[MISS] The spell fizzled!", GRAY)
                 return

        # Direct Hit (No Shield or Magic Penetration)
        # Original: elif cont.shield == 0 or isSpell == True:
        if cont.shield == 0 or isSpell:
            if is_crit:
                logger.log(f"[CRIT] {cont.name} takes {attack_val} dmg!", ORANGE)
            else:
                logger.log(f"[HIT] {cont.name} takes {round(attack_val)} dmg.", RED)
            cont.health -= attack_val

        # Shield Mitigation
        else:
            mitigation_percent = min(0.80, cont.shield * 0.04)
            damage_multiplier = 1 - mitigation_percent
            damage_taken = attack_val * damage_multiplier

            cont.health -= damage_taken

            shield_loss = 2 if attack_val > 30 else 1
            cont.shield = max(0, cont.shield - shield_loss)

            block_amt = int(mitigation_percent * 100)
            logger.log(f"[BLOCK] Shield absorbed {block_amt}% damage.", BLUE)
            logger.log(f"{cont.name} takes {round(damage_taken)} dmg (Shield -{shield_loss})", RED)

    def spell(self, spell, cont):
        logger.log(f"{self.name} casts {spell.name}!", BLUE)

        mattack = 0
        if isinstance(cont, Monster):
            if spell.type == cont.weakness:
                logger.log(f"[WEAKNESS] It's super effective!", ORANGE)
                mattack = spell.atpower + round(spell.atpower * 0.5)
            else:
                mattack = randint(spell.atpower - 10, spell.atpower)
        else:
            mattack = randint(spell.atpower - 10, spell.atpower)

        self.mana -= spell.exhaust
        self.attack(cont, True, mattack)

    def debuff(self, inflict, target): # Changed signature to include target for logging
        # Logic from original objects.py/actions.py is split.
        # objects.py has debuff() which applies the EFFECT of the debuff tick.
        # But applying the debuff initially happens in spell logic.
        # Here we implement the 'tick' effect.

        logger.log(f"[DEBUFF] {self.name} is affected by {inflict.effect}!", MAGENTA)
        if inflict.effect == "Poison":
            self.health -= inflict.atpower
            logger.log(f"Took {inflict.atpower} poison damage.", RED)
        elif inflict.effect == "Stun":
            self.isStunned = True
            logger.log(f"Stunned for 1 turn.", ORANGE)
        elif inflict.effect == "Weakness":
            self.damage -= inflict.atpower
            logger.log(f"Damage reduced by {inflict.atpower}.", GRAY)
        elif inflict.effect == "Break":
            self.shield = 0
            logger.log(f"Shield BROKEN!", RED)

    def buff(self, rebound):
        logger.log(f"[BUFF] {self.name} uses {rebound.effect}!", GREEN)
        if rebound.effect == "Heal":
            self.health += rebound.atpower
            if self.health > self.max_health:
                self.health = self.max_health
                logger.log(f"Healed to MAX HP.", GREEN)
            else:
                logger.log(f"Restored {rebound.atpower} HP.", GREEN)
        elif rebound.effect == "Remana":
            self.mana += rebound.atpower
            if self.mana > self.max_mana:
                self.mana = self.max_mana
                logger.log(f"Restored to MAX MANA.", BLUE)
            else:
                logger.log(f"Restored {rebound.atpower} Mana.", BLUE)
        elif rebound.effect == "Strength":
            self.damage += rebound.atpower
            logger.log(f"Damage increased by {rebound.atpower}.", RED)
        elif rebound.effect == "Resistance":
            self.shield += rebound.atpower
            logger.log(f"Shield reinforced by {rebound.atpower}.", CYAN)

    def drink(self, potion):
        self.health += potion.heal
        self.mana += potion.remana
        logger.log(f"{self.name} drank {potion.name}.", GREEN)
        logger.log(f"+{potion.heal} HP, +{potion.remana} MP", GREEN)
        if self.health > self.max_health: self.health = self.max_health
        if self.mana > self.max_mana: self.mana = self.max_mana

    def equip(self, itemj):
        if itemj.power > 0:
            self.damage += itemj.power
            logger.log(f"Equipped {itemj.name}. Damage +{itemj.power}", YELLOW)
        elif itemj.armor > 0:
            self.shield += itemj.armor
            logger.log(f"Equipped {itemj.name}. Shield +{itemj.armor}", YELLOW)

class Player(Cont):
    def __init__(self, role, name, max_health, max_mana, health, damage, shield, mana, crit_chance, dodge_chance, isStunned = False, money = 150):
        super().__init__(name, max_health, max_mana, health, damage, shield, mana, crit_chance, dodge_chance, isStunned, money)
        self.role = role
        self.inventory_potions = {} # Name -> Qty

class Monster(Cont):
    def __init__(self, weakness, role, name, max_health, max_mana, health, damage, shield, mana, crit_chance, dodge_chance, isStunned = False, money = 150):
        super().__init__(name, max_health, max_mana, health, damage, shield, mana, crit_chance, dodge_chance, isStunned, money)
        self.role = role
        self.weakness = weakness

class Item:
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

class Potions(Item):
    def __init__(self, name, price, heal, remana, quantity = 10, power = 0, armor = 0):
        super().__init__(name, price, power, quantity, heal, armor, remana)

class Armor(Item):
    def __init__(self, name, price, armor, quantity, remana = 0, power = 0, heal = 0):
        super().__init__(name, price, power, quantity, heal, armor, remana)

class Spell:
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

# --- DATA INSTANTIATION (Copied from items.py) ---

def create_game_data():
    # Classes
    warrior = Player("Warrior", "Faruko", 200, 50, 200, 35, 15, 50, 0.3, 0.2)
    mage = Player("Mage", "Kaputio", 120, 200, 120, 20, 10, 200, 0.2, 0.1)
    rogue = Player("Rogue", "Harpun", 90, 100, 90, 25, 8, 100, 0.6, 0.3)

    # Monsters
    boss = Monster(None, "Boss", "Govnior", 150, 200, 150, 30, 10, 200, 0.4, 0.1, False, float('inf'))
    slime = Monster("Fire", "Minion", "Sticky Slime", 50, 20, 50, 8, 0, 20, 0.1, 0.3, False, 20)
    goblin = Monster("Ice", "Scout", "Goblin Raider", 90, 50, 90, 15, 5, 50, 0.2, 0.1, False, 45)
    orc = Monster(None, "Tank", "Orc Warlord", 140, 40, 140, 25, 20, 40, 0.1, 0.05, False, 80)
    lich = Monster("Holy", "Mage", "Dark Lich", 80, 200, 80, 40, 2, 200, 0.3, 0.1, False, 100)

    # Items
    dagger = Weapon("Rusty Dagger", 15, 5, 1)
    club = Weapon("Wooden Club", 10, 3, 1)
    axe = Weapon("Battle Axe", 45, 15, 1)
    spear = Weapon("Steel Spear", 40, 12, 1)
    excalibur = Weapon("Excalibur", 150, 45, 1)
    mjolnir = Weapon("Thunder Hammer", 120, 35, 1)
    djin = Item("Jin Jitnq", 250, float("inf"), 1, float("inf"), float("inf"), float("inf"))

    leather = Armor("Leather Tunic", 15, 4, 1)
    buckler = Armor("Wooden Buckler", 10, 2, 1)
    chainmail = Armor("Chainmail Vest", 50, 14, 1)
    kite_shield = Armor("Knight's Shield", 45, 12, 1)
    dragon = Armor("Dragon Scale", 130, 35, 1)
    aegis = Armor("Aegis of Immortality", 200, 50, 1)

    sip_hp = Potions("Sip of Health", 3, 5, 0, 5)
    sip_mana = Potions("Sip of Mana", 3, 0, 5, 5)
    elixir = Potions("Grand Elixir", 50, 50, 50, 2)
    panacea = Potions("Panacea", 30, 100, 0, 1)
    spirit_water = Potions("Spirit Water", 30, 0, 100, 1)

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

    return {
        "classes": [warrior, mage, rogue],
        "beasts": [slime, goblin, orc, lich, boss],
        "items": [dagger, club, axe, spear, excalibur, mjolnir, djin, leather, buckler, chainmail, kite_shield, dragon, aegis],
        "potions": [sip_hp, sip_mana, elixir, panacea, spirit_water],
        "spells": [fblas, iblas, lighty, strike, maxdop, poison, poweak, strip, stun_1, barding, remaning, berserk, protec, cleanse]
    }

# --- UI ELEMENTS ---

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=BLUE, text_color=WHITE, callback=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.callback = callback
        self.is_hovered = False

    def draw(self, surface, font):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, WHITE, self.rect, 2) # Border

        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered and event.button == 1 and self.callback:
                self.callback()

class GameManager:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Gauntlet V2")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, FONT_SIZE_MAIN)
        self.title_font = pygame.font.SysFont(None, FONT_SIZE_TITLE)

        self.data = create_game_data()
        self.state = STATE_MENU

        self.player = None
        self.monster = None
        self.floor = 0

        # UI Components
        self.buttons = []
        self.init_menu_buttons()

        # Battle Logic
        self.monster_turn_timer = 0
        self.awaiting_monster_turn = False

    def init_menu_buttons(self):
        self.buttons = []
        btn_w, btn_h = 200, 50
        start_y = 300

        # Create Class Selection Buttons
        for i, p_class in enumerate(self.data["classes"]):
            def make_callback(c):
                return lambda: self.select_class(c)

            btn = Button(
                (SCREEN_WIDTH - btn_w) // 2,
                start_y + i * (btn_h + 20),
                btn_w, btn_h,
                p_class.role,
                callback=make_callback(p_class)
            )
            self.buttons.append(btn)

    def select_class(self, p_class):
        self.player = p_class
        # Initialize Potions for player (using logic from actions.py - giving default potions)
        # Original logic: player_potions_1 = global_potions.copy()
        # We need to give the player some starting potions
        for p in self.data["potions"]:
            # Logic says 'quantity' in items.py, usually 10?
            # Actually items.py says: sip_hp = Potions(..., quantity=5)
            # So we create a personal inventory
            self.player.inventory_potions[p.name] = p.quantity

        self.start_floor(0)

    def start_floor(self, floor_idx):
        self.floor = floor_idx
        if self.floor >= len(self.data["beasts"]):
            self.state = STATE_VICTORY
            logger.log("YOU CONQUERED THE GAUNTLET!", GREEN)
            return

        self.monster = self.data["beasts"][self.floor]
        # Reset monster health for new encounter (since we share objects from list)
        self.monster.health = self.monster.max_health
        self.monster.shield = 0

        logger.clear()
        logger.log(f"Entering Floor {self.floor + 1}...", WHITE)
        logger.log(f"{self.monster.name} approaches!", RED)

        self.init_battle_buttons()
        self.state = STATE_BATTLE
        self.awaiting_monster_turn = False

    def init_battle_buttons(self):
        self.buttons = []
        # Action Buttons
        actions = ["Attack", "Spells", "Potions", "Surrender"]
        btn_w = 150
        spacing = 20
        start_x = 50
        y = 600

        self.buttons.append(Button(start_x, y, btn_w, 50, "Attack", color=RED, callback=self.player_attack))
        self.buttons.append(Button(start_x + (btn_w + spacing), y, btn_w, 50, "Spells", color=BLUE, callback=self.open_spell_menu))
        self.buttons.append(Button(start_x + (btn_w + spacing)*2, y, btn_w, 50, "Potions", color=GREEN, callback=self.open_potion_menu))
        self.buttons.append(Button(start_x + (btn_w + spacing)*3, y, btn_w, 50, "Surrender", color=GRAY, callback=self.surrender))

    def player_attack(self):
        if self.awaiting_monster_turn: return
        self.player.attack(self.monster)
        self.check_battle_end()
        if self.state == STATE_BATTLE:
            self.end_player_turn()

    def open_spell_menu(self):
        # Dynamically switch buttons to spells
        if self.awaiting_monster_turn: return
        self.buttons = []
        btn_w, btn_h = 180, 40
        rows = 4
        cols = 4

        # Back Button
        self.buttons.append(Button(50, 700, 100, 40, "Back", color=GRAY, callback=self.init_battle_buttons))

        for i, spell in enumerate(self.data["spells"]):
            r = i // cols
            c = i % cols

            x = 50 + c * (btn_w + 10)
            y = 500 + r * (btn_h + 10)

            def make_spell_cb(s):
                return lambda: self.cast_spell(s)

            # Check mana
            color = BLUE
            if self.player.mana < spell.exhaust:
                color = DARK_GRAY

            self.buttons.append(Button(x, y, btn_w, btn_h, f"{spell.name} ({spell.exhaust})", color=color, callback=make_spell_cb(spell)))

    def cast_spell(self, spell):
        if self.player.mana >= spell.exhaust:
            # Check spell type
            if isinstance(spell, Buff):
                self.player.mana -= spell.exhaust
                self.player.active_buffs[spell] = spell.duration
                logger.log(f"Cast {spell.name} on self.", GREEN)
            elif isinstance(spell, Debuff):
                self.player.mana -= spell.exhaust
                self.monster.active_debuffs[spell] = spell.duration
                logger.log(f"Cast {spell.name} on enemy.", MAGENTA)
            else:
                self.player.spell(spell, self.monster)

            self.check_battle_end()
            if self.state == STATE_BATTLE:
                self.end_player_turn()
        else:
            logger.log("Not enough Mana!", RED)

    def open_potion_menu(self):
        if self.awaiting_monster_turn: return
        self.buttons = []

        # Back Button
        self.buttons.append(Button(50, 700, 100, 40, "Back", color=GRAY, callback=self.init_battle_buttons))

        y = 500
        for name, qty in self.player.inventory_potions.items():
            if qty > 0:
                # Find potion obj
                potion_obj = next((p for p in self.data["potions"] if p.name == name), None)
                if potion_obj:
                    def make_pot_cb(p):
                        return lambda: self.drink_potion(p)

                    self.buttons.append(Button(200, y, 300, 40, f"{name} (x{qty})", color=GREEN, callback=make_pot_cb(potion_obj)))
                    y += 50

    def drink_potion(self, potion):
        if self.player.inventory_potions[potion.name] > 0:
            self.player.inventory_potions[potion.name] -= 1
            self.player.drink(potion)
            self.end_player_turn()

    def surrender(self):
        self.state = STATE_GAME_OVER
        logger.log("You surrendered.", RED)

    def end_player_turn(self):
        # Process Player Buffs/Debuffs (Tick down)
        self.process_effects(self.player)

        if self.monster.health <= 0:
            self.win_battle()
        else:
            self.awaiting_monster_turn = True
            self.monster_turn_timer = pygame.time.get_ticks() + 1000 # 1 sec delay

    def process_effects(self, char):
        # Debuffs
        to_remove = []
        for debuff, duration in char.active_debuffs.items():
            char.debuff(debuff, char) # Apply tick effect
            char.active_debuffs[debuff] -= 1
            if char.active_debuffs[debuff] <= 0:
                to_remove.append(debuff)
                logger.log(f"{debuff.effect} wore off.", WHITE)
        for d in to_remove: del char.active_debuffs[d]

        # Buffs
        to_remove_b = []
        for buff, duration in char.active_buffs.items():
            char.buff(buff)
            char.active_buffs[buff] -= 1
            if char.active_buffs[buff] <= 0:
                to_remove_b.append(buff)
                logger.log(f"{buff.effect} wore off.", WHITE)
        for b in to_remove_b: del char.active_buffs[b]

    def monster_turn(self):
        self.process_effects(self.monster)

        if self.monster.health <= 0: # Check if debuffs killed monster
            self.win_battle()
            return

        if self.monster.isStunned:
            logger.log(f"{self.monster.name} is stunned!", ORANGE)
            self.monster.isStunned = False # Consumed
        else:
            # AI Logic
            if self.monster.health < self.monster.max_health * 0.3 and randint(1, 10) > 7:
                 # Try heal
                 # Simplified monster potion
                 p = self.data["potions"][0]
                 self.monster.drink(p)
            else:
                 # Attack or Spell
                 if randint(1, 10) > 7:
                     # Cast random spell
                     s = self.data["spells"][randint(0, len(self.data["spells"])-1)]
                     if self.monster.mana >= s.exhaust:
                         # Monster casting logic
                         if isinstance(s, Buff):
                             self.monster.mana -= s.exhaust
                             self.monster.active_buffs[s] = s.duration
                             logger.log(f"Monster casts {s.name} (Buff)", MAGENTA)
                         elif isinstance(s, Debuff):
                             self.monster.mana -= s.exhaust
                             self.player.active_debuffs[s] = s.duration
                             logger.log(f"Monster casts {s.name} (Debuff)", MAGENTA)
                         else:
                             self.monster.spell(s, self.player)
                     else:
                         self.monster.attack(self.player)
                 else:
                     self.monster.attack(self.player)

        self.awaiting_monster_turn = False
        self.check_battle_end()
        # Reset Player buttons if still fighting
        if self.state == STATE_BATTLE:
             self.init_battle_buttons()

    def check_battle_end(self):
        if self.monster.health <= 0:
            self.win_battle()
        elif self.player.health <= 0:
            self.state = STATE_GAME_OVER
            logger.log("You have been defeated.", RED)

    def win_battle(self):
        logger.log(f"Victory! {self.monster.name} defeated.", GREEN)
        self.player.refund_money(self.monster)
        # Store State
        self.init_store_buttons()
        self.state = STATE_STORE

    def init_store_buttons(self):
        self.buttons = []
        self.buttons.append(Button(SCREEN_WIDTH - 200, SCREEN_HEIGHT - 100, 150, 50, "Next Floor", color=BLUE, callback=lambda: self.start_floor(self.floor + 1)))

        # Store Items
        y = 100
        x = 50
        # Equipment
        for item in self.data["items"]:
            if item.quantity > 0:
                def make_buy_cb(i):
                    return lambda: self.buy_item(i)

                label = f"{item.name} (${item.price})"
                self.buttons.append(Button(x, y, 300, 40, label, color=ORANGE, callback=make_buy_cb(item)))
                y += 50
                if y > 600:
                    y = 100
                    x += 350

    def buy_item(self, item):
        if self.player.money >= item.price and item.quantity > 0:
            self.player.money -= item.price
            item.quantity -= 1
            self.player.equip(item)
            logger.log(f"Bought {item.name}", GREEN)
            # Refresh buttons to update list/availability
            self.init_store_buttons()
        else:
            logger.log("Not enough money or out of stock.", RED)

    def draw(self):
        self.screen.fill(BLACK)

        if self.state == STATE_MENU:
            text = self.title_font.render("GAUNTLET V2", True, RED)
            rect = text.get_rect(center=(SCREEN_WIDTH//2, 100))
            self.screen.blit(text, rect)

            sub = self.font.render("Select your Class", True, WHITE)
            self.screen.blit(sub, (SCREEN_WIDTH//2 - sub.get_width()//2, 200))

        elif self.state == STATE_BATTLE:
            # Draw Background
            if assets and assets.images.get("background"):
                bg = pygame.transform.scale(assets.images["background"], (SCREEN_WIDTH, SCREEN_HEIGHT))
                self.screen.blit(bg, (0, 0))

            # Draw HUD
            self.draw_stats(self.player, 50, 50)
            self.draw_stats(self.monster, SCREEN_WIDTH - 300, 50)

            # Draw Log
            self.draw_log()

            # Draw Sprites
            player_rect = pygame.Rect(100, 250, 100, 150)
            if assets and assets.images.get("player"):
                self.screen.blit(assets.images["player"], player_rect)
            else:
                pygame.draw.rect(self.screen, BLUE, player_rect) # Fallback

            monster_rect = pygame.Rect(SCREEN_WIDTH - 200, 250, 100, 150)
            if assets and assets.images.get("monster"):
                self.screen.blit(assets.images["monster"], monster_rect)
            else:
                pygame.draw.rect(self.screen, RED, monster_rect) # Fallback

        elif self.state == STATE_STORE:
             title = self.title_font.render("WANDERING TRADER", True, YELLOW)
             self.screen.blit(title, (50, 20))

             money = self.font.render(f"Money: ${self.player.money}", True, GREEN)
             self.screen.blit(money, (SCREEN_WIDTH - 200, 50))

             self.draw_log() # Keep log visible to see purchase msg

        elif self.state == STATE_GAME_OVER:
             text = self.title_font.render("GAME OVER", True, RED)
             self.screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))

        elif self.state == STATE_VICTORY:
             text = self.title_font.render("VICTORY!", True, GREEN)
             self.screen.blit(text, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2))

        # Draw Buttons
        for btn in self.buttons:
            btn.draw(self.screen, self.font)

        pygame.display.flip()

    def draw_stats(self, char, x, y):
        # Name
        name = self.font.render(char.name, True, WHITE)
        self.screen.blit(name, (x, y))

        # HP Bar
        pygame.draw.rect(self.screen, DARK_GRAY, (x, y + 30, 200, 20))
        hp_pct = max(0, char.health / char.max_health)
        pygame.draw.rect(self.screen, RED, (x, y + 30, 200 * hp_pct, 20))
        hp_txt = self.font.render(f"{int(char.health)}/{char.max_health}", True, WHITE)
        self.screen.blit(hp_txt, (x + 5, y + 30))

        # MP Bar
        pygame.draw.rect(self.screen, DARK_GRAY, (x, y + 60, 200, 20))
        mp_pct = max(0, char.mana / char.max_mana)
        pygame.draw.rect(self.screen, BLUE, (x, y + 60, 200 * mp_pct, 20))
        mp_txt = self.font.render(f"{int(char.mana)}/{char.max_mana}", True, WHITE)
        self.screen.blit(mp_txt, (x + 5, y + 60))

        # Shield
        shield_txt = self.font.render(f"Shield: {char.shield}", True, CYAN)
        self.screen.blit(shield_txt, (x, y + 90))

    def draw_log(self):
        # Draw log box at bottom center (above buttons)
        log_rect = pygame.Rect(SCREEN_WIDTH//2 - 250, 450, 500, 140)
        pygame.draw.rect(self.screen, (20, 20, 20), log_rect)
        pygame.draw.rect(self.screen, WHITE, log_rect, 2)

        y = log_rect.top + 10
        for msg, color in logger.get_recent():
            txt = pygame.font.SysFont(None, 20).render(msg, True, color)
            self.screen.blit(txt, (log_rect.left + 10, y))
            y += 18

    def run(self):
        while True:
            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                for btn in self.buttons:
                    btn.handle_event(event)

            # Logic Update
            if self.state == STATE_BATTLE and self.awaiting_monster_turn:
                if pygame.time.get_ticks() >= self.monster_turn_timer:
                    self.monster_turn()

            # Draw
            self.draw()
            self.clock.tick(FPS)

if __name__ == "__main__":
    game = GameManager()
    game.run()
