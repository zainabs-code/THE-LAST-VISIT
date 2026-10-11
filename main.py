import tkinter as tk
import os
import pygame
from PIL import Image, ImageTk


# ---------------- WINDOW SETTINGS ----------------

root = tk.Tk()
root.title("THE LAST VISIT")
root.geometry("900x600")
root.minsize(700, 450)
root.configure(bg="#0b1220")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGE_DIR = os.path.join(BASE_DIR, "images")
SOUND_DIR = os.path.join(BASE_DIR, "sounds")

background_image = None
current_frame = None
sound_enabled = True


# ---------------- SOUND SETUP ----------------

try:
    pygame.mixer.init()
except Exception as error:
    print("Sound initialization error:", error)


def play_background_sound(filename, volume=0.25):
    global sound_enabled

    if not sound_enabled:
        return

    sound_path = os.path.join(SOUND_DIR, filename)

    try:
        # Don't restart the same sound if it is already playing
        if pygame.mixer.music.get_busy():
            current_file = getattr(
                play_background_sound,
                "current_file",
                None
            )

            if current_file == filename:
                return

        pygame.mixer.music.load(sound_path)
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

        play_background_sound.current_file = filename

    except Exception as error:
        print("Background sound error:", error)


# ---------------- SCREEN MANAGEMENT ----------------

def clear_screen():
    """Remove every widget from the previous screen."""
    global current_frame, background_image

    for widget in root.winfo_children():
        widget.destroy()

    current_frame = None
    background_image = None


# ---------------- SCREEN 1: TITLE ----------------

def show_title_screen():
    global current_frame, background_image

    clear_screen()

    current_frame = tk.Frame(root, bg="#0b1220")
    current_frame.pack(fill="both", expand=True)

    background_label = tk.Label(
        current_frame,
        bg="#0b1220",
        borderwidth=0
    )
    background_label.place(
        x=0, y=0, relwidth=1, relheight=1
    )

    def resize_background(event):
        global background_image

        if event.width < 2 or event.height < 2:
            return

        image_path = os.path.join(
            IMAGE_DIR, "title_mansion.png"
        )

        try:
            image = Image.open(image_path)
            image = image.resize(
                (event.width, event.height),
                Image.Resampling.LANCZOS
            )

            background_image = ImageTk.PhotoImage(image)
            background_label.configure(image=background_image)

        except Exception as error:
            print("Title image error:", error)

    current_frame.bind("<Configure>", resize_background)

    # Start Investigation button
    tk.Button(
        current_frame,
        text="START INVESTIGATION",
        font=("Arial", 13, "bold"),
        bg="#38bdf8",
        fg="#07111c",
        activebackground="#7dd3fc",
        relief="flat",
        padx=25,
        pady=12,
        command=show_crime_scene
    ).place(
        relx=0.5,
        rely=0.82,
        anchor="center"
    )

    play_background_sound("suspense.wav", 0.25)


# ---------------- SCREEN 2: CRIME SCENE ----------------

