import tkinter as tk
import time
import pygame
import threading

class Terminal(tk.Text):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg="black", fg="cyan", font=("Recharge Rg", 15), wrap="word")
        self.max_lines = 20 
        pygame.mixer.init() 

    def play_sound(self):
        pygame.mixer.music.load('click.mp3')
        pygame.mixer.music.play()

    def type_code(self, code_lines):
        self.delete(1.0, tk.END) 
        lines = code_lines.strip().splitlines()  
        
        for line in lines:
            for char in line:
                self.insert(tk.END, char) 
                self.update()
                
                
                threading.Thread(target=self.play_sound).start()
                
                time.sleep(0.01)
            self.insert(tk.END, "\n")
            self.update() 
            time.sleep(0.1)
            
            if int(self.index('end-1c').split('.')[0]) > self.max_lines:
                self.see(tk.END)

        self.see(tk.END)
        
    def toggle_typing(self, event=None):
        if self.typing_active:
            self.typing_active = False 
            if self.typing_thread is not None:
                self.typing_thread.join() 
        else:
            self.typing_active = True
            self.typing_thread = threading.Thread(target=self.typing_process)
            self.typing_thread.start()
            
        self.master.bind("<space>", self.toggle_typing)
