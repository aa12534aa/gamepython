import pygame
import json
from buttons import create_player_buttons, create_player2_buttons
import logic

# take data
with open('players_info.json', 'r') as f:
    data = json.load(f)
class Game:
    def __init__(self, players_info):
        pygame.init()
        self.screen = pygame.display.set_mode((1100, 600))  # Zmieniono wysokość ekranu
        pygame.display.set_caption("Gra")

        # initialization players data

        # p1
        self.p1position = data['p1']['p1position']
        self.p1health = data['p1']['p1health']
        self.p1attack = data['p1']['p1attack']
        self.p1name = data['p1']['p1name']
        self.p1defense = data['p1']['p1defense']
        self.p1range = data['p1']['p1range']

        # p2
        self.p2position = data['p2']['p2position']
        self.p2health = data['p2']['p2health']
        self.p2attack = data['p2']['p2attack']
        self.p2name = data['p2']['p2name']
        self.p2defense = data['p2']['p2defense']
        self.p2range = data['p2']['p2range']

        # turn
        self.turn = data['turn']

        self.font = pygame.font.Font(None, 36)

        # initialization buttons
        self.player_attack_button, self.player_movef_button, self.player_moveb_button = create_player_buttons(self)
        self.player2_attack_button, self.player2_movef_button, self.player2_moveb_button = create_player2_buttons(self)

        # is game ended
        self.game_over = False

        # changing activity of buttons
        if self.turn == 1:
            self.player_attack_button.active = True
            self.player_movef_button.active = True
            self.player_moveb_button.active = True
            self.player2_attack_button.active = False
            self.player2_movef_button.active = False
            self.player2_moveb_button.active = False
        else:
            self.player_attack_button.active = False
            self.player_movef_button.active = False
            self.player_moveb_button.active = False
            self.player2_attack_button.active = True
            self.player2_movef_button.active = True
            self.player2_moveb_button.active = True


    def start_game(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:  # is game ended
                    pos = pygame.mouse.get_pos()
                    if self.player_attack_button.is_clicked(pos):
                        logic.player_attack(self)
                        self.change_turn()
                    elif self.player_movef_button.is_clicked(pos):
                        logic.player_movef(self)
                        self.change_turn()
                    elif self.player_moveb_button.is_clicked(pos):
                        logic.player_moveb(self)
                        self.change_turn()
                    elif self.player2_attack_button.is_clicked(pos):
                        logic.player2_attack(self)
                        self.change_turn()
                    elif self.player2_movef_button.is_clicked(pos):
                        logic.player2_movef(self)
                        self.change_turn()
                    elif self.player2_moveb_button.is_clicked(pos):
                        logic.player2_moveb(self)
                        self.change_turn()

            # creating interface and map
            self.screen.fill((255, 255, 255))
            self.draw_board()
            self.update_game_state()
            pygame.display.flip()

        pygame.quit()

    def draw_board(self):
        for i in range(-5, 6):
            x = (i + 5) * 100
            pygame.draw.rect(self.screen, (0, 0, 0), (x, 10, 100, 100))
            pygame.draw.rect(self.screen, (255, 255, 255), (x + 5, 15, 90, 90))
        pygame.draw.rect(self.screen, (0, 0, 255), ((self.p1position + 5) * 100 + 5, 15, 90, 90))
        pygame.draw.rect(self.screen, (255, 0, 0), ((self.p2position + 5) * 100 + 5, 15, 90, 90))

    def update_game_state(self):
        turn_label = self.font.render(f"Turn: {self.p1name if self.turn == 1 else self.p2name}", True, (0, 0, 0))
        player_label = self.font.render(f"Player 1 - HP: {self.p1health}", True, (0, 0, 0))
        player2_label = self.font.render(f"Player 2 - HP: {self.p2health}", True, (0, 0, 0))
        p1position_label = self.font.render(f"position: {self.p1position}", True, (0, 0, 0))
        p2position_label = self.font.render(f"position: {self.p2position}", True, (0, 0, 0))

        self.screen.blit(turn_label, (20, 120))
        self.screen.blit(player_label, (20, 160))
        self.screen.blit(player2_label, (20, 200))
        self.screen.blit(p1position_label, (20, 240))
        self.screen.blit(p2position_label, (20, 280))

        self.player_attack_button.draw(self.screen)
        self.player_movef_button.draw(self.screen)
        self.player_moveb_button.draw(self.screen)
        self.player2_attack_button.draw(self.screen)
        self.player2_movef_button.draw(self.screen)
        self.player2_moveb_button.draw(self.screen)

        if self.p1health <= 0 or self.p2health <= 0:
            self.end_game()

    def change_turn(self):
        if self.turn == 1:
            self.turn = 2
            self.player_attack_button.active = False
            self.player_movef_button.active = False
            self.player_moveb_button.active = False
            self.player2_attack_button.active = True
            self.player2_movef_button.active = True
            self.player2_moveb_button.active = True
        else:
            self.turn = 1
            self.player2_attack_button.active = False
            self.player2_movef_button.active = False
            self.player2_moveb_button.active = False
            self.player_attack_button.active = True
            self.player_movef_button.active = True
            self.player_moveb_button.active = True

    def end_game(self):
        data['p1']['p1health'] = self.p1health
        data['p2']['p2health'] = self.p2health

        with open('players_info.json', 'w') as f:
            json.dump(data, f)

        # Dodajemy przycisk "continue"
        continue_button = pygame.Rect(450, 300, 200, 50)  # Ustawiamy pozycję i rozmiar przycisku
        pygame.draw.rect(self.screen, (0, 255, 0), continue_button)  # Rysujemy przycisk na ekranie
        font3 = pygame.font.Font(None, 50)
        continue_label = font3.render("Continue", True, (0, 0, 0))
        self.screen.blit(continue_label, (475, 305))  # Dodajemy etykietę do przycisku

        # Sprawdzamy, czy przycisk "continue" został naciśnięty
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(
                            pygame.mouse.get_pos()):  # Jeśli przycisk "continue" został naciśnięty
                        pygame.quit()  # Zamykamy grę
                        return
            pygame.display.update()

game = Game('players_info.json')
game.start_game()
