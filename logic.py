import random

def ai_action(game_instance):
    if game_instance.turn == 1:
        if abs(game_instance.p1position - game_instance.p2position) <= game_instance.p1range:
            player_attack(game_instance)
        else:
            if random.randint(1, 10) <= 3:
                player_moveb(game_instance)
            else:
                player_movef(game_instance)
    else:
        if abs(game_instance.p2position - game_instance.p1position) <= game_instance.p2range:
            player2_attack(game_instance)
        else:
            if random.randint(1, 10) <= 3:
                player2_moveb(game_instance)
            else:
                player2_movef(game_instance)

def player_attack(self):
    if self.turn == 1 and abs(self.p2position - self.p1position) <= self.p1range:
        self.p2health = round(self.p2health - round((random.randint(int(self.p1attack * 0.2), self.p1attack) / ((self.p1attack + self.p2defense) / self.p1attack)), 2), 2)
        self.update_game_state()

def player2_attack(self):
    if self.turn == 2 and abs(self.p2position - self.p1position) <= self.p2range:
        self.p1health = round(self.p1health - round((random.randint(int(self.p2attack * 0.2), self.p2attack) / ((self.p2attack + self.p1defense) / self.p2attack)), 2), 2)
        self.update_game_state()

def player_movef(self):
    if self.turn == 1 and self.p1position != self.p2position:
        self.p1position += 1
        self.update_game_state()

def player2_movef(self):
    if self.turn == 2 and self.p1position != self.p2position:
        self.p2position -= 1
        self.update_game_state()

def player_moveb(self):
    if self.turn == 1:
        self.p1position -= 1 if self.p1position != -5 else 0
        self.update_game_state()

def player2_moveb(self):
    if self.turn == 2:
        self.p2position += 1 if self.p2position != 5 else 0
        self.update_game_state()
