import socket
import pickle
import struct
from time import sleep
from copy import deepcopy
from os import system

# Import game modules
import items as game
from actions import *
from misc_actions import *
import objects as temp

# --- Network Utilities ---
def send_data(sock, data):
    """Pickles and sends data with a size prefix."""
    serialized = pickle.dumps(data)
    # Pack the length of the data as a 4-byte big-endian integer
    sock.sendall(struct.pack('>I', len(serialized)) + serialized)

def recv_data(sock):
    """Receives size prefix and then the full pickled data."""
    # Read the first 4 bytes to get the length
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the rest of the data
    return pickle.loads(recvall(sock, msglen))

def recvall(sock, n):
    """Helper to receive exactly n bytes."""
    data = bytearray()
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data.extend(packet)
    return data

# --- Game Setup ---
def setup_network():
    system('cls')
    print_banner("LAN PVP SETUP", color=MAGENTA)
    print("1. Host a Game")
    print("2. Join a Game")
    choice = input("Select option: ")

    if choice == '1':
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 0.0.0.0 listens on all available interfaces
        server_socket.bind(('0.0.0.0', 5555)) 
        server_socket.listen(1)
        
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        print_banner(f"HOSTING ON {local_ip}", color=GREEN)
        print("Waiting for opponent...")
        
        conn, addr = server_socket.accept()
        print(f"Connected to {addr}")
        return conn, True # True = I am Host (Player 1)
        
    elif choice == '2':
        target_ip = input("Enter Host IP: ")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((target_ip, 5555))
            print("Connected!")
            return client_socket, False # False = I am Client (Player 2)
        except:
            print("Connection failed.")
            sleep(2)
            return None, None
            
    return None, None

def select_character():
    print_banner("SELECT CLASS", color=RED, separator='/')
    ind = 0
    for clas in game.classes:
        ind += 1
        print(f"{ind}. {clas.role}")
    
    while True:
        try:
            role_choice = int(input("Choice: "))
            if 1 <= role_choice <= len(game.classes):
                # Return a COPY so we don't modify the template
                return deepcopy(game.classes[role_choice - 1])
        except ValueError:
            pass
        print("Invalid choice.")

# --- Main PvP Loop ---
def run_lan_game():
    conn, is_host = setup_network()
    if not conn:
        return

    # 1. Select Character
    my_player = select_character()
    game.player = my_player # Set global for stat display functions

    print("Waiting for opponent to select...")
    
    # 2. Exchange Initial States
    # Send my character data
    send_data(conn, my_player)
    # Receive enemy character data
    enemy_player = recv_data(conn)
    
    if not enemy_player:
        print("Opponent disconnected.")
        return

    print_banner(f"VERSUS: {enemy_player.role}", color=RED)
    sleep(2)

    # 3. Battle Loop
    battle_active = True
    
    # Host goes first
    my_turn = is_host
    
    while my_player.health > 0 and enemy_player.health > 0:
        clean_up()
        
        # Display Stats (Enemy is passed as 'monster' so it shows Red)
        display_battle_status(enemy_player, my_player)
        
        if my_turn:
            print_banner("YOUR TURN", color=GREEN)
            
            # Apply my Buffs/Debuffs locally
            debuff_effect(my_player, active_debuffs_p)
            buff_effect(my_player, active_buffs_p)
            
            if not my_player.isStunned:
                print(
                    f"1. {RED}⚔️  ATTACK{RESET}\n"
                    f"2. {GREEN}🧪  HEAL{RESET}\n"
                    f"3. {MAGENTA}🛡️  VISIT STORE{RESET}"
                )
                try:
                    choice_p = int(input("Action: "))
                    if choice_p in [1, 2]:
                        # Execute action locally against the copy of the enemy
                        choice_f(my_player, enemy_player, choice_p)
                        if choice_p == 1:
                            status = "atk"
                            stats_pulsate(my_player, status, enemy_player, my_player)
                        elif choice_p == 2:
                            status = "heal"
                            stats_pulsate(my_player, status, enemy_player, my_player)

                    elif choice_p == 3:
                        # Open Store - This takes a turn
                        store(my_player, player_potions_1)
                    else:
                        print("Skipped turn (Invalid Input)")
                except ValueError:
                    print("Skipped turn (Invalid Input)")
            else:
                print_banner("YOU ARE STUNNED", color=ORANGE)
            
            sleep(1)
            print("Sending move to opponent...")
            
            # Send the updated state of BOTH players to sync the game
            # We send [My_New_State, Enemy_New_State_After_Damage]
            send_data(conn, (my_player, enemy_player))
            
            my_turn = False
            
        else:
            print_banner("OPPONENT'S TURN", color=RED)
            print("Waiting for move...")
            
            # Wait for data
            new_states = recv_data(conn)
            if not new_states:
                break
                
            # Unpack: The sender sent (Them, Me). 
            # So for me, index 0 is Enemy, index 1 is Me.
            enemy_player = new_states[0]
            my_player = new_states[1]
            
            # Update global reference for UI
            game.player = my_player 
            
            my_turn = True

    # End Game
    clean_up()
    display_battle_status(enemy_player, my_player)
    
    if my_player.health > 0:
        print_banner("YOU WON!", color=GREEN, separator='*')
    else:
        print_banner("YOU LOST...", color=RED, separator='*')
        
    conn.close()
    input("Press Enter to exit...")

if __name__ == "__main__":
    run_lan_game()