import tkinter as tk
from tkinter import messagebox, ttk
import random
import math
import winsound
# ---------------- CHARACTER CUSTOMIZER CLASS ---------------- #

class CharacterCustomizer:
    """Manages the UI and logic for the character customization screen."""
    
    def __init__(self, master):
        self.window = tk.Toplevel(master)
        self.window.title("Character Customizer")
        
        # --- Toplevel Fixes for Clean Behavior ---
        self.window.resizable(False, False) 
        self.window.transient(master)         
        self.window.grab_set()           
        
        # UI Styling Setup
        self.BG_COLOR = "#f0f0f0"
        self.window.config(bg=self.BG_COLOR)
        
        # --- 1. Load Images and Indices (State) ---
        # Note: These files must exist in the directory for the game to work properly.
        # If files are missing, placeholder blocks will be drawn.
        self.head_options = self._load_images(["head1.png", "head2.png", "head3.png", "head4.png"], "head", 'black')
        self.shirt_options = self._load_images(["shirt1.png", "shirt2.png", "shirt3.png"], "shirt", 'blue')
        self.pants_options = self._load_images(["pants1.png", "pants2.png", "pants3.png", "pants4.png"], "pants", 'green')
        
        glass_options_loaded = self._load_images(["glasses1.png", "glasses2.png"], "glasses", 'white')
        self.no_glasses_image = tk.PhotoImage() 
        self.glass_options = [self.no_glasses_image] + glass_options_loaded


        self.current_indices = { "head": 0, "glasses": 0, "shirt": 0, "pants": 0 }
        self.part_options = {
            "head": self.head_options,
            "glasses": self.glass_options, 
            "shirt": self.shirt_options,
            "pants": self.pants_options
        }
        
        # --- 2. Setup Canvas ---
        self.canvas_frame = tk.Frame(self.window, bg="black", width=500, height=550) 
        self.canvas_frame.pack(padx=20, pady=(5, 3)) 
        
        self.canvas = tk.Canvas(self.canvas_frame, width=450, height=500, bg="black", highlightthickness=0)
        self.canvas.pack(padx=10, pady=10)

        # --- 3. Create UI and Draw Initial Character ---
        self._create_ui()
        self.update_character()
        
        # --- 4. Wait for window closure ---
        master.wait_window(self.window) 

    def _load_images(self, file_list, part_name, placeholder_color):
        images = []
        try:
            for file_name in file_list:
                images.append(tk.PhotoImage(file=file_name))
        except tk.TclError:
            print(f"Warning: Could not load {part_name} images. Using a placeholder.")
            num_placeholders = len(file_list)
            # Create simple 100x100 placeholders if images are missing
            images = [tk.PhotoImage(width=100, height=100) for _ in range(num_placeholders)]
            for img in images:
                # Use put method to color the placeholder image
                img.put(placeholder_color, to=(0, 0, 99, 99))
        return images
        
    def update_character(self):
        """
        Redraws the character based on current indices, using center anchor 
        for predictable, stacked positioning.
        """
        self.canvas.delete("all")

        base_x = 225
        base_y = 250 
        
        y_offsets = {
            "pants": base_y + 150,  
            "shirt": base_y - 1,    
            "head": base_y - 135,   
            "glasses": base_y - 90  
        }

        # Draw order ensures clothes appear beneath the head/glasses
        draw_order = ["pants", "shirt", "head", "glasses"] 
        
        for part in draw_order:
            index = self.current_indices[part]
            options = self.part_options[part]
            
            if 0 <= index < len(options):
                self.canvas.create_image(
                    base_x, 
                    y_offsets[part], 
                    image=options[index], 
                    anchor="center"
                )

    def change_part(self, part_name, direction):
        options = self.part_options[part_name]
        current_index = self.current_indices[part_name]
        
        new_index = (current_index + direction) % len(options)
        
        self.current_indices[part_name] = new_index
        self.update_character()

    def _create_ui(self):
        """Creates the button interface rows using the Grid layout for cleaner alignment."""
        
        control_frame = tk.Frame(self.window, bg=self.BG_COLOR)
        control_frame.pack(padx=40, pady=(5, 3)) 
        
        control_frame.grid_columnconfigure(0, weight=1, minsize=100) 
        control_frame.grid_columnconfigure(1, weight=0) 
        control_frame.grid_columnconfigure(2, weight=0) 

        parts_list = [
            ("Head", "head"),
            ("Glasses", "glasses"),
            ("Shirt", "shirt"),
            ("Pant", "pants"),
        ]
        
        button_style = {
            "padding": (5, 3), 
        }
        
        for i, (label_text, part_name) in enumerate(parts_list):
            
            ttk.Label(control_frame, text=label_text, font=('Arial', 14), background=self.BG_COLOR).grid(
                row=i, column=0, sticky="w", padx=(0, 30), pady=(3, 3)
            )
            
            ttk.Button(control_frame, text="<", 
                        command=lambda pn=part_name: self.change_part(pn, -1), **button_style).grid(
                row=i, column=1, padx=5, pady=(3, 3)
            )
                        
            ttk.Button(control_frame, text=">", 
                        command=lambda pn=part_name: self.change_part(pn, 1), **button_style).grid(
                row=i, column=2, padx=(0, 5), pady=(3, 3)
            )
        
        tk.Button(self.window, text="Save Outfit", command=self.save_outfit, 
                          font=('Arial', 14, 'bold'), 
                          bg="#1f6feb", fg="white", bd=0, 
                          padx=15, pady=6).pack(
                              pady=(5, 8), padx=40, fill='x'
                          )

    def save_outfit(self):
        """Prints the final configuration."""
        print("Sucessfully saved outfit!")
        print("Head:", self.current_indices["head"])
        
        glasses_index = self.current_indices["glasses"]
        if glasses_index == 0:
            print("Glasses: None")
        else:
            print(f"Glasses: {glasses_index}") 
            
        print("Shirt:", self.current_indices["shirt"])
        print("Pant:", self.current_indices["pants"])
        messagebox.showinfo("Saved", "Outfit configuration saved to console/memory!")
        self.window.destroy() # Close customizer after saving
        