def show_crime_scene():
    global current_frame, background_image

    clear_screen()

    current_frame = tk.Frame(root, bg="#0b1220")
    current_frame.pack(fill="both", expand=True)

    # Crime scene background
    background_label = tk.Label(
        current_frame,
        bg="#0b1220",
        borderwidth=0
    )
    background_label.place(
        x=0, y=0, relwidth=1, relheight=1
    )

    def resize_background(event):
        global background_image

        if event.width < 2 or event.height < 2:
            return

        image_path = os.path.join(
            IMAGE_DIR, "crime_scene.png"
        )

        try:
            image = Image.open(image_path)
            image = image.resize(
                (event.width, event.height),
                Image.Resampling.LANCZOS
            )

            background_image = ImageTk.PhotoImage(image)
            background_label.configure(image=background_image)

        except Exception as error:
            print("Crime scene image error:", error)

    current_frame.bind("<Configure>", resize_background)

    # Left panel: Crime description
    description_panel = tk.Frame(
        current_frame,
        bg="#0b1220",
        highlightbackground="#475569",
        highlightthickness=1
    )

    description_panel.place(
        relx=0.03,
        rely=0.05,
        relwidth=0.43,
        relheight=0.57
    )

    tk.Label(
        description_panel,
        text="THE INCIDENT",
        font=("Arial", 19, "bold"),
        bg="#0b1220",
        fg="#38bdf8"
    ).pack(pady=(15, 8))

    description = (
        "James Carter was found dead in his study "
        "at 10:30 PM.\n\n"
        "There were no signs of forced entry.\n\n"
        "His phone contained a message from an "
        "unknown sender:\n\n"
        "\"We need to talk about what you found. "
        "Come alone.\"\n\n"
        "A torn business document was discovered "
        "near his body.\n\n"
        "Your investigation begins here."
    )

    tk.Label(
        description_panel,
        text=description,
        font=("Arial", 10),
        bg="#0b1220",
        fg="#f1f5f9",
        wraplength=350,
        justify="left",
        padx=12
    ).pack(fill="both", expand=True, pady=(0, 12))

    # Right panel: Clue information
    clue_panel = tk.Frame(
        current_frame,
        bg="#0b1220",
        highlightbackground="#475569",
        highlightthickness=1
    )

    clue_panel.place(
        relx=0.53,
        rely=0.05,
        relwidth=0.44,
        relheight=0.72
    )

    tk.Label(
        clue_panel,
        text="INVESTIGATE THE CLUES",
        font=("Arial", 16, "bold"),
        bg="#0b1220",
        fg="#38bdf8"
    ).pack(pady=(15, 10))

    clue_text = tk.Label(
        clue_panel,
        text="Select a clue below to examine it.",
        font=("Arial", 11),
        bg="#0b1220",
        fg="#f1f5f9",
        wraplength=330,
        justify="left",
        padx=15,
        pady=10
    )

    clue_text.pack(fill="both", expand=True)

    # Display clue details on the same screen
    def show_clue(title, details):
        clue_text.config(
            text=f"{title}\n\n{details}"
        )
        
    # Phone clue button
    tk.Button(
        clue_panel,
        text="CHECK PHONE",
        font=("Arial", 10, "bold"),
        bg="#172235",
        fg="#f1f5f9",
        activebackground="#334155",
        activeforeground="white",
        relief="flat",
        pady=8,
        command=lambda: show_clue(
            "PHONE MESSAGE",
            "The message reads:\n\n"
            "\"We need to talk about what you found. "
            "Come alone.\"\n\n"
            "The sender is unknown. "
            "Someone wanted James to meet them privately."
        )
    ).pack(fill="x", padx=18, pady=5)

    # Torn document clue button
    tk.Button(
        clue_panel,
        text="EXAMINE TORN DOCUMENT",
        font=("Arial", 10, "bold"),
        bg="#172235",
        fg="#f1f5f9",
        activebackground="#334155",
        activeforeground="white",
        relief="flat",
        pady=8,
        command=lambda: show_clue(
            "TORN BUSINESS DOCUMENT",
            "The document appears to be part of a "
            "company financial record.\n\n"
            "Several lines are missing. "
            "The remaining information suggests "
            "that James had discovered something "
            "suspicious about the business."
        )
    ).pack(fill="x", padx=18, pady=(5, 15))

    # Continue button
    tk.Button(
        current_frame,
        text="CONTINUE",
        font=("Arial", 11, "bold"),
        bg="#38bdf8",
        fg="#07111c",
        activebackground="#7dd3fc",
        relief="flat",
        padx=25,
        pady=10,
        command=show_next_message
    ).place(
        relx=0.75,
        rely=0.88,
        anchor="center"
    )

    # Back to title button
    tk.Button(
        current_frame,
        text="BACK TO TITLE",
        font=("Arial", 9),
        bg="#172235",
        fg="#f1f5f9",
        relief="flat",
        padx=12,
        pady=7,
        command=show_title_screen
    ).place(
        relx=0.12,
        rely=0.88,
        anchor="center"
    )

    # Switch from suspense to rain ambience
    play_background_sound("rain.wav", 0.30)


# ---------------- CONTINUE MESSAGE ----------------

# ---------------- SCREEN 3: BUSINESS OFFICE ----------------

def show_next_message():
    show_business_office()


def show_business_office():
    global current_frame, background_image

    clear_screen()

    current_frame = tk.Frame(root, bg="#0b1220")
    current_frame.pack(fill="both", expand=True)

    # Background image
    background_label = tk.Label(
        current_frame,
        bg="#0b1220",
        borderwidth=0
    )
    background_label.place(
        x=0, y=0, relwidth=1, relheight=1
    )

    def resize_background(event):
        global background_image

        if event.width < 2 or event.height < 2:
            return

        image_path = os.path.join(
            IMAGE_DIR, "business_office.png"
        )

        try:
            image = Image.open(image_path)
            image = image.resize(
                (event.width, event.height),
                Image.Resampling.LANCZOS
            )

            background_image = ImageTk.PhotoImage(image)
            background_label.configure(image=background_image)

        except Exception as error:
            print("Business office image error:", error)

    current_frame.bind("<Configure>", resize_background)

    # Investigation panel
    office_panel = tk.Frame(
        current_frame,
        bg="#0b1220",
        highlightbackground="#475569",
        highlightthickness=1
    )

    office_panel.place(
        relx=0.52,
        rely=0.08,
        relwidth=0.44,
        relheight=0.72
    )

    tk.Label(
        office_panel,
        text="JAMES CARTER'S OFFICE",
        font=("Arial", 17, "bold"),
        bg="#0b1220",
        fg="#38bdf8"
    ).pack(pady=(18, 12))

    office_text = tk.Label(
        office_panel,
        text=(
            "You enter James's business office.\n\n"
            "His financial records are scattered "
            "across the desk.\n\n"
            "One transaction looks suspicious."
        ),
        font=("Arial", 11),
        bg="#0b1220",
        fg="#f1f5f9",
        wraplength=320,
        justify="left",
        padx=15
    )
    office_text.pack(fill="both", expand=True, pady=10)

    def examine_records():
        office_text.config(
            text=(
                "SUSPICIOUS FINANCIAL TRANSACTION\n\n"
                "Company account: James Carter's business\n\n"
                "Amount transferred: ₹50,00,000\n\n"
                "Destination: Private account\n\n"
                "Account holder: Name hidden in this record.\n\n"
                "Someone may have stolen company money."
            )
        )

        

    tk.Button(
        office_panel,
        text="EXAMINE FINANCIAL RECORDS",
        font=("Arial", 10, "bold"),
        bg="#172235",
        fg="#f1f5f9",
        relief="flat",
        pady=10,
        command=examine_records
    ).pack(fill="x", padx=18, pady=12)

    # Back button
    tk.Button(
        current_frame,
        text="BACK TO CRIME SCENE",
        font=("Arial", 9),
        bg="#172235",
        fg="#f1f5f9",
        relief="flat",
        padx=12,
        pady=8,
        command=show_crime_scene
    ).place(
        relx=0.15,
        rely=0.90,
        anchor="center"
    )

    # Continue to hidden file
    tk.Button(
        current_frame,
        text="CONTINUE",
        font=("Arial", 11, "bold"),
        bg="#38bdf8",
        fg="#07111c",
        relief="flat",
        padx=25,
        pady=10,
        command=show_hidden_file
    ).place(
        relx=0.78,
        rely=0.90,
        anchor="center"
    )

    # Office background sound
    play_background_sound("suspense.wav", 0.20)


