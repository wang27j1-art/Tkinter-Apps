import tkinter as tk
from tkinter import *
import random

# Part 1: Game Engine
# Logic (Model and Controller)

# Milestone 1: The Map (List of Dictionaries)
''' Global variables
    Dictionaries: rooms, player state
    Functions: move_player(destination), get_current_room_description(),
               take_item(item_name), get_directions(), check_win_condition()
'''
rooms = [
         {"name": "Command Nexus",
          "description": ("A circular hub lined with tactical holo-panels." +
                         " Faint vibrations from the ship's engines pulse through the floor." +
                         " The captain's console sits dormant, awaiting authorization."),
          "paths": {
              "Stellar Bridge": 1,
              "Holographic Interface Atrium": 11,
              "Reactor Containment Core": 2
              },
          "items": ["Damaged captain's datapad", "Emergency override key", "Holomap fragment"]
          },

         
         {"name": "Stellar Bridge",
          "description": ("The primary command deck, with panoramic starfield projections." +
                         " Warning glyphs blink across the navigation pillars, hinting at recent system failures."),
          "paths": {
              "Command Nexus": 0,
              "Celestial Observation Deck": 5
              },
          "items": ["Navigation stylus", "Captain's chair access card", "Faulty star-chart sphere"]
          },

         
         {"name": "Reactor Containment Core",
          "description": ("A massive cylindrical engine chamber bathed in blue radiation shields." +
                         " The hum is nearly overwhelming. Robotic arms cling to the fusion chamber like metallic insects."),
          "paths": {
              "Command Nexus": 0,
              "Nanoforge Fabrication Lab": 6
              },
          "items": ["Plasma coolant canister", "Reactor diagnostic module", "Safety visor"]
          },

         
         {"name": "Cryosleep Ward",
          "description": ("Rows of frosted cryopods line the dimly lit hall." +
          " Most are empty, but one flickers with an unknown life signature."),
          "paths": {
              "Hydroponics Dome": 4,
              "Hyperlane Charting Theater": 14
              },
          "items": ["Cryo-gel pack", "Bio-monitor tablet", "Unlabeled stasis injector"]
          },

         
         {"name": "Hydroponics Dome",
          "description": ("A humid greenhouse sphere of spiraling vines, nutrien pools, and oxygen trees." +
          " Artificial sunlight cycles overhead every few minutes."),
          "paths": {
              "Cryosleep Ward": 3,
              "Prototype Weapons Cell": 10
              },
          "items": ["Sealed nutrient vial", "Mutated leaf sample", "Garden shears (broken)"]
          },

         
         {"name": "Celestial Observation Deck",
          "description": ("A wide glass dome offering a clear view of the nebula outside." +
          " Telescopes and long-range scanners sit powered off."),
          "paths": {
              "Stellar Bridge": 1
              },
          "items": ["Astronomer's log", "Infrared lens", "Nebula dust vial"]
          },

         
          {"name": "Nanoforge Fabrication Lab",
           "description": ("Rows of micro-assembly pods churn out tiny components." +
           " A damaged nanoforge sputters sparks and molten filament."),
           "paths": {
               "Reactor Containment Core": 2,
               "Quantum Entanglement Suite": 7,
               "Holographic Interface Atrium": 11
               },
           "items": ["Box of micro-wafers", "Liquid alloy cartridge", "Nanobot cluster in stasis jar"]
           },

         
          {"name": "Quantum Entanglement Suite",
           "description": ("The air feels thick, distorted." +
                          " Twin entanglement cores spin in perfect parallel, glowing with synchronized pulses."),
           "paths": {
               "Nanoforge Fabrication Lab": 6,
               "Xenobiology Quarantine Pod": 8,
               "Gravimetric Distortion Room": 9
               },
           "items": ["Phase-key crystal", "Quantom logbook", "Stabilizer gloves"]
           },

         
          {"name": "Xenobiology Quarantine Pod",
           "description": ("A sterile, sealed bio-containment pod. The airlock hisses." +
           " Strange specimens float in reinforced fluid tanks."),
           "paths": {
               "Quantum Entanglement Suite": 7,
               "Prototype Weapons Cell": 10
               },
           "items": ["Biological sample case", "Containment badge", "Unknown spore sample (unstable)"]
           },

         
          {"name": "Gravimetric Distortion Room",
           "description": ("Gravity warpsunpredictably here." +
           " Floating debris drifts past you in slow spirals, and shadows curve unnaturally."),
           "paths": {
               "Quantum Entanglement Suite": 7,
               "Prototype Weapons Cell": 10
               },
           "items": ["Grav-anchor boots", "Mass fluctuation sensor", "Energency tether"]
           },

         
          {"name": "Prototype Weapons Cell",
           "description": ("A secure chamber containing experimental weapons locked behind energy barriers." +
           " Warning signs urge extreme caution."),
           "paths": {
               "Hydroponics Dome": 4,
               "Xenobiology Quarantine Pod": 8,
               "Gravimetric Distortion Room": 9
               },
           "items": ["Deactivated plasma cutter", "Energy blade prototype", "Weapon coolant cylinder"]
           },

         
          {"name": "Holographic Interface Atrium",
           "description": ("A towering hall filled with floating neon interfaces." +
           " The space reshapes itself based on movement --- doors phase in and out."),
           "paths": {
               "Command Nexus": 0,
               "Nanoforge Fabrication Lab": 6,
               "Warp-Field Stabilizer Room": 12
               },
           "items": ["Holo-emitter node", "Control wand", "System access chip"]
           },

         
          {"name": "Warp-Field Stabilizer Room",
           "description": ("A spinning gyroscopic ring dominates the center, humming with warp energy." +
           " A mist of charged particles drifts through the air."),
           "paths": {
               "Holographic Interface Atrium": 11,
               "Neural Sync Capsule Room": 13
               },
           "items": ["Warp tuning rod", "Stabilizer coolant", "Field interference gauge"]
           },

         
          {"name": "Neural Sync Capsule Room",
           "description": ("A chamber of neural-link capsules arranged in a circle." +
           " Ghostly echoes of the past simulations flicker in the air."),
           "paths": {
               "Warp-Field Stabilizer Room": 12,
               "Hyperlane Charting Theater": 14
               },
           "items": ["Neural interface cable", "Simulation transcript", "Memory gel pack"]
           },

         
          {"name": "Hyperlane Charting Theater",
           "description": ("A sweeping amphitheater where hyperlanes are mapped in real time." +
           " Holograms of star systems float overhead."),
           "paths": {
               "Cryosleep Ward": 3,
               "Neural Sync Capsule Room": 13
               },
           "items": ["Hyperlane star-map disc", "Coordinate stylus", "Sensor calibration plate."]
           }
          ]
        

