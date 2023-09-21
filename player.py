import pygame

class Player():
    
    def __init__(self):
        self.MAX_MANA = 10
        self.MAX_HP = 50
        self.mana = 10
        self.hp = 50
        self.shield = 0
        self.state = [0, 0] #[attackup amount, defenseup amount]
        
        #mana number
        self.mana_font = pygame.font.Font('graphics/fonts/mana_font.ttf', 100)
        self.mana_surf = self.mana_font.render(str(self.mana), True, 'Blue')
        self.mana_rect = self.mana_surf.get_rect(midtop = (82, 540))
        #mana ball
        self.mana_ball = pygame.image.load('graphics/player/mana_ball.png').convert_alpha()
        self.mana_ball = pygame.transform.smoothscale(self.mana_ball, (130, 130))
        self.mana_ball_rect = self.mana_ball.get_rect(midtop = (82, 520))
        #shield
        self.shield_surf = pygame.image.load('graphics/player/shield.png').convert_alpha()
        self.shield_surf = pygame.transform.smoothscale(self.shield_surf, (100, 90))
        self.shield_rect = self.shield_surf.get_rect(center = ((1180, 680)))
        #shield number
        self.shield_font = pygame.font.Font('graphics/fonts/mana_font.ttf', 50)
        self.shield_num_surf = self.shield_font.render(str(self.shield), True, 'White')
        self.shield_num_rect = self.shield_num_surf.get_rect(center = (1180, 680))
        #hp bar
        self.hp_font = pygame.font.Font('graphics/fonts/card_title_font.otf', 20)
        
    def update(self):
        self.mana_surf = self.mana_font.render(str(self.mana), True, 'Blue')
        self.mana_rect = self.mana_surf.get_rect(midtop = (82, 540))
        self.shield_num_surf = self.shield_font.render(str(self.shield), True, 'White')
        self.shield_num_rect = self.shield_num_surf.get_rect(center = (1180, 680))