# ---------------- SCREEN 4: HIDDEN FILE ----------------
# ---------------- HIDDEN FILE ----------------

def show_hidden_file():
    global current_frame, background_image

    clear_screen()

    current_frame = tk.Frame(root, bg="#080d18")
    current_frame.pack(fill="both", expand=True)

    image_path = os.path.join(IMAGE_DIR, "hidden_file.png")

    try:
        original_image = Image.open(image_path)

        background_label = tk.Label(current_frame, bg="#080d18")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        def resize_background(event=None):
            global background_image

            width = current_frame.winfo_width()
            height = current_frame.winfo_height()

            if width <= 1 or height <= 1:
                return

            resized = original_image.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )

            background_image = ImageTk.PhotoImage(resized)
            background_label.configure(image=background_image)

        current_frame.bind("<Configure>", resize_background)
        resize_background()

    except Exception as error:
        print("Image loading error:", error)

    # COMPACT STORY PANEL
    panel = tk.Frame(
        current_frame,
        bg="#101b2b",
        padx=18,
        pady=15
    )
    panel.place(
        relx=0.035,
        rely=0.12,
        relwidth=0.46,
        relheight=0.65
    )

    tk.Label(
        panel,
        text="THE HIDDEN FILE",
        font=("Georgia", 22, "bold"),
        bg="#101b2b",
        fg="#38bdf8",
        anchor="w"
    ).pack(fill="x", pady=(0, 14))

    story = (
        "You recover a deleted financial record.\n\n"
        "The private account belongs to "
        "MICHAEL BROWN, James Carter's business partner.\n\n"
        "₹50,00,000 was transferred from the company "
        "account to his private account.\n\n"
        "But stealing money does not automatically "
        "prove murder.\n\n"
        "You need more evidence."
    )

    tk.Label(
        panel,
        text=story,
        font=("Arial", 12),
        bg="#101b2b",
        fg="#f1f5f9",
        justify="left",
        anchor="nw",
        wraplength=340
    ).pack(fill="both", expand=True)

    # CONTINUE BUTTON
    tk.Button(
        current_frame,
        text="CONTINUE  →",
        font=("Arial", 12, "bold"),
        bg="#0ea5e9",
        fg="#07111c",
        activebackground="#38bdf8",
        relief="flat",
        padx=22,
        pady=10,
        cursor="hand2",
        command=show_cctv
    ).place(
        relx=0.12,
        rely=0.84,
        anchor="center"
    )

    play_background_sound("suspense.wav")
# ---------------- CLOSE GAME ----------------

def close_game():
    try:
        pygame.mixer.music.stop()
        pygame.mixer.quit()
    except Exception:
        pass

    root.destroy()
# ---------------- SCREEN 5: CCTV INVESTIGATION ----------------