# Milestone 2: Player State (Dictionary)
player_state = {
    "current_room": 0,
    "inventory": [],
    "score": 0
    }

# Milestone 3: Game Functions
def move_player(destination):
    """Changes the player's location based on valid paths."""
    
    current_room = rooms[player_state["current_room"]]
    paths = current_room["paths"]
    
    if destination in paths:
        player_state["current_room"] = paths[destination]
        return True
    else:
        return False


def get_current_room_description():
    """Returns the description of the player's current room."""
    location_index = player_state["current_room"]
    current_room =  rooms[player_state["current_room"]]
    current_room_name = current_room["name"]
    current_room_description = current_room["description"]
    items = current_room["items"]
    paths = current_room["paths"]
    
    if items:
        item_text = ""
        for item in items:
            item_text += "- " + item + "\n"
    else:
        item_text = "None\n"

    path_text = ""
    for path in paths.keys():
        path_text += "- " + path + "\n"
        
    return ("Current Location: " + current_room_name + "\n"
            + current_room_description + "\n\n"
            + "It contains the following items: \n"
            + item_text + "\n"
            + "Available paths: \n"
            + path_text
            )
    
def take_item(item_name):
    """Picks up an item from the current room."""
    location_index = player_state["current_room"]
    current_room =  rooms[player_state["current_room"]]
    current_room_name = current_room["name"]
    current_room_items = current_room["items"]
    inventory = player_state["inventory"]
    
    if item_name in current_room_items:
        current_room_items.remove(item_name)
        inventory.append(item_name)
        player_state["score"] += 10
    elif item_name in inventory:
        return "You already have the " + item_name
    else:
        return "Sorry, but " + str(current_room_name) + " does not have the " + item_name + "."
            
