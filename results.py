import pygame
import sys
import json

# Pygame setup
pygame.init()

# Screen settings
SCREEN_SIZE = (800, 600)
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Game Results")

# Load player data
with open('players_info.json', 'r') as f:
    playerdata = json.load(f)

# Determine winner
winner = None
if playerdata['p1']['p1health'] <= 0:
    winner = 2
elif playerdata['p2']['p2health'] <= 0:
    winner = 1

# Main loop to display results
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            pygame.quit()
            sys.exit()

    # Clear screen
    screen.fill((0, 0, 0))

    # Display results
    font = pygame.font.Font(None, 74)
    if winner == 1:
        result_text = f"{playerdata['p1']['p1name']} Wins!"
    else:
        result_text = f"{playerdata['p2']['p2name']} Wins!"
    text = font.render(result_text, True, (0, 255, 0))
    text_rect = text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2))
    screen.blit(text, text_rect)

    # Update the display
    pygame.display.flip()