# ---------------- CHARACTER CUSTOMIZER FUNCTION (The entry point) ---------------- #

def open_customizer():
    """Starts the customizer window by instantiating the class."""
    CharacterCustomizer(root)

# ---------------- PLANE PARTS DATA ---------------- #

plane_parts = {
    "Wing": "Produces lift that keeps the plane in the air.",
    "Elevator": "Controls the plane's pitch (up and down movement).",
    "Fuselage": "The main body of the airplane.",
    "Engine": "Provides thrust to move the plane forward.",
    "Flaps": "Increase lift at slower speeds during takeoff and landing.",
    "Ailerons": "Control the plane's roll, tilting the wings left or right.",
    "Rudder": "Controls yaw, making the nose turn left or right.",
    "Cockpit": "Where the pilots control the aircraft.",
    "Altimeter": "Measures the plane's altitude.",
    "Airspeed Indicator": "Shows how fast the plane is moving through the air.",
    "Wing root": "The part of the wing closest to the fuselage.",
    "Black box": "A device that records flight data and cockpit audio.",
    "Glide slope": "The descent path used when approaching a runway.",
    "Leading edge": "The front edge of the wing that first meets the airflow.",
    "Wake turbulence": "Air disturbance caused by another aircraft.",
    "Thrust": "The forward force produced by the engines.",
    "Gravity": "The force pulling the aircraft toward the Earth."
}

parts_reviewed = set()
total_parts = len(plane_parts)

# ---------------- MAIN WINDOW SETUP ---------------- #

root = tk.Tk()
root.title("Haunted Plane Game")
root.geometry("1000x800")
root.config(padx=10, pady=10, bg="#050816")

root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

main_menu = tk.Frame(root, bg="#050816")
# Row 0: Top Padding/Ghosts (Weight 1 - takes up space)
main_menu.grid_rowconfigure(0, weight=1) 
# Row 1: Title & Buttons (Weight 0 - shrinks to content, centered)
main_menu.grid_rowconfigure(1, weight=0) 
# Row 2: Bottom Padding/Ghosts (Weight 1 - takes up space)
main_menu.grid_rowconfigure(2, weight=1) 
main_menu.grid_columnconfigure(0, weight=1)

parts_screen = tk.Frame(root, bg="#050816")
parts_screen.grid_columnconfigure(0, weight=0)
parts_screen.grid_columnconfigure(1, weight=1)
parts_screen.grid_rowconfigure(1, weight=1)

quiz_screen = tk.Frame(root, bg="#050816")
quiz_screen.grid_rowconfigure(0, weight=1)
quiz_screen.grid_columnconfigure(0, weight=1)

# --- NEW SCREENS ---
options_screen = tk.Frame(root, bg="#050816")
options_screen.grid_rowconfigure(0, weight=1)
options_screen.grid_rowconfigure(1, weight=0)
options_screen.grid_rowconfigure(2, weight=1)
options_screen.grid_columnconfigure(0, weight=1)

credits_screen = tk.Frame(root, bg="#050816")
credits_screen.grid_rowconfigure(0, weight=1)
credits_screen.grid_rowconfigure(1, weight=0)
credits_screen.grid_rowconfigure(2, weight=1)
credits_screen.grid_columnconfigure(0, weight=1)
# -------------------
def play_music():
    """Play or stop background music based on sound_enabled."""
    if sound_enabled.get():
        winsound.PlaySound(
            "background_music.wav",
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP
        )
    else:
        winsound.PlaySound(None, winsound.SND_PURGE)
# -------------------


for frame in (main_menu, parts_screen, quiz_screen, options_screen, credits_screen):
    frame.grid(row=0, column=0, sticky="nsew")

def show_menu():
    play_music()  
    main_menu.tkraise()
    # Force recalculation of positions when returning to the menu
    if 'ghost_canvas' in globals():
        global GHOST_POSITIONS 
        GHOST_POSITIONS = []
        # Ensure the canvas is configured correctly before drawing
        ghost_canvas.update_idletasks()
        draw_random_ghosts(ghost_canvas, count=GHOST_COUNT) 
    
def show_parts_screen():
    parts_screen.tkraise()

def show_quiz_screen():
    quiz_screen.tkraise()
    
