import pygame

# Use to create and draw buttons using images
class Button:
    def __init__(self, x: int, y: int, image, scale):
        self.image = pygame.transform.scale(image, scale)
        self.rect = self.image.get_rect()
        self.rect.topleft: tuple[int, int] = (x, y)
        self.clicked: bool = False

    def draw(self, screen: pygame.display) -> bool:
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
def draw_text(screen: pygame.display, text: str, font: pygame.font, text_col: tuple[int, int, int], x: int, y: int) -> None:
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))