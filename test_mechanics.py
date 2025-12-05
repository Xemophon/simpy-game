from objects import Player, Cont

def test_combat_mechanics():
    print("Initializing Player and Monster...")
    # High crit chance to ensure we see it, High dodge chance to ensure we see it
    player = Player("TestWarrior", "Tester", 100, 100, 100, 20, 0, 100, crit_chance=80, dodge_chance=0)
    monster = Cont("TestMonster", 100, 100, 100, 10, 0, 100, crit_chance=0, dodge_chance=80)

    print("\n--- Test 1: Player Attacks Monster (High Crit, High Dodge) ---")
    # Monster has 80% dodge, Player has 80% crit
    # We expect many DODGES, and if it hits, likely CRIT.
    for i in range(5):
        print(f"Attack {i+1}:")
        player.attack(monster)

    print("\n--- Test 2: Monster Attacks Player (No Crit, No Dodge) ---")
    # Player has 0 dodge, Monster has 0 crit
    # We expect normal hits.
    player.dodge_chance = 0
    monster.crit_chance = 0
    for i in range(3):
        print(f"Attack {i+1}:")
        monster.attack(player)

if __name__ == "__main__":
    test_combat_mechanics()
