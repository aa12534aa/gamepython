import pygame
import json
from buttons import create_player_buttons, create_player2_buttons
import logic

# Wczytywanie danych
with open('players_info.json', 'r') as f:
    playerdata = json.load(f)
with open('mobs.json', 'r') as f:
    mobsdata = json.load(f)

class Player:
    def __init__(self, pdata, pos):
        self.position = pos
        self.name = pdata['name']
        self.health = pdata['health']
        self.attack = pdata['attack']
        self.defense = pdata['defense']
        self.range = pdata['range']
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1100, 600))
        pygame.display.set_caption("Gra")

        self.is_mob_fight = False

        # Sprawdzenie czy jest walka z mobem
        for mob, mob_info in mobsdata.items():
            if mob_info["fight"] == 1:
                self.mob = mob
                self.is_mob_fight = True
                if mob == "tower":
                    mobsdata["tower"]["fight"] = -1
                else:
                    mobsdata[f"{mob}"]["fight"] = 0
                with open('mobs.json', 'w') as f:
                    json.dump(mobsdata, f)
                break

        # Inicjalizacja graczy
        self.p1 = Player(playerdata['p1'], -2)
        if playerdata['turn'] == 1 and self.is_mob_fight:
            self.p1 = Player(playerdata['p2'], -2)

        if self.is_mob_fight:
            self.playermove = 1
            self.p2 = Player(mobsdata[self.mob], 2)
        else:
            self.p2 = Player(playerdata['p2'], 2)

        # Turn
        if self.is_mob_fight:
            self.turn = 1
        elif playerdata['turn'] == 1:
            self.turn = 2
        else:
            self.turn = 1

        self.font = pygame.font.Font(None, 36)

        # Inicjalizacja przycisków
        self.player_attack_button, self.player_movef_button, self.player_moveb_button = create_player_buttons(self)
        self.player2_attack_button, self.player2_movef_button, self.player2_moveb_button = create_player2_buttons(self)

        # Sprawdzanie zakończenia gry
        self.game_over = False

        # Zmiana aktywności przycisków
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
                elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                    pos = pygame.mouse.get_pos()
                    if self.turn == 1:
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
                        if self.player2_attack_button.is_clicked(pos):
                            logic.player2_attack(self)
                            self.change_turn()
                        elif self.player2_movef_button.is_clicked(pos):
                            logic.player2_movef(self)
                            self.change_turn()
                        elif self.player2_moveb_button.is_clicked(pos):
                            logic.player2_moveb(self)
                            self.change_turn()

            if not self.game_over and self.is_mob_fight and self.turn == 2:
                logic.ai_action(self)
                self.change_turn()

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
        pygame.draw.rect(self.screen, (0, 0, 255), ((self.p1.position + 5) * 100 + 5, 15, 90, 90))
        pygame.draw.rect(self.screen, (255, 0, 0), ((self.p2.position + 5) * 100 + 5, 15, 90, 90))

    def update_game_state(self):
        turn_label = self.font.render(f"Turn: {self.p1.name if self.turn == 1 else self.p2.name}", True, (0, 0, 0))
        player_label = self.font.render(f"Player 1 - HP: {self.p1.health}", True, (0, 0, 0))
        player2_label = self.font.render(f"Player 2 - HP: {self.p2.health}", True, (0, 0, 0))
        p1position_label = self.font.render(f"Position: {self.p1.position}", True, (0, 0, 0))
        p2position_label = self.font.render(f"Position: {self.p2.position}", True, (0, 0, 0))

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

        if self.p1.health <= 0 or self.p2.health <= 0:
            print(self.p1.health, self.p2.health)
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
        if self.is_mob_fight:
            if playerdata['turn'] == 2:
                playerdata['p1']['health'] = self.p1.health
            else:
                playerdata['p2']['health'] = self.p1.health
            mobsdata[self.mob]['health'] = self.p2.health
        else:
            playerdata['p1']['health'] = self.p1.health
            playerdata['p2']['health'] = self.p2.health
        with open('players_info.json', 'w') as f:
            json.dump(playerdata, f)

        font2 = pygame.font.Font(None, 80)
        winner = self.p1.name if self.p1.health > 0 else self.p2.name
        winner_label = font2.render(f"{winner} won!", True, (0, 0, 0))
        self.screen.blit(winner_label, (500, 500))
        self.game_over = True

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

if __name__ == "__main__":
    game = Game()
    game.start_game()