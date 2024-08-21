import pygame
import sys
import json

# Import player data
with open('players_info.json', 'r') as f:
    playerdata = json.load(f)

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
BACKGROUND_COLOR = (240, 240, 240)

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)  # Zmniejszona czcionka dla legendy
tiny_font = pygame.font.Font(None, 20)

# Screen dimensions
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 500

# Items in the shop with categories
items = {
    "Health Potion": 50,
    "T1 Leather Cap (HE)": 20,
    "T1 Leather Armor (CH)": 40,
    "T1 Leather Boots (BO)": 15,
    "T1 Leather Gloves (GL)": 10,
    "T1 Wooden Sword (RH)": 30,
    "T1 Wooden Club (TH)": 50,
    "T1 Wooden Shield (LH)": 25,
    "T2 Iron Helm (HE)": 50,
    "T2 Iron Chestplate (CH)": 100,
    "T2 Iron Boots (BO)": 40,
    "T2 Iron Gauntlets (GL)": 30,
    "T2 Iron Sword (RH)": 80,
    "T2 Iron Axe (TH)": 120,
    "T2 Iron Shield (LH)": 60,
    "T3 Steel Helm (HE)": 100,
    "T3 Steel Plate (CH)": 200,
    "T3 Steel Boots (BO)": 80,
    "T3 Steel Gauntlets (GL)": 60,
    "T3 Steel Sword (RH)": 150,
    "T3 Steel Greatsword (TH)": 250,
    "T3 Steel Shield (LH)": 120,
    "T4 Mithril Helm (HE)": 200,
    "T4 Mithril Chestplate (CH)": 400,
    "T4 Mithril Boots (BO)": 150,
    "T4 Mithril Gauntlets (GL)": 120,
    "T4 Mithril Sword (RH)": 300,
    "T4 Mithril Warhammer (TH)": 500,
    "T4 Mithril Shield (LH)": 240,
    "T5 Dragonbone Helm (HE)": 500,
    "T5 Dragonbone Armor (CH)": 1000,
    "T5 Dragonbone Boots (BO)": 400,
    "T5 Dragonbone Gauntlets (GL)": 300,
    "T5 Dragonbone Sword (RH)": 800,
    "T5 Dragonbone Halberd (TH)": 1500,
    "T5 Dragonbone Shield (LH)": 600
}

item_stats = {
    "T1 Wooden Sword (RH)": {"attack": 10, "defense": 0, "range": 2},
    "T1 Wooden Club (TH)": {"attack": 20, "defense": 0, "range": 3},
    "T1 Leather Cap (HE)": {"attack": 0, "defense": 5, "range": 0},
    "T1 Leather Armor (CH)": {"attack": 0, "defense": 10, "range": 0},
    "T1 Leather Boots (BO)": {"attack": 0, "defense": 3, "range": 0},
    "T1 Leather Gloves (GL)": {"attack": 0, "defense": 2, "range": 0},
    "T1 Wooden Shield (LH)": {"attack": 0, "defense": 8, "range": 0},
    "T2 Iron Sword (RH)": {"attack": 20, "defense": 0, "range": 2},
    "T2 Iron Axe (TH)": {"attack": 40, "defense": 0, "range": 3},
    "T2 Iron Helm (HE)": {"attack": 0, "defense": 10, "range": 0},
    "T2 Iron Chestplate (CH)": {"attack": 0, "defense": 20, "range": 0},
    "T2 Iron Boots (BO)": {"attack": 0, "defense": 6, "range": 0},
    "T2 Iron Gauntlets (GL)": {"attack": 0, "defense": 4, "range": 0},
    "T2 Iron Shield (LH)": {"attack": 0, "defense": 16, "range": 0},
    "T3 Steel Sword (RH)": {"attack": 30, "defense": 0, "range": 2},
    "T3 Steel Greatsword (TH)": {"attack": 60, "defense": 0, "range": 3},
    "T3 Steel Helm (HE)": {"attack": 0, "defense": 15, "range": 0},
    "T3 Steel Plate (CH)": {"attack": 0, "defense": 30, "range": 0},
    "T3 Steel Boots (BO)": {"attack": 0, "defense": 10, "range": 0},
    "T3 Steel Gauntlets (GL)": {"attack": 0, "defense": 6, "range": 0},
    "T3 Steel Shield (LH)": {"attack": 0, "defense": 24, "range": 0},
    "T4 Mithril Sword (RH)": {"attack": 40, "defense": 0, "range": 2},
    "T4 Mithril Warhammer (TH)": {"attack": 80, "defense": 0, "range": 3},
    "T4 Mithril Helm (HE)": {"attack": 0, "defense": 20, "range": 0},
    "T4 Mithril Chestplate (CH)": {"attack": 0, "defense": 40, "range": 0},
    "T4 Mithril Boots (BO)": {"attack": 0, "defense": 15, "range": 0},
    "T4 Mithril Gauntlets (GL)": {"attack": 0, "defense": 10, "range": 0},
    "T4 Mithril Shield (LH)": {"attack": 0, "defense": 32, "range": 0},
    "T5 Dragonbone Sword (RH)": {"attack": 60, "defense": 0, "range": 2},
    "T5 Dragonbone Halberd (TH)": {"attack": 120, "defense": 0, "range": 3},
    "T5 Dragonbone Helm (HE)": {"attack": 0, "defense": 30, "range": 0},
    "T5 Dragonbone Armor (CH)": {"attack": 0, "defense": 60, "range": 0},
    "T5 Dragonbone Boots (BO)": {"attack": 0, "defense": 25, "range": 0},
    "T5 Dragonbone Gauntlets (GL)": {"attack": 0, "defense": 20, "range": 0},
    "T5 Dragonbone Shield (LH)": {"attack": 0, "defense": 40, "range": 0}
}

