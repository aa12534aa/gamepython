import pygame
import logic

class Button:
    def __init__(self, text, x, y, width, height, command):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.command = command
        self.active = True

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, (0, 0, 0), (self.x, self.y, self.width, self.height))
            font = pygame.font.Font(None, 36)
            text = font.render(self.text, True, (255, 255, 255))
            screen.blit(text, (self.x + 10, self.y + 10))

    def is_clicked(self, pos):
        x, y = pos
        if self.active:
            return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
        return False

def create_player_buttons(game_instance):
    player_attack_button = Button("Attack", 330, 320, 250, 50, lambda: logic.player_attack(game_instance))
    player_movef_button = Button("Move forward", 330, 380, 250, 50, lambda: logic.player_movef(game_instance))
    player_moveb_button = Button("Move backwards", 330, 440, 250, 50, lambda: logic.player_moveb(game_instance))

    return player_attack_button, player_movef_button, player_moveb_button

def create_player2_buttons(game_instance):
    player2_attack_button = Button("Attack", 610, 320, 250, 50, lambda: logic.player2_attack(game_instance))
    player2_movef_button = Button("Move forward", 610, 380, 250, 50, lambda: logic.player2_movef(game_instance))
    player2_moveb_button = Button("Move backwards", 610, 440, 250, 50, lambda: logic.player2_moveb(game_instance))

    return player2_attack_button, player2_movef_button, player2_moveb_button