def show_options_screen():
    options_screen.tkraise()
    
def show_credits_screen():
    credits_screen.tkraise()


# ---------------- GHOST PLACEMENT LOGIC (Unchanged) ---------------- #

# Ghost Canvas (Placed first, spanning all rows to be in the background)
ghost_canvas = tk.Canvas(main_menu, bg="#050816", highlightthickness=0)
# This places the canvas behind the elements that follow in rows 0, 1, 2
ghost_canvas.grid(row=0, column=0, rowspan=3, sticky="nsew") 

GHOST_COUNT = 20
GHOST_POSITIONS = [] 

# Exclusion Zone (normalized values 0.0 to 1.0)
EXCLUSION_ZONE_Y_START = 0.35  
EXCLUSION_ZONE_Y_END = 0.65    

# Minimum required distance between ghosts (normalized)
MIN_DISTANCE_NORM = 0.15 

def is_in_exclusion_zone(y_norm):
    """Checks if a normalized Y coordinate is within the central exclusion zone."""
    return EXCLUSION_ZONE_Y_START < y_norm < EXCLUSION_ZONE_Y_END

def calculate_spaced_random_positions(target_count):
    """
    Generates target_count positions, split evenly between the upper and lower 
    safe regions, ensuring minimum distance between all ghosts.
    """
    
    count_per_region = target_count // 2 
    positions = []
    
    # Define the two safe regions (Y_min, Y_max)
    regions = [
        (0.0, EXCLUSION_ZONE_Y_START),  # Upper Safe Area
        (EXCLUSION_ZONE_Y_END, 1.0)     # Lower Safe Area
    ]
    
    max_attempts = target_count * 20
    
    for y_min, y_max in regions:
        
        region_positions = []
        attempts = 0
        
        # Calculate positions for the current region
        while len(region_positions) < count_per_region and attempts < max_attempts:
            
            y_range = y_max - y_min
            y_norm = y_min + random.random() * y_range 
            x_norm = random.random() 
            
            is_safe = True
            
            # Check Minimum Distance from existing accepted positions (in BOTH regions)
            for px, py in positions + region_positions:
                # Use Euclidean distance (math.sqrt) for accurate spacing
                distance = math.sqrt((x_norm - px)**2 + (y_norm - py)**2)
                if distance < MIN_DISTANCE_NORM:
                    is_safe = False
                    break 

            if is_safe:
                region_positions.append((x_norm, y_norm))
                
            attempts += 1
        
        positions.extend(region_positions)

    if len(positions) < target_count:
        print(f"Warning: Could only place {len(positions)} out of {target_count} ghosts with the minimum distance constraint.")
            
    return positions

def draw_random_ghosts(canvas, count):
    """
    Draws the specified number of ghost emojis using safe, *spaced* positions.
    """
    canvas.delete("all")
    
    canvas.update_idletasks() 
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    
    if canvas_width < 50 or canvas_height < 50:
        # Retry if the canvas hasn't fully rendered yet
        canvas.after(50, lambda: draw_random_ghosts(canvas, count))
        return

    global GHOST_POSITIONS
    
    if not GHOST_POSITIONS or len(GHOST_POSITIONS) != count:
        GHOST_POSITIONS = calculate_spaced_random_positions(count)
            
    ghost_font = ("Helvetica", 40) 
    emoji = "👻"
    
    for x_norm, y_norm in GHOST_POSITIONS:
        
        x = int(canvas_width * x_norm)
        y = int(canvas_height * y_norm)
        
        # Keep ghosts slightly away from the edges
        x = max(30, min(x, canvas_width - 30)) 
        y = max(30, min(y, canvas_height - 30))
        
        canvas.create_text(
            x, y, 
            text=emoji, 
            font=ghost_font, 
            fill="white", 
            anchor="center"
        )
        
# Bind the drawing function to the canvas configure event
ghost_canvas.bind("<Configure>", lambda event: draw_random_ghosts(ghost_canvas, count=GHOST_COUNT))

# ---------------- MAIN MENU FOREGROUND ELEMENTS (CENTERED) ----------------

# Create a content frame to hold the Title, Story, and Buttons. 
content_frame_menu = tk.Frame(main_menu, bg="#050816")
# Place the content frame in the center row of the main menu
content_frame_menu.grid(row=1, column=0) 

# Configure its column to center its own contents
content_frame_menu.grid_columnconfigure(0, weight=1)

# Title is placed in Row 0 of the content frame
title_label_menu = tk.Label(
    content_frame_menu, # Use the inner frame
    text="Haunted Plane Game",
    font=("Helvetica", 32, "bold"),
    fg="#eaf4ff",
    bg="#050816"
)
# Using 'pack' or 'grid' inside content_frame_menu works, let's use grid for consistent spacing
title_label_menu.grid(row=0, column=0, pady=(0, 20)) 

# --- STORYLINE LABEL ---
story_text = (
    "You are trapped on a haunted airplane! To escape the specters and avoid a crash,\n"
    "you must quickly learn the function of all the plane's parts and pass the final quiz."
)

