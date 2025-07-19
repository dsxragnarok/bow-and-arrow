import pygame
from constants import GREY


class Arrow(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        img = pygame.Surface((16, 64)).convert_alpha()
        img.fill(GREY)
        self.image = img

        self.rect = self.image.get_rect(topleft=pos)
        self.last_update = pygame.time.get_ticks()

        self.speed = 600

    def update(self, *args, **kwargs):
        delta_time = args[0] if args else 0

        self.rect.y = self.rect.y - self.speed * delta_time
        if self.rect.y < -128:
            self.kill()
