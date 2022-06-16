import pygame

pygame.font.init()

DISPLAY_FONT = pygame.font.SysFont(None, 30)


def debug(info, x_pos=10, y_pos=10):
    display_surface = pygame.display.get_surface()
    debug_info = DISPLAY_FONT.render(str(info), True, 'White')
    debug_rect = debug_info.get_rect(topleft=(x_pos, y_pos))
    display_surface.blit(debug_info, debug_rect)
    pygame.display.update()