story_label_menu = tk.Label(
    content_frame_menu, # Use the inner frame
    text=story_text,
    font=("Arial", 16),
    fg="#bdbdbd",  
    bg="#050816",
    justify="center"
)
# Place the story in Row 1 of the content frame
story_label_menu.grid(row=1, column=0, pady=(0, 40)) 
# -------------------------

# Button frame is placed in Row 2 of the content frame
menu_buttons_frame = tk.Frame(content_frame_menu, bg="#050816") # Use the inner frame
menu_buttons_frame.grid(row=2, column=0, pady=(0, 0)) 

# --- FIX: LIFT the foreground elements above the ghost_canvas ---
content_frame_menu.lift() # Lift the entire content block
# -------------------------------------------------------------

button_style_menu = {
    "font": ("Montserrat", 18, "bold"),
    "fg": "white",
    "padx": 10,
    "pady": 5,
    "bd": 0,
    "width": 12
}

play_button_menu = tk.Button(
    menu_buttons_frame,
    text="PLAY",
    bg="#1f6feb",
    command=show_parts_screen,
    **button_style_menu
)
play_button_menu.grid(row=0, column=0, padx=10, sticky = "ew")

customize_button_menu = tk.Button(
    menu_buttons_frame,
    text="CUSTOMIZE",
    bg="#3a8fb7",
    command=open_customizer,
    **button_style_menu
)
customize_button_menu.grid(row=0, column=1, padx=10)

options_button_menu = tk.Button(
    menu_buttons_frame,
    text="OPTIONS",
    bg="#5b5f97",
    command=show_options_screen, # LINKED TO NEW SCREEN
    **button_style_menu
)
options_button_menu.grid(row=0, column=2, padx=10)

credits_button_menu = tk.Button(
    menu_buttons_frame,
    text="CREDITS",
    bg="#8a4fff",
    command=show_credits_screen, # LINKED TO NEW SCREEN
    **button_style_menu
)
credits_button_menu.grid(row=0, column=3, padx=10)


# ---------------- OPTIONS SCREEN ---------------- #

# Placeholder state variable for sound
sound_enabled = tk.BooleanVar(value=True)

def toggle_sound():
    """Toggles the sound_enabled state and updates the button text."""
    current_state = sound_enabled.get()
    sound_enabled.set(not current_state)
    update_sound_button_text()
    
def update_sound_button_text():
    """Updates the text of the sound toggle button."""
    if sound_enabled.get():
        sound_toggle_button.config(text="Sound: ENABLED")
    else:
        sound_toggle_button.config(text="Sound: DISABLED")


options_content_frame = tk.Frame(options_screen, bg="#050816")
options_content_frame.grid(row=1, column=0, sticky="ew")
options_content_frame.grid_columnconfigure(0, weight=1)

tk.Label(
    options_content_frame,
    text="Game Options",
    font=("Helvetica", 32, "bold"),
    fg="#eaf4ff",
    bg="#050816"
).grid(row=0, column=0, pady=(0, 40))

# Sound Toggle Button
sound_toggle_button = tk.Button(
    options_content_frame,
    text="Sound: ENABLED", # Initial text
    font=("Montserrat", 18, "bold"),
    fg="white",
    bg="#5b5f97",
    padx=20,
    pady=10,
    bd=0,
    width=20,
    command=toggle_sound
)
sound_toggle_button.grid(row=1, column=0, pady=10)
update_sound_button_text() # Set initial text correctly

# Back Button
tk.Button(
    options_content_frame,
    text="BACK TO MENU",
    font=("Montserrat", 16, "bold"),
    fg="white",
    bg="#8a4fff",
    padx=15,
    pady=8,
    bd=0,
    width=20,
    command=show_menu
).grid(row=2, column=0, pady=(40, 10))


# ---------------- CREDITS SCREEN ---------------- #

credits_content_frame = tk.Frame(credits_screen, bg="#050816")
credits_content_frame.grid(row=1, column=0, sticky="ew")
credits_content_frame.grid_columnconfigure(0, weight=1)

tk.Label(
    credits_content_frame,
    text="Game Credits",
    font=("Helvetica", 32, "bold"),
    fg="#eaf4ff",
    bg="#050816"
).grid(row=0, column=0, pady=(0, 40))

tk.Label(
    credits_content_frame,
    text="Made by:",
    font=("Arial", 24, "italic"),
    fg="#bdbdbd",
    bg="#050816"
).grid(row=1, column=0, pady=(0, 5))

tk.Label(
    credits_content_frame,
    text="Ritika\nVanessa\nJoyce",
    font=("Arial", 28, "bold"),
    fg="white",
    bg="#050816",
    justify="center"
).grid(row=2, column=0, pady=(5, 40))

# Back Button
tk.Button(
    credits_content_frame,
    text="BACK TO MENU",
    font=("Montserrat", 16, "bold"),
    fg="white",
    bg="#8a4fff",
    padx=15,
    pady=8,
    bd=0,
    width=20,
    command=show_menu
).grid(row=3, column=0, pady=(20, 10))


# ---------------- PARTS VIEWER SCREEN---------------- #

title_label = tk.Label(
    parts_screen,
    text="Plane Parts Viewer",
    font=("Helvetica", 24, "bold"),
    fg="#eaf4ff",
    bg="#050816"
)
title_label.grid(row=0, column=0, columnspan=2, pady=(10, 20))