def show_cctv():
    global current_frame, background_image

    clear_screen()

    current_frame = tk.Frame(root, bg="#0b1220")
    current_frame.pack(fill="both", expand=True)

    # CCTV background image
    background_label = tk.Label(
        current_frame,
        bg="#0b1220",
        borderwidth=0
    )
    background_label.place(
        x=0, y=0, relwidth=1, relheight=1
    )

    def resize_background(event):
        global background_image

        if event.width < 2 or event.height < 2:
            return

        image_path = os.path.join(
            IMAGE_DIR, "cctv_scene.png"
        )

        try:
            image = Image.open(image_path)
            image = image.resize(
                (event.width, event.height),
                Image.Resampling.LANCZOS
            )

            background_image = ImageTk.PhotoImage(image)
            background_label.configure(image=background_image)

        except Exception as error:
            print("CCTV image error:", error)

    current_frame.bind("<Configure>", resize_background)

    # CCTV investigation panel
    cctv_panel = tk.Frame(
        current_frame,
        bg="#0b1220",
        highlightbackground="#475569",
        highlightthickness=1
    )

    cctv_panel.place(
        relx=0.53,
        rely=0.10,
        relwidth=0.43,
        relheight=0.70
    )

    tk.Label(
        cctv_panel,
        text="CCTV FOOTAGE",
        font=("Arial", 19, "bold"),
        bg="#0b1220",
        fg="#38bdf8"
    ).pack(pady=(18, 10))

    cctv_text = tk.Label(
        cctv_panel,
        text=(
            "The security camera recorded "
            "someone entering the house.\n\n"
            "The person's face is unclear.\n\n"
            "Examine the footage for more details."
        ),
        font=("Arial", 11),
        bg="#0b1220",
        fg="#f1f5f9",
        wraplength=320,
        justify="left",
        padx=15
    )

    cctv_text.pack(fill="both", expand=True, pady=10)

    def examine_footage():
        cctv_text.config(
            text=(
                "CCTV FINDINGS\n\n"
                "Time: 9:41 PM\n\n"
                "A person entered the house.\n\n"
                "Clothing: Black jacket\n\n"
                "Object carried: Silver briefcase\n\n"
                "The person's face remains hidden.\n\n"
                "You need to examine the briefcase "
                "before making a conclusion."
            )
        )

    

    tk.Button(
        cctv_panel,
        text="EXAMINE CCTV FOOTAGE",
        font=("Arial", 10, "bold"),
        bg="#172235",
        fg="#f1f5f9",
        relief="flat",
        pady=10,
        command=examine_footage
    ).pack(fill="x", padx=18, pady=15)

    # Return to hidden file
    tk.Button(
        current_frame,
        text="BACK TO HIDDEN FILE",
        font=("Arial", 9),
        bg="#172235",
        fg="#f1f5f9",
        relief="flat",
        padx=12,
        pady=8,
        command=show_hidden_file
    ).place(
        relx=0.17,
        rely=0.90,
        anchor="center"
    )

    # Continue to briefcase
    tk.Button(
        current_frame,
        text="CONTINUE",
        font=("Arial", 11, "bold"),
        bg="#38bdf8",
        fg="#07111c",
        relief="flat",
        padx=25,
        pady=10,
        command=show_briefcase
    ).place(
        relx=0.78,
        rely=0.90,
        anchor="center"
    )

    play_background_sound("suspense.wav", 0.20)


# ---------------- SILVER BRIEFCASE ----------------

def show_briefcase():
    global current_frame, background_image

    clear_screen()

    current_frame = tk.Frame(root, bg="#080d18")
    current_frame.pack(fill="both", expand=True)

    image_path = os.path.join(IMAGE_DIR, "silver_briefcase.png")

    try:
        original_image = Image.open(image_path)

        background_label = tk.Label(current_frame, bg="#080d18")
        background_label.place(
            x=0, y=0, relwidth=1, relheight=1
        )

        def resize_background(event=None):
            global background_image

            width = current_frame.winfo_width()
            height = current_frame.winfo_height()

            if width <= 1 or height <= 1:
                return

            resized = original_image.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )

            background_image = ImageTk.PhotoImage(resized)
            background_label.configure(image=background_image)

        current_frame.bind("<Configure>", resize_background)
        resize_background()

    except Exception as error:
        print("Briefcase image loading error:", error)

    # STORY PANEL
    panel = tk.Frame(
        current_frame,
        bg="#101b2b",
        padx=18,
        pady=15
    )

    panel.place(
        relx=0.035,
        rely=0.12,
        relwidth=0.46,
        relheight=0.67
    )

    tk.Label(
        panel,
        text="THE SILVER BRIEFCASE",
        font=("Georgia", 20, "bold"),
        bg="#101b2b",
        fg="#38bdf8",
        anchor="w"
    ).pack(fill="x", pady=(0, 12))

    story = (
        "You examine the briefcase seen in the CCTV footage.\n\n"
        "Inside, you discover three important clues:\n\n"
        "1. Financial papers linked to Michael Brown.\n\n"
        "2. A blood-stained handkerchief.\n\n"
        "3. A handwritten note:\n\n"
        '"SOMEONE HAS BEEN WATCHING YOU.\n'
        'DON’T TRUST WHAT YOU SEE."\n\n'
        "The warning raises another question: "
        "Was James being followed, and by whom?"    
    )

    tk.Label(
        panel,
        text=story,
        font=("Arial", 11),
        bg="#101b2b",
        fg="#f1f5f9",
        justify="left",
        anchor="nw",
        wraplength=340
    ).pack(fill="both", expand=True)

    # CONTINUE TO SUSPECTS
    tk.Button(
        current_frame,
        text="INVESTIGATE SUSPECTS  →",
        font=("Arial", 11, "bold"),
        bg="#0ea5e9",
        fg="#07111c",
        activebackground="#38bdf8",
        relief="flat",
        padx=16,
        pady=10,
        cursor="hand2",
        command=show_suspects
    ).place(
        relx=0.15,
        rely=0.86,
        anchor="center"
    )

    # BACK TO CCTV
    tk.Button(
        current_frame,
        text="← BACK TO CCTV",
        font=("Arial", 10),
        bg="#172235",
        fg="#f1f5f9",
        activebackground="#24364d",
        relief="flat",
        padx=12,
        pady=8,
        cursor="hand2",
        command=show_cctv
    ).place(
        relx=0.15,
        rely=0.94,
        anchor="center"
    )

    play_background_sound("suspense.wav")

