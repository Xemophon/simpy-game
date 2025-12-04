# Simpy Game - Console RPG

A turn-based, text-adventure RPG built in Python. Battle smart monsters, manage your economy, and utilize a complex system of spells, buffs, and degrading armor to survive.

## 🎮 Key Features

### ⚔️ Tactical Combat
* **Smart Enemy AI**: The monster isn't just a punching bag anymore. It can **cast spells**, **buff itself**, and **stun you**.
* **Advanced Shield System**: Armor is no longer a flat block. Your shield provides **% based damage mitigation** (4% per point, capped at 80%). However, shield integrity **degrades** with every hit, forcing you to time your defenses carefully.
* **Status Effects**: Master the flow of battle with **Stuns** (skip turns), **Poison** (DoT), and **Buffs** (Strength/Resistance).

### 💰 Economy & Assets
* **Earn & Spend**: You are no longer given everything for free. Defeating monsters earns you **Money** (Assets).
* **Shop System**: Potions and Equipment now have a **Price**. You must manage your finances to afford that life-saving "FulHeal" or "GodSword" mid-battle.

### 🪄 Expanded Magic
* **Offensive Spells**: "Blast", "Icicle", "Meteo Strike".
* **Strategic Buffs**: 
    * *Berserker Fury* (Damage Up)
    * *Earth's Protection* (Shield Regen)
    * *Bard Healing* (Health Regen)
    * *Mana Extraction* (Mana Regen)
* **Debuffs**: "Mirage" (Stun), "Deadly Mist" (Poison).

## 📂 Project Structure

The project is split into five modules for better organization:

* **`SImple_Game.py`**: The entry point. Runs the main game loop, handles turn progression, and checks win/loss conditions.
* **`actions.py`**: Contains the core logic for Player and Monster turns, including spell casting, AI decisions, and handling buff/debuff timers.
* **`objects.py`**: Defines the game classes (`Player`, `Monster`) and mechanic logic (Damage calculation, Shield degradation, Stat updates).
* **`items.py`**: The "Database" file. Initializes all items, spells, monsters, and player stats.
* **`misc_actions.py`**: Handles UI elements like health bars, banners, screen clearing, and ASCII art rendering.

## 🚀 How to Play

### Prerequisites
* Python 3.x

### Installation
1.  Clone the repository:
    ```bash
    git clone [https://github.com/xemophon/simpy-game.git](https://github.com/xemophon/simpy-game.git)
    ```
2.  Navigate to the directory:
    ```bash
    cd simpy-game
    ```

### Running the Game
Execute the main script:
```bash
python SImple_Game.py
