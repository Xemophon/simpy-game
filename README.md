# Simpy Game ⚔️

![Python](https://img.shields.io/badge/Python-3.x-blue.svg)
![Status](https://img.shields.io/badge/Status-Active-green.svg)
![License](https://img.shields.io/badge/License-MIT-orange.svg)

**Simpy Game** is a feature-rich, turn-based console RPG built entirely in Python. It combines strategic combat, resource management, and real-time visual feedback into a terminal-based experience. Battle against AI monsters in the Gauntlet, challenge a friend on the same PC, or fight across the network in the new LAN PvP mode.

## ✨ Key Features

### ⚔️ Deep Tactical Combat
* **Shield Mechanics:** Shields provide **% based damage mitigation** but degrade over time. Managing your shield integrity is key to survival.
* **Status Effects:** Master the flow of battle with **Stuns** (skip turns), **Poison** (Damage over Time), **Weakness** (Damage Down), and **Breaks** (Shield Destruction).
* **Elemental System:** Enemies have specific elemental weaknesses (Fire, Ice, Holy, etc.) that deal critical damage.

### 👁️ Immersive Visuals
* **Pulsating Stats:** Health and Mana bars flash **Green** when healing or **Red/Orange** when taking damage/critical hits.
* **Color-Coded Logs:** Combat actions use distinct colors for Crits, Evades, Blocks, and Spells for instant readability.
* **Clean UI:** Menus for Spells, Potions, and the Shop are displayed in aligned, easy-to-read tables.

### 💰 Economy & Shop
* **Earn Assets:** Defeating monsters and winning rounds earns you Gold.
* **The Wandering Trader:** Visit the shop mid-game to purchase **Potions** (Health/Mana/Elixirs) or upgrade your **Equipment** (Weapons/Armor).

### 🌐 Multiplayer Support
* **Local PvP:** Hotseat mode for two players on a single keyboard.
* **LAN PvP:** Fully functional Peer-to-Peer networking using Python `sockets`. Host a game and battle a friend on your local Wi-Fi.

---

## 🎮 Game Modes

Launch the game with `python Simpy_Game.py` and choose from:

### 1. 🏰 The Gauntlet (PvE)
Ascend through floors of increasingly difficult enemies.
* **Enemies:** Slime → Goblin → Orc → Lich → **The Boss**.
* **Mechanic:** Health and Mana persist between fights. Use the **Campfire/Store** phase wisely to restock.

### 2. 🤝 Local PvP (Hotseat)
* Draft your class (Warrior, Mage, Rogue).
* Take turns on the same terminal window.
* Buy items between rounds to counter your opponent.

### 3. 🌐 LAN PvP (Network)
* **Host:** Select "Host Game" to open a server on port `5555`.
* **Join:** Enter the Host's local IP address to connect.
* **Sync:** Game state, health, and animations are synchronized across the network.

---

## 🛠️ Installation

**No external dependencies required!** This project uses only Python standard libraries (`socket`, `pickle`, `time`, `random`, `re`, `os`).

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/xemophon/simpy-game.git](https://github.com/xemophon/simpy-game.git)
    cd simpy-game
    ```

2.  **Run the Game**
    ```bash
    python Simpy_Game.py
    ```

---

## 📖 How to Play

### Controls
The game uses numeric inputs for navigation.
* `1`: **Attack** (Physical damage)
* `2`: **Heal / Potion** (Open Potion Satchel)
* `3`: **Shop / Item** (Open Store or Equip Menu)

### Classes
| Class | Role | Stats | Playstyle |
| :--- | :--- | :--- | :--- |
| **Warrior** | Tank | High HP, High Shield | Absorb damage and win attrition battles. |
| **Mage** | Caster | High Mana, Low HP | Glass cannon. Use spells to nuke enemies. |
| **Rogue** | DPS | High Crit, High Dodge | RNG-