# Display directions
def get_directions():
    """Returns the game's directions and available commands."""
    print("--- Welcome to the SCI-FI ADVENTURE GAME! :D ---")
    print()
    return ("Instructions: \n"
          "- Emergency override key \n"
          "- System access chip \n"
          "- Captain's chair access card \n"
          "- Stabilizer coolant \n"
          "Once you find all four items, move to the Warp-Field Stabilizer Room to escape! \n\n"
          "Commands: \n"
          "- go [destination]: Move to a new room. (e.g., Stellar Bridge) \n"
          "- take [item]: Pick up an item. (e.g., (take datapad)) \n"
          "- look: Look around the current room. \n"
          "- inventory: Check your inventory. \n"
          "- score: See your current score. \n"
          "- help: Display these directions again. \n"
          )
    
    return """
    *** Sci-Fi Adventure Game ***
    Commands:
    - go [destination]: Move to a new room. (e.g., go cargo bay)
    - take [item]: Pick up an item. (e.g., take datapad)
    - look: Look around the current room.
    - inventory: Check your inventory.
    - score: See your current score.
    - help: Display these directions again.
    """
    
          
def check_win_condition():
    """Checks if the player has won the game."""
    #list of required items
    required_items = [
        "Emergency override key",
        "System access chip",
        "Captain's chair access card",
        "Stabilizer coolant"
        ]

    inventory = player_state["inventory"]
    current_room = player_state["current_room"]

    return all(item in inventory for item in required_items) and current_room == 12
        
# Milestone 5: Linking Logic to GUI
def update_gui(text):
    """Helper function to update the main text box."""
    textbox.config(state="normal")          #enable editing
    textbox.insert("end", text + "\n\n")    #add text at the end
    textbox.see("end")                      #scroll to bottom
    textbox.config(state="disabled")        #lock again

# Main event handler for game for "Go" button
def handle_input():
    """Main function that handles user input and updates the game state."""
    raw = user_input.get().strip()      # read input
    user_input.delete(0, "end")         # clear entry
    update_gui("> " + raw)              # show command entry

    # parse input
    parts = raw.split()
    if len(parts) == 0:
        return

    command = parts[0].lower()
    if len(parts) > 1:
        argument = " ".join(parts[1:])
    else:
        argument = ""

    # commands
    if command == "go":
        if argument == "":
            update_gui("Go where?")
        else:
            success = move_player(argument)
            if success:
                update_gui(get_current_room_description())
            else:
                update_gui("You cannot go to: " + argument)
    elif command == "look":
        update_gui(get_current_room_description())
    elif command == "take":
        if argument == "":
            update_gui("Take what?")
        else:
            result = take_item(argument)
            if result:
                update_gui(result)
            else:
                update_gui("You picked up the " + argument)
    elif command == "inventory":
        inv = player_state["inventory"]
        if inv:
            update_gui("You have: " + ", ".join(inv))
        else:
            update_gui("Your inventory is empty.")
    elif command == "score":
        update_gui("Current score: " + str(player_state["score"]))
    elif command == "help":
        update_gui(get_directions())
    else:
        update_gui("I don't understand that command.")

    # WIN CHECK
    if check_win_condition():
        update_gui("🎉 You repaired the warp systems and escaped! You win! 🎉")
        go_button.config(state="disabled")
        user_input.config(state="disabled")


# Part 2: GUI Setup
# Main (View)
''' Milestone 4: GUI Layout
    Create app window and add title as "Sci-Fi Adventure"
    Add widgets: game_text, user_input_entry, go_button,
'''
window = tk.Tk()
window.title("Sci-Fi Text Adventure")

window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# Text box for game output
textbox = tk.Text(window,width=80,height=20)
textbox.grid(row=0,column=0,columnspan=2,padx=10,pady=10)
textbox.config(
    bg="#1f2d40",
    fg="#e0fbfc",
    font=("Consolas",11,"bold"),
    insertbackground="#e0fbfc",
    state="disabled"
)

# User Input Entry field
user_input = tk.Entry(window)
user_input.grid(row=1,column=0,sticky="ew",padx=10,pady=10)
user_input.config(
    bg="#1f2d40",
    fg="#e0fbfc",
    font=("Consolas",11,"bold"),
    insertbackground="#e0fbfc"
)

# Go button (command is linked in Milestone 5)
go_button = tk.Button(window,text="Go",command=handle_input)
go_button.grid(row=1,column=1,sticky="ew",padx=10,pady=10)
go_button.config(
    bg="#3a86ff",
    fg="white",
    font=("Bahnschrift",12,"bold"),
    activebackground="#265dab",
    bd=0
)

# Link the button to the handle_input function (event-triggering widget) (DONE)



# Initial game setup: Create a welcome message and directions
# Display using the update_gui function
update_gui("Welcome to the Sci-Fi Adventure!")
update_gui(get_directions())
update_gui(get_current_room_description())


#Start App
window.mainloop()
