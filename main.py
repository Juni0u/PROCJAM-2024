import pygame, random
from CONS import SCREEN_DATA
from rgplant import RGPlant
from textbox import TextBox

class Game():
    def __init__(self,window_title:str="RGPlants"):
        self.plants_list = []
        self.textbox_list = []
        self.configuration_start(window_title=window_title)
        #self.plants_list.append(RGPlant(63,63,(255,0,0)))

    def start_game(self):
        while not self.exit:
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    self.exit=True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.toogle_pause()


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
        if not self.pause:
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

        if self.pause:
            font = pygame.font.Font(None,12)
            pause_text = font.render(f"GAME PAUSED",True, (255,255,255))
            self.canvas.blit(pause_text,self.pause_pos)

            #Text Boxes
            for textbox in self.textbox_list:
                self.canvas = textbox.draw(self.canvas)
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
        self.clock.tick(self.fps_cap) #TODO: Option to change this value

    def get_mouse_position(self) -> tuple:
        mouse_pos = pygame.mouse.get_pos()
        canvas_x = int(mouse_pos[0] * self.x_screen_scale)
        canvas_y = int(mouse_pos[1] * self.y_screen_scale)
        canvas_x = max(0, min(self.resolution[0] - 1, canvas_x))
        canvas_y = max(0, min(self.resolution[1] - 1, canvas_y))
        return canvas_x,canvas_y
    
    def toogle_pause(self):
        if self.pause:
            self.pause=False
        else:
            self.pause=True
    
    def manage_mouse_clicks(self):
        left, scroll, right = pygame.mouse.get_pressed()
        if left: 
            if self.pause:
                pass                
            self.add_plant_to_position(self.mouse_pos[0],self.mouse_pos[1],(random.randint(0,255),random.randint(0,255),random.randint(0,255)))


    def add_plant_to_position(self,x:int,y:int,gene):
        # for plant in self.plants_list:
        #     if (plant.x==x) and (plant.y==y):
        #         self.plants_list.remove(plant)
        #         break
        self.plants_list.append(RGPlant(x,y,gene))

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
        self.fps_cap = SCREEN_DATA["FPS_CAP"]
        pygame.display.set_caption(window_title)
        self.exit = False
        self.pause = False
        self.mouse_pos = (0,0)
        self.clock = pygame.time.Clock()
        self.pause_pos = [3,0]

        ### Pause Menu Configuration
        tbox_width = 10
        tbox_height = 5
        tbox_y_pos = 30
        tbox_x_initial = 12
        #red box, most left
        self.textbox_list.append(TextBox(tbox_x_initial,tbox_y_pos,tbox_width,tbox_height,(255,0,0),(125,0,0)))
        #green box, middle
        self.textbox_list.append(TextBox(self.textbox_list[0].x+15,tbox_y_pos,tbox_width,tbox_height,(0,255,0),(0,125,0)))
        #blue box, most right
        self.textbox_list.append(TextBox(self.textbox_list[1].x+15,tbox_y_pos,tbox_width,tbox_height,(0,0,255),(0,0,125)))

        
def main():
    A = Game()
    A.start_game()

if __name__ == "__main__":
    main()