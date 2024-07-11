import pygame
import sys
import subprocess
import json
import random
import copy

# players creating starting options of the game
subprocess.run(["C:\\Program Files\\Python312\\python.exe", "options.py"])

# pygame
pygame.init()

# take playerdata
with open('players_info.json', 'r') as f:
    playerdata = json.load(f)
with open('mobs.json', 'r') as f:
    mobsdata = json.load(f)

# map and players info
SCREEN_SIZE = (800, 650) # map size
GRID_SIZE = 31
CELL_SIZE = (SCREEN_SIZE[0] - 200) // GRID_SIZE
RED = (255, 0, 0)
BLUE = (0, 0, 255)
Destroying = {"destroying": 0, "time": 0}

# creating map
gameMap = [[0]*GRID_SIZE for _ in range(GRID_SIZE)]
for x in range(GRID_SIZE):
    for y in range(GRID_SIZE):
        if x == 0 or y == 0 or x == GRID_SIZE - 1 or y == GRID_SIZE - 1 or x + y == GRID_SIZE - 1:
            gameMap[x][y] = 'X'
        elif abs(x - y) > 1 and random.randint(1, 100) <= 20:
            gameMap[x][y] = 'X'
        elif abs(x - y) > 1 and random.randint(1, 100) <= 8:
            gameMap[x][y] = 'V'
        elif abs(x - y) > 1 and random.randint(1, 100) <= 8:
            gameMap[x][y] = 'C'
        elif abs(x - y) > 1 and random.randint(1, 100) <= 3:
            gameMap[x][y] = 'B'
