import pygame
from random import choice

class Enemy:
    
    def __init__(self, type, enemy_no):
        
        self.animation_index = 0
        self.state = [0, 0]
        self.shield = 0
        self.alive = True
        if type == 'saber':
            self.image = pygame.image.load('graphics/enemies/saber.png').convert_alpha()
            # self.image = pygame.transform.smoothscale(self.image, (100, 100))
            self.MAX_HP = 200
            self.hp = 200
            self.moves = {
                'damage': 10,
                'atkbuff': 3
            }
        elif type == 'archer':
            self.image = pygame.image.load('graphics/enemies/archer.png').convert_alpha()
            # self.image = pygame.transform.smoothscale(self.image, (150, 150))
            self.MAX_HP = 200
            self.hp = 200
            self.moves = {
                'damage': 10,
                'atkbuff': 3
            }
        elif type == 'lancer':
            self.image = pygame.image.load('graphics/enemies/lancer.png').convert_alpha()
            # self.image = pygame.transform.smoothscale(self.image, (300, 300))
            self.MAX_HP = 200
            self.hp = 200
            self.moves = {
                'damage': 10,
                'atkbuff': 3
            }
        elif type == 'golem':
            self.image = pygame.image.load('graphics/enemies/golem.png').convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (140, 160))
            self.MAX_HP = 40
            self.hp = 40
            self.moves = {
                'damage': 4,
            }
        elif type == 'skeleton':
            self.image = pygame.image.load('graphics/enemies/skeleton.png').convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (140, 160))
            self.MAX_HP = 30
            self.hp = 30
            self.moves = {
                'damage': 5,
            }
        elif type == 'wyvern':
            self.image = pygame.image.load('graphics/enemies/wyvern.png').convert_alpha()
            self.image = pygame.transform.smoothscale(self.image, (240, 240))
            self.MAX_HP = 60
            self.hp = 60
            self.moves = {
                'damage': 5,
                'atkbuff': 2
            }
        if enemy_no == 0:
            self.rect = self.image.get_rect(midbottom = (600, 400))
        elif enemy_no == 1:
            self.rect = self.image.get_rect(midbottom = (200, 450))
        else:
            self.rect = self.image.get_rect(midbottom = (1000, 450))
        
    def get_move(self):
        return choice(list(self.moves.keys()))
    
    # def do_move(self, move):
    
    def update(self):
        if self.hp <= 0:
            self.hp = 0
        # self.animation_index += 0.05
        # if self.animation_index < 1:
        #     self.rect.bottom -= 1
        # elif self.animation_index < 1.95:
        #     self.rect.bottom += 1
        # if self.animation_index >= 2:
        #     self.animation_index = 0