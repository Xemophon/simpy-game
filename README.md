# Simpy Game - Console RPG

A turn-based, text-adventure RPG built in Python. Battle monsters, manage your health and mana, and utilize a variety of spells and items to survive.

## 🎮 Features

* **Turn-Based Combat**: Classic RPG battle system with Player vs. Monster mechanics.
* **Resource Management**: Manage **Health** and **Mana** carefully. Use potions to regenerate resources during battle.
* **Magic System**: Cast offensive spells like "Blast" and "Icicle" or inflict status effects like "Poison" and "Stun".
* **Inventory System**:
    * **Potions**: Restore Health and Mana (e.g., "Balanced Rejuvenation", "FulHeal").
    * **Equipment**: Equip weapons and armor to boost your Damage or Shield stats dynamically during the fight.
* **Rich Console UI**: Features color-coded text for damage types, healing, and alerts, along with ASCII art for monsters and UI banners.

## 📂 Project Structure

The game is modularized into four main Python files:

* **`SImple_Game.py`**: The main entry point. Contains the primary game loop, turn handling, and win/loss conditions.
* **`actions.py`**: Handles core game logic, including combat calculations, inventory management, UI rendering, and user input handling.
* **`objects.py`**: Defines the base classes for the game entities (`Player`, `Monster`) and item templates (`Weapon`, `Potion`, `Spell`).
* **`items.py`**: Acts as the database for the game, initializing specific instances of items, spells, and the player/monster stats.

## 🚀 How to Run

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

### Playing the Game
Run the main script to start the battle:
```bash
python SImple_Game.py
