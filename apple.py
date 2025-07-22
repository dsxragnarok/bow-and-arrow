import pygame
from random import randint
from constants import WHITE
from utils import create_flash_image, red_flash_image
HURT_ANIM_TIME_MS = 1000
HURT_FLASH_INTERVAL_MS = 100


class Apple(pygame.sprite.Sprite):
    def __init__(self, group, pos):
        super().__init__(group)
        texture = (
            pygame.image.load("assets/apple.png", "apple").convert_alpha()
        )
        texture = pygame.transform.scale(texture, (64, 64)).convert_alpha()
        self.normal_img = texture

        self.flash_img = red_flash_image(texture)
        # self.flash_img = create_flash_image(texture)

        self.image = self.normal_img

        self.rect = self.image.get_rect(topleft=pos)
        self.last_update = pygame.time.get_ticks()

        self.speed = 300 + randint(0, 6) * 100
        self.health = 3

        # Hurt animation control
        self.hurt_start_tm = 0
        self.last_flash_tm = 0
        self.flashing = False

    def update(self, *args, **kwargs):
        delta_time = args[0] if args else 0
        screen = args[1]

        current_time = pygame.time.get_ticks()
        if (self.flashing and current_time - self.hurt_start_tm
                < HURT_ANIM_TIME_MS):
            if current_time - self.last_flash_tm >= HURT_FLASH_INTERVAL_MS:
                self.image = self.flash_img if self.image == self.normal_img \
                    else self.normal_img
                self.last_flash_tm = current_time
        else:
            self.image = self.normal_img
            self.flashing = False

        self.rect.x = self.rect.x + self.speed * delta_time
        if self.rect.x >= screen.get_rect().right + 128:
            self.rect.x = screen.get_rect().left - 128
            self.rect.y = randint(0, 400)

    def take_damage(self):
        self.health -= 1

        if self.health <= 0:
            self.kill()
            return 1
        else:
            self.flashing = True
            self.hurt_start_tm = pygame.time.get_ticks()
            self.last_flash_tm = self.hurt_start_tm
            return 0
