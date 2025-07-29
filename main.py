from constants import BLACK
from random import randint
import pygame
from constants import (
    ORIGIN,
    SKY_BLUE,
    DARK_CYAN,
    YELLOW,
    SHOOT_COOLDOWN_MS,
    MAX_NUM_FOES,
    FOES_SPAWN_COOLDOWN_MS
)
from fruit import Fruit
from bow import Bow
from arrow import Arrow
from utils import red_flash_image


def main():
    pygame.init()

    screen = pygame.display.set_mode((1280, 720))
    font = pygame.font.SysFont(None, 48)
    clock = pygame.time.Clock()
    last_shoot_update = pygame.time.get_ticks()
    last_spawn_update = pygame.time.get_ticks()

    running = True
    delta_time = 0

    score = 0

    # Textures
    atlas = pygame.image.load("assets/atlas.png").convert_alpha()
    fruit_atlas = pygame.image.load("assets/garrison-fruit-atlas.png").convert_alpha()

    bow_texture = pygame.Surface((32, 32))
    bow_texture.blit(atlas, ORIGIN, (0, 0, 32, 32))
    bow_texture.set_colorkey(BLACK)
    bow_texture = pygame.transform.scale(bow_texture, (128, 128))

    arrow_texture = pygame.Surface((32, 32))
    arrow_texture.blit(atlas, ORIGIN, (64, 32, 32, 32))
    arrow_texture.set_colorkey(BLACK)
    arrow_texture = pygame.transform.scale(arrow_texture, (64, 128))

    # Setup Apple
    apple_sheet = pygame.Surface((128, 64))
    apple_sheet.blit(atlas, ORIGIN, (0, 64, 128, 64))

    apple_die_tx = pygame.Surface((32, 32))
    apple_die_tx.blit(atlas, ORIGIN, (96, 32, 32, 32))
    apple_die_tx.set_colorkey(BLACK)

    apple_die_textures = [
        pygame.transform.scale(apple_die_tx, (64, 64)).convert_alpha(),
        pygame.transform.scale(apple_die_tx, (128, 128)).convert_alpha(),
    ]

    # Setup Orange
    orange_sheet = pygame.Surface((128, 64))
    orange_sheet.blit(fruit_atlas, ORIGIN, (0, 64, 128, 64))

    orange_die_tx = pygame.Surface((32, 32))
    orange_die_tx.blit(fruit_atlas, ORIGIN, (0, 64, 32, 32))
    orange_die_tx.set_colorkey(BLACK)

    # Setup Watermelon
    watermelon_sheet = pygame.Surface((128, 64))
    watermelon_sheet.blit(fruit_atlas, ORIGIN, (0, 0, 128, 64))

    watermelon_die_tx = pygame.Surface((32, 32))
    watermelon_die_tx.blit(fruit_atlas, ORIGIN, (0, 0, 32, 32))
    watermelon_die_tx.set_colorkey(BLACK)

    # hp: int, speed: int, bonus: int, size: Coordinate
    foes_stats = [
        (3, 900, 1, (64, 64), apple_sheet, apple_die_textures[0]),  # apple
        (6, 600, 3, (128, 128), apple_sheet, apple_die_textures[1]),  # big_apple
        (10, 500, 5, (64, 64), orange_sheet, orange_die_tx),  # orange
        (25, 200, 20, (96, 96), watermelon_sheet, watermelon_die_tx),  # watermelon
    ]

    # SpriteGroups
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    projectile_group = pygame.sprite.Group()

    # Initialize Player
    player_position = (
        screen.get_rect().centerx, screen.get_rect().bottom - 256
    )
    player = Bow(player_group, player_position, bow_texture)

    # Initialize Enemies
    apple_spawn_position = (screen.get_rect().left - 128, 200)
    Fruit(enemy_group, apple_spawn_position, apple_sheet, apple_die_textures[0], (64, 64))

    # Game Loop
    while running:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        delta_time = clock.tick(60) / 1000
        shoot_delta_time = current_time - last_shoot_update
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and shoot_delta_time > SHOOT_COOLDOWN_MS:
            Arrow(projectile_group, (player.rect.centerx - 32, player.rect.top), arrow_texture)
            last_shoot_update = current_time

        spawn_delta_time = current_time - last_spawn_update
        if (len(enemy_group) < MAX_NUM_FOES and
                spawn_delta_time > FOES_SPAWN_COOLDOWN_MS):
            idx = randint(0, 3)
            (hp, speed, bonus, size, spritesheet, die_tx) = foes_stats[idx]
            Fruit(enemy_group, (screen.get_rect().left - 128, randint(0, 400)), spritesheet, die_tx, size, hp, speed, bonus)
            last_spawn_update = current_time

        player_group.update(delta_time)
        enemy_group.update(delta_time, screen)
        projectile_group.update(delta_time, screen)

        collisions = pygame.sprite.groupcollide(
            projectile_group, enemy_group, True, False)
        for _, apples in collisions.items():
            for apple in apples:
                score += apple.take_damage()

        # Draw
        # R , G, B
        screen.fill(SKY_BLUE)
        pygame.draw.line(screen, DARK_CYAN, (0, 0),
                         screen.get_rect().topright, 960)

        player_group.draw(screen)
        enemy_group.draw(screen)
        projectile_group.draw(screen)

        score_text = font.render(f"Score: {score}", True, YELLOW)
        score_rect = score_text.get_rect(
            bottomleft=(64, screen.get_height() - 32))
        screen.blit(score_text, score_rect)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
