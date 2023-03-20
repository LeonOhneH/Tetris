import pygame
from pygame.locals import *
from sys import exit
import random


# Definiert die Wände als Sprites
        
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.image.set_alpha(0)
        self.mask = pygame.mask.from_surface(self.image)


# Definiert den steuerbaren Tetromino
    
class Tetromino (pygame.sprite.Sprite):
    def __init__(self, x, y, shape):
        super().__init__()      
        self.shape = shape
        # Laden der Bilder
        self.image = pygame.image.load("graphics/" + str(shape) + ".png")
   
        # Anwenden der Maske
        self.mask = pygame.mask.from_surface(self.image)   
         
        # Einstellen des Rect-Attributs
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        # Einen transparenten Surface erstellen, um die Maske anzuzeigen
        self.mask_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA, 32)
        self.mask_surface.fill((255, 255, 255, 100))
      
        # Die Maske des Tetrominos auf die Surface setzen
        self.mask_surface.blit(self.image, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
      
        self.is_moving_left = False
        self.is_moving_right = False
        self.is_turning_right = False

    def can_move_down(self, wall_group, move_group):
        # Erstellt eine vorübergehende Kopie des Tetrominos
        temp_tetromino = Tetromino(self.rect.x, self.rect.y + 20, self.shape)
        temp_tetromino.mask = pygame.mask.from_surface(temp_tetromino.image)

        # Überprüft, ob der vorübergehende Tetromino kollidiert
        for wall in wall_group:
            if pygame.sprite.collide_mask(temp_tetromino, wall):
                return False
        for tetromino in move_group:
            if tetromino != self:
                if pygame.sprite.collide_mask(temp_tetromino, tetromino):
                    return False

        return True
      
    def update(self, wall_group):
        keys = pygame.key.get_pressed()
        if keys[K_RIGHT] and self.rect.topright[0] < 259:
            if not self.is_moving_right:
                self.rect.x = self.rect.x + 20
                self.is_moving_right = True
        else:
            self.is_moving_right = False
         
        if keys[K_LEFT] and self.rect.topleft[0] > 61:
            if not self.is_moving_left:
                self.rect.x = self.rect.x - 20
                self.is_moving_left = True
        else:
            self.is_moving_left = False

        if keys[K_UP]:
            self.rect.y = self.rect.y - 1

        elif keys[K_DOWN] and self.can_move_down(wall_group, move_group):
            self.rect.y = self.rect.y + 20

        if keys[K_e]:
            if not self.is_turning_right:
                self.image = pygame.transform.rotate(self.image, 90)
                self.mask = pygame.mask.from_surface(self.image)                
                self.is_turning_right = True
        else:
            self.is_turning_right = False
            
  
         
      

    

      

# Standart Kram

pygame.init()
screen = pygame.display.set_mode

pygame.init()
screen = pygame.display.set_mode((400,500))
pygame.display.set_caption("Tetris")
clock = pygame.time.Clock()

# Setzt den Hintergrund auf background.jpg

background_surface = pygame.image.load("graphics/background.jpg")

# Initialisiert die Wände und fügt sie wall_group hinzu
        
ground = Wall(60, 440, 200, 20)
left_wall = Wall(40, 40, 20, 400)
right_wall = Wall(260, 40, 20, 400)

wall_group = pygame.sprite.Group()
wall_group.add(ground, left_wall, right_wall)       

# Initialisiert den Tetromino t und fügt in in move_group


tetromino_list = ["i","o","l","j","s","z","t"]
move_group = pygame.sprite.Group()



# count für langsames absenken

count = 0


def collision():
    move_group.sprites()[0].rect.y = move_group.sprites()[0].rect.y - 20
    wall_group.add(move_group.sprites()[0])
    move_group.empty()
               
while True:
    #Sollte der letzte Tetromino gesetzt sein, wird ein neuer gewählt
    #und in die move_group geschoben; ist die Tetromino liste leer
    if len(move_group) == 0:
        if len(tetromino_list) == 0:
            tetromino_list = ["i","o","l","j","s","z","t"]
        random_pop = random.randint(0,len(tetromino_list)-1)
        pop = tetromino_list.pop(random_pop)
        print(pop)
        new_tetromino = Tetromino(140,40,pop)
        move_group.add(new_tetromino)
        print(tetromino_list)
      
    #Zähler
    count = count + 1

    # Ermöglicht das Schließen per X
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
         
   

    
    # Updates und draws
    screen.blit(background_surface,(0,0))
    wall_group.draw(screen)
    move_group.update(wall_group)
    move_group.draw(screen)

    
    
    for wall in wall_group:
        if pygame.sprite.collide_mask(move_group.sprites()[0],wall):
            move_group.sprites()[0].rect.y = move_group.sprites()[0].rect.y - 20
            wall_group.add(move_group.sprites()[0])
            move_group.empty()
            break
  
    # Alle 40 frames bewegt sich das Tetromino nach unten
    if count % 60 == 0:
      
        if move_group.sprites()[0].can_move_down(wall_group, move_group):
            move_group.sprites()[0].rect.y = move_group.sprites()[0].rect.y + 20
        else:
            wall_group.add(move_group.sprites()[0])
            move_group.empty()
         

    # Standart Kram
    pygame.display.update()
    clock.tick(60)
