import pygame
from constants import BLACK
from apple import Apple
from player import BowAndArrow


def main():
    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    clock = pygame.time.Clock()
    last_update = pygame.time.get_ticks()

    running = True
    delta_time = 0

    # Textures
    # SpriteGroups
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()

    # Initialize Player
    player_position = (screen.get_rect().centerx, screen.get_rect().bottom - 128)
    player = BowAndArrow(player_group, player_position)

    # Initialize Enemies
    apple_spawn_position = (screen.get_rect().left - 128, 200)
    apple = Apple(enemy_group, apple_spawn_position)

    # Game Loop
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        delta_time = clock.tick(60) / 1000

        # Updates
        player_group.update(delta_time)
        enemy_group.update(delta_time, screen)

        # Draw
        # R , G, B
        screen.fill(BLACK)
        player_group.draw(screen)
        enemy_group.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
