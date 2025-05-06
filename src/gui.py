import tkinter as tk
import random
import time

class ReactionTimeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Reaction Time Tester")
        self.label = tk.Label(master, text="Press the button when it turns green!")
        self.label.pack()
        self.button = tk.Button(master, text="Start", command=self.start_test)
        self.button.pack()
        self.start_time = None

    def start_test(self):
        self.label.config(text="Get ready...")
        self.master.update()
        time.sleep(random.randint(2, 5))
        self.label.config(text="Now!")
        self.button.config(bg="green")
        self.start_time = time.time()
        self.button.bind("<Button-1>", self.stop_test)

    def stop_test(self, event):
        if self.start_time is None:
            return
        reaction_time = time.time() - self.start_time
        self.label.config(text=f"Your reaction time is {reaction_time:.3f} seconds.")
        self.button.config(bg="SystemButtonFace")
        self.start_time = None