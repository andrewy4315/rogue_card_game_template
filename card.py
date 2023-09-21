import pygame

class Card():
    
    def __init__(self, type, x_pos, y_pos):
        self.image = pygame.Surface((150, 240))
        self.rect = self.image.get_rect(midbottom = (x_pos, y_pos))
        self.font = pygame.font.Font('graphics/fonts/card_des_font.ttf', 13)
        self.title_font = pygame.font.Font('graphics/fonts/card_title_font.otf', 15)
        self.mana_font = pygame.font.Font('graphics/fonts/mana_font.ttf', 20)

        self.card_frame = pygame.image.load('graphics/card_elements/card_frame.png').convert_alpha()
        self.card_frame = pygame.transform.smoothscale(self.card_frame, (150, 240))
        
        self.card_type = type
        
        if type == 'padoru':
            self.pict = pygame.image.load('graphics/card_elements/padoru.png').convert_alpha()
            self.pict = pygame.transform.smoothscale(self.pict, (100, 100))
            self.title = 'padoru'
            self.text = 'deal 50 damage to an enemy and 20 damage to yourself'
            self.mana = 1
            self.extinct = False
            self.need_target = True
        elif type == 'jolt':
            self.pict = pygame.image.load('graphics/card_elements/jolt.png').convert_alpha()
            self.pict = pygame.transform.smoothscale(self.pict, (100, 100))
            self.title = 'jolt'
            self.text = 'deal 6 damage to an enemy'
            self.mana = 1
            self.extinct = False
            self.need_target = True
        elif type == 'meditate':
            self.pict = pygame.image.load('graphics/card_elements/meditate.png').convert_alpha()
            self.pict = pygame.transform.smoothscale(self.pict, (100, 100))
            self.title = 'meditate'
            self.text = 'gain 2 mana'
            self.mana = 0
            self.extinct = False
            self.need_target = False
        elif type == 'shieldup':
            self.pict = pygame.image.load('graphics/card_elements/shieldup.png').convert_alpha()
            self.pict = pygame.transform.smoothscale(self.pict, (100, 100))
            self.title = 'shield up'
            self.text = 'gain +5 shield'
            self.mana = 1
            self.extinct = False
            self.need_target = False
        elif type == 'attackup':
            self.pict = pygame.image.load('graphics/card_elements/attackup.png').convert_alpha()
            self.pict = pygame.transform.smoothscale(self.pict, (100, 100))
            self.title = 'attack buff'
            self.text = 'gain +2 attack'
            self.mana = 3
            self.extinct = True
            self.need_target = False
        elif type == 'defenseup':
            self.pict = pygame.image.load('graphics/card_elements/defenseup.png').convert_alpha()
            self.pict = pygame.transform.smoothscale(self.pict, (100, 100))
            self.title = 'defense up'
            self.text = 'gain +2 shield every time you gain shield'
            self.mana = 2
            self.extinct = True
            self.need_target = False
        elif type == 'mulligan':
            self.pict = pygame.image.load('graphics/card_elements/mulligan.png').convert_alpha()
            self.pict = pygame.transform.smoothscale(self.pict, (100, 100))
            self.title = 'mulligan'
            self.text = 'draw 3 cards'
            self.mana = 2
            self.extinct = False
            self.need_target = False
        
        
    def update_x_pos(self, new_pos):
        self.rect = self.image.get_rect(midbottom = (new_pos, 750))
    
    def update_pos(self, new_x, new_y):
        self.rect = self.image.get_rect(midbottom = (new_x, new_y))
    
    def update(self):
        self.image.blit(self.card_frame, (0, 0))
        self.image.blit(self.pict, (30, 20))
        
        title_surf = self.title_font.render(self.title, True, 'Purple')
        title_rect = title_surf.get_rect(center = (75, 133))
        self.image.blit(title_surf, title_rect)
        
        mana_surf = self.mana_font.render(str(self.mana), True, 'Blue')
        mana_rect = mana_surf.get_rect(center = (18, 23))
        self.image.blit(mana_surf, mana_rect)
        
        words = self.text.split()
        max_line_width = 120
        lines = []
        current_line = ''
        for word in words:
            test_line = current_line + word + ' '
            test_text = self.font.render(test_line, True, (0, 0, 0))
            if test_text.get_width() <= max_line_width:
                current_line = test_line
            else:
                current_line = current_line[:-1]
                lines.append(current_line)
                current_line = word + ' '
        lines.append(current_line)
        if self.extinct:
            lines.append('ONE USE ONLY')
        
        text_y_pos = 160
        for line in lines:
            text_surf = self.font.render(line, True, 'Black')
            text_rect = text_surf.get_rect(center = (75, text_y_pos))
            self.image.blit(text_surf, text_rect)
            text_y_pos += self.font.get_linesize()