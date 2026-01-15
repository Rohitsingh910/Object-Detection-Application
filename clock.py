import tkinter as tk
import time

class Clock:
    def __init__(self, master):
        self.master = master
        
        # Frame for background
        self.clock_frame = tk.Frame(master, bg='cyan', bd=2, relief=tk.SUNKEN)
        self.clock_frame.place(relx=0.95, rely=0.05, anchor=tk.NE)  # Position 
        
        # Create the clock label
        self.label = tk.Label(self.clock_frame, font=('Recharge Rg', 15, 'bold'), bg='aqua', fg='black')
        self.label.pack(padx=10, pady=5)  # Add padding 

        # =updating the clock
        self.update_clock()

    def update_clock(self):
        current_time = time.strftime('%H:%M:%S')  # Get current time 
        self.label.config(text=current_time)
        self.master.after(1000, self.update_clock)  # Update the time 
