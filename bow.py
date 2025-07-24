import pygame


class Bow(pygame.sprite.Sprite):
    def __init__(self, group, pos, texture):
        super().__init__(group)

        self.image = texture

        self.rect = self.image.get_rect(topleft=pos)
        self.last_update = pygame.time.get_ticks()

        self.speed = 300

    def update(self, *args, **kwargs):
        delta_time = args[0] if args else 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed * delta_time
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed * delta_time

        screen_width = pygame.display.get_surface().get_width()
        self.rect.x = max(0, min(self.rect.x, screen_width - self.rect.width))
