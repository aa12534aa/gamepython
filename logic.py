import random

def ai_action(game_instance):
    if game_instance.turn == 1:
        if abs(game_instance.p1.position - game_instance.p2.position) <= game_instance.p1.range:
            player_attack(game_instance)
        else:
            if random.randint(1, 10) <= 3:
                player_moveb(game_instance)
            else:
                player_movef(game_instance)
    else:
        if abs(game_instance.p2.position - game_instance.p1.position) <= game_instance.p2.range:
            player2_attack(game_instance)
        else:
            if random.randint(1, 10) <= 3:
                player2_moveb(game_instance)
            else:
                player2_movef(game_instance)

def player_attack(self):
    if self.turn == 1 and abs(self.p2.position - self.p1.position) <= self.p1.range:
        self.p2.health = round(self.p2.health - round((random.randint(int(self.p1.attack * 0.5), self.p1.attack) / (1 + self.p2.defense / self.p1.attack)), 2), 2)
        self.update_game_state()

def player2_attack(self):
    if self.turn == 2 and abs(self.p2.position - self.p1.position) <= self.p2.range:
        self.p1.health = round(self.p1.health - round((random.randint(int(self.p2.attack * 0.5), self.p2.attack) / (1 + self.p1.defense / self.p2.attack)), 2), 2)
        self.update_game_state()

def player_movef(self):
    if self.turn == 1 and self.p1.position != self.p2.position:
        self.p1.position += 1
        self.update_game_state()

def player2_movef(self):
    if self.turn == 2 and self.p1.position != self.p2.position:
        self.p2.position -= 1
        self.update_game_state()

def player_moveb(self):
    if self.turn == 1:
        self.p1.position -= 1 if self.p1.position != -5 else 0
        self.update_game_state()

def player2_moveb(self):
    if self.turn == 2:
        self.p2.position += 1 if self.p2.position != 5 else 0
        self.update_game_state()
