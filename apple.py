import pygame
from constants import RED


class Apple(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        img = pygame.surface.Surface((64, 64)).convert_alpha()
        img.fill(RED)
        self.image = img

        self.last_update = pygame.time.get_ticks()

        self.speed = 300

    def update(self, delta_time, screen):
        self.rect.x = self.rect.x + self.speed * delta_time
        if self.rect.x >= screen.get_rect().right + 128:
            self.rect.x = screen.get_rect().left - 128
