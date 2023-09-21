import pygame
from sys import exit
from random import shuffle, sample, choice

from card import Card
from enemy import Enemy
from player import Player

#game base
pygame.init()
DISPLAY = pygame.display.set_mode((1300, 750))
pygame.display.set_caption('Dungeon')
icon = pygame.image.load('graphics/player/gudako.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

#background
bg_image = pygame.image.load('graphics/backgrounds/background1.png').convert_alpha()
bg_image = pygame.transform.smoothscale(bg_image, (900, 500))
bg_rect1 = bg_image.get_rect(topleft = (0, 0))
bg_rect2 = bg_image.get_rect(topleft = (900, 0))

#hand, deck, tomb
MAX_HAND_SIZE = 10
#card types: [padoru, jolt, meditate, shieldup, attackup, defenseup, mulligan]
hand = []
deck = [
        # Card('mulligan', 0, 750), 
        # Card('mulligan', 0, 750),
        # Card('mulligan', 0, 750),
        # Card('mulligan', 0, 750),
        # Card('mulligan', 0, 750),
        Card('shieldup', 0, 750),
        Card('shieldup', 0, 750),
        Card('shieldup', 0, 750),
        Card('shieldup', 0, 750),
        Card('jolt', 0, 750),
        Card('jolt', 0, 750),
        Card('jolt', 0, 750),
        Card('jolt', 0, 750),
        Card('mulligan', 0, 750),
        Card('mulligan', 0, 750),
        Card('jolt', 0, 750),
        # Card('meditate', 0, 750),
        # Card('meditate', 0, 750),
        # Card('meditate', 0, 750),
        # Card('meditate', 0, 750),
        # Card('meditate', 0, 750),
        ]
tomb = []
shuffle(deck)

#reward phase
reward_font = pygame.font.Font('graphics/fonts/reward_font.ttf', 50)
rewards = [Card('padoru', 0, 495), 
           Card('jolt', 0, 495),
           Card('meditate', 0, 495),
           Card('shieldup', 0, 495),
           Card('attackup', 0, 495),
           Card('defenseup', 0, 495),
           Card('mulligan', 0, 495),]
choices = []
reward_held = False
reward_held_index = -1

#end turn button
button_image = pygame.image.load('graphics/buttons/end_turn.png').convert_alpha()
button_image = pygame.transform.smoothscale(button_image, (140, 40))
button_rect = button_image.get_rect(center = (1200, 430))
button_image_clicked = pygame.image.load('graphics/buttons/end_turn_clicked.png').convert_alpha()
button_image_clicked = pygame.transform.smoothscale(button_image_clicked, (140, 40))
button_rect_clicked = button_image_clicked.get_rect(center = (1200, 430))

#enemies
enemies = []
enemy_moves = []

#player
player = Player()

#player state images
attackup_icon = pygame.image.load('graphics/player/attackupicon.png').convert_alpha()
defenseup_icon = pygame.image.load('graphics/player/defenseupicon.png').convert_alpha()

#dungeon
dungeon = [0, 0, 0, 1, 1, 1, 2, 1, 2, 1, 2]
next_room_index = 0

#card draw timer
draw_timer = pygame.USEREVENT + 1
pygame.time.set_timer(draw_timer, 300)
keep_drawing = True

#enemy move
enemy_move_timer = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_move_timer, 1000)
keep_drawing = True
atk_i = 0

#game states
in_battle = False
in_reward = False
in_dungeon = True
player_turn = True
button_held = False
card_hovered = -1
card_held = False

