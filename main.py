import pygame
from sys import exit
from random import randint, choice

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk1 = pygame.image.load('Player/knight1.png').convert_alpha()
        player_walk2 = pygame.image.load('Player/knight2.png').convert_alpha()
        self.player_walk = [player_walk1, player_walk2]
        self.player_index = 0
        self.player_jump = pygame.image.load('Player/knightjump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=(120, 660))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('Sounds/jump.mp3')
        self.jump_sound.set_volume(200)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 660:
            self.gravity = -30
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 660:
            self.rect.bottom = 660

    def animation_state(self):
        if self.rect.bottom < 660:
            self.image = self.player_jump
        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()

        if type == 'bat':
            bat_1 = pygame.image.load('Enemies/bat1.png').convert_alpha()
            bat_2 = pygame.image.load('Enemies/bat2.png').convert_alpha()
            self.frames = [bat_1, bat_2]
            y_pos = 400
        else:
            demon_1 = pygame.image.load('Enemies/demon1.png').convert_alpha()
            demon_2 = pygame.image.load('Enemies/demon2.png').convert_alpha()
            self.frames = [demon_1, demon_2]
            y_pos = 660

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom=(randint(1300, 1500), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 8
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def displayscore():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score = font.render(f'Score {current_time}', False, 'Red')
    score_rect = score.get_rect(center=(600, 100))
    screen.blit(score, score_rect)
    return current_time

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        death_sound = pygame.mixer.Sound('Sounds/death.mp3')
        death_sound.play()
        death_sound.set_volume(40)
        obstacle_group.empty()
        return False
    return True

pygame.init()
screen = pygame.display.set_mode((1200, 800))
pygame.display.set_caption('DUNGEON JUMPER')
clock = pygame.time.Clock()
font = pygame.font.Font('Background/ARCADECLASSIC.TTF', 70)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('Sounds/music.mp3')
bg_music.play(loops=-1)
bg_music.set_volume(0.3)

# Groups
player = pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()

sky = pygame.image.load('Background/dungeon.png').convert()
ground = pygame.image.load('Background/ground.png').convert()

text = font.render('Dungeon Jumper', False, 'Black')
title = text.get_rect(center=(600, 130))

# Intro screen
player_stand = pygame.image.load('Player/knight1.png').convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rec = player_stand.get_rect(center=(600, 400))

death_message = font.render('YOU DIED', False, 'Black')
death_rect = death_message.get_rect(center=(600, 100))

continue_message = font.render('Press space to continue', False, 'Black')
continue_rect = continue_message.get_rect(center=(600, 650))

# Timer
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['bat', 'demon', 'demon', 'demon'])))
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)

    if game_active:
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 630))
        score = displayscore()

        player.draw(screen)
        player.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill('Red')
        screen.blit(player_stand, player_stand_rec)
        score_message = font.render(f'Score {score}', False, 'Black')
        score_message_rect = score_message.get_rect(center=(600, 175))
        screen.blit(continue_message, continue_rect)

        if score == 0:
            screen.blit(text, title)
        else:
            screen.blit(score_message, score_message_rect)
            screen.blit(death_message, death_rect)

    pygame.display.update()
    clock.tick(60)
