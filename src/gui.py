import tkinter as tk
import random
import time
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ReactionTimeApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Reaction Time Tester")

        # Initialize variables
        self.start_time = None
        self.reaction_times = []
        self.all_reaction_times = []  # New attribute to store all reaction times across games
        self.num_trials = 5
        self.current_trial = 0

        # Create UI elements
        self.label = tk.Label(master, text="Choose the number of trials and press Start!", font=("Arial", 14))
        self.label.pack(pady=10)

        self.trials_entry = tk.Entry(master)
        self.trials_entry.insert(0, "5")
        self.trials_entry.pack(pady=5)

        self.start_button = tk.Button(master, text="Start", command=self.start_game)
        self.start_button.pack(pady=10)

        self.canvas_frame = tk.Frame(master)
        self.canvas_frame.pack()

        # Matplotlib figure for real-time plotting
        self.figure = Figure(figsize=(5, 3), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.ax.set_title("Reaction Times")
        self.ax.set_xlabel("Trial")
        self.ax.set_ylabel("Time (s)")
        self.line, = self.ax.plot([], [], marker="o")

        self.canvas = FigureCanvasTkAgg(self.figure, self.canvas_frame)
        self.canvas.get_tk_widget().pack()

        # Trial information label
        self.trial_info_label = tk.Label(master, text="", font=("Arial", 12))
        self.trial_info_label.pack(anchor="nw", padx=10, pady=10)

    def start_game(self):
        try:
            self.num_trials = int(self.trials_entry.get())
        except ValueError:
            self.label.config(text="Please enter a valid number of trials.")
            return

        self.all_reaction_times.extend(self.reaction_times)  # Save previous game's reaction times
        self.reaction_times = []  # Reset for the new game
        self.current_trial = 0
        self.label.config(text="Get ready for the first trial!")
        self.master.after(1000, self.start_trial)

    def start_trial(self):
        self.label.config(text="Wait for green...", bg="red")
        self.master.update()
        delay = random.randint(2000, 5000)  # Random delay between 2-5 seconds
        self.master.after(delay, self.show_green)

    def show_green(self):
        self.label.config(text="Click now!", bg="green")
        self.start_time = time.time()
        self.master.bind("<Button-1>", self.record_reaction_time)

    def record_reaction_time(self, event):
        if self.start_time is None:
            return

        reaction_time = time.time() - self.start_time
        self.reaction_times.append(reaction_time)
        self.start_time = None

        # Update plot
        self.update_plot()

        # Display stats
        best_time = min(self.reaction_times)
        worst_time = max(self.reaction_times)
        avg_time = sum(self.reaction_times) / len(self.reaction_times)
        self.label.config(text=(
            f"Trial {self.current_trial + 1}/{self.num_trials}\n"
            f"Reaction Time: {reaction_time:.3f}s\n"
            f"Best: {best_time:.3f}s, Worst: {worst_time:.3f}s, Avg: {avg_time:.3f}s"
        ), bg="SystemButtonFace")

        # Update trial information
        self.update_trial_info(self.current_trial + 1)

        self.current_trial += 1
        if self.current_trial < self.num_trials:
            self.master.after(2000, self.start_trial)
        else:
            self.label.config(text="Game Over! Thanks for playing.")
            self.master.unbind("<Button-1>")

    def update_plot(self):
        self.ax.clear()
        self.ax.set_title("Reaction Times")
        self.ax.set_xlabel("Trial")
        self.ax.set_ylabel("Time (s)")
        self.ax.plot(range(1, len(self.all_reaction_times) + len(self.reaction_times) + 1),
                     self.all_reaction_times + self.reaction_times, marker="o")  # Plot all reaction times
        self.canvas.draw()

    def update_trial_info(self, trial_number):
        self.trial_info_label.config(text=f"Trial: {trial_number}\nAll Reaction Times: {', '.join(f'{t:.3f}s' for t in self.all_reaction_times + self.reaction_times)}")

root = tk.Tk()
app = ReactionTimeApp(root)
root.mainloop()