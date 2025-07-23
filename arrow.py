import pygame
from constants import BLACK


class Arrow(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        texture = pygame.image.load("assets/Arrows.png").convert_alpha()
        img = pygame.Surface((32, 32)).convert_alpha()
        img.blit(texture, (0, 0), pygame.Rect(0, 0, 32, 32))
        img = pygame.transform.rotate(img, -45).convert_alpha()
        img = pygame.transform.scale(img, (128, 256))
        img.set_colorkey(BLACK)
        self.image = img

        self.rect = self.image.get_rect(topleft=pos)
        self.last_update = pygame.time.get_ticks()

        self.speed = 600

    def update(self, *args, **kwargs):
        delta_time = args[0] if args else 0

        self.rect.y = self.rect.y - self.speed * delta_time
        if self.rect.y < -128:
            self.kill()
