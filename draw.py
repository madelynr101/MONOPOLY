import pygame
from typing import Union

# Use to create and draw buttons using images
class Button:
    def __init__(self, x: int, y: int, image: pygame.surface.Surface, scale):
        self.image: pygame.surface.Surface = pygame.transform.scale(image, scale)
        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked: bool = False

    def draw(self, screen: pygame.surface.Surface) -> bool:
        action: bool = False

        pos: tuple[int, int] = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action


# Text draw function
def draw_text(
    screen: pygame.surface.Surface,
    text: str,
    font: pygame.font.Font,
    text_col: tuple[int, int, int],
    x: Union[int, float],
    y: Union[int, float],
) -> None:
    img: pygame.surface.Surface = font.render(text, True, text_col)
    screen.blit(img, (x, y))