def reposition_hand():
    hand_len = len(hand)
    if hand_len <= 10:
        if hand_len == 0:
            pass
        elif hand_len == 1:
            x_pos = 600
            hand[0].update_x_pos(x_pos)
        elif hand_len == 2:
            x_pos = 650
            for card in hand:
                card.update_x_pos(x_pos)
                x_pos -= 90
        elif hand_len == 3:
            x_pos = 700
            for card in hand:
                card.update_x_pos(x_pos)
                x_pos -= 90
        elif hand_len == 4:
            x_pos = 750
            for card in hand:
                card.update_x_pos(x_pos)
                x_pos -= 90
        elif hand_len == 5:
            x_pos = 800
            for card in hand:
                card.update_x_pos(x_pos)
                x_pos -= 90
        elif hand_len == 6:
            x_pos = 850
            for card in hand:
                card.update_x_pos(x_pos)
                x_pos -= 90
        elif hand_len == 7:
            x_pos = 900
            for card in hand:
                card.update_x_pos(x_pos)
                x_pos -= 90
        elif hand_len == 8:
            x_pos = 950
            for card in hand:
                card.update_x_pos(x_pos)
                x_pos -= 90
        elif hand_len == 9:
            x_pos = 1000
            for card in hand:
                card.update_x_pos(x_pos)
                x_pos -= 90
        elif hand_len == 10:
            x_pos = 1050
            for card in hand:
                card.update_x_pos(x_pos)
                x_pos -= 90
    else:
        raise ValueError("exceeded max hand size")

def draw_card(new_deck):
    if len(hand) < 10 and not(len(new_deck) == 0 and len(tomb) == 0):
        if len(new_deck) <= 0:
            for card in tomb:
                new_deck.append(card)
            tomb.clear()
            shuffle(new_deck)
            hand.append(new_deck[0])
            reposition_hand()
            del new_deck[0]
        else:
            hand.append(new_deck[0])
            reposition_hand()
            del new_deck[0]

def clear_hand():
    tomb.extend(hand)
    hand.clear()

def turn_start():
    for _ in range(5):
        draw_card(deck)


