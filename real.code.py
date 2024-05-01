import pygame
import sys
import random

pygame.init()

# Window:
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shagai Games")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_GREEN = (0, 200, 0)
DARK_RED = (200, 0, 0)
font = pygame.font.Font(None, 36)

main_menu_background = pygame.transform.scale(pygame.image.load("main_menu_background.jpg"), (WIDTH, HEIGHT))
games_background = pygame.transform.scale(pygame.image.load("game_background.png"), (WIDTH, HEIGHT))

player1_score = 0
player2_score = 0
current_player = 1

SHAGAI_SIZE = (60, 45)
SHAGAI_POSITIONS = [
   (WIDTH / 2 - 150, HEIGHT / 2 - 50),
   (WIDTH / 2 - 50, HEIGHT / 2 - 50),
   (WIDTH / 2 + 50, HEIGHT / 2 - 50),
   (WIDTH / 2 + 150, HEIGHT / 2 - 50)
]
shagai_images = [
   pygame.transform.scale(pygame.image.load("Mori.jpeg"), SHAGAI_SIZE),
   pygame.transform.scale(pygame.image.load("Temee.jpeg"), SHAGAI_SIZE),
   pygame.transform.scale(pygame.image.load("Ymaa.jpeg"), SHAGAI_SIZE),
   pygame.transform.scale(pygame.image.load("Honi.jpeg"), SHAGAI_SIZE)
]

def draw_text_centered(text, font, color, x, y):
   text_surface = font.render(text, True, color)
   text_rect = text_surface.get_rect(center=(x, y))
   window.blit(text_surface, text_rect)

def button(text, x, y, width, height, inactive_color, active_color, action=None):
   mouse = pygame.mouse.get_pos()
   click = pygame.mouse.get_pressed()
   rect = pygame.Rect(x, y, width, height)
   pygame.draw.rect(window, active_color if rect.collidepoint(mouse) else inactive_color, rect)
   draw_text_centered(text, font, BLACK, x + width / 2, y + height / 2)
   if rect.collidepoint(mouse) and click[0] == 1:
       pygame.time.wait(200)  # Delay to prevent multiple activations
       if action:
           action()

def display_game_state(shagais, score1, score2, turn_message):
   window.blit(games_background, (0, 0))
   for i, shagai in enumerate(shagais):
       window.blit(shagai_images[shagai], SHAGAI_POSITIONS[i])
   draw_text_centered(f"Player 1 Score: {score1}", font, RED, WIDTH / 2, 30)
   draw_text_centered(f"Player 2 Score: {score2}", font, RED, WIDTH / 2, HEIGHT - 50)
   draw_text_centered(turn_message, font, DARK_RED, WIDTH / 2, HEIGHT / 2 + 100)
   pygame.display.update()


def calculate_score(shagais):
    score = 0
    
    if all(shagai == 0 for shagai in shagais):
        score += 8  # All horses
    elif all(shagai == 1 for shagai in shagais):
        score += 4  # All camels
    elif all(shagai == 2 for shagai in shagais):
        score += 4  # All goats
    elif all(shagai == 3 for shagai in shagais):
        score += 4  # All sheep
    elif len(set(shagais)) == 4:
        score += 8  # Four different shagais
    elif len(set(shagais)) == 2:
        score += 2  # Two pairs of the same shagais
    
    return score

def play_turn():
   global player1_score, player2_score, current_player
   shagais = [random.randint(0, 3) for _ in range(4)]
   score = calculate_score(shagais)
   turn_message = f"Rolled: {', '.join([['Horse', 'Camel', 'Goat', 'Sheep'][s] for s in shagais])} - Scored: {score} points"
   
   if current_player == 1:
       player1_score += score
       if player1_score > 32:
           turn_message += f" - Player 1 returns to 0 with {player1_score} points"
           player1_score = 0
       display_game_state(shagais, player1_score, player2_score, turn_message)
       if player1_score == 32:
           turn_message = "Player 1 wins! Click to play again."
           end_game(shagais, turn_message)
           current_player = 1  # Reset to player 1 for new game
   else:
       player2_score += score
       if player2_score > 32:
           turn_message += f" - Player 2 returns to 0 with {player2_score} points"
           player2_score = 0
       display_game_state(shagais, player1_score, player2_score, turn_message)
       if player2_score == 32:
           turn_message = "Player 2 wins! Click to play again."
           end_game(shagais, turn_message)
           current_player = 1  # Reset to player 1 for new game
   current_player = 2 if current_player == 1 else 1  # Toggle players


def end_game(shagais, turn_message):
   global player1_score, player2_score
   display_game_state(shagais, player1_score, player2_score, turn_message)
   pygame.time.wait(4000)  # Wait a bit before restarting
   player1_score = 0
   player2_score = 0
   show_game_choice()


def show_game_choice():
   while True:
       window.blit(main_menu_background, (0, 0))
       button("Play Shagai", WIDTH / 2 - 100, HEIGHT / 3, 200, 50, LIGHT_GREEN, GREEN, play_game)
       button("Ask Questions", WIDTH / 2 - 100, HEIGHT / 2, 200, 50, LIGHT_GREEN, GREEN, lambda: ask_questions([]))
       pygame.display.update()
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()


