import tkinter as tk
from tkinter import ttk
import time
import threading
import platform

# --- SOUND FUNCTION ---
def play_sound():
    try:
        if platform.system() == "Windows":
            import winsound
            winsound.Beep(1000, 500)
        else:
            print("\a")
    except:
        pass

# --- SETTINGS ---
interval = 600  # seconds (10 minutes)
running = False

# --- HELPER ---
def format_time(seconds):
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes:02d}:{secs:02d}"

# --- FUNCTIONS ---
def start():
    global running
    if not running:
        running = True
        threading.Thread(target=loop, daemon=True).start()

def stop():
    global running
    running = False
    label.config(text="Stopped 🛑")

def faster():
    global interval
    interval = max(5, interval // 2)
    label.config(text=f"Speed: every {format_time(interval)} ⚡")

def loop():
    global running

    while running:
        start_time = time.time()

        while time.time() - start_time < interval:
            if not running:
                return

            elapsed = time.time() - start_time
            progress = (elapsed / interval) * 100
            progress_bar["value"] = progress

            time_left = interval - elapsed
            label.config(text=f"Next shot in: {format_time(time_left)}")

            time.sleep(0.1)

        # TIME'S UP → SHOT
        progress_bar["value"] = 100
        label.config(text="TAKE A SHOT NOW! 🥃")
        play_sound()

        time.sleep(2)

# --- UI ---
root = tk.Tk()
root.title("Race Mode 🏁")
root.geometry("400x200")

label = tk.Label(root, text="Press Start", font=("Arial", 14))
label.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
progress_bar.pack(pady=10)

btn_start = tk.Button(root, text="Start", command=start)
btn_start.pack(pady=5)

btn_fast = tk.Button(root, text="FASTER ⚡", command=faster)
btn_fast.pack(pady=5)

btn_stop = tk.Button(root, text="Stop", command=stop)
btn_stop.pack(pady=5)

root.mainloop()