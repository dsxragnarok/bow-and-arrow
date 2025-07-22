import pygame


def create_flash_image(img):
    flash_img = img.copy()
    flash_overlay = pygame.Surface(img.get_size()).convert_alpha()
    flash_overlay.fill((255, 255, 255, 100))
    flash_img.blit(flash_overlay, (0, 0))

    return flash_img


def red_flash_image(surface):
    flash = surface.copy()
    px_array = pygame.PixelArray(flash)

    for y in range(flash.get_height()):
        for x in range(flash.get_width()):
            color = surface.unmap_rgb(px_array[x, y])
            r, g, b, a = color.r, color.g, color.b, color.a

            # Only flash red-ish pixels
            if r > 0 or g > 0 or b > 0:
            # if r > 150 and g < 100 and b < 100:
                px_array[x, y] = pygame.Color(255, 255, 255, 100)
            else:
                px_array[x, y] = pygame.Color(r, g, b, a)

    del px_array  # unlock the surface
    return flash
