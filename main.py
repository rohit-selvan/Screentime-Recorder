import tkinter as tk
from tkinter import ttk, messagebox
import time
import psutil
import matplotlib.pyplot as plt
from datetime import datetime
import threading

class ScreenTimeRecorder(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Screen Time Recorder")
        self.geometry("400x300")
        self.configure(bg="#f0f4f8")
        
        self.start_time = None
        self.total_screen_time = 0  # in seconds
        self.app_usage = {}  # Dictionary to store time spent on each app
        self.running = True  # Control flag for the tracking loop
        
        self.create_widgets()
        threading.Thread(target=self.track_screen_time, daemon=True).start()  # Start the tracking in a separate thread

    def create_widgets(self):
        tk.Label(self, text="Screen Time Recorder", font=("Verdana", 18, "bold"), bg="#f0f4f8", fg="#2c3e50").pack(pady=10)
        
        self.total_time_label = tk.Label(self, text="Total Screen Time: 0s", font=("Verdana", 12), bg="#f0f4f8")
        self.total_time_label.pack(pady=10)
        
        tk.Button(self, text="Show Usage Report", command=self.show_report, font=("Verdana", 12), bg="#3498db", fg="white").pack(pady=10)
        tk.Button(self, text="Reset Data", command=self.reset_data, font=("Verdana", 12), bg="#e74c3c", fg="white").pack(pady=10)
        
    def track_screen_time(self):
        self.start_time = time.time()
        while self.running:
            active_window = self.get_active_window()
            if active_window:
                self.app_usage[active_window] = self.app_usage.get(active_window, 0) + 1  # Increment time by 1 second
                self.total_screen_time = int(time.time() - self.start_time)
                self.update_total_time_label()
            time.sleep(1)
    
    def get_active_window(self):
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name']:
                    return proc.info['name']  # Return the name of the active process
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
        return None
    
    def update_total_time_label(self):
        self.total_time_label.config(text=f"Total Screen Time: {self.total_screen_time}s")
    
    def show_report(self):
        if not self.app_usage:
            messagebox.showinfo("Usage Report", "No data to show.")
            return
        
        # Create a pie chart for app usage
        apps = list(self.app_usage.keys())
        times = list(self.app_usage.values())
        
        plt.figure(figsize=(8, 6))
        plt.pie(times, labels=apps, autopct="%1.1f%%", startangle=140)
        plt.title("App Usage Report")
        plt.show()
    
    def reset_data(self):
        self.start_time = time.time()
        self.total_screen_time = 0
        self.app_usage.clear()
        self.update_total_time_label()
        messagebox.showinfo("Reset Data", "All data has been reset.")

    def on_close(self):
        self.running = False
        self.destroy()

if __name__ == "__main__":
    app = ScreenTimeRecorder()
    app.protocol("WM_DELETE_WINDOW", app.on_close)
    app.mainloop()
