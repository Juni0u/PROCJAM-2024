import pygame, random
from CONS import SCREEN_DATA
from rgplant import RGPlant
from textbox import TextBox
from button import Button

class Game():
    def __init__(self,window_title:str="RGPlants"):
        self.plants_list = []
        self.textbox_list = []
        self.button_list = []
        self.configuration_start(window_title=window_title)
        #self.plants_list.append(RGPlant(63,63,(255,0,0)))

    def start_game(self):
        while not self.exit:
            events = pygame.event.get()
            for event in events: 
                if event.type == pygame.QUIT: 
                    self.exit=True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.toogle_pause()
                        
            self.update(events)
            self.before_draw()
            self.draw()
            self.update_screen()

    def update (self, events):
        new_plants = []
        marked_for_death = []
        random.shuffle(self.plants_list)
        self.mouse_pos = self.get_mouse_position()
        self.manage_mouse_clicks(events)

        #Not Paused
        if not self.pause:
            if self.plants_list:
                for plant in self.plants_list:
                    death, new_plants = plant.update(self.plants_list)
                    if death: marked_for_death.append(plant)

            if new_plants:
                for x,y,gene in new_plants:
                    self.add_plant_to_position(x,y,gene)

            if marked_for_death:
                plants_list_set = set(self.plants_list)
                for plant in marked_for_death:
                    plants_list_set.remove(plant)
                self.plants_list = list(plants_list_set)
        #Paused
        else:
            for textbox in self.textbox_list:
                textbox.update(events)
            for button in self.button_list:
                button.update(events)
        
            if self.button_list[0].active:
                self.new_gene = (random.randint(0,255),random.randint(0,255),random.randint(0,255))
            else:
                self.new_gene = (int(self.textbox_list[0].color_choice),
                                int(self.textbox_list[1].color_choice),
                                int(self.textbox_list[2].color_choice))            

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

            #Button
            for button in self.button_list:
                self.canvas = button.draw(self.canvas)

##############################################
##############################################
##############################################
##############################################
##############################################
    def before_draw(self):
        self.canvas.fill((0, 0, 0)) 

    def update_screen(self):
        #draw mouse
        self.canvas.set_at((self.mouse_pos[0],self.mouse_pos[1]), self.new_gene)
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
    
    def manage_mouse_clicks(self,events):
        for event in events:
            if (event.type == pygame.MOUSEBUTTONDOWN) and (event.button==1):
                if self.pause:
                    textbox_clicked = False
                    for textbox in self.textbox_list:
                        if textbox.rect.collidepoint(self.mouse_pos[0],self.mouse_pos[1]):
                            textbox.active = True
                            self.toogle_textboxes(textbox)
                            textbox_clicked = True
                            break
                    if not textbox_clicked:
                        self.add_plant_to_position(self.mouse_pos[0],self.mouse_pos[1],self.new_gene)
                    for button in self.button_list:
                        if button.rect.collidepoint(self.mouse_pos[0],self.mouse_pos[1]):
                            button.toogle()
                            break
                #Game Loop
                else:
                    self.add_plant_to_position(self.mouse_pos[0],self.mouse_pos[1],self.new_gene)
                    

    def toogle_textboxes(self,active_textbox):
        for textbox in self.textbox_list:
            if textbox == active_textbox: next
            else:
                if textbox.active: textbox.active = False

    def add_plant_to_position(self,x:int,y:int,gene):
        plants_list_set = set(self.plants_list)
        for plant in self.plants_list:
            if (plant.x==x) and (plant.y==y):
                self.plants_list.remove(plant)
                break
        self.plants_list = list(plants_list_set)
        self.plants_list.append(RGPlant(x,y,gene,self.neighbor_dict))

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
        self.new_gene = (255,255,255)
        self.neighbor_dict = self.Build_Neighbor_Dict()

        ### Pause Menu Configuration
        tbox_width = 19
        tbox_height = 10
        tbox_y_pos = 30
        tbox_x_initial = 2 
        tbox_x_interval = 20
        #red box, most left 
        self.textbox_list.append(TextBox(tbox_x_initial,tbox_y_pos,tbox_width,tbox_height,(255,0,0),(125,0,0)))
        #green box, middle
        self.textbox_list.append(TextBox(self.textbox_list[0].x+tbox_x_interval,tbox_y_pos,tbox_width,tbox_height,(0,255,0),(0,125,0)))
        #blue box, most right
        self.textbox_list.append(TextBox(self.textbox_list[1].x+tbox_x_interval,tbox_y_pos,tbox_width,tbox_height,(0,0,255),(0,0,125)))
        #randombox, botton middle
        self.button_list.append(Button(self.textbox_list[0].x+tbox_x_interval,tbox_y_pos+tbox_height+2,tbox_width,tbox_height,(0,255,0),(255,0,0)," R"))

    def Build_Neighbor_Dict(self):
        X_MAX = self.resolution[0]
        Y_MAX = self.resolution[1]
        neighbors_dict = {}

        neighbors_dict[(0,0)] = [(0,1),(1,0),(1,1)]
        neighbors_dict[(0,Y_MAX-1)] = [(0,Y_MAX-1),(1,Y_MAX-1),(1,X_MAX-1)]
        neighbors_dict[(X_MAX-1,0)] = [(Y_MAX-1,0),(X_MAX-1,1),(Y_MAX-1,1)]

        for x in range(X_MAX):
            for y in range(Y_MAX):
                key = (x,y)
                if key not in neighbors_dict:
                    neighbors_dict[key] = []
                if x==0 and y!=Y_MAX-1:
                    for ix in range(0,2):
                        for iy in range(-1,2):
                            if not (ix==0 and iy==0):
                                neighbors_dict[key].append((x+ix,y+iy))
                elif y==0 and x!=X_MAX-1:
                    for ix in range(-1,2):
                        for iy in range(0,2):
                            if not (ix==0 and iy==0):
                                neighbors_dict[key].append((x+ix,y+iy))
                else:
                    for ix in range(-1,2):
                        for iy in range(-1,2):
                            if not (ix==0 and iy==0):
                                neighbors_dict[key].append((x+ix,y+iy))
        return neighbors_dict

def main():
    A = Game()
    A.start_game()

if __name__ == "__main__":
    main()