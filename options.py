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

# Adding Player Nickname fields
tk.Label(window, text="Player nickname").grid(row=1, column=0)
for j in range(1, 3):
    entry = tk.Entry(window)
    entry.grid(row=1, column=j, padx=20)
    entries.append(entry)

# Adding remaining fields
for i, stat in enumerate(["Attack", "Health Points", "Defense", "Money"], start=2):
    tk.Label(window, text=stat).grid(row=i, column=0)
    entry = tk.Entry(window)
    entry.grid(row=i, column=1, columnspan=2, padx=20)
    entries.append(entry)

# function to save data and end action
def save_data():
    data = [entry.get() for entry in entries]
    datajson = {
        "turn": 1,
        "p1": {
            "p1name": data[0],
            "p1attack": int(data[2]),
            "p1health": int(data[3]),
            "p1defense": int(data[4]),
            "p1money": int(data[5])
        },
        "p2": {
            "p2name": data[1],
            "p2attack": int(data[2]),
            "p2health": int(data[3]),
            "p2defense": int(data[4]),
            "p2money": int(data[5])
        }
    }
    datajson2 = {
        "tower": {
            "fight": 0,
            "attack": int(data[2]) * 2,
            "defense": int(data[4]) * 4,
            "health": int(data[3]) * 10,
            "range": 2
        },
        "village": {
            "fight": 0,
            "attack": int(data[2]) * 0.7,
            "defense": int(data[4]) * 0,
            "health": int(data[3]) * 0.7,
            "range": 2
        },
        "boss": {
            "fight": 0,
            "attack": int(data[2]) * 1.5,
            "defense": int(data[4]) * 0,
            "health": int(data[3]) * 5,
            "range": 2
        }
    }
    with open('players_info.json', 'w') as f:
        json.dump(datajson, f)
    with open('mobs.json', 'w') as f:
        json.dump(datajson2, f)
    window.quit()

# button to save
tk.Button(window, text="Graj", command=save_data).grid(row=7, column=1, columnspan=2)

# show window
window.mainloop()
