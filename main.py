#imports and initialization
import pygame
from random import randint
pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("AlphaZed's Block Game")

#mixer music
pygame.mixer.init()
pygame.mixer.music.load("theme.mp3")
pygame.mixer.music.play(-1)

#variables and parameters
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
score_counter = 0

#tickspeed in milliseconds
tickspeed = 50

#matrix for enemy coords
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

#scoreboard
font = pygame.font.Font('slkscr.ttf', 12)
text = font.render(f"Score: {score} Lives: {lives}", True, (255, 255 , 255), (0, 0, 0))

textRect = text.get_rect()
textRect.center = (70, 10)

run = True

#run loop
while run:
  #slows down the program to not crash computer
  pygame.time.delay(tickspeed)

  #timer
  if score_counter == 1000 / tickspeed:
    score_counter = 0
    score += 1
  else:
    score_counter += 1
  
  #update score and lives on the scoreboard
  text = font.render(f"Score: {score} Lives: {lives}", True, (255, 255 , 255), (0, 0, 0))

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
    block_coordinates[1][value] += randint(1, enemy_speed)

    #move to top
    if block_coordinates[1][value] >= 480:
      block_coordinates[1][value] = 0
      block_coordinates[0][value] = randint(0,480)


    #collisions (WIP)
    #use the website in the README. It has much simpler methods for getting collisions. 
    """
    if block_coordinates[1][value] >= player_y + player_height and block_coordinates[1][value] <= player_y and block_coordinates[0][value] >= player_y + player_height:
  
    for x in range(player_x,player_x+20):
      for y in range(player_y,player_y+30):
        if x in range(block_coordinates[0][value],block_coordinates[0][value]+20) and y in range(block_coordinates[1][value],block_coordinates[1][value]+20):
          lives -=1
          block_coordinates[1][value]=0
          block_coordinates[0][value]=randint(0,480)"""

    #life check
    if lives <= 0:
        pygame.quit()
        quit()

  #update the screen and draw the character
  window.fill((0, 0, 0))
  pygame.draw.rect(window, (0, 255, 0), (player_x, player_y, player_width, player_height))

  #draw enemies
  for enemy in range(0,4):
    pygame.draw.rect(window, (255, 0, 0), (block_coordinates[0][enemy], block_coordinates[1][enemy], fallingblock_width, fallingblock_height))
  
  #draw scoreboard
  window.blit(text, textRect)
  pygame.display.update()

#end program
pygame.quit()
quit()

