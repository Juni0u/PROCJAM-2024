import pygame

POSSIBLE_KEYS = (
    pygame.K_0,
    pygame.K_1,
    pygame.K_2,
    pygame.K_3,
    pygame.K_4,
    pygame.K_5,
    pygame.K_6,
    pygame.K_7,
    pygame.K_8,
    pygame.K_9,
    pygame.K_KP0,
    pygame.K_KP1,
    pygame.K_KP2,
    pygame.K_KP3,
    pygame.K_KP4,
    pygame.K_KP5,
    pygame.K_KP6,
    pygame.K_KP7,
    pygame.K_KP8,
    pygame.K_KP9,
)


class TextBox:
    def __init__(
        self, x: int, y: int, w: int, h: int, active_color: tuple, inactive_color: tuple, value_choice: int, role: str = "rgb"
    ):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, w, h)
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.active = False
        self.font = pygame.font.Font(None, 15)
        self.text_color = (255, 255, 255)
        self.role = role
        self.role_dict = self.make_role_dict()
        self.role = role
        self.value_choice = value_choice
        self.text = str(self.value_choice)

    def update(self, events):
        if self.active:
            self.color = self.active_color
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    elif (event.key in POSSIBLE_KEYS) and len(self.text) < self.role_dict[self.role]["max_len"]:
                        self.text += event.unicode

                    if self.text == "":
                        self.value_choice = 0
                    else:
                        self.value_choice = float(self.text)
                        if self.value_choice > self.role_dict[self.role]["max_value"]:
                            self.value_choice = self.role_dict[self.role]["max_value"]
                            self.text = str(self.role_dict[self.role]["max_value"])
        else:
            self.color = self.inactive_color

    def draw(self, canvas):
        pygame.draw.rect(canvas, self.color, self.rect)
        text = self.font.render(f"{self.text}", True, (255, 255, 255))
        canvas.blit(text, (self.rect.x + 1, self.rect.y + 1))
        return canvas

    def make_role_dict(self):
        role_dict = {"rgb": {"max_value": 255, "max_len": 3}, "probability": {"max_value": 100, "max_len": 2}}
        return role_dict