menu_frame = tk.Frame(parts_screen, bg="#050816")
menu_frame.grid(row=2, column=0, columnspan=2, pady=(30, 20), sticky="ew")
menu_frame.grid_columnconfigure(0, weight=1)
menu_frame.grid_columnconfigure(1, weight=1)
menu_frame.grid_columnconfigure(2, weight=1)

canvas = tk.Canvas(parts_screen, bg="#050816", highlightthickness=0)
canvas.grid(row=1, column=0, padx=(30, 0), pady=20, sticky="nsw")

scrollbar = tk.Scrollbar(parts_screen, orient="vertical", command=canvas.yview)
scrollbar.grid(row=1, column=0, sticky="nse", padx=(0, 25), pady=20)

canvas.config(yscrollcommand=scrollbar.set)
canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

buttons_frame = tk.Frame(canvas, bg="#050816")
canvas.create_window((0, 0), window=buttons_frame, anchor="nw")

def update_scroll_region(event=None):
    canvas.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

buttons_frame.bind("<Configure>", update_scroll_region)


def make_part_button(part_name, row):
    def click():
        description_label.config(
            text=f"{part_name}\n\n{plane_parts[part_name]}"
        )

        global parts_reviewed
        global total_parts
        
        parts_reviewed.add(part_name)
        
        if len(parts_reviewed) == total_parts:
            quiz_button.config(state="normal", bg="#1f6feb")
            print("All parts reviewed! Quiz is unlocked.")
            
    btn = tk.Button(
        buttons_frame,
        text=part_name,
        font=("Helvetica", 14, "bold"),
        fg="white",
        bg="#1f2937",
        activebackground="#374151",
        activeforeground="white",
        width=20,
        command=click
    )
    btn.grid(row=row, column=0, padx=8, pady=4, sticky="w")

row_number = 0
for part in plane_parts:
    make_part_button(part, row_number)
    row_number += 1

right_frame = tk.Frame(parts_screen, bg="#050816")
right_frame.grid(row=1, column=1, padx=(20, 30), pady=20, sticky="nsew")
right_frame.grid_columnconfigure(0, weight=1)

description_label = tk.Label(
    right_frame,
    text="Click a part to learn more about it.",
    wraplength=450,
    justify="left",
    fg="white",
    bg="#050816",
    font=("Helvetica", 16),
    anchor="nw"
)
description_label.grid(row=0, column=0, sticky="nw")

right_frame.grid_rowconfigure(1, weight=1)

notebook_frame = tk.Frame(right_frame, bg="#050816")

notebook_label = tk.Label(
    notebook_frame,
    text="Notebook",
    fg="#eaf4ff",
    bg="#050816",
    font=("Helvetica", 14, "bold"),
    anchor="w"
)
notebook_label.grid(row=0, column=0, pady=(0, 5), sticky="w")

notebook_text = tk.Text(
    notebook_frame,
    width=75,
    height=30,
    bg="#0b1220",
    fg="#eaf4ff",
    insertbackground="#eaf4ff",
    wrap="word",
    font=("Helvetica", 12)
)
notebook_text.grid(row=1, column=0, sticky="nsew")

notebook_frame.grid(row=2, column=0, sticky="sew", pady=10)

notebook_frame.grid_remove()

notebook_visible = False

def toggle_notebook():
    global notebook_visible

    if notebook_visible:
        notebook_frame.grid_remove()
        notebook_visible = False
    else:
        notebook_frame.grid()
        notebook_visible = True

def start_quiz():
    if quiz_button.cget('state') == 'disabled':
        messagebox.showinfo("Wait!", "Please review all plane parts before starting the quiz.")
        return

    notes = notebook_text.get("1.0", "end-1c")

    # Clear the quiz screen contents before starting
    for widget in quiz_screen.winfo_children():
        widget.destroy()

    QuizGame(quiz_screen, ALL_QUESTIONS, initial_notes=notes)
    show_quiz_screen()

notebook_button = tk.Button(
    menu_frame,
    text="NOTEBOOK",
    bg="#7c3aed",
    fg="white",
    font=("Montserrat", 18, "bold"),
    padx=15,
    pady=8,
    bd=0,
    command=toggle_notebook
    )
notebook_button.grid(row=0, column=0, padx=15, sticky="w")

quiz_button = tk.Button(
    menu_frame,
    text="START QUIZ",
    bg="#95a5a6",
    fg="white",
    font=("Montserrat", 18, "bold"),
    padx=15,
    pady=8,
    bd=0,
    command=start_quiz,
    state="disabled"
)
quiz_button.grid(row=0, column=1, padx=15, sticky="ew")

home_button_parts = tk.Button(
    menu_frame,
    text="HOME",
    bg="#8a4fff",
    fg="white",
    font=("Montserrat", 18, "bold"),
    padx=15,
    pady=8,
    bd=0,
    command=show_menu
)
home_button_parts.grid(row=0, column=2, padx=15, sticky="e")

# ---------------- QUIZ QUESTIONS ---------------- #