# ---------------- SUSPECT INVESTIGATION ----------------

def show_suspects():
    global current_frame, background_image

    clear_screen()

    current_frame = tk.Frame(root, bg="#080d18")
    current_frame.pack(fill="both", expand=True)

    image_path = os.path.join(IMAGE_DIR, "final_deduction.png")

    try:
        original_image = Image.open(image_path)
        background_label = tk.Label(current_frame, bg="#080d18")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        def resize_background(event=None):
            global background_image

            width = current_frame.winfo_width()
            height = current_frame.winfo_height()

            if width <= 1 or height <= 1:
                return

            resized = original_image.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )

            background_image = ImageTk.PhotoImage(resized)
            background_label.configure(image=background_image)

        current_frame.bind("<Configure>", resize_background)
        resize_background()

    except Exception as error:
        print("Suspect image error:", error)

    # SMALL PANEL WITH NAMES ONLY
    panel = tk.Frame(
        current_frame,
        bg="#101b2b",
        padx=20,
        pady=18
    )

    panel.place(
        relx=0.95,
        rely=0.15,
        relwidth=0.36,
        relheight=0.65,
        anchor="ne"
    )

    tk.Label(
        panel,
        text="SUSPECTS",
        font=("Georgia", 24, "bold"),
        bg="#101b2b",
        fg="#38bdf8"
    ).pack(pady=(0, 22))

    suspects = [
        "DANIEL CARTER",
        "MICHAEL BROWN",
        "EMILY WILSON"
    ]

    for name in suspects:
        tk.Button(
            panel,
            text=name,
            font=("Arial", 12, "bold"),
            bg="#172235",
            fg="#f1f5f9",
            activebackground="#24364d",
            activeforeground="#38bdf8",
            relief="flat",
            cursor="hand2",
            pady=12,
            command=lambda n=name: show_suspect_details(n)
        ).pack(fill="x", pady=8)

    tk.Button(
        current_frame,
        text="← BACK TO BRIEFCASE",
        font=("Arial", 10),
        bg="#172235",
        fg="#f1f5f9",
        relief="flat",
        cursor="hand2",
        command=show_briefcase
    ).place(
        relx=0.20,
        rely=0.90,
        anchor="center"
    )

    play_background_sound("suspense.wav")
        # SOLVE THE CASE BUTTON
    tk.Button(
        current_frame,
        text="SOLVE THE CASE",
        font=("Arial", 11, "bold"),
        bg="#38bdf8",
        fg="#07111c",
        activebackground="#0ea5e9",
        relief="flat",
        cursor="hand2",
        padx=20,
        pady=10,
        command=show_final_deduction
    ).place(
        relx=0.78,
        rely=0.90,
        anchor="center"
    )


# ---------------- SUSPECT DETAILS ----------------

def show_suspect_details(name):
    global current_frame

    clear_screen()

    current_frame = tk.Frame(root, bg="#0b1220")
    current_frame.pack(fill="both", expand=True)

    details = {
        "DANIEL CARTER": (
            "DANIEL CARTER",
            "RELATION: James's brother\n\n"
            "MOTIVE:\n"
            "Daniel argued with James over family property "
            "shortly before his death.\n\n"
            "SUSPICIOUS DETAIL:\n"
            "He claims he left before 9:00 PM, but nobody "
            "has confirmed his whereabouts."
        ),

        "MICHAEL BROWN": (
            "MICHAEL BROWN",
            "RELATION: James's business partner\n\n"
            "MOTIVE:\n"
            "A financial record connects Michael to the "
            "₹50,00,000 transfer.\n\n"
            "SUSPICIOUS DETAIL:\n"
            "He says he was working late, but his exact "
            "movements that night remain unclear."
        ),

        "EMILY WILSON": (
            "EMILY WILSON",
            "RELATION: James's close friend\n\n"
            "MOTIVE:\n"
            "James had recently confronted Emily about "
            "something she had kept secret.\n\n"
            "SUSPICIOUS DETAIL:\n"
            "She admits meeting James that evening but "
            "has not explained what they discussed."
        )
    }

    title, information = details[name]

    tk.Label(
        current_frame,
        text=title,
        font=("Georgia", 26, "bold"),
        bg="#0b1220",
        fg="#38bdf8"
    ).pack(pady=(90, 25))

    tk.Label(
        current_frame,
        text=information,
        font=("Arial", 12),
        bg="#0b1220",
        fg="#f1f5f9",
        justify="left",
        wraplength=580
    ).pack(pady=15)

    tk.Button(
        current_frame,
        text="← BACK TO SUSPECTS",
        font=("Arial", 11, "bold"),
        bg="#0ea5e9",
        fg="#07111c",
        relief="flat",
        cursor="hand2",
        padx=18,
        pady=10,
        command=show_suspects
    ).pack(pady=25)

    play_background_sound("suspense.wav")
    tk.Button(
        current_frame,
        text="SOLVE THE CASE",
        command=show_final_deduction,
        bg="#38bdf8",
        fg="#07111c",
        font=("Arial", 11, "bold"),
        relief="flat",
        padx=20,
        pady=8
    ).place(
        relx=0.78,
        rely=0.88,
        anchor="center"
    )
