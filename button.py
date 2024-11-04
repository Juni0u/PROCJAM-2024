import pygame

class Button():
    def __init__(self,x:int, y:int, w:int, h:int,active_color:tuple, inactive_color:tuple, text:str=""):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x,y,w,h)
        self.text = text
        self.active_color = active_color
        self.inactive_color = inactive_color
        self.color = self.inactive_color
        self.active = False
        self.font = pygame.font.Font(None,15)

    def update(self,events):
        if self.active: self.color = self.active_color
        else: self.color = self.inactive_color

    def draw(self,canvas):
        pygame.draw.rect(canvas,self.color,self.rect)
        if self.text:
            text = self.font.render(f"{self.text}", True, (0,0,0))
            canvas.blit(text,(self.rect.x+1,self.rect.y+1))
        return canvas

    def toogle(self):
        if self.active: self.active = False
        else: self.active = True