ALL_QUESTIONS = {
    "easy": [
        {"prompt": "Which part of the plane produces lift?", "choices": ["Engines", "Wings", "Rudder", "Fuselage"], "answer": "Wings"},
        {"prompt": "What part controls the plane’s up-and-down motion (pitch)?", "choices": ["Elevator", "Aileron", "Rudder", "Flap"], "answer": "Elevator"},
        {"prompt": "What is the main body of the plane called?", "choices": ["Cabin", "Fuselage", "Nosecone", "Tail"], "answer": "Fuselage"},
        {"prompt": "Which part provides thrust to move the plane forward?", "choices": ["Flaps", "Engines", "Ailerons", "Landing Gear"], "answer": "Engines"},
        {"prompt": "What part of the wing increases lift during takeoff/landing?", "choices": ["Ailerons", "Flaps", "Spoilers", "Rudder"], "answer": "Flaps"}
    ],
    "medium": [
        {"prompt": "Which part controls the plane’s left-right roll?", "choices": ["Flaps", "Rudder", "Ailerons", "Spoilers"], "answer": "Ailerons"},
        {"prompt": "Which part controls the plane’s yaw (left-right turn)?", "choices": ["Elevator", "Rudder", "Ailerons", "Tailcone"], "answer": "Rudder"},
        {"prompt": "What is the pilot’s room called?", "choices": ["Cockpit", "Cabin", "Deck", "Bay"], "answer": "Cockpit"},
        {"prompt": "Which instrument shows the plane’s altitude?", "choices": ["Barometer", "Compass", "Altimeter", "Airspeed Indicator"], "answer": "Altimeter"},
        {"prompt": "Which gauge shows how fast the plane is moving?", "choices": ["Variometer", "Altimeter", "Airspeed Indicator", "Fuel Flow Meter"], "answer": "Airspeed Indicator"}
    ],
    "spooky": [
        {"prompt": "A ghost whispers: ‘The heart of the plane burns with fire… name it.’", "choices": ["Wing", "Engine", "Landing Gear", "Cabin Lights"], "answer": "Engine"},
        {"prompt": "Where did the pilots guide souls through the sky?", "choices": ["Cargo Hold", "Lavatory", "Cockpit", "Wing root"], "answer": "Cockpit"},
        {"prompt": "The cursed hatch asks: Which part lets the plane turn left or right in the sky?", "choices": ["Rudder", "Flaps", "Elevator", "Spoilers"], "answer": "Rudder"},
        {"prompt": "A phantom asks: What lifts this metal bird into the air?", "choices": ["Engines", "Wings", "Landing Gear", "Fuel Tanks"], "answer": "Wings"}
    ],
    "hard": [
        {"prompt": "What is the purpose of the black box?", "choices": ["Navigation", "Sleeping quarters", "Recording flight data", "Fuel storage"], "answer": "Recording flight data"},
        {"prompt": "What is the safe descent guidance path called?", "choices": ["Jet stream", "Glide slope", "Roll path", "Descent arc"], "answer": "Glide slope"},
        {"prompt": "What is the front edge of the wing called?", "choices": ["Trailing edge", "Leading edge", "Wingtip", "Root edge"], "answer": "Leading edge"},
        {"prompt": "Turbulence caused by another aircraft is called…", "choices": ["Tailwind bump", "Shadow turbulence", "Wake turbulence", "Air rush"], "answer": "Wake turbulence"},
        {"prompt": "What force pushes an aircraft forward?", "choices": ["Drag", "Lift", "Thrust", "Load"], "answer": "Thrust"},
        {"prompt": "What force pulls the plane downward?", "choices": ["Lift", "Gravity", "Thrust", "Drag"], "answer": "Gravity"},
    ]
}

# ---------------- QUIZ GAME CLASS---------------- #

