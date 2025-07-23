from random import randint
import pygame
from constants import (
    BLACK,
    SKY_BLUE,
    YELLOW,
    GREY,
    SHOOT_COOLDOWN_MS,
    MAX_NUM_FOES,
    FOES_SPAWN_COOLDOWN_MS
)
from apple import Apple
from player import Bow
from arrow import Arrow


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
    # SpriteGroups
    player_group = pygame.sprite.Group()
    enemy_group = pygame.sprite.Group()
    projectile_group = pygame.sprite.Group()

    # Initialize Player
    player_position = (
        screen.get_rect().centerx, screen.get_rect().bottom - 256
    )
    player = Bow(player_group, player_position)

    # Initialize Enemies
    apple_spawn_position = (screen.get_rect().left - 128, 200)
    Apple(enemy_group, apple_spawn_position)

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
            Arrow(projectile_group, (player.rect.left + 64, player.rect.top + 128))
            last_shoot_update = current_time

        spawn_delta_time = current_time - last_spawn_update
        if (len(enemy_group) < MAX_NUM_FOES and
                spawn_delta_time > FOES_SPAWN_COOLDOWN_MS):
            Apple(enemy_group, (screen.get_rect().left - 128, randint(0, 400)))
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
        player_group.draw(screen)
        enemy_group.draw(screen)
        projectile_group.draw(screen)

        pygame.draw.line(screen, GREY, (0, 0),
                         screen.get_rect().topright, 32)
        pygame.draw.line(screen, GREY, (0, 464),
                         (screen.get_rect().right, 464), 16)
        score_text = font.render(f"Score: {score}", True, YELLOW)
        score_rect = score_text.get_rect(
            bottomleft=(64, screen.get_height() - 32))
        screen.blit(score_text, score_rect)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
