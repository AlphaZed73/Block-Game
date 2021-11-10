#imports and initialization
import pygame
from random import randint
pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption("AlphaZed's Block Game")
cube = pygame.image.load("true_art.jpg")

#mixer music (does not work in repl)
pygame.mixer.init()
pygame.mixer.music.load("Block game theme.wav")
pygame.mixer.music.set_volume(4.0)
pygame.mixer.music.play(0)

#variables and parameters
lives = 3
score = 0
player_x = 240
player_y = 460
player_width = 20
player_height = 30
speed = 8
isJump = False
jump_height = 7
jumpCount = jump_height
fallingblock_height = 20
fallingblock_width = 20
enemy_speed = 10
score_counter = 0
enemy_counter = 0
enemy_interval = randint(1, 4)
enemy_colors = []
min_red = 200
max_blue = 64
max_green = 64
epilepsy = False
window_fill = (0, 0, 0)
epilepsy_limit = 20
window_flash_time = randint(100, 400)

#tickspeed in milliseconds
tickspeed = 50

#matrix for enemy coords
block_coordinates = [
  [
  ],
  [
  ]
]

r_cube = pygame.transform.scale(cube, (fallingblock_width, fallingblock_height))
bg_cube = pygame.transform.scale(cube, (500, 500))

#scoreboard
font = pygame.font.Font('slkscr.ttf', 12)
font_large = pygame.font.Font('slkscr.ttf', 48)
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
    enemy_counter += 1
    #add new enemy after interval
    if enemy_counter == enemy_interval:
      block_coordinates[0].append(randint(0, 480))
      block_coordinates[1].append(0)
      enemy_colors.append((randint(min_red, 255), randint(0, max_green), randint(0, max_blue)))
      enemy_counter = 0
      enemy_interval = randint(1, 4)
  else:
    score_counter += 1
  
  #update score and lives on the scoreboard
  text = font.render(f"Score: {score} Lives: {lives}", True, (255, 255 , 255), (0, 0, 0))

  window_flash_time -= 1

  #quit button detection
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      run = False
  
  #left and right controls
  keys = pygame.key.get_pressed()
  if keys[pygame.K_LEFT]:
    player_x -= speed
  if keys[pygame.K_RIGHT]:
    player_x += speed

  if keys[pygame.K_BACKSLASH] and not epilepsy:
    epilepsy = True
    epilepsy_limit = 200
  if epilepsy_limit < 0:
    epilepsy = False
  if epilepsy:
    epilepsy_limit -= 1
  

  if player_x > 500 - player_width:
    player_x = 0
  if player_x < 0:
    player_x = 500 - player_width

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
  

  #update the screen and draw the character
  if epilepsy:
    window.fill((randint(0, 255), randint(0, 255), randint(0, 255)))
  else:
    window.fill(window_fill)
  
  pygame.draw.rect(window, (0, 255, 0), (player_x, player_y, player_width, player_height))

  if window_flash_time < 0:
    window.blit(bg_cube, (0, 0))
    window_flash_time = randint(100, 400)

  #draw enemies
  for enemy in range(0,len(block_coordinates[0])):
    pygame.draw.rect(window, enemy_colors[enemy], (block_coordinates[0][enemy], block_coordinates[1][enemy], fallingblock_width, fallingblock_height))
    if not epilepsy:
      window.blit(r_cube, (block_coordinates[0][enemy], block_coordinates[1][enemy]))
  
  #draw scoreboard
  window.blit(text, textRect)
  pygame.display.update()

  #enemy logic (collisions and moving to the top)
  for value in range(0,len(block_coordinates[1])):
    block_coordinates[1][value] += randint(1, enemy_speed)
    
    #move to top
    if block_coordinates[1][value] >= 480:
      block_coordinates[1][value] = 0
      block_coordinates[0][value] = randint(0, 480)
      
    if epilepsy:
      enemy_colors[value] = (randint(0, 255), randint(0, 255), randint(0, 255))

    #collisions
    enemy_hit_box = pygame.Rect(block_coordinates[0][value], block_coordinates[1][value], fallingblock_width, fallingblock_height)
    player_hit_box = pygame.Rect(player_x, player_y, player_width, player_height)
    collide = player_hit_box.colliderect(enemy_hit_box)
    #life check
    if collide == True:
      lives -= 1
      block_coordinates[1][value] = 0
      block_coordinates[0][value] = randint(0, 480)
      if lives <= 0:
        run = False

#end program and game over screen
font = pygame.font.Font('slkscr.ttf', 24)

text = font_large.render('Game Over', True, (0, 0, 0), (255, 255, 255))
text_score = font.render(f"Your Score: {score}", True, (0, 0, 0), (255, 255, 255))
# create a rectangular object for the
# text surface object
textRect = text.get_rect()
textRect_score = text_score.get_rect()
 
# set the center of the rectangular object.
textRect.center = (250, 250)
textRect_score.center = (250, 300)
window.fill((0, 0, 0))
window.blit(text_score, textRect_score)
window.blit(text, textRect)
pygame.display.update()
pygame.time.delay(5000)

pygame.quit()
quit()

