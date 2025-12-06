#gamemodes
from subprocess import run
from misc_actions import *

try:
    print_banner(" SELECT GAMEMODE: ", BLUE, "=", 50)
    print_banner("1. THE GAUNTLET", RED, "*", 50)
    print("You fight through various monsters and levels with increasing difficulty.")
    print_banner("2. LOCAL PVP", ORANGE, "*", 50)
    print("You fight against a comrade on same PC.")
    print_banner("3. P2P PVP", CYAN, "*", 50)
    print("You fight against a comrade on local network.")
    gamemode = int(input("Enter gamemode: "))
    match gamemode:
        case 1:
            run(["python", "gauntlet.py"])     
        case 2:
            run(["python", "local_pvp.py"])  
        case 3:
            run(["python", "lan_pvp.py"]) 
except Exception as e:
    print("Exited")
    print(e)