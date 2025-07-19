import pygame
from constants import RED


class Apple(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        img = pygame.Surface((64, 64)).convert_alpha()
        img.fill(RED)
        self.image = img

        self.rect = self.image.get_rect(topleft=pos)
        self.last_update = pygame.time.get_ticks()

        self.speed = 300

    def update(self, *args, **kwargs):
        delta_time = args[0] if args else 0
        screen = args[1]

        self.rect.x = self.rect.x + self.speed * delta_time
        if self.rect.x >= screen.get_rect().right + 128:
            self.rect.x = screen.get_rect().left - 128