gameMap[(GRID_SIZE - 1) // 2][(GRID_SIZE - 1) // 2] = "T"
gameMap[1][2] = "S"
gameMap[GRID_SIZE - 2][GRID_SIZE - 3] = "S"

# screen initialization
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Poruszające się kwadraty")

# start position
red_x, red_y = GRID_SIZE - 2, GRID_SIZE - 2
blue_x, blue_y = 1, 1

# updating fields on the map
def changingField(x, y):
    global playerdata
    t = 1 if playerdata['turn'] == 2 else 2
    with open('players_info.json', 'w') as f:
        json.dump(playerdata, f)
    if gameMap[x][y] == "V":
        gameMap[x][y] = 0
        mobsdata['village']['fight'] = 1
        with open('mobs.json', 'w') as f:
            json.dump(mobsdata, f)
        subprocess.run(["C:\\Program Files\\Python312\\python.exe", "fight.py"])
        playerdata[f'p{t}'][f'p{t}money'] += random.randint(30, 50)
    elif gameMap[x][y] == "B":
        gameMap[x][y] = 0
        mobsdata['boss']['fight'] = 1
        with open('mobs.json', 'w') as f:
            json.dump(mobsdata, f)
        subprocess.run(["C:\\Program Files\\Python312\\python.exe", "fight.py"])
        playerdata[f'p{t}'][f'p{t}money'] += random.randint(60, 80)
    elif gameMap[x][y] == "C":
        gameMap[x][y] = 0
        playerdata[f'p{t}'][f'p{t}money'] += random.randint(10, 20)
    elif gameMap[x][y] == "T" and mobsdata['tower']['fight'] != -1:
        mobsdata['tower']['fight'] = 1
        with open('mobs.json', 'w') as f:
            json.dump(mobsdata, f)
        subprocess.run(["C:\\Program Files\\Python312\\python.exe", "fight.py"])
        global Destroying
        Destroying["destroying"] = 1
        mobsdata['tower']['fight'] = -1
        with open('mobs.json', 'w') as f:
            json.dump(mobsdata, f)
    elif gameMap[x][y] == "X":
        playerdata[f'p{t}'][f'p{t}health'] = 0
    elif gameMap[x][y] == "S":
        subprocess.run(["C:\\Program Files\\Python312\\python.exe", "shop.py"])
        with open('players_info.json', 'r') as f:
            playerdata = json.load(f)


    with open('players_info.json', 'w') as f:
            json.dump(playerdata, f)
    with open('players_info.json', 'r') as f:
        playerdata = json.load(f)
    if playerdata['p1']['p1health'] <= 0 or playerdata['p2']['p2health'] <= 0:
        subprocess.run(["C:\\Program Files\\Python312\\python.exe", "results.py"])
        sys.exit()
def destroying():
    global Destroying
    if Destroying["destroying"] == 1:
        Destroying["time"] += 1
        i = Destroying["time"]
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                if x <= i or y <= i or x >= GRID_SIZE - i - 1 or y >= GRID_SIZE - i - 1:
                    gameMap[x][y] = "X"

# main loop of game
while playerdata[f'p1'][f'p1health'] > 0 and playerdata[f'p2'][f'p2health'] > 0:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            flag = copy.deepcopy([red_x, red_y, blue_x, blue_y])
            if event.key == pygame.K_LEFT:
                if playerdata['turn'] == 1 and gameMap[blue_x][blue_y - 1] != 'X':
                    blue_y -= 1
                    playerdata['turn'] = 2
                elif playerdata['turn'] == 2 and gameMap[red_x][red_y - 1] != 'X':
                    red_y -= 1
                    playerdata['turn'] = 1
            elif event.key == pygame.K_RIGHT:
                if playerdata['turn'] == 1 and gameMap[blue_x][blue_y + 1] != 'X':
                    blue_y += 1
                    playerdata['turn'] = 2
                elif playerdata['turn'] == 2 and gameMap[red_x][red_y + 1] != 'X':
                    red_y += 1
                    playerdata['turn'] = 1
            elif event.key == pygame.K_UP:
                if playerdata['turn'] == 1 and gameMap[blue_x - 1][blue_y] != 'X':
                    blue_x -= 1
                    playerdata['turn'] = 2
                elif playerdata['turn'] == 2 and gameMap[red_x - 1][red_y] != 'X':
                    red_x -= 1
                    playerdata['turn'] = 1
            elif event.key == pygame.K_DOWN:
                if playerdata['turn'] == 1 and gameMap[blue_x + 1][blue_y] != 'X':
                    blue_x += 1
                    playerdata['turn'] = 2
                elif playerdata['turn'] == 2 and gameMap[red_x + 1][red_y] != 'X':
                    red_x += 1
                    playerdata['turn'] = 1
            # is somebody moved
            if flag != [red_x, red_y, blue_x, blue_y]:
                destroying()
            changingField(blue_x, blue_y)
            changingField(red_x, red_y)

    # creating map on the screen
    font = pygame.font.Font(None, 26)
    font2 = pygame.font.Font(None, 30)
    for x in range(GRID_SIZE):
        for y in range(GRID_SIZE):
            color = RED if (x, y) == (red_x, red_y) else BLUE if (x, y) == (blue_x, blue_y) else (0, 0, 0)
            pygame.draw.rect(screen, color, pygame.Rect(y * CELL_SIZE + 180, x * CELL_SIZE + 50, CELL_SIZE, CELL_SIZE))

            # drawing X
            if color == (0, 0, 0) and gameMap[x][y] == 'X':
                text = font.render('X', True, (255, 255, 255))
                text_rect = text.get_rect(center=(y * CELL_SIZE + CELL_SIZE // 2 + 180, x * CELL_SIZE + CELL_SIZE // 2 + 50))
                screen.blit(text, text_rect)

            # drawing A
            if color == (0, 0, 0) and gameMap[x][y] == 'V':
                text = font.render('V', True, (0,255,0))
                text_rect = text.get_rect(center=(y * CELL_SIZE + CELL_SIZE // 2 + 180, x * CELL_SIZE + CELL_SIZE // 2 + 50))
                screen.blit(text, text_rect)

            # drawing C
            if color == (0, 0, 0) and gameMap[x][y] == 'C':
                text = font.render('C', True, (255,215,0))
                text_rect = text.get_rect(center=(y * CELL_SIZE + CELL_SIZE // 2 + 180, x * CELL_SIZE + CELL_SIZE // 2 + 50))
                screen.blit(text, text_rect)

            # drawing T
            if color == (0, 0, 0) and gameMap[x][y] == 'T':
                text = font2.render('T', True, (191, 64, 191))
                text_rect = text.get_rect(center=(y * CELL_SIZE + CELL_SIZE // 2 + 180, x * CELL_SIZE + CELL_SIZE // 2 + 50))
                screen.blit(text, text_rect)

            # drawing S
            if color == (0, 0, 0) and gameMap[x][y] == 'S':
                text = font.render('S', True, (139,0,139))
                text_rect = text.get_rect(center=(y * CELL_SIZE + CELL_SIZE // 2 + 180, x * CELL_SIZE + CELL_SIZE // 2 + 50))
                screen.blit(text, text_rect)

            # drawing S
            if color == (0, 0, 0) and gameMap[x][y] == 'B':
                text = font.render('B', True, (150, 0, 0))
                text_rect = text.get_rect(center=(y * CELL_SIZE + CELL_SIZE // 2 + 180, x * CELL_SIZE + CELL_SIZE // 2 + 50))
                screen.blit(text, text_rect)

    # show player turn
    turn_surface = pygame.Surface((600, 40))
    turn_font = pygame.font.Font(None, 45)
    if playerdata['turn'] == 1:
        turn_text = turn_font.render(playerdata['p1']['p1name'], True, (255, 255, 255))
    else:
        turn_text = turn_font.render(playerdata['p2']['p2name'], True, (255, 255, 255))
    turn_surface.fill((0, 0, 0))
    turn_surface.blit(turn_text, (0, 0))
    screen.blit(turn_surface, (SCREEN_SIZE[0] // 2, 10))

    # players info
    info_font = pygame.font.Font(None, 28)

    # creating players info and updating it

    # p1
    p1_surface = pygame.Surface((160, 600))
    p1_info = info_font.render(playerdata['p1']['p1name'], True, (255, 255, 255))
    p1_attack = info_font.render(f'Attack: {playerdata['p1']['p1attack']}', True, (255, 255, 255))
    p1_hp = info_font.render(f'HP: {playerdata['p1']['p1health']}', True, (255, 255, 255))
    p1_def = info_font.render(f'Defense: {playerdata['p1']['p1defense']}', True, (255, 255, 255))
    p1_surface.fill((0, 0, 0))
    p1_surface.blit(p1_info, (0, 0))
    p1_surface.blit(p1_attack, (0, 30))
    p1_surface.blit(p1_hp, (0, 60))
    p1_surface.blit(p1_def, (0, 90))
    screen.blit(p1_surface, (10, 10))

    # p2
    p2_surface = pygame.Surface((160, 600))
    p2_info = info_font.render(playerdata['p2']['p2name'], True, (255, 255, 255))
    p2_attack = info_font.render(f'Attack: {playerdata['p2']['p2attack']}', True, (255, 255, 255))
    p2_hp = info_font.render(f'HP: {playerdata['p2']['p2health']}', True, (255, 255, 255))
    p2_def = info_font.render(f'Defense: {playerdata['p2']['p2defense']}', True, (255, 255, 255))
    p2_surface.fill((0, 0, 0))
    p2_surface.blit(p2_info, (0, 0))
    p2_surface.blit(p2_attack, (0, 30))
    p2_surface.blit(p2_hp, (0, 60))
    p2_surface.blit(p2_def, (0, 90))
    screen.blit(p2_surface, (10, 400))

    # is blue and red fighting
    if (blue_x, blue_y) == (red_x, red_y) or playerdata[f'p1'][f'p1health'] <= 0 or playerdata[f'p2'][f'p2health'] <= 0:
        with open('players_info.json', 'w') as f:
            json.dump(playerdata, f)
        pygame.quit()
        subprocess.run(["C:\\Program Files\\Python312\\python.exe", "fight.py"])
        subprocess.run(["C:\\Program Files\\Python312\\python.exe", "results.py"])
        sys.exit()

    pygame.display.flip()
