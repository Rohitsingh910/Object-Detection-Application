import tkinter as tk
import time

class Clock(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg="black")
        self.label = tk.Label(self, bg="black", fg="white", font=("Helvetica", 16, "bold"), width=20, height=2)
        self.label.pack(padx=10, pady=10)

        self.update_clock()

    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.label.config(text=current_time)
        self.after(1000, self.update_clock) 
