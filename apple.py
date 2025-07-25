import pygame
from random import randint
HURT_ANIM_TIME_MS = 1000
HURT_FLASH_INTERVAL_MS = 100
DEATH_ANIM_TIME_MS = 1000


class Apple(pygame.sprite.Sprite):
    def __init__(
        self,
        group,
        pos,
        normal_img,
        die_img,
        health=3,
        speed=900,
        bonus=1
    ):
        super().__init__(group)

        # save base img for transformations
        self.original_img = normal_img
        self.normal_img = normal_img
        self.die_img = die_img
        self.image = self.normal_img

        self.rect = self.image.get_rect(topleft=pos)
        self.last_update = pygame.time.get_ticks()

        self.speed = speed
        self.health = health
        self.bonus = bonus

        # Hurt animation control
        self.hurt_start_tm = 0
        self.last_flash_tm = 0
        self.flashing = False

        # Death animation control
        self.dying = False
        self.dying_start_tm = 0

        # Rotation
        self.angle = 0

    def update(self, *args, **kwargs):
        delta_time = args[0] if args else 0
        screen = args[1]

        current_time = pygame.time.get_ticks()
        if self.dying:
            if current_time - self.dying_start_tm >= DEATH_ANIM_TIME_MS:
                self.kill()
        elif (self.flashing and current_time - self.hurt_start_tm
                < HURT_ANIM_TIME_MS):
            if current_time - self.last_flash_tm >= HURT_FLASH_INTERVAL_MS:
                self.last_flash_tm = current_time
        else:
            self.image = self.normal_img
            self.flashing = False

        self.rect.x = self.rect.x + self.speed * delta_time
        if self.rect.x >= screen.get_rect().right + 128:
            self.rect.x = screen.get_rect().left - 128
            self.rect.y = randint(0, 400)

        # Rotation
        if not self.dying:
            self.angle += -180 * delta_time
            self.image = pygame.transform.rotate(self.original_img, self.angle)
            self.rect = self.image.get_rect(center=self.rect.center)

    def take_damage(self):
        self.health -= 1

        if self.dying:
            return 0
        elif self.health <= 0:
            self.image = self.die_img
            self.dying_start_tm = pygame.time.get_ticks()
            self.dying = True
            self.speed = 0
            return self.bonus
        else:
            self.flashing = True
            self.hurt_start_tm = pygame.time.get_ticks()
            self.last_flash_tm = self.hurt_start_tm
            return 0
