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


def show_punchline(event=None):  # Add event for key press handling
    if current_joke:
        punchline_text.set(current_joke[1])

# Quit the application


def quit_app():
    root.destroy()


# Load jokes from file
jokes = load_jokes()
current_joke = None

# Set up the main application window
root = tk.Tk()
root.title("Alexa Tell Me a Joke")
root.geometry("400x250")

# String variables for joke setup and punchline
joke_text = tk.StringVar()
punchline_text = tk.StringVar()

# Widgets
joke_label = tk.Label(root, textvariable=joke_text,
                      wraplength=350, font=("Arial", 12))
punchline_label = tk.Label(
    root, textvariable=punchline_text, wraplength=350, font=("Arial", 12, "italic"))
tell_joke_button = tk.Button(
    root, text="Tell me a Joke", command=tell_joke, width=20)
quit_button = tk.Button(root, text="Quit", command=quit_app, width=20)

# Layout
joke_label.pack(pady=10)
punchline_label.pack(pady=10)
tell_joke_button.pack(pady=5)
quit_button.pack(pady=5)

# Bind key for showing punchline (e.g., Enter key)
root.bind('<Return>', show_punchline)

# Start the tkinter loop
root.mainloop()
