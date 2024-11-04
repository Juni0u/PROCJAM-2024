import pygame

class TextBox():
    def __init__(self,x:int, y:int, w:int, h:int,active_color:tuple, inactive_color:tuple):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x,y,w,h)
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.active = False

    def update(self):
        if self.active: self.color = self.active_color
        else: self.color = self.inactive_color

    def draw(self,canvas):
        pygame.draw.rect(canvas,self.color,self.rect)

        return canvas