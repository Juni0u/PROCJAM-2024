import pygame, random, uuid

WHITE = (255, 255, 255)


class RGPlant:
    def __init__(self, x: int, y: int, gene: list, neighbor_dict: dict, PLANTS_CONS: dict):
        self.id = uuid.uuid1()
        self.x = x
        self.y = y
        self.gene = gene
        self.color = gene
        self.body = pygame.Rect(x, y, 1, 1)
        self.neighbor_region = pygame.Rect(self.x - 1, self.y - 1, 3, 3)
        self.mitosis_chance = PLANTS_CONS["MITOSIS_CHANCE"] / 100
        self.death_chance = PLANTS_CONS["DEATH_CHANCE"] / 100
        self.mutation_chance = PLANTS_CONS["MUTATION_CHANCE"] / 100
        # self.neighbors = self.get_neighbors(neighbor_dict)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, value):
        return (self.id) == (value.id)

    def update(self, all_plants):
        new_plants = []
        death = False
        neighbors = self.get_neighbors(all_plants)
        self.color = self.update_color(neighbors)
        dice = random.random()
        if dice <= self.mitosis_chance:
            new_plants = self.mitosis()
        elif dice <= self.mitosis_chance + self.death_chance:
            death = True
        return death, new_plants

    def draw(self, canvas):
        # pygame.draw.rect(canvas,WHITE,self.neighbor_region)
        canvas.set_at((self.x, self.y), self.color)
        return canvas

    def get_neighbors(self, all_plants):
        neighbors = []
        # for key in neighbor_dict:
        #     if key==(self.x,self.y):
        #         return neighbor_dict
        for plant in all_plants:
            if self.neighbor_region.colliderect(plant.body):
                neighbors.append(plant)
        return neighbors

    def update_color(self, neighbors):
        color = [0, 0, 0]
        if neighbors:
            for plant in neighbors:
                color[0] += plant.gene[0]
                color[1] += plant.gene[1]
                color[2] += plant.gene[2]

            for i, value in enumerate(color):
                color[i] = value / len(neighbors)
        return color

    def mitosis(self):
        gene = self.gene
        if random.random() < self.mutation_chance:
            gene = self.mutate(self.gene)

        new_plants = []
        for x in range(-1, 2):
            for y in range(-1, 2):
                new_plants.append([self.x + x, self.y + y, gene])
        return new_plants

    def mutate(self, gene):
        gene = list(gene)
        index = random.randint(0, 2)
        if random.random() < 0.5:
            gene[index] *= 1.25
            if gene[index] > 255:
                gene[index] = 255
        else:
            gene[index] *= 0.75
            if gene[index] < 0:
                gene[index] = 0
        return gene
