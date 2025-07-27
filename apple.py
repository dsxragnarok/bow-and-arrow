import pygame
import math
from random import randint
from constants import ORIGIN, BLACK, FRAME_WIDTH, FRAME_HEIGHT
from utils import red_flash_image
HURT_ANIM_TIME_MS = 1000
HURT_FLASH_INTERVAL_MS = 100
DEATH_ANIM_TIME_MS = 1000
ANIM_DURATION_MS = 50
ANIM_FRAMES = 8


class Apple(pygame.sprite.Sprite):
    def __init__(
        self,
        group,
        pos,
        spritesheet,
        die_img,
        size=(FRAME_WIDTH, FRAME_HEIGHT),
        health=3,
        speed=900,
        bonus=1
    ):
        super().__init__(group)

        self.spritesheet = spritesheet
        self.normalsheet = spritesheet
        self.flashsheet = red_flash_image(spritesheet)

        self.size = size

        self.cur_frame_idx = 0
        self.last_anim_update_tm = 0

        self.die_img = die_img
        self.image = self.get_frame(self.cur_frame_idx, self.size)

        self.rect = self.image.get_rect(topleft=pos)

        self.speed = speed
        self.health = health
        self.bonus = bonus

        # Death animation control
        self.dying = False
        self.dying_start_tm = 0

        # Hurt animation control
        self.hurt_start_tm = 0
        self.last_flash_tm = 0
        self.flashing = False

    def get_frame(self, idx: int, size):
        frame = pygame.Surface((FRAME_WIDTH, FRAME_HEIGHT))
        columns = ANIM_FRAMES / 2
        x = idx % columns
        y = math.floor(self.cur_frame_idx / columns)
        frame.blit(self.spritesheet, ORIGIN, (x * FRAME_WIDTH, y * FRAME_HEIGHT, FRAME_WIDTH, FRAME_HEIGHT))
        frame = pygame.transform.scale(frame, size)
        frame.set_colorkey(BLACK)

        return frame

    def update(self, *args, **kwargs):
        delta_time = args[0] if args else 0
        screen = args[1]

        current_time = pygame.time.get_ticks()
        if self.dying:
            if current_time - self.dying_start_tm >= DEATH_ANIM_TIME_MS:
                self.kill()
        else:
            if (self.flashing and current_time - self.hurt_start_tm
                    < HURT_ANIM_TIME_MS):
                if current_time - self.last_flash_tm >= HURT_FLASH_INTERVAL_MS:
                    self.spritesheet = self.flashsheet if self.spritesheet == self.normalsheet else self.normalsheet
                    self.last_flash_tm = current_time
            else:
                self.spritesheet = self.normalsheet
                self.flashing = False

            if current_time - self.last_anim_update_tm >= ANIM_DURATION_MS:
                self.cur_frame_idx = (self.cur_frame_idx + 1) % ANIM_FRAMES
                self.image = self.get_frame(self.cur_frame_idx, self.size)
                self.last_anim_update_tm = current_time
    
        self.rect.x = self.rect.x + self.speed * delta_time
        if self.rect.x >= screen.get_rect().right + 128:
            self.rect.x = screen.get_rect().left - 128
            self.rect.y = randint(0, 400)

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
