import pygame,random
from CONS import PLANTS_CONS
WHITE = (255,255,255)
MITOSIS_CHANCE = PLANTS_CONS["MITOSIS_CHANCE"]
DEATH_CHANCE = PLANTS_CONS["DEATH_CHANCE"]
MUTATION_CHANCE = PLANTS_CONS["MUTATION_CHANCE"]

class RGPlant():
    def __init__(self, x:int, y:int, gene:list):
        self.x = x
        self.y = y
        self.gene = gene
        self.color = gene
        self.body = pygame.Rect(x,y,1,1)
        self.neighbor_region = pygame.Rect(self.x-1,self.y-1,3,3)

    def update(self,all_plants):
        new_plants = []
        death = False
        neighbors = self.get_neighbors(all_plants)
        self.color = self.update_color(neighbors)
        dice = random.random()
        if dice <= MITOSIS_CHANCE:
            new_plants = self.mitosis()
        elif dice <= MITOSIS_CHANCE + DEATH_CHANCE:
            death = True
        return death, new_plants

    def draw(self,canvas):
        #pygame.draw.rect(canvas,WHITE,self.neighbor_region)
        canvas.set_at((self.x,self.y), self.color)
        return canvas

    def get_neighbors(self,all_plants):
        neighbors = []
        for plant in all_plants:
            if self.neighbor_region.colliderect(plant.body):
                neighbors.append(plant)
        return neighbors

    def update_color(self,neighbors):
        color=[0,0,0]
        if neighbors:
            for plant in neighbors:
                color[0] += plant.gene[0]
                color[1] += plant.gene[1]
                color[2] += plant.gene[2]
            
            for i,value in enumerate(color):
                color[i] = value/len(neighbors)
        return color

    def mitosis(self):
        gene = self.gene
        if random.random() < MUTATION_CHANCE: 
            gene = self.mutate(self.gene)

        new_plants = []
        for x in range(-1,2):
            for y in range(-1,2):
                    new_plants.append([self.x+x,self.y+y,gene])
        return new_plants
                    
    def mutate(self, gene):
        gene = list(gene)
        index = random.randint(0,2)
        if random.random() < 0.5:
            gene[index] *= 1.25
            if gene[index] > 255: gene[index] = 255
        else:
            gene[index] *= 0.75
            if gene[index] < 0: gene[index] = 0
        return gene
