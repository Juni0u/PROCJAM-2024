import pygame, random
from CONS import SCREEN_DATA
from rgplant import RGPlant

class Game():
    def __init__(self,window_title:str="RGPlants"):
        self.configuration_start(window_title=window_title)
        self.plants_list = []
        #self.plants_list.append(RGPlant(63,63,(255,0,0)))

    def start_game(self):
        while not self.exit:
            self.exit = self.check_closed_window()

            self.update()
            self.before_draw()
            self.draw()
            self.update_screen()

    def update (self):
        new_plants = []
        marked_for_death = []
        random.shuffle(self.plants_list)
        self.mouse_pos = self.get_mouse_position()
        self.manage_mouse_clicks()

        #plants
        if self.plants_list:
            for plant in self.plants_list:
                death, new_plants = plant.update(self.plants_list)
                if death: marked_for_death.append(plant)

        if new_plants:
            for x,y,gene in new_plants:
                self.add_plant_to_position(x,y,gene)

        if marked_for_death:
            for plant in marked_for_death:
                self.plants_list.remove(plant)

    def draw (self):
        #plants
        for plant in self.plants_list:
            self.canvas = plant.draw(self.canvas)

        # font = pygame.font.Font(None,15)
        # plants_n = font.render(f"{len(self.plants_list)}",True, (255,0,255))
        # self.canvas.blit(plants_n,(5,5))


##############################################
##############################################
##############################################
##############################################
##############################################
    def before_draw(self):
        self.canvas.fill((0, 0, 0)) 

    def update_screen(self):
        #draw mouse
        self.canvas.set_at((self.mouse_pos[0],self.mouse_pos[1]), (255,0,255))
        scaled_canvas = pygame.transform.scale(self.canvas, self.screen_size)
        self.screen.blit(scaled_canvas, (0, 0))  # Draw scaled canvas on the screen
        pygame.display.update() 
        self.clock.tick(120)

    def get_mouse_position(self) -> tuple:
        mouse_pos = pygame.mouse.get_pos()
        canvas_x = int(mouse_pos[0] * self.x_screen_scale)
        canvas_y = int(mouse_pos[1] * self.y_screen_scale)
        canvas_x = max(0, min(self.resolution[0] - 1, canvas_x))
        canvas_y = max(0, min(self.resolution[1] - 1, canvas_y))
        return canvas_x,canvas_y
    
    def manage_mouse_clicks(self):
        left, scroll, right = pygame.mouse.get_pressed()
        if left: 
            self.add_plant_to_position(self.mouse_pos[0],self.mouse_pos[1],(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    def add_plant_to_position(self,x:int,y:int,gene):
        # for plant in self.plants_list:
        #     if (plant.x==x) and (plant.y==y):
        #         self.plants_list.remove(plant)
        #         break
        self.plants_list.append(RGPlant(x,y,gene))

    def check_closed_window(self) -> bool:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                return True
        return False

    def configuration_start(self, window_title):
        pygame.init()
        pygame.font.init()
        pygame.mouse.set_visible(False)
        self.resolution = SCREEN_DATA["RESOLUTION"]
        self.screen_size = SCREEN_DATA["SCREEN_SIZE"]
        self.canvas = pygame.Surface(self.resolution)
        self.screen = pygame.display.set_mode(self.screen_size)
        self.x_screen_scale = self.resolution[0] / self.screen_size[0]
        self.y_screen_scale = self.resolution[1] / self.screen_size[1]
        pygame.display.set_caption(window_title)
        self.exit = False
        self.mouse_pos = (0,0)
        self.clock = pygame.time.Clock()
        
def main():
    A = Game()
    A.start_game()

if __name__ == "__main__":
    main()