import pygame
from constants import WHITE


class BowAndArrow(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        img = pygame.surface.Surface((64, 64)).convert_alpha()
        img.fill(WHITE)
        self.image = img

        self.last_update = pygame.time.get_ticks()

        self.speed = 300

    def update(self, delta_time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * delta_time
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * delta_time