# Legend for item types
legend = {
    "HE": "Helmet",
    "CH": "Chest",
    "BO": "Boots",
    "GL": "Gloves",
    "RH": "Right Hand",
    "LH": "Left Hand",
    "TH": "Two-Handed",
}

def draw_text(surface, text, pos, font, color=BLACK):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, pos)

def itemtype(legend):
    if legend == "(HE)":
        return "helmet"
    elif legend == "(CH)":
        return "chest"
    elif legend == "(BO)":
        return "boots"
    elif legend == "(GL)":
        return "gloves"
    elif legend == "(RH)":
        return "rhand"
    elif legend == "(LH)":
        return "lhand"
    else:
        return ["rhand", "B"]

# Function after buy health potion
def apply_health_potion(player):
    player["health"] += 50

# Function to reset player's stats before applying new equipment stats
def reset_item_stats(player, item_type):
    # Reset stats based on the item type
    if item_type == "RH":
        # Reset right-hand weapon stats
        if player["items"]["rhand"] != 0:
            item_stat = item_stats.get(player["items"]["rhand"], {"attack": 0, "defense": 0, "range": 1})
            player["attack"] -= item_stat["attack"]
            player["range"] = 1  # Default range without a weapon
    elif item_type == "LH":
        # Reset left-hand shield stats
        if player["items"]["lhand"] != 0:
            item_stat = item_stats.get(player["items"]["lhand"], {"attack": 0, "defense": 0, "range": 0})
            player["defense"] -= item_stat["defense"]
    elif item_type == "TH":
        # Reset two-handed weapon stats
        if player["items"]["rhand"] != 0:
            item_stat = item_stats.get(player["items"]["rhand"], {"attack": 0, "defense": 0, "range": 1})
            player["attack"] -= item_stat["attack"]
            player["range"] = 1  # Default range without a weapon
            player["items"]["rhand"] = 0  # Remove the two-handed weapon
        if player["items"]["lhand"] != 0:
            player["items"]["lhand"] = 0  # Remove anything in the left hand
    else:
        # Reset armor stats (HE, CH, BO, GL)
        armor_piece = {
            "HE": "helmet",
            "CH": "chest",
            "BO": "boots",
            "GL": "gloves"
        }[item_type]
        if player["items"][armor_piece] != 0:
            item_stat = item_stats.get(player["items"][armor_piece], {"attack": 0, "defense": 0, "range": 0})
            player["defense"] -= item_stat["defense"]


# Function to apply new item stats to the player
def apply_item_stats(player, item_key):
    item_type = item_key[-3:-1]  # Extract item type (RH, LH, HE, etc.)
    reset_item_stats(player, item_type)

    item_stat = item_stats.get(item_key, {"attack": 0, "defense": 0, "range": 1})

    # Apply the new stats
    if item_type == "RH":
        player["attack"] += item_stat["attack"]
        player["range"] = item_stat["range"]
        player["items"]["rhand"] = item_key  # Save current weapon type
    elif item_type == "LH":
        player["defense"] += item_stat["defense"]
        player["items"]["lhand"] = item_key  # Save current shield type
    elif item_type == "TH":
        player["attack"] += item_stat["attack"]
        player["range"] = item_stat["range"]
        player["items"]["rhand"] = item_key  # Save current two-handed weapon type
        player["items"]["lhand"] = 0  # Clear left-hand for two-handed weapon
    else:
        armor_piece = {
            "HE": "helmet",
            "CH": "chest",
            "BO": "boots",
            "GL": "gloves"
        }[item_type]
        player["defense"] += item_stat["defense"]
        player["items"][armor_piece] = item_key  # Save current armor type