# ---------------- FINAL DEDUCTION ----------------

def show_final_deduction():
    global current_frame, background_image

    clear_screen()

    current_frame = tk.Frame(root, bg="#080d18")
    current_frame.pack(fill="both", expand=True)

    image_path = os.path.join(IMAGE_DIR, "final_deduction.png")

    try:
        original_image = Image.open(image_path)

        background_label = tk.Label(current_frame, bg="#080d18")
        background_label.place(x=0, y=0, relwidth=1, relheight=1)

        def resize_background(event=None):
            global background_image

            width = current_frame.winfo_width()
            height = current_frame.winfo_height()

            if width <= 1 or height <= 1:
                return

            resized = original_image.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )

            background_image = ImageTk.PhotoImage(resized)
            background_label.configure(image=background_image)

        current_frame.bind("<Configure>", resize_background)
        resize_background()

    except Exception as error:
        print("Final deduction image error:", error)

    panel = tk.Frame(
        current_frame,
        bg="#101b2b",
        padx=20,
        pady=18
    )
    panel.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        relwidth=0.48,
        relheight=0.65
    )

    tk.Label(
        panel,
        text="FINAL DEDUCTION",
        font=("Arial", 20, "bold"),
        bg="#101b2b",
        fg="#38bdf8"
    ).pack(pady=(5, 15))

    tk.Label(
        panel,
        text=(
            "James Carter is dead.\n\n"
            "A suspicious financial transfer, a hidden file,\n"
            "CCTV footage, and a torn note have led you here.\n\n"
            "Who killed James Carter?"
        ),
        font=("Arial", 10),
        bg="#101b2b",
        fg="#f1f5f9",
        justify="center",
        wraplength=360
    ).pack(pady=10)

    tk.Button(
        panel,
        text="MAKE YOUR ACCUSATION",
        font=("Arial", 10, "bold"),
        bg="#38bdf8",
        fg="#07111c",
        relief="flat",
        padx=15,
        pady=9,
        command=show_accusation
    ).pack(pady=15)

    tk.Button(
        panel,
        text="BACK TO SUSPECTS",
        font=("Arial", 9),
        bg="#263449",
        fg="#f1f5f9",
        relief="flat",
        padx=12,
        pady=7,
        command=show_suspects
    ).pack(pady=5)

    play_background_sound("suspense.wav")


# ---------------- MAKE ACCUSATION ----------------

def show_accusation():
    global current_frame

    clear_screen()

    current_frame = tk.Frame(root, bg="#080d18")
    current_frame.pack(fill="both", expand=True)

    panel = tk.Frame(
        current_frame,
        bg="#101b2b",
        padx=30,
        pady=25
    )
    panel.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    tk.Label(
        panel,
        text="WHO KILLED JAMES CARTER?",
        font=("Arial", 18, "bold"),
        bg="#101b2b",
        fg="#38bdf8"
    ).pack(pady=(5, 20))

    tk.Label(
        panel,
        text="Choose the suspect you believe is guilty.",
        font=("Arial", 10),
        bg="#101b2b",
        fg="#f1f5f9"
    ).pack(pady=(0, 15))

    suspects = [
        "Daniel Carter",
        "Michael Brown",
        "Emily Wilson"
    ]

    for suspect in suspects:
        tk.Button(
            panel,
            text=suspect,
            font=("Arial", 11, "bold"),
            bg="#263449",
            fg="#f1f5f9",
            activebackground="#38bdf8",
            relief="flat",
            width=25,
            pady=9,
            command=lambda name=suspect: show_ending(name)
        ).pack(pady=6)

    tk.Button(
        panel,
        text="BACK",
        font=("Arial", 9),
        bg="#101b2b",
        fg="#94a3b8",
        relief="flat",
        command=show_final_deduction
    ).pack(pady=(15, 0))

    play_background_sound("suspense.wav")


# ---------------- CASE SOLVED ----------------

def show_ending(suspect):
    global current_frame

    clear_screen()

    current_frame = tk.Frame(root, bg="#080d18")
    current_frame.pack(fill="both", expand=True)


    if suspect == "Michael Brown":
        title = "CASE SOLVED"

        message = (
            "The evidence exposes Michael Brown.\n\n"
            "The stolen money, the hidden file, and the CCTV\n"
            "footage finally fit together.\n\n"
            "Michael is arrested.\n\n"
            "For the first time in days, you can breathe again."
        )

        final_line = "CASE CLOSED."

    else:
        title = "CASE UNSOLVED"

        message = (
            "The investigation has been officially closed.\n\n"
            "There is not enough evidence to continue the case.\n\n"
            "The files are sealed. The investigation is over.\n\n"
            "But you know something is missing.\n\n"
            "You cannot accept that this is the end."
        )

        final_line = "SOME CASES REFUSE TO STAY CLOSED."   

    panel = tk.Frame(
        current_frame,
        bg="#030912",
        padx=25,
        pady=25,
        highlightbackground="#24445d",
        highlightthickness=1
    )
    panel.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        relwidth=0.70,
        relheight=0.78
    )

    title_color = "#38bdf8" if suspect == "Michael Brown" else "#ff4055"

    tk.Label(
        panel,
        text=title,
        font=("Arial", 22, "bold"),
        bg="#030912",
        fg=title_color
    ).pack(pady=(15, 20))

    tk.Label(
        panel,
        text=message,
        font=("Arial", 11),
        bg="#030912",
        fg="#f1f5f9",
        justify="center",
        wraplength=480
    ).pack(pady=10)

    tk.Label(
        panel,
        text=final_line,
        font=("Arial", 15, "bold"),
        bg="#030912",
        fg=title_color
    ).pack(pady=20)

    if suspect == "Michael Brown":
        play_background_sound("case_solved.wav")
        root.after(6000, show_correct_ending_twist)

    else:
         play_background_sound("case_unsolved.wav")
         root.after(8000, show_three_days_later)

