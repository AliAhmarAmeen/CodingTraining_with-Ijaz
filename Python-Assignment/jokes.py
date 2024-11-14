import tkinter as tk
import random

# Function to load jokes from the file
def load_jokes(filename="randomJokes.txt"):
    jokes = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                if '?' in line:
                    setup, punchline = line.strip().split('?')
                    jokes.append((setup + "?", punchline))
    except FileNotFoundError:
        jokes.append(("Joke file not found!", "Please check the file path."))
    return jokes

# Function to display a new joke setup
def tell_joke():
    global current_joke
    current_joke = random.choice(jokes)
    joke_text.set(current_joke[0])  # Show setup
    punchline_text.set("")  # Clear punchline

# Function to display the punchline
def show_punchline():
    punchline_text.set(current_joke[1])

# Load jokes from file
jokes = load_jokes()
current_joke = None

# Set up the main application window
root = tk.Tk()
root.title("Alexa Tell Me a Joke")
root.geometry("400x200")

# String variables for joke setup and punchline
joke_text = tk.StringVar()
punchline_text = tk.StringVar()

# Widgets
joke_label = tk.Label(root, textvariable=joke_text, wraplength=350, font=("Arial", 12))
punchline_label = tk.Label(root, textvariable=punchline_text, wraplength=350, font=("Arial", 12, "italic"))
tell_joke_button = tk.Button(root, text="Tell me a Joke", command=tell_joke)
show_punchline_button = tk.Button(root, text="Show Punchline", command=show_punchline)

# Layout
joke_label.pack(pady=10)
punchline_label.pack(pady=10)
tell_joke_button.pack(side="left", padx=20)
show_punchline_button.pack(side="right", padx=20)

# Start the tkinter loop
root.mainloop()
