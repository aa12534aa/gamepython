import pygame
import sys
import json

# Wczytywanie danych gracza
with open('players_info.json', 'r') as f:
    playerdata = json.load(f)

# Inicjalizacja pygame
pygame.init()

# Kolory
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Wymiary ekranu
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 300

# Przedmioty w sklepie
items = {
    "sword": 50,
    "shield": 30,
    "potion": 10
}

# Czcionki
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

def draw_text(surface, text, pos, font, color=BLACK):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

def shop(money):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Sklep")

    item_rects = []
    for i, (item, price) in enumerate(items.items()):
        rect = pygame.Rect(50, 50 + i * 60, 300, 50)
        item_rects.append((rect, item, price))

    running = True
    while running:
        screen.fill(WHITE)

        draw_text(screen, f"Twoje pieniądze: {money}", (50, 10), font)

        for rect, item, price in item_rects:
            pygame.draw.rect(screen, GREEN if money >= price else RED, rect)
            draw_text(screen, f"{item.capitalize()}: {price} złota", (rect.x + 10, rect.y + 10), small_font)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for rect, item, price in item_rects:
                    if rect.collidepoint(event.pos):
                        if money >= price:
                            money -= price
                            if playerdata['turn'] == 2:
                                playerdata['p1']['p1money'] = money
                            else:
                                playerdata['p2']['p2money'] = money
                            with open('players_info.json', 'w') as f:
                                json.dump(playerdata, f)

        pygame.display.flip()

    return money

if __name__ == "__main__":
    if playerdata['turn'] == 2:
        money = playerdata['p1']['p1money']
    else:
        money = playerdata['p2']['p2money']
    new_money = shop(money)
    sys.exit(new_money)
