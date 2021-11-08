import pygame
from random import randint
pygame.init()

window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("AlphaZed's Block Game")

#variables
lives = 10
score = 0
player_x = 10
player_y = 460
player_width = 20
player_height = 30
speed = 5
isJump = False
jump_height = 7
jumpCount = jump_height
fallingblock_height = 20
fallingblock_width = 20
enemy_speed = 10

#matrix
block_coordinates = [
  [
    0, 0, 0, 0
  ],
  [
    0, 0, 0, 0
  ]
]
for coord in range(0,len(block_coordinates[0])):
  block_coordinates[0][coord] = randint(0,480)


run = True
print(block_coordinates)
#run loop
while run:
  #slows down the program to not crash computer
  pygame.time.delay(50)

  #quit button detection
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  
  #left and right controls
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT] and player_x > 0:
    player_x -= speed
  if keys[pygame.K_RIGHT] and player_x < 500 - player_width:
    player_x += speed
  
  #jumping controls
  if not isJump:
    """
    if keys[pygame.K_UP] and y > 0:
      y -= speed
    if keys[pygame.K_DOWN] and y < 500 - player_height:
      y += speed
    """
    if keys[pygame.K_UP]:
      isJump = True
  else:
    if jumpCount >= -jump_height:
      neg = 1
      if jumpCount < 0:
        neg = -1
      player_y -= (jumpCount ** 2) * 0.5 * neg
      jumpCount -= 1
    else:
      isJump = False
      jumpCount = jump_height
  
  #enemy logic (collisions and moving to the top)
  for value in range(0,len(block_coordinates[1])):
    block_coordinates[1][value] += randint(1,enemy_speed)
    if block_coordinates[1][value] >= 480:
      block_coordinates[1][value] = 0
      block_coordinates[0][value] = randint(0,480)


#collisions
    if block_coordinates[1][value] >= player_y + player_height and block_coordinates[1][value] <= player_y and block_coordinates[0][value] >= player_y + player_height:
      lives -=1
      block_coordinates[1][value]=0
      block_coordinates[0][value]=randint(0,480)
    if lives <= 0:
        pygame.quit()
        quit()
  #update the screen and draw the character
  window.fill((0, 0, 0))
  pygame.draw.rect(window, (0, 255, 0), (player_x, player_y, player_width, player_height))

  #draw enemies
  for enemy in range(0,4):
    pygame.draw.rect(window, (255, 0, 0), (block_coordinates[0][enemy], block_coordinates[1][enemy], fallingblock_width, fallingblock_height))
 
  print(lives)
  pygame.display.update()

pygame.quit()
quit()