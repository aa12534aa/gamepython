import tkinter as tk
import json

# Maksymalna liczba punktów do rozdysponowania
MAX_POINTS = 8


class PlayerStatsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Statystyki graczy")

        self.stats_labels = ["Attack", "Health Points", "Defense"]
        self.stats_p1 = {stat: 1 for stat in self.stats_labels}
        self.stats_p2 = {stat: 1 for stat in self.stats_labels}
        self.remaining_points_p1 = MAX_POINTS
        self.remaining_points_p2 = MAX_POINTS

        self.create_widgets()

    def create_widgets(self):
        # Tworzenie etykiet dla graczy
        tk.Label(self.root, text="Player 1", font=("Arial", 16)).grid(row=0, column=1)
        tk.Label(self.root, text="Player 2", font=("Arial", 16)).grid(row=0, column=4)

        # Nickname fields
        tk.Label(self.root, text="Player nickname").grid(row=1, column=0)
        self.nickname_p1 = tk.Entry(self.root)
        self.nickname_p1.grid(row=1, column=1, padx=20)
        self.nickname_p2 = tk.Entry(self.root)
        self.nickname_p2.grid(row=1, column=4, padx=20)

        # Statystyki
        for i, stat in enumerate(self.stats_labels, start=2):
            tk.Label(self.root, text=stat).grid(row=i, column=0)

            self.create_stat_row(i, stat, self.stats_p1, 1)
            self.create_stat_row(i, stat, self.stats_p2, 4)

        # Przyciski zapisu
        tk.Button(self.root, text="Graj", command=self.save_data).grid(row=len(self.stats_labels) + 2, column=1, columnspan=4)

    def create_stat_row(self, row, stat, stats_dict, column):
        label_var = tk.StringVar(value="1")
        tk.Label(self.root, textvariable=label_var).grid(row=row, column=column)
        tk.Button(self.root, text="+", command=lambda s=stat, p=1 if column == 1 else 2, var=label_var: self.update_stat(s, 1, p, var)).grid(row=row, column=column + 1)
        tk.Button(self.root, text="-", command=lambda s=stat, p=1 if column == 1 else 2, var=label_var: self.update_stat(s, -1, p, var)).grid(row=row, column=column + 2)

    def update_stat(self, stat, delta, player, label_var):
        if player == 1:
            if self.stats_p1[stat] + delta >= 1 and self.remaining_points_p1 - delta >= 1:
                self.stats_p1[stat] += delta
                self.remaining_points_p1 -= delta
                label_var.set(self.stats_p1[stat])
        else:
            if self.stats_p2[stat] + delta >= 1 and self.remaining_points_p2 - delta >= 1:
                self.stats_p2[stat] += delta
                self.remaining_points_p2 -= delta
                label_var.set(self.stats_p2[stat])

    def save_data(self):
        datajson = {
            "turn": 1,
            "p1": {
                "name": self.nickname_p1.get(),
                "attack": self.stats_p1["Attack"] * 5,
                "health": self.stats_p1["Health Points"] * 20,
                "defense": self.stats_p1["Defense"] * 3,
                "money": 100,
                "range": 1,
                "items": {"gloves": 0, "lhand": 0, "rhand": 0, "chest": 0, "helmet": 0, "boots": 0}
            },
            "p2": {
                "name": self.nickname_p2.get(),
                "attack": self.stats_p2["Attack"] * 5,
                "health": self.stats_p2["Health Points"] * 20,
                "defense": self.stats_p2["Defense"] * 3,
                "money": 100,
                "range": 1,
                "items": {"gloves": 0, "lhand": 0, "rhand": 0, "chest": 0, "helmet": 0, "boots": 0}
            }
        }
        datajson2 = {
            "tower": {
                "fight": 0,
                "name": "tower",
                "attack": 60,
                "health": 1500,
                "defense": 30,
                "range": 3
            },
            "village": {
                "fight": 0,
                "name": "village",
                "attack": 15,
                "health": 150,
                "defense": 8,
                "range": 1
            },
            "boss": {
                "fight": 0,
                "name": "boss",
                "attack": 40,
                "health": 900,
                "defense": 20,
                "range": 2
            }
        }
        with open('players_info.json', 'w') as f:
            json.dump(datajson, f)
        with open('mobs.json', 'w') as f:
            json.dump(datajson2, f)
        self.root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    app = PlayerStatsApp(root)
    root.mainloop()