def play_game():
   display_game_state([], player1_score, player2_score, "Player 1's turn, roll the shagai!")
   running = True
   while running:
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               pygame.quit()
               sys.exit()
       button("Roll Shagai", WIDTH / 2 - 100, HEIGHT - 150, 200, 50, LIGHT_GREEN, GREEN, play_turn)
       pygame.display.update()

def roll_shagais():
    shagais = [random.randint(0,3) for _ in range(4)]
    return shagais

def draw_shagais(shagais):
    for i, shagai in enumerate(shagais):
        x = 150 * i + 100
        y = HEIGHT // 2 - 50
        window.blit(shagai_images[shagai], (x, y))
        text = "".format(i+1)
        draw_text_centered(text, font, BLACK, x + 40, y + 100)

def ask_questions(shagais):
    window.blit(games_background, (0, 0))
    print("Asking questions...")
    rolled_shagais = roll_shagais()
    draw_shagais(rolled_shagais)
    shagais = rolled_shagais
    text = ""
    if shagais.count(0) == 4:
        text = "the best portent appears"
    elif shagais.count(1) == 4:
        text = "everything will be successful"
    elif shagais.count(2) == 4:
        text = "it will be kept long in other's hands"
    elif shagais.count(3) == 4:
        text = "everlasting luck"
    elif len(set(shagais)) == 4:
        text = "the best of fortune"
    elif shagais.count(0) == 3 and shagais.count(1) == 1:
        text = "one will come or come back soon"
    elif shagais.count(0) == 3 and shagais.count(3) == 1:
        text = "without any obstacles"
    elif shagais.count(0) == 3 and shagais.count(2) == 1:
        text = "evenly good"
    elif shagais.count(0) == 2 and shagais.count(1) == 1 and shagais.count(3) == 1:
        text = "with luck and happiness"
    elif shagais.count(0) == 2 and shagais.count(1) == 1 and shagais.count(2) == 1:
        text = "good and beneficient"
    elif shagais.count(0) == 2 and shagais.count(2) == 1 and shagais.count(3) == 1:
        text = "good and without any difficulties"
    elif shagais.count(0) == 2 and shagais.count(1) == 2:
        text = "work and deeds will be successes"
    elif shagais.count(0) == 2 and shagais.count(2) == 2:
        text = "without success"
    elif shagais.count(0) == 2 and shagais.count(3) == 2:
        text = "no difficulties"
    elif shagais.count(0) == 1 and shagais.count(1) == 3:
        text = "fortunate on your side"
    elif shagais.count(0) == 1 and shagais.count(2) == 3:
        text = "something will cause difficulties"
    elif shagais.count(0) == 1 and shagais.count(3) == 3:
        text = "happy for long time, good for you"
    elif shagais.count(0) == 1 and shagais.count(1) == 2 and shagais.count(3) == 1:
        text = "more to come"
    elif shagais.count(0) == 1 and shagais.count(1) == 1 and shagais.count(3) == 2:
        text = "someone will bring news to you"
    elif shagais.count(0) == 1 and shagais.count(1) == 1 and shagais.count(2) == 2:
        text = "successful"
    elif shagais.count(0) == 1 and shagais.count(2) == 1 and shagais.count(3) == 2:
        text = "you will hear good news"
    elif shagais.count(0) == 1 and shagais.count(1) == 2 and shagais.count(2) == 1:
        text = "your work and deeds will be done without any obstacles"
    elif shagais.count(1) == 2 and shagais.count(2) == 1 and shagais.count(3) == 1:
        text = "good business"
    elif shagais.count(1) == 2 and shagais.count(3) == 2:
        text = "with kindest part on your side"
    elif shagais.count(1) == 2 and shagais.count(2) == 2:
        text = "very misfortunate or dull"
    elif shagais.count(1) == 1 and shagais.count(2) == 1 and shagais.count(3) == 2:
        text = "without any success and decision so you must try well"
    elif shagais.count(1) == 1 and shagais.count(2) == 2 and shagais.count(3) == 1:
        text = "fortunate on other's side"
    elif shagais.count(1) == 1 and shagais.count(3) == 3:
        text = "unsuccessful"
    elif shagais.count(1) == 1 and shagais.count(2) == 3:
        text = "one's thought and idea is bad"
    elif shagais.count(2) == 1 and shagais.count(3) == 3:
        text = "other's power will win"
    elif shagais.count(2) == 2 and shagais.count(3) == 2:
        text = "generally with much obstacles and difficulties"
    elif shagais.count(2) == 3 and shagais.count(3) == 1:
        text = "your work and deeds won't have any success"
    draw_text_centered(text, font, BLACK, WIDTH / 2, HEIGHT / 2 + 150)
    button("Roll Again", 230, HEIGHT / 2 + 200, 150, 50, GREEN, (0, 200, 0), lambda: ask_questions([]))
    button("Back to Menu", 430, HEIGHT / 2 + 200, 150, 50, GREEN, (0, 200, 0), show_game_choice)
    button_area_roll_again = pygame.Rect(230, HEIGHT / 2 + 200, 150, 50)
    button_area_back_to_menu = pygame.Rect(430, HEIGHT / 2 + 200, 150, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_area_roll_again.collidepoint(event.pos):
                    ask_questions([])
                elif button_area_back_to_menu.collidepoint(event.pos):
                    show_game_choice()
        pygame.display.update()

if __name__ == "__main__":
   show_game_choice()
