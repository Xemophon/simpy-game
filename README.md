# Simpy Game ⚔️

A comprehensive, turn-based console RPG built in Python. Use strategy, manage your economy, and battle against AI monsters or your friends via Local and LAN multiplayer.

## 📄 Overview

**Simpy Game** is a text-based role-playing game that simulates complex combat mechanics in a terminal environment. Unlike simple text adventures, it features a robust **stat system** (Health, Mana, Shield, Money), **economy management**, and **networking capabilities** for PvP battles.

## 🎮 Game Modes

You can select from three distinct game modes upon launching `Simpy_Game.py`:

1.  **🏰 The Gauntlet (PvE)**
    * Fight through floors of increasingly difficult monsters (Slime → Goblin → Orc → Lich → Boss).
    * Manage your resources (HP/Mana) between fights.
    * **Goal:** Survive all 5 levels to win.

2.  **🤝 Local PvP (Hotseat)**
    * Two players take turns on the *same computer*.
    * Draft your class (Warrior, Mage, Rogue) and battle to the death.
    * Includes an economy phase where players can buy items.

3.  **🌐 LAN PvP (P2P)**
    * Battle a friend over your **Local Area Network**.
    * Uses Python `socket` programming to sync game states.
    * One player Hosts, the other Joins via IP address.

## ✨ Key Features

### ⚔️ Tactical Combat System
* **Shield Mechanics:** Shields aren't just extra HP. They provide **% based damage mitigation** (4% per point) but **degrade** when hit.
* **Status Effects:**
    * **Stun:** Forces the opponent to skip a turn.
    * **Poison:** Deals damage over time.
    * **Buffs:** Temporarily increase Strength (Damage) or Resistance (Shield).
* **Classes:** Choose between **Warrior** (High HP/Defense), **Mage** (High Mana/Spells), or **Rogue** (High Crit/Dodge).

### 💰 Economy
* **Assets (Money):** You earn money by damaging opponents or winning rounds.
* **Shop:** Spend assets mid-battle on **Potions** (Health/Mana/Elixirs) or **Equipment** (Weapons/Armor) to turn the tide of battle.

## 🛠️ Installation & Setup

### Prerequisites
* **Python 3.x** is required.
* Standard libraries used: `socket`, `pickle`, `time`, `random`, `copy`, `os`, `subprocess`. (No `pip install` required!)

### Getting Started

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/yourusername/simpy-game.git](https://github.com/yourusername/simpy-game.git)
    cd simpy-game
    ```

2.  **Run the Game**
    ```bash
    python Simpy_Game.py
    ```

## 📖 How to Play LAN PvP

1.  Ensure both computers are on the same Wi-Fi/Network.
2.  **Player 1 (Host):**
    * Select **Gamemode 3** (P2P PVP).
    * Select **1. Host a Game**.
    * The console will display your IP Address (e.g., `192.168.1.5`). Share this with Player 2.
    * Wait for connection.
3.  **Player 2 (Client):**
    * Select **Gamemode 3** (P2P PVP).
    * Select **2. Join a Game**.
    * Enter the Host's IP Address when prompted.
4.  Once connected, both players pick their classes and the battle begins!

## 📂 Project Structure

* `Simpy_Game.py`: **Entry point**. Handles the main menu and game mode selection.
* `gauntlet.py`: Logic for the Single-player PvE campaign.
* `local_pvp.py`: Logic for Hotseat Multiplayer.
* `lan_pvp.py`: Handles **Networking**, socket connections, and data serialization (`pickle`) for online play.
* `actions.py`: Core combat logic (Attacking, Casting Spells, Using Items).
* `objects.py`: Class definitions for `Player`, `Monster`, and combat math (Crit/Dodge/Shield calcs).
* `items.py`: Database of all Items, Spells, Monsters, and Player Classes.
* `misc_actions.py`: UI utilities (Banners, Health Bars, Stat displays).

## 📄 License

This project is open-source. Feel free to fork and improve!