# ---------------- GRADUAL TWIST IMAGE REVEAL ----------------

def show_correct_ending_twist():
    global current_frame, background_image

    clear_screen()

    current_frame = tk.Frame(root, bg="black")
    current_frame.pack(fill="both", expand=True)

    image_path = os.path.join(
        IMAGE_DIR,
        "correct_ending_twist.png"
    )

    try:
        original_image = Image.open(image_path).convert("RGB")

        background_label = tk.Label(
            current_frame,
            bg="black"
        )
        background_label.place(
            x=0,
            y=0,
            relwidth=1,
            relheight=1
        )

        reveal_step = {"value": 0}
        total_steps = 40

        # Start the twist sound as the image begins to appear
        play_background_sound("twist.wav", volume=0.35)

        def reveal_image():
            global background_image

            if not current_frame.winfo_exists():
                return

            width = current_frame.winfo_width()
            height = current_frame.winfo_height()

            if width <= 1 or height <= 1:
                root.after(50, reveal_image)
                return

            step = reveal_step["value"]

            # Resize the original image to fit the window
            resized = original_image.resize(
                (width, height),
                Image.Resampling.LANCZOS
            )

            # Begin completely dark and gradually reveal the image
            brightness = step / total_steps

            revealed = resized.point(
                lambda pixel: int(pixel * brightness)
            )

            background_image = ImageTk.PhotoImage(revealed)
            background_label.configure(image=background_image)

            if step < total_steps:
                reveal_step["value"] += 1
                root.after(100, reveal_image)
            else:
                # Keep the fully revealed image on screen
                root.after(3000, show_twist_warning)

        # Start from a completely black screen
        reveal_image()

    except Exception as error:
        print("Twist image error:", error)
        root.after(5000, show_twist_warning)

    

# ---------------- TWIST WARNING SCREEN ----------------

def show_twist_warning():
    global current_frame

    clear_screen()

    current_frame = tk.Frame(
        root,
        bg="#000000"
    )
    current_frame.pack(fill="both", expand=True)

    warning_text = (
        "YOU THOUGHT THE CASE WAS CLOSED.\n\n"
        "Michael Brown was arrested.\n"
        "The evidence was found.\n"
        "The truth was uncovered.\n\n"
        "BUT DID YOU FORGET THE WARNING?\n\n"
        "\"DON'T TRUST WHAT YOU SEE.\""
    )

    tk.Label(
        current_frame,
        text=warning_text,
        font=("Arial", 13),
        bg="#000000",
        fg="#f1f5f9",
        justify="center",
        wraplength=700
    ).place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    root.after(10000, show_final_title)




# ---------------- FINAL TITLE ----------------

def show_final_title():
    global current_frame

    clear_screen()

    current_frame = tk.Frame(root, bg="black")
    current_frame.pack(fill="both", expand=True)

    title = "THE LAST VISIT"

    label = tk.Label(
    current_frame,
    text="",
    font=("Georgia", 38, "bold"),
    bg="black",
    fg="#b91c1c"
)
    label.place(relx=0.5, rely=0.4, anchor="center")

    def reveal_title(index=0):
        if index <= len(title):
            label.config(text=title[:index])
            root.after(180, lambda: reveal_title(index + 1))
        else:
            # Show PLAY AGAIN after the title finishes
            play_again_button.place(
                relx=0.5,
                rely=0.65,
                anchor="center"
            )

            root.after(3000, stop_final_sound)

    def stop_final_sound():
        pygame.mixer.music.stop()

    def play_again():
        pygame.mixer.music.stop()
        show_title_screen()

    play_again_button = tk.Button(
        current_frame,
        text="PLAY AGAIN",
        font=("Arial", 12, "bold"),
        bg="#38bdf8",
        fg="black",
        activebackground="#0ea5e9",
        activeforeground="white",
        relief="flat",
        padx=25,
        pady=12,
        cursor="hand2",
        command=play_again
    )

    reveal_title()

# ---------------- UNSOLVED ENDING: SCENE 2 ----------------

def show_three_days_later():
    global current_frame

    clear_screen()

    # Start the twist sound at the beginning of Scene 2
    play_background_sound("twist.wav", 0.25)

    current_frame = tk.Frame(root, bg="black")
    current_frame.pack(fill="both", expand=True)

    message = "THREE DAYS LATER..."
    label = tk.Label(
        current_frame,
        text="",
        font=("Arial", 26, "bold"),
        bg="black",
        fg="white"
    )
    label.place(relx=0.5, rely=0.5, anchor="center")

    def reveal_text(index=0):
        if index <= len(message):
            label.config(text=message[:index])
            root.after(180, lambda: reveal_text(index + 1))
        else:
            # Keep the text visible briefly, then continue
            root.after(4000, show_shadow_scene)

    reveal_text()
