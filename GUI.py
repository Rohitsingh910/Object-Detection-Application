import tkinter as tk
from PIL import Image, ImageTk
import pygame
import time
import human3   # your detection file

# ---------------- CONFIG ----------------
IMAGE_PATH = "loading.png"
SOUND_PATH = "loading.mp3"
ROTATE_SPEED = 5
LOAD_DELAY = 20  # ms
# ----------------------------------------


class LoadingScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Initializing System")
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg="black")

        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        # Load image
        self.original_image = Image.open(IMAGE_PATH).resize((450, 450), Image.LANCZOS)
        self.angle = 0
        self.tk_image = None
        self.image_id = None

        # Percentage
        self.percent = 0
        self.text_id = None

        # Init sound
        pygame.mixer.init()
        pygame.mixer.music.load(SOUND_PATH)
        pygame.mixer.music.play(-1)

        # Start automatically
        self.root.after(300, self.update)

    def update(self):
        self.rotate_image()
        self.update_percentage()

        if self.percent < 100:
            self.root.after(LOAD_DELAY, self.update)
        else:
            pygame.mixer.music.stop()
            self.root.after(300, self.launch_main_app)

    def rotate_image(self):
        rotated = self.original_image.rotate(self.angle, expand=True)
        self.tk_image = ImageTk.PhotoImage(rotated)

        cx = self.root.winfo_screenwidth() // 2
        cy = self.root.winfo_screenheight() // 2

        if self.image_id is None:
            self.image_id = self.canvas.create_image(cx, cy, image=self.tk_image)
        else:
            self.canvas.itemconfig(self.image_id, image=self.tk_image)

        self.angle = (self.angle + ROTATE_SPEED) % 360

    def update_percentage(self):
        cx = self.root.winfo_screenwidth() // 2
        cy = self.root.winfo_screenheight() // 2

        if self.text_id is None:
            self.text_id = self.canvas.create_text(
                cx, cy,
                text="0%",
                fill="cyan",
                font=("Arial", 40, "bold")
            )
        else:
            self.canvas.itemconfig(self.text_id, text=f"{self.percent}%")

        self.percent += 1

    def launch_main_app(self):
        self.root.destroy()
        new_root = tk.Tk()
        human3.HumanDetectionApp(new_root)
        new_root.mainloop()


# ---------------- RUN ----------------
if __name__ == "__main__":
    root = tk.Tk()
    LoadingScreen(root)
    root.mainloop()