class QuizGame:
    BG_DARK = "#2c3e50"
    FG_LIGHT = "#ecf0f1"
    ACCENT_BLUE = "#3498db"
    ACCENT_GREEN = "#2ecc71"
    ACCENT_RED = "#e74c3c"

    def __init__(self, parent, questions_data, initial_notes=""):
        self.parent = parent
        self.parent.config(bg=self.BG_DARK)

        self.score = 0
        self.current_question_index = 0
        self.all_questions = []
        self.TOTAL_QUESTIONS = 15
        self.initial_notes = initial_notes
        self.notebook_visible = True

        self.load_questions(questions_data)
        self.create_widgets()
        self.display_question()

    def load_questions(self, questions_data):
        for category in questions_data.values():
            self.all_questions.extend(category)
            
        random.shuffle(self.all_questions)
            
        self.all_questions = self.all_questions[:self.TOTAL_QUESTIONS]

    def create_widgets(self):
        self.parent.grid_columnconfigure(0, weight=1)
        self.parent.grid_columnconfigure(1, weight=0)
        self.parent.grid_rowconfigure(0, weight=1)

        notebook_panel = tk.Frame(self.parent, bg=self.BG_DARK)
        notebook_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        notebook_panel.grid_columnconfigure(0, weight=1)
        notebook_panel.grid_rowconfigure(1, weight=1)
        
        tk.Label(
            notebook_panel,
            text="Notebook",
            font=("Helvetica", 14, "bold"),
            fg=self.FG_LIGHT,
            bg=self.BG_DARK,
            anchor="w"
        ).grid(row=0, column=0, pady=(0, 5), sticky="ew")

        self.quiz_notebook = tk.Text(
            notebook_panel,
            width=32,
            height=2,
            bg="#0b1220",
            fg=self.FG_LIGHT,
            insertbackground=self.FG_LIGHT,
            wrap="word",
            font=("Helvetica", 12)
        )
        self.quiz_notebook.grid(row=1, column=0, sticky="nsew")

        if self.initial_notes.strip():
            self.quiz_notebook.insert("1.0", self.initial_notes)

        self.main_quiz_area = tk.Frame(self.parent, bg=self.BG_DARK)
        self.main_quiz_area.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        self.main_quiz_area.grid_columnconfigure(0, weight=1)
        self.main_quiz_area.grid_rowconfigure(5, weight=1)

        self.score_text = tk.StringVar(value=f"Score: 0/{self.TOTAL_QUESTIONS}")
        tk.Label(
            self.main_quiz_area,
            textvariable=self.score_text,
            font=("Arial", 16, "bold"),
            fg=self.FG_LIGHT,
            bg=self.BG_DARK
        ).grid(row=0, column=0, pady=(0, 20), sticky="w")
        
        tk.Button(
            self.main_quiz_area,
            text="EXIT QUIZ",
            font=("Arial", 14, "bold"),
            bg="#8a4fff",
            fg="black",
            bd=0,
            padx=10,
            pady=5,
            command=show_menu
        ).grid(row=0, column=0, pady=(0, 20), sticky="e")

        q_frame = tk.Frame(self.main_quiz_area, bg=self.BG_DARK)
        q_frame.grid(row=1, column=0, pady=20, sticky="ew")

        # ------------ QUESTION PANEL ------------
        q_frame = tk.Frame(self.main_quiz_area, bg=self.BG_DARK)
        q_frame.grid(row=1, column=0, pady=20, sticky="ew")
        q_frame.grid_columnconfigure(0, weight=1)

        self.question_text = tk.StringVar()
        self.question_label = tk.Label(
            q_frame,
            textvariable=self.question_text,
            wraplength=600,          # temporary; will be updated on resize
            font=("Arial", 18),
            fg=self.FG_LIGHT,
            bg="#34495e",
            padx=25,
            pady=25
        )
        self.question_label.grid(row=0, column=0, sticky="ew")

        # Make wraplength follow the frame width so long questions always wrap
        def _update_wrap(event):
            # some padding so text doesn’t touch the edges
            self.question_label.config(wraplength=event.width - 40)

        q_frame.bind("<Configure>", _update_wrap)


        self.feedback_text = tk.StringVar(value="")
        tk.Label(
            self.main_quiz_area,
            textvariable=self.feedback_text,
            font=("Arial", 14),
            fg=self.FG_LIGHT,
            bg=self.BG_DARK
        ).grid(row=2, column=0, pady=(0, 10), sticky="ew")

        btn_container = tk.Frame(self.main_quiz_area, bg=self.BG_DARK)
        btn_container.grid(row=3, column=0, pady=(0, 10), sticky="n")
        btn_container.grid_columnconfigure(0, weight=1)
        btn_container.grid_columnconfigure(1, weight=1)
        
        self.choice_buttons = []
        for i in range(4):
            btn = tk.Button(
                btn_container,
                text="",
                width=25,
                height=2,
                font=("Arial", 14),
                bg=self.ACCENT_BLUE,
                fg="black",
                relief="flat",
                command=lambda i=i: self.check_answer(i)
            )
            btn.grid(row=i//2, column=i % 2, padx=15, pady=10, sticky="ew")
            self.choice_buttons.append(btn)


    def display_question(self):
        if self.current_question_index >= len(self.all_questions):
            self.show_result()
            return

        q = self.all_questions[self.current_question_index]
        self.question_text.set(f"Q{self.current_question_index + 1}: {q['prompt']}")
        self.feedback_text.set("")

        choices = q["choices"][:]
        random.shuffle(choices)
        self.current_choices = choices

        for i, choice in enumerate(choices):
            self.choice_buttons[i].config(text=choice, bg=self.ACCENT_BLUE, state="normal")

    def check_answer(self, idx):
        q = self.all_questions[self.current_question_index]
        chosen = self.current_choices[idx]

        for b in self.choice_buttons:
            b.config(state="disabled")

        if chosen == q["answer"]:
            self.score += 1
            self.score_text.set(f"Score: {self.score}/{self.TOTAL_QUESTIONS}")
            self.feedback_text.set("Correct! ✅")
            self.choice_buttons[idx].config(bg=self.ACCENT_GREEN)
        else:
            self.feedback_text.set(f"Incorrect — answer: {q['answer']} 👻")
            self.choice_buttons[idx].config(bg=self.ACCENT_RED)
            try:
                correct_idx = self.current_choices.index(q["answer"])
                self.choice_buttons[correct_idx].config(bg=self.ACCENT_GREEN)
            except ValueError:
                pass

        self.current_question_index += 1
        self.parent.after(1200, self.display_question)

    def show_result(self):
        """
        Displays the final score and creates a new screen with the result
        and a 'Play Again' button.
        """
        # Clear the quiz screen
        for widget in self.parent.winfo_children():
            widget.destroy()

        if self.score >= 12:
            msg = f"Score: {self.score}/{self.TOTAL_QUESTIONS}"
            win = True
        else:
            msg = f"Score: {self.score}/{self.TOTAL_QUESTIONS}"
            win = False

        show_results_screen(self.parent, msg, win)

# ---------------- NEW GAME FLOW AND RESET FUNCTIONS (Modified for cinematic win screen) ---------------- #

def reset_game_state():
    """Resets all global game state variables to prepare for a new game."""
    global parts_reviewed
    global GHOST_POSITIONS

    # 1. Reset parts viewer progress
    parts_reviewed.clear()
    
    # 2. Reset the quiz button state on the parts viewer
    quiz_button.config(state="disabled", bg="#95a5a6")

    # 3. Reset the parts viewer description
    description_label.config(text="Click a part to learn more about it.")
    
    # 4. Clear the notebook
    notebook_text.delete("1.0", "end")

    # 5. Reset the ghost positions (will be recalculated on show_menu)
    GHOST_POSITIONS = []
    
    print("Game state successfully reset. Returning to Main Menu.")
    show_menu()
    
def show_results_screen(parent_frame, message, win_status):
    """
    Creates the final result screen with the score and a 'Play Again' button.
    The 'PLAY AGAIN' button is removed if the quiz was failed (win_status=False).
    """
    
    # 1. Clear any remnants from the old quiz frame layout
    for widget in parent_frame.winfo_children():
        widget.destroy()
        
    # --- New Cinematic Background ---
    BG_COLOR = "#050816" # Your original dark background
    parent_frame.config(bg=BG_COLOR)
    
    # Configure the screen layout to center everything vertically
    parent_frame.grid_columnconfigure(0, weight=1)
    parent_frame.grid_rowconfigure(0, weight=1) # Top Spacer
    parent_frame.grid_rowconfigure(1, weight=0) # Title
    parent_frame.grid_rowconfigure(2, weight=0) # Message
    parent_frame.grid_rowconfigure(3, weight=0) # Button Row 1 (Win only)
    parent_frame.grid_rowconfigure(4, weight=0) # Button Row 2 (Loss only)
    parent_frame.grid_rowconfigure(5, weight=1) # Bottom Spacer

    if win_status:
        # --- WIN SCREEN CUSTOMIZATION (Score >= 12) ---
        
        win_title = "YOU ESCAPED! 🪂"
        
        tk.Label(
            parent_frame,
            text=win_title,
            font=("Helvetica", 48, "bold"),
            fg="#2ecc71", # Bright green for victory
            bg=BG_COLOR
        ).grid(row=1, column=0, pady=(0, 20))

        cinematic_message = "You got a parachute and escaped the plane right before it exploded!"
        
        tk.Label(
            parent_frame,
            text=f"{cinematic_message}\n\n{message}", # Shows the score below the message
            font=("Arial", 20),
            fg="#eaf4ff",
            bg=BG_COLOR,
            wraplength=700,
            justify="center"
        ).grid(row=2, column=0, pady=(0, 40))
        
        # Play Again Button (Row 3 for win screen)
        tk.Button(
            parent_frame,
            text="PLAY AGAIN",
            font=("Montserrat", 20, "bold"),
            bg="#1f6feb",
            fg="white",
            padx=30,
            pady=10,
            bd=0,
            command=reset_game_state
        ).grid(row=3, column=0, pady=(0, 20))
        
    else:
        # --- LOSS SCREEN (Score < 12) ---
        
        tk.Label(
            parent_frame,
            text="GAME OVER",
            font=("Helvetica", 48, "bold"),
            fg="#e74c3c", # Red for defeat
            bg=BG_COLOR
        ).grid(row=1, column=0, pady=(0, 20))

        tk.Label(
            parent_frame,
            text=f"You failed… try again.\n{message}",
            font=("Arial", 24),
            fg="#eaf4ff",
            bg=BG_COLOR
        ).grid(row=2, column=0, pady=(0, 40))
        
        # MAIN MENU button (Row 3 for loss screen)
        tk.Button(
            parent_frame,
            text="MAIN MENU",
            font=("Montserrat", 20, "bold"), # Made the button larger
            bg="#8a4fff",
            fg="black",
            padx=30, # Increased padding
            pady=10,
            bd=0,
            command=show_menu
        ).grid(row=3, column=0, pady=(0, 100))
        
    # Empty labels used as vertical spacers to center content
    tk.Label(parent_frame, bg=BG_COLOR).grid(row=0, column=0, sticky="nsew")
    tk.Label(parent_frame, bg=BG_COLOR).grid(row=5, column=0, sticky="nsew")


# ----------------- MAC OS X FIX -----------------
try:
    root.eval('tk::unsupported::MacWindowStyle style normal') 
    root.update_idletasks() 
    root.deiconify() 
except tk.TclError:
    pass
# ----------------- END OF MAC OS X FIX -----------------


show_menu()
root.mainloop()