# ---------------- SCENE 3: THE SHADOW ----------------

def show_shadow_scene():
    global current_frame

    clear_screen()

    current_frame = tk.Frame(root, bg="black")
    current_frame.pack(fill="both", expand=True)

    # Load the shadow scene image
    image_path = os.path.join(IMAGE_DIR, "wrong_ending_twist.png")

    try:
        image = Image.open(image_path)
        image = image.resize((900, 600))
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(
            current_frame,
            image=photo,
            bg="black"
        )
        image_label.image = photo
        image_label.pack(fill="both", expand=True)

    except Exception as error:
        print("Could not load shadow scene image:", error)

    # Messages appear gradually
        # Messages appear gradually
    messages = [
        "You are alone at home.",
        "After Finishing the work.",
        "You're getting ready to go to bed.",
        "Just as you're about to fall asleep, your phone lights up.",
        "You pick up your phone.",
        "A new message appears from an unknown sender.",
        "UNKNOWN SENDER",
        "I GUESS YOU DIDN'T HEED THE WARNING.",
        "A spike of fear shot through you. What was that?” "
    ]
    message_label = tk.Label(
        current_frame,
        text="",
        font=("Arial", 15, "bold"),
        bg="black",
        fg="white",
        wraplength=700
    )
    message_label.place(relx=0.5, rely=0.85, anchor="center")

    def reveal_message(message_index=0, char_index=0):
        if message_index >= len(messages):
            root.after(2500, show_final_warning)
            return

        message = messages[message_index]

        if char_index <= len(message):
            message_label.config(text=message[:char_index])
            root.after(
                70,
                lambda: reveal_message(
                    message_index,
                    char_index + 1
                )
            )
        else:
            root.after(
                1800,
                lambda: reveal_message(message_index + 1, 0)
            )

    reveal_message()    

# ---------------- SCENE 4: WRONG-ENDING FINAL IMAGE ----------------

def show_final_warning():
    global current_frame

    clear_screen()

    # Screen 1: Display the final image alone
    current_frame = tk.Frame(root, bg="black")
    current_frame.pack(fill="both", expand=True)

    image_path = os.path.join(IMAGE_DIR, "wrong_ending_finalimage.png")

    try:
        image = Image.open(image_path)
        image = image.resize((900, 600))
        photo = ImageTk.PhotoImage(image)

        image_label = tk.Label(
            current_frame,
            image=photo,
            bg="black"
        )
        image_label.image = photo
        image_label.pack(fill="both", expand=True)

    except Exception as error:
        print("Could not load wrong-ending final image:", error)

    # Show the warning on a new screen after 5 seconds
    root.after(5000, show_warning_text)


# ---------------- SCENE 5: FINAL WARNING TEXT ----------------

def show_warning_text():
    global current_frame

    clear_screen()

    # Screen 2: Warning text on a separate black screen
    current_frame = tk.Frame(root, bg="black")
    current_frame.pack(fill="both", expand=True)

    message = "YOU SHOULD HAVE LEFT IT ALONE."

    label = tk.Label(
        current_frame,
        text="",
        font=("Arial", 25, "bold"),
        bg="black",
        fg="white"
    )
    label.place(relx=0.5, rely=0.5, anchor="center")

    def reveal_text(index=0):
        if index <= len(message):
            label.config(text=message[:index])
            root.after(180, lambda: reveal_text(index + 1))
        else:
            # Screen 3: Final title
            root.after(4000, show_final_title)

    reveal_text()
# ---------------- SCENE 5: THE LAST VISIT ----------------

def show_final_title():
    global current_frame

    clear_screen()

    current_frame = tk.Frame(root, bg="black")
    current_frame.pack(fill="both", expand=True)

    title = "THE LAST VISIT"

    label = tk.Label(
    current_frame,
    text="",
    font=("Georgia", 38, "bold"),
    bg="black",
    fg="#b91c1c"
)
    label.place(relx=0.5, rely=0.4, anchor="center")

    def reveal_title(index=0):
        if index <= len(title):
            label.config(text=title[:index])
            root.after(180, lambda: reveal_title(index + 1))
        else:
            # Show PLAY AGAIN after the title finishes
            play_again_button.place(
                relx=0.5,
                rely=0.65,
                anchor="center"
            )

            root.after(3000, stop_final_sound)

    def stop_final_sound():
        pygame.mixer.music.stop()

    def play_again():
        pygame.mixer.music.stop()
        show_title_screen()

    play_again_button = tk.Button(
        current_frame,
        text="PLAY AGAIN",
        font=("Arial", 12, "bold"),
        bg="#38bdf8",
        fg="black",
        activebackground="#0ea5e9",
        activeforeground="white",
        relief="flat",
        padx=25,
        pady=12,
        cursor="hand2",
        command=play_again
    )

    reveal_title()
# ---------------- START PROGRAM ----------------

show_title_screen()
root.mainloop()