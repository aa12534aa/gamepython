import pygame
import json
from buttons import create_player_buttons, create_player2_buttons
import logic

# take playerdata
with open('players_info.json', 'r') as f:
    playerdata = json.load(f)
with open('mobs.json', 'r') as f:
    mobsdata = json.load(f)
class Game:
    def __init__(self, players_info):
        pygame.init()
        self.screen = pygame.display.set_mode((1100, 600))  # Zmieniono wysokość ekranu
        pygame.display.set_caption("Gra")

        for i in mobsdata.keys():
            if mobsdata[i]["fight"] == 1:
                mob = i

        # initialization players playerdata
        self.playermove = 2 if playerdata['turn'] == 1 else 1
        self.aimove = playerdata['turn']
        self.mob = mob

        # creating player and mob stats
        if self.playermove == 1:
            self.p1position = playerdata['p1']['p1position']
            self.p1health = playerdata['p1']['p1health']
            self.p1attack = playerdata['p1']['p1attack']
            self.p1name = playerdata['p1']['p1name']
            self.p1defense = playerdata['p1']['p1defense']
            self.p1range = playerdata['p1']['p1range']

            self.p2position = 2
            self.p2health = mobsdata[mob]['health']
            self.p2attack = mobsdata[mob]['attack']
            self.p2name = mob
            self.p2defense = mobsdata[mob]['defense']
            self.p2range = mobsdata[mob]['range']
        else:
            self.p2position = playerdata['p2']['p2position']
            self.p2health = playerdata['p2']['p2health']
            self.p2attack = playerdata['p2']['p2attack']
            self.p2name = playerdata['p2']['p2name']
            self.p2defense = playerdata['p2']['p2defense']
            self.p2range = playerdata['p2']['p2range']

            self.p1position = -2
            self.p1health = mobsdata[mob]['health']
            self.p1attack = mobsdata[mob]['attack']
            self.p1name = mob
            self.p1defense = mobsdata[mob]['defense']
            self.p1range = mobsdata[mob]['range']

        # turn
        self.turn = playerdata['turn']

        self.font = pygame.font.Font(None, 36)

        # initialization buttons
        self.player_attack_button, self.player_movef_button, self.player_moveb_button = create_player_buttons(self)
        self.player2_attack_button, self.player2_movef_button, self.player2_moveb_button = create_player2_buttons(self)

        # is game ended
        self.game_over = False

        # changing activity of buttons
        if self.aimove == 1:
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
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over and self.turn == self.playermove:
                    if self.playermove == 1:
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
                    else:
                        pos = pygame.mouse.get_pos()
                        if self.player2_attack_button.is_clicked(pos):
                            logic.player2_attack(self)
                            self.change_turn()
                        elif self.player2_movef_button.is_clicked(pos):
                            logic.player2_movef(self)
                            self.change_turn()
                        elif self.player2_moveb_button.is_clicked(pos):
                            logic.player2_moveb(self)
                            self.change_turn()

            if not self.game_over and self.turn == self.aimove:
                logic.ai_action(self)
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
        font2 = pygame.font.Font(None, 80)
        winner = self.p1name if self.p1health > 0 else self.p2name
        winner_label = font2.render(f"{winner} won!", True, (0, 0, 0))
        self.screen.blit(winner_label, (450, 200))
        self.game_over = True

        if self.playermove == 1:
            playerdata['p1']['p1health'] = self.p1health
            mobsdata[self.mob]['health'] = self.p2health
        else:
            playerdata['p2']['p2health'] = self.p2health
            mobsdata[self.mob]['health'] = self.p1health
        mobsdata[self.mob]['fight'] = 0
        print(playerdata)
        with open('mobs.json', 'w') as f:
            json.dump(mobsdata, f)
        with open('players_info.json', 'w') as f:
            json.dump(playerdata, f)

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
