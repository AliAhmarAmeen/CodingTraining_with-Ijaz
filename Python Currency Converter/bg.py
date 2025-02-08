import tkinter as tk
from PIL import Image, ImageTk

# Create main window
root = tk.Tk()
root.title("Background Image Example")
root.geometry("800x600")  # Set window size

# Load and set background image
image_path = "back.jpg"  # Make sure the image is in the same folder
bg_image = Image.open(image_path)
bg_image = bg_image.resize((800, 600), Image.Resampling.LANCZOS)  # Resize image to fit window
bg_photo = ImageTk.PhotoImage(bg_image)

# Create a label to hold the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(relwidth=1, relheight=1)  # Make it cover the entire window

# Add a simple label on top of the background
label = tk.Label(root, text="Hello, Tkinter!", font=("Arial", 24), bg="white")
label.pack(pady=20)

root.mainloop()
