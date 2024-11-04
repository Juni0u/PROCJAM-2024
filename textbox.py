import pygame
POSSIBLE_KEYS = (pygame.K_0,pygame.K_1,pygame.K_2,pygame.K_3,pygame.K_4,pygame.K_5,pygame.K_6,pygame.K_7,pygame.K_8,pygame.K_9,
                 pygame.K_KP0,pygame.K_KP1,pygame.K_KP2,pygame.K_KP3,pygame.K_KP4,pygame.K_KP5,pygame.K_KP6,pygame.K_KP7,pygame.K_KP8,pygame.K_KP9)

class TextBox():
    def __init__(self,x:int, y:int, w:int, h:int,active_color:tuple, inactive_color:tuple):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x,y,w,h)
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.active = False
        self.font = pygame.font.Font(None,15)
        self.text = "255"
        self.text_color = (255,255,255)
        self.color_choice = int(self.text)

    def update(self,events):
        if self.active: 
            self.color = self.active_color
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1] 
                    elif (event.key in POSSIBLE_KEYS) and len(self.text) < 3:
                        self.text += event.unicode
                    if self.text == "": self.color_choice = 0
                    else:
                        self.color_choice = int(self.text)
                        if self.color_choice > 255: 
                            self.color_choice=255
                            self.text="255"
        else: 
            self.color = self.inactive_color
        

    def draw(self,canvas):
        pygame.draw.rect(canvas,self.color,self.rect)
        text = self.font.render(f"{self.text}", True, (255,255,255))
        canvas.blit(text,(self.rect.x+1,self.rect.y+1))
        return canvas