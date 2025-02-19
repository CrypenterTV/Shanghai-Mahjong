# Example file showing a circle moving on screen
import pygame

WIDTH = 1000;
HEIGHT = 1000;

s_offset = 10

grid = [ [  [0, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1] ],

         [  [0, 1, 1, 0, 1, 0],
            [0, 1, 1, 0, 1, 1],
            [1, 1, 1, 1, 1, 0] ],

         [  [0, 1, 0, 0, 1, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 0, 1, 1, 0] ], 

         [  [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 1, 0],
            [0, 0, 0, 1, 1, 0] ] ]

def draw_card(x, y):


    card_width = 100;
    card_height = 160;

    points = [(x - s_offset, y + s_offset), (x, y), (x, y + card_height), (x + card_width, y + card_height), (x + card_width - s_offset, y + card_height + s_offset), (x - s_offset, y + card_height + s_offset)]
    pygame.draw.polygon(screen, shadow_color, points, width=0)


    card_rect = pygame.Rect(x, y, card_width, card_height)
    pygame.draw.rect(screen, "white", card_rect, width=0, border_radius=2);

    pygame.draw.line(screen, "black", card_rect.topleft, card_rect.topright, width = 1);
    pygame.draw.line(screen, "black", card_rect.topright, card_rect.bottomright, width = 1);


    pygame.draw.line(screen, "black", points[0], points[1], width = 1);
    pygame.draw.line(screen, "black", points[3], points[4], width = 1);
    pygame.draw.line(screen, "black", points[4], points[5], width = 1);
    pygame.draw.line(screen, "black", points[5], points[0], width = 1);



shadow_color = (219, 219, 219)

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((75, 89, 216))

    x_start = 150
    y_start = 500

    for level in range(len(grid)):

        for i in range(len(grid[level])):

            for j in range(len(grid[level][i]) - 1, -1, -1):


                if grid[level][i][j] == 0:
                    continue
            

                draw_card(x_start + j * 100 + level * (s_offset ), y_start - (len(grid[level]) - i - 1) * 160 - level * (s_offset ))

    pygame.display.flip()

    dt = clock.tick(60) / 1000

pygame.quit()