while True:
    
    if in_battle:
        
        #player turn
        if player_turn:
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                #pressing end turn button
                if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
                    button_held = True
                if event.type == pygame.MOUSEBUTTONUP:
                    if button_held and button_rect.collidepoint(event.pos):
                        player_turn = False
                        clear_hand()
                    if button_held:
                        button_held = False
                
                #dealing with cards and attacks
                if card_hovered != -1 and event.type == pygame.MOUSEBUTTONDOWN:
                    card_held = True
                if event.type == pygame.MOUSEBUTTONUP and card_held:
                    if player.mana >= hand[card_hovered].mana: #if have mana
                        if hand[card_hovered].need_target: #if need target check collide with enemy
                            
                            for enemy in enemies:
                                if enemy.rect.collidepoint(event.pos) and enemy.alive:
                                    #card effects
                                    if hand[card_hovered].card_type == 'jolt':
                                        enemy.hp -= (6 + player.state[0])
                                    elif hand[card_hovered].card_type == 'padoru':
                                        enemy.hp -= (50 + player.state[0])
                                        player.hp -= (20 + player.state[0])
                                        
                                    if not hand[card_hovered].extinct:
                                        tomb.append(hand[card_hovered])
                                    player.mana -= hand[card_hovered].mana
                                    del hand[card_hovered]
                                    DISPLAY.fill('Black')
                                    reposition_hand()
                                    
                        else: #if don't need target check collide with background image
                            if bg_rect1.collidepoint(event.pos) or bg_rect2.collidepoint(event.pos):
                                #card effects
                                if hand[card_hovered].card_type == 'meditate':
                                    player.mana += 2
                                elif hand[card_hovered].card_type == 'shieldup':
                                    player.shield += (5 + player.state[1])
                                elif hand[card_hovered].card_type == 'attackup':
                                    player.state[0] += 2
                                elif hand[card_hovered].card_type == 'defenseup':
                                    player.state[1] += 2
                                elif hand[card_hovered].card_type == 'mulligan':
                                    for _ in range(3):
                                        draw_card(deck)
                                    
                                if not hand[card_hovered].extinct:
                                    tomb.append(hand[card_hovered])
                                player.mana -= hand[card_hovered].mana
                                del hand[card_hovered]
                                DISPLAY.fill('Black')
                                reposition_hand()
                    card_held = False
                    card_hovered = -1
                    
                    
            #display background
            DISPLAY.fill('Black') #cover up what's left behind in previous frame
            DISPLAY.blit(bg_image, bg_rect1)
            DISPLAY.blit(bg_image, bg_rect2)
            
            
            #display end turn button (deciding which to use)
            if button_held: DISPLAY.blit(button_image_clicked, button_rect_clicked)
            else: DISPLAY.blit(button_image, button_rect)
            
            
            #display hand
            mouse_pos = pygame.mouse.get_pos()
            if not card_held:
                card_hovered = -1
            for i in range(len(hand)-1, -1, -1):
                if hand[i].rect.collidepoint(mouse_pos) and card_hovered == -1:
                    card_hovered = i
                else:
                    hand[i].update()
                    DISPLAY.blit(hand[i].image, hand[i].rect)
            if card_hovered != -1:
                hand[card_hovered].update()
                DISPLAY.blit(hand[card_hovered].image, hand[card_hovered].rect)
            if card_held:
                pygame.draw.rect(DISPLAY, (255, 0, 0), hand[card_hovered].rect, 6)
            
        #enemy turn    
        else:
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == enemy_move_timer and atk_i < len(enemies):
                    if enemies[atk_i].alive and enemy_moves[atk_i] != None:
                        if enemy_moves[atk_i] == 'damage':
                            if player.shield > 0:
                                player.shield -= (enemies[atk_i].moves['damage'] + enemies[atk_i].state[0])
                            else:
                                player.hp -= (enemies[atk_i].moves['damage'] + enemies[atk_i].state[0])
                            if player.shield < 0:
                                player.hp += player.shield
                                player.shield = 0
                        elif enemy_moves[atk_i] == 'atkbuff':
                            enemies[atk_i].state[0] += enemies[atk_i].moves['atkbuff']
                        ### add other moves ###
                        
                        # enemy_moves[atk_i] = None
                        enemy_moves[atk_i] = enemies[atk_i].get_move()
                        atk_i += 1
                    else:
                        atk_i += 1
            if atk_i >= len(enemies):
                player_turn = True
                player.mana = 10
                player.shield = 0
                atk_i = 0
                turn_start()
                    
                    
            #draw background
            DISPLAY.fill('Black') #cover up what's left behind in previous frame
            DISPLAY.blit(bg_image, bg_rect1)
            DISPLAY.blit(bg_image, bg_rect2)
            
        #display enemies
        for i in range (0, len(enemies)):
            if enemies[i].hp > 0:
                enemies[i].update()
                #enemy itself
                DISPLAY.blit(enemies[i].image, enemies[i].rect)
                #enemy hp
                enemy_hp_rect = pygame.Rect(enemies[i].rect.centerx - enemies[i].MAX_HP, enemies[i].rect.top - 50, enemies[i].MAX_HP * 2, 15)
                enemy_hp_len = enemies[i].hp * 2
                pygame.draw.rect(DISPLAY, (60, 10, 10), enemy_hp_rect)
                pygame.draw.rect(DISPLAY, (200, 10, 10), pygame.Rect(enemies[i].rect.centerx - enemies[i].MAX_HP, enemies[i].rect.top - 50, enemy_hp_len, 15))
                enemy_hp_num_surf = player.hp_font.render(str(enemies[i].hp) + ' / ' + str(enemies[i].MAX_HP), True, 'Red')
                enemy_hp_num_rect = enemy_hp_num_surf.get_rect(center = (enemy_hp_rect.centerx, enemy_hp_rect.centery - 20))
                DISPLAY.blit(enemy_hp_num_surf, enemy_hp_num_rect)
                #enemy buff debuff
                if enemies[i].state[0] != 0:
                    enemy_attackup_rect = attackup_icon.get_rect(topleft = (enemies[i].rect.left, enemies[i].rect.bottom + 8))
                    DISPLAY.blit(attackup_icon, enemy_attackup_rect)
                    enemy_attackup_num_surf = player.hp_font.render(str(enemies[i].state[0]), True, 'Orange')
                    enemy_attackup_num_rect = enemy_attackup_num_surf.get_rect(topleft = (enemies[i].rect.left + 30, enemies[i].rect.bottom + 12))
                    DISPLAY.blit(enemy_attackup_num_surf, enemy_attackup_num_rect)
                # if enemies[i].state[1] != 0:
                #     enemy_defenseup_rect = defenseup_icon.get_rect(topleft = (1150, 560))
                #     DISPLAY.blit(defenseup_icon, enemy_defenseup_rect)
                #     enemy_defenseup_num_surf = enemy.hp_font.render(str(enemies[i].state[1]), True, 'Orange')
                #     enemy_defenseup_num_rect = enemy_defenseup_num_surf.get_rect(topleft = (1182, 564))
                #     DISPLAY.blit(enemy_defenseup_num_surf, enemy_defenseup_num_rect)
                #red rectangle when targeted
                if card_held and enemies[i].rect.collidepoint(mouse_pos) and hand[card_hovered].need_target:
                    pygame.draw.rect(DISPLAY, (255, 0, 0), enemies[i].rect, 6)
            else:
                if enemies[i].alive:
                    enemies[i].alive = False
                    enemies[i].image = pygame.transform.rotate(enemies[i].image, 270)
                    if i == 0:
                        enemies[i].rect = enemies[i].image.get_rect(midbottom = (600, 400))
                    elif i == 1:
                        enemies[i].rect = enemies[i].image.get_rect(midbottom = (200, 450))
                    else:
                        enemies[i].rect = enemies[i].image.get_rect(midbottom = (1000, 450))
                DISPLAY.blit(enemies[i].image, enemies[i].rect)

        #display player
        if True:
            player.update()
            #mana ball
            DISPLAY.blit(player.mana_ball, player.mana_ball_rect)
            DISPLAY.blit(player.mana_surf, player.mana_rect)
            #hp bar
            player_hp_rect = pygame.Rect(1250, 530, 30, 200)
            player_hp_len = 200 * player.hp / player.MAX_HP
            pygame.draw.rect(DISPLAY, (60, 10, 10), player_hp_rect)
            pygame.draw.rect(DISPLAY, (200, 10, 10), pygame.Rect(1250, 730 - player_hp_len, 30, player_hp_len))
            if player_hp_rect.collidepoint(mouse_pos):
                hp_num_surf = player.hp_font.render(str(player.hp) + ' / ' + str(player.MAX_HP), True, 'Red')
                hp_num_rect = hp_num_surf.get_rect(topleft = (1220, 503))
                DISPLAY.blit(hp_num_surf, hp_num_rect)
            #shield
            DISPLAY.blit(player.shield_surf, player.shield_rect)
            DISPLAY.blit(player.shield_num_surf, player.shield_num_rect)
            #buff debuff
            if player.state[0] != 0:
                player_attackup_rect = attackup_icon.get_rect(topleft = (1150, 530))
                DISPLAY.blit(attackup_icon, player_attackup_rect)
                player_attackup_num_surf = player.hp_font.render(str(player.state[0]), True, 'Orange')
                player_attackup_num_rect = player_attackup_num_surf.get_rect(topleft = (1182, 534))
                DISPLAY.blit(player_attackup_num_surf, player_attackup_num_rect)
            if player.state[1] != 0:
                player_defenseup_rect = defenseup_icon.get_rect(topleft = (1150, 560))
                DISPLAY.blit(defenseup_icon, player_defenseup_rect)
                player_defenseup_num_surf = player.hp_font.render(str(player.state[1]), True, 'Orange')
                player_defenseup_num_rect = player_defenseup_num_surf.get_rect(topleft = (1182, 564))
                DISPLAY.blit(player_defenseup_num_surf, player_defenseup_num_rect)
            
        #check if all enemies died and battle ends
        if all(enemy.hp <= 0 for enemy in enemies):
            clear_hand()
            for card in tomb:
                deck.append(card)
            tomb.clear()
            in_battle = False
            in_reward = True
            
    elif in_reward:
        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                
            #card choice
            if event.type == pygame.MOUSEBUTTONDOWN:
                for i in range (0, len(choices), 1):
                    if choices[i].rect.collidepoint(event.pos):
                        reward_held = True
                        reward_held_index = i
                        
            if event.type == pygame.MOUSEBUTTONUP:
                if choices[reward_held_index].rect.collidepoint(event.pos):
                    choices[reward_held_index].update_pos(0, 0)
                    deck.append(choices[reward_held_index])
                    choices.clear()
                    reward_held_index = -1
                    in_reward = False
                    in_dungeon = True
                reward_held = False
                
        #cover up previous frame
        DISPLAY.fill('Black')
        
        #text
        reward_text_surf = reward_font.render('Choose a Card to Add to Your Deck', True, (133, 94, 66))
        reward_text_rect = reward_text_surf.get_rect(center = (650, 200))
        DISPLAY.blit(reward_text_surf, reward_text_rect)
        
        #get reward cards player can choose from
        if len(choices) == 0:
            choices.extend(sample(rewards, 4))
        
        #display all the cards
        x_pos = 215
        for i in range (0, len(choices)):
            choices[i].update_pos(x_pos, 555)
            x_pos += 290
            choices[i].update()
            DISPLAY.blit(choices[i].image, choices[i].rect)
            
        #holding card
        if reward_held:
            pygame.draw.rect(DISPLAY, (255, 0, 0), choices[reward_held_index].rect, 6)
        
    elif in_dungeon:
        #event loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        DISPLAY.fill('Black')
        for i in range (0, len(dungeon)):
            #load different images for different levels
            if dungeon[i] == 0:
                level_image = pygame.image.load('graphics/dungeon/bronze.png')
            elif dungeon[i] == 1:
                level_image = pygame.image.load('graphics/dungeon/silver.png')
            elif dungeon[i] == 2:
                level_image = pygame.image.load('graphics/dungeon/gold.png')
            
            #darken rooms passed
            if i < next_room_index:
                for x in range(level_image.get_width()):
                    for y in range(level_image.get_height()):
                        # Get the color of the pixel
                        color = level_image.get_at((x, y))
                        
                        # Decrease the brightness of each color channel
                        new_color = (
                            max(0, color.r - 120),
                            max(0, color.g - 120),
                            max(0, color.b - 120),
                            color.a
                        )
                        
                        # Set the new color of the pixel
                        level_image.set_at((x, y), new_color)
                
            #draw levels
            level_rect = level_image.get_rect(center = (100 + i * 100, 375))
            DISPLAY.blit(level_image, level_rect)
            pygame.draw.rect(DISPLAY, 'silver', level_rect, 2)
            
            #check if clicked
            mouse = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            if i == next_room_index and (mouse[0] or mouse[1] or mouse[2]) and level_rect.collidepoint(mouse_pos):
                in_dungeon = False
                in_battle = True
                next_room_index += 1
                if next_room_index >= len(dungeon):
                    in_dungeon = False
                else:
                    in_dungeon = False
                    in_battle = True
                    turn_start()
                    if dungeon[i] == 0:
                        enemies = [choice([Enemy('golem', 0), Enemy('skeleton', 0)]),
                                   choice([Enemy('golem', 1), Enemy('skeleton', 1)]),
                                   choice([Enemy('golem', 2), Enemy('skeleton', 2)])]
                    elif dungeon[i] == 1:
                        enemies = [choice([Enemy('golem', 0), Enemy('skeleton', 0)]),
                                   Enemy('wyvern', 1),
                                   choice([Enemy('golem', 2), Enemy('skeleton', 2)])]
                    elif dungeon[i] == 2:
                        enemies = [choice([Enemy('saber', 0), Enemy('lancer', 0), Enemy('archer', 0)])]
                    for enemy in enemies:
                        enemy_moves.append(enemy.get_move())
    
    #game ends
    else:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        
        DISPLAY.fill('Black')
        congrat_text_surf = reward_font.render('Congratulations! You have cleared the dungeon!', True, (133, 94, 66))
        congrat_text_rect = congrat_text_surf.get_rect(center = (650, 375))
        DISPLAY.blit(congrat_text_surf, congrat_text_rect)
        
    
    pygame.display.update() #update every frame
    clock.tick(60) #set framerate to 60 cap