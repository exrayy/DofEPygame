import pygame
import math
import random

pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Click & Blast!")

clock = pygame.time.Clock()

#ui
font = pygame.font.Font('freesansbold.ttf', 34)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
screen_width = 900
screen_height = 600
score = '0'

#player
player = pygame.image.load('./img/player.png')
player_size = (30, 30)
player_rot = ''
player_x = 420
player_y = 400
angle = 0

#bullets
bullets_left_01 = 100
bullets = []
bullet_rect = ()
bullet_pos = (player_x, player_y)
bullet_x = 420
bullet_y = 400
bullet_angle = angle
bullet_speed = 25


class EnemyClass(pygame.sprite.Sprite):
    def __init__(self):
        super(EnemyClass, self).__init__()
        self.explosion_01 = pygame.image.load('./img/particles/muzzle_01.png').convert_alpha()
        self.explosion_02 = pygame.image.load('./img/particles/muzzle_02.png').convert_alpha()
        self.explosion_03 = pygame.image.load('./img/particles/muzzle_03.png').convert_alpha()
        self.explosion_04 = pygame.image.load('./img/particles/muzzle_04.png').convert_alpha()
        self.explosion_05 = pygame.image.load('./img/particles/muzzle_05.png').convert_alpha()

        self.anim_explosion = [self.explosion_01, self.explosion_02, self.explosion_03, self.explosion_04, self.explosion_05]
        self.index = 0
        self.image = pygame.image.load('./img/enemy.jpg').convert_alpha()
        self.image = pygame.transform.scale(self.image, enemy_size)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, screen_width - self.rect.width)
        self.rect.y = -self.rect.height
        self.sound = pygame.mixer.Sound('./audio/mixkit-short-explosion-1694.wav')
        self.hp = 1
        self.vel_x = 0
        self.vel_y = random.randrange(3, 8)

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def hit(self):
        print("hit")
    
    def destroy(self):
        max_index = len(self.anim_explosion) - 1
        if self.index > max_index:
            self.kill()
        else:    
            self.image = self.anim_explosion[self.index]
            self.index += 1     


class EnemySpawner:
    def __init__(self):
        self.enemy_group = pygame.sprite.Group()
        self.spawn_timer = random.randrange(30, 120)

    def update(self):
        self.enemy_group.update()
        if self.spawn_timer == 0:
            self.spawn_enemy()
            self.spawn_timer = random.randrange(30, 120)
        else:
            self.spawn_timer -= 1    

    def spawn_enemy(self):
        new_enemy = EnemyClass()
        self.enemy_group.add(new_enemy)

enemy_spawner = EnemySpawner()
enemy_size = (80, 80)
enemy_class = EnemyClass()

class Bullet:
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(- self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((14, 4)).convert_alpha()
        self.bullet.fill((white))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 8

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed, 
        self.pos[1] + self.dir[1] * self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center = self.pos)
        surf.blit(self.bullet, bullet_rect)


def draw_bullets():
    for bullet in bullets:
        bullet.draw(screen)

def int_score():
    bullets_left_02 = font.render(str(bullets_left_01), True, (white))
    screen.blit(bullets_left_02, [845, 15])

    if bullets_left_01 <= 0:
        game_over()

def msg_to_screen(msg, color, text_pos):
    screen_text = font.render(msg, True, color)
    screen.blit(screen_text, text_pos)

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False   
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        screen.fill(black)
        msg_to_screen("paused", white, [415 - 50, 290])
        msg_to_screen("esc to quit", white, [415 - 50, 290 + 50])
        msg_to_screen("P to unpause", white, [400 - 50, 45])
        
        pygame.display.update()
        clock.tick(10)

def game_over():
    dead = True
    while dead:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                #if event.key == pygame.K_r:
                    
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()        
        
        screen.fill(black)
        msg_to_screen("GAME OVER", white, [415 - 50, 290])
        msg_to_screen("esc to quit", white, [415 - 50, 290 + 50])

        pygame.display.update()
        clock.tick(10)

def rotate_player(player, angle):
    angle = 360 - math.atan2(mouse_pos[1]- 300, mouse_pos[0]- 400) * 180 / math.pi
    player = pygame.transform.scale(player, player_size)
    player_rot = pygame.transform.rotate(player, angle)
    new_rect = player_rot.get_rect(center = (player_x, player_y))
    screen.blit(player_rot, new_rect)

def is_collision():
    distance = math.sqrt(math.pow(enemy_class.rect.x - bullet_x, 2)) + (math.pow(enemy_class.rect.y - bullet_y, 2))
    if distance <= 30:
        return True
    else:
        return False    

def collisions():
    collision = is_collision(enemy_class.rect.x, enemy_class.rect.y, bullet_x, bullet_y)
    if collision:
        print("collision")        


while True:
    clock.tick(60)
    screen.fill((black))
    msg_to_screen(score, white, [15, 15])
    int_score()
    mouse_pos = pygame.mouse.get_pos()
    rotate_player(player, angle)
    enemy_spawner.update()
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                pause()
            if event.key == pygame.K_r:
                game_over()       
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullets_left_01 -= 1
            bullets.append(Bullet(* bullet_pos))

    for bullet in bullets[:]:
        bullet.update()
        if not screen.get_rect().collidepoint(bullet.pos):
            bullets.remove(bullet)           

    enemy_spawner.enemy_group.draw(screen)
    draw_bullets()
    pygame.display.flip()
    pygame.display.update()