def shop(money):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Shop")

    item_rects = []
    item_height = 60
    legend_height = 100  # Adjusted for smaller font
    total_items_height = len(items) * item_height
    visible_items_height = SCREEN_HEIGHT - 100 - legend_height  # Adjusted for legend height
    scroll_offset = 0
    max_scroll = max(0, total_items_height - visible_items_height)

    scrollbar_rect = pygame.Rect(470, 100 + legend_height, 20, visible_items_height)
    scrollbar_dragging = False

    running = True
    while running:
        screen.fill(BACKGROUND_COLOR)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    if scrollbar_rect.collidepoint(event.pos):
                        scrollbar_dragging = True
                        mouse_y = event.pos[1]
                        start_scroll_offset = scroll_offset
                    else:
                        for rect, item, price in item_rects:
                            if rect.collidepoint(event.pos) and 100 + legend_height <= rect.y <= SCREEN_HEIGHT - 50:
                                if money >= price:
                                    money -= price
                                    if item == "Health Potion":
                                        if playerdata['turn'] == 2:
                                            apply_health_potion(playerdata['p1'])
                                            playerdata['p1']['money'] = money
                                        else:
                                            apply_health_potion(playerdata['p2'])
                                            playerdata['p2']['money'] = money
                                    else:
                                        type = itemtype(item[-4:])
                                        if playerdata['turn'] == 2:
                                            apply_item_stats(playerdata['p1'], item)
                                            if type[1] == "B":
                                                playerdata['p1']['items']['rhand'] = item[0:2]
                                                playerdata['p1']['items']['lhand'] = 'B'
                                            else:
                                                playerdata['p1']['items'][f'{type}'] = item[0:2]
                                            playerdata['p1']['money'] = money
                                        else:
                                            apply_item_stats(playerdata['p2'], item)
                                            if type[1] == "B":
                                                playerdata['p2']['items']['rhand'] = item[0:2]
                                                playerdata['p2']['items']['lhand'] = 'B'
                                            else:
                                                playerdata['p2']['items'][f'{type}'] = item[0:2]
                                            playerdata['p2']['money'] = money
                                    with open('players_info.json', 'w') as f:
                                        json.dump(playerdata, f)
            elif event.type == pygame.MOUSEBUTTONUP:
                scrollbar_dragging = False
            elif event.type == pygame.MOUSEMOTION:
                if scrollbar_dragging:
                    dy = event.pos[1] - mouse_y
                    scroll_offset = max(0, min(max_scroll, start_scroll_offset + dy * total_items_height / visible_items_height))

        # Update the position of the scrollbar
        if max_scroll > 0:
            scrollbar_rect.y = 100 + legend_height + int((scroll_offset / total_items_height) * visible_items_height)

        # Draw fixed money display
        draw_text(screen, f"Money: {money}", (50, 10), font)

        # Draw legend just above the items
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 50, SCREEN_WIDTH, legend_height))  # Unified background for legend
        y_offset = 60
        for key, value in legend.items():
            draw_text(screen, f"{key}: {value}", (50, y_offset), tiny_font)
            y_offset += 20

        # Draw items with scrolling
        pygame.draw.rect(screen, BACKGROUND_COLOR, (0, 100 + legend_height, SCREEN_WIDTH, SCREEN_HEIGHT - 100 - legend_height))  # Unified background
        item_rects.clear()
        for i, (item, price) in enumerate(items.items()):
            rect = pygame.Rect(50, 100 + legend_height + i * item_height - scroll_offset, 400, 50)
            item_rects.append((rect, item, price))

        for rect, item, price in item_rects:
            if 100 + legend_height <= rect.y <= SCREEN_HEIGHT - 50:  # Only draw items that are within the visible area
                pygame.draw.rect(screen, GREEN if money >= price else RED, rect)
                draw_text(screen, f"{item}: {price} Gold", (rect.x + 10, rect.y + 10), small_font)

        # Draw the scrollbar
        if max_scroll > 0:
            pygame.draw.rect(screen, GRAY, scrollbar_rect)

        pygame.display.flip()

    return money

if __name__ == "__main__":
    if playerdata['turn'] == 2:
        money = playerdata['p1']['money']
    else:
        money = playerdata['p2']['money']
    new_money = shop(money)
    sys.exit(new_money)
