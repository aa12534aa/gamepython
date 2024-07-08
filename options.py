import tkinter as tk
import json

# create window
window = tk.Tk()
window.title("Statystyki graczy")

# Tworzenie etykiet
tk.Label(window, text="Player 1", font=("Arial", 16)).grid(row=0, column=1)
tk.Label(window, text="Player 2", font=("Arial", 16)).grid(row=0, column=2)

# fields to fill
entries = []
for i, stat in enumerate(["Player nickname", "Attack", "Health Points", "Defense"], start=1):
    if stat == "Player nickname":
        tk.Label(window, text=stat).grid(row=i, column=0)
        for j in range(1, 3):
            entry = tk.Entry(window)
            entry.grid(row=i, column=j, padx=20)
            entries.append(entry)
    else:
        tk.Label(window, text=stat).grid(row=i+1, column=0)
        entry = tk.Entry(window)
        entry.grid(row=i+1, column=1, columnspan=2, padx=20)
        entries.append(entry)

# function to save data and end action
def save_data():
    data = [entry.get() for entry in entries]
    datajson = {"turn": 1, "p1": {"p1name": data[0], "p1health": int(data[3]), "p1attack": int(data[2]), "p1defense": int(data[4]), "p1range": 2}, "p2": {"p2name": data[1], "p2health": int(data[3]), "p2attack": int(data[2]), "p2defense": int(data[4]), "p2range": 2}}
    datajson2 = {"tower": {"fight": 0, "attack": int(data[2]) * 2, "defense": int(data[4]) * 4, "health": int(data[3]) * 10, "range": 2}, "village": {"fight": 0, "attack": int(data[2]) * 0.7, "defense": int(data[4]) * 0, "health": int(data[3]) * 0.7, "range": 2}}
    with open('players_info.json', 'w') as f:
        json.dump(datajson, f)
    with open('mobs.json', 'w') as f:
        json.dump(datajson2, f)
    window.quit()

# button to save
tk.Button(window, text="Graj", command=save_data).grid(row=6, column=1, columnspan=2)

# show window
window.mainloop()
