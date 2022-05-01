import time
from pygame import mixer
import argparse

#user_input=input('Please write the name of the song that you would like to listen to ')


# mixer.init()
# mixer.music.load(user_input +'.mp3')
# mixer.music.set_volume(0.8)
# mixer.music.play()
# while mixer.music.get_busy():
#     time.sleep(1)



parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="the base prompt (comma seperate each weighted section")
args = parser.parse_args()
user_input = args.prompt+'.mp3'
	


# import the pygame module
# import pygame

# # Define the background colour
# # using RGB color coding.
# background_colour = (234, 212, 252)

# # Define the dimensions of
# # screen object(width,height)
# screen = pygame.display.set_mode((300, 300))

# # Set the caption of the screen
# pygame.display.set_caption('Geeksforgeeks')

# # Fill the background colour to the screen
# screen.fill(background_colour)

# # Update the display using flip
# pygame.display.flip()

# # Variable to keep our game loop running
# running = True

# # game loop
# while running:
	
# # for loop through the event queue
# 	for event in pygame.event.get():
	
# 		# Check for QUIT event	
# 		if event.type == pygame.QUIT:
# 			running = False





# # 1: Import the library pygame
# import pygame
# from pygame.locals import *
# # 2: Initiate pygame 
# pygame.init()
# pygame.font.init()
# # 3: Determine the size of the playing field
# width, height = 64*10, 64*8
# screen=pygame.display.set_mode((width, height))
# # 4: Create x and y position for the player
# # player_x = 200
# # player_y = 200
# # 5: Import Images
# #player = pygame.image.load("hero.png")
# # 6: Create while loop that don't end
# while 1:
#     # 7: Illustrate a white board
#     screen.fill((255,255,255))
#     # 8: Draw the image player on an x, y coordinate
#     #screen.blit(player, (player_x, player_y))
#     # 9: Update the playing field
#     pygame.display.flip()
#     # 10: Process all new events


#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit() 
#             exit(0)

#     if event.type == pygame.KEYDOWN:
#         if event.key==pygame.K_UP:
#             print("U")
#         elif event.key==pygame.K_LEFT:
#             print("L")
#         elif event.key==pygame.K_DOWN:
#             print("D")
#         elif event.key==pygame.K_RIGHT:
#             print("R")





import pygame
 
# importing sys module
import sys


# initialising pygame
pygame.init()
 
# creating display
display = pygame.display.set_mode((300, 300))

# creating a running loop
while True:
       
    # creating a loop to check events that
    # are occuring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()



        # checking if keydown event happened or not
        if event.type == pygame.KEYDOWN:
           
            # if keydown event happened
            # than printing a string to output
            #print(event.unicode)

            with  open("MyFile.txt", "r") as file:
                current = file.read()

            with  open("MyFile.txt", "w+") as file:
                content = str(event.unicode)
                file.writelines(current + content +'\n')

            if event.key == pygame.K_SPACE:
                mixer.init()
                mixer.music.load(user_input)
                mixer.music.set_volume(0.8)
                mixer.music.play()
                # while mixer.music.get_busy():
                #     time.sleep(1)
               

            if event.key==pygame.K_UP:
                print("U")
            elif event.key==pygame.K_LEFT:
                print("L")
            elif event.key==pygame.K_DOWN:
                print("D")
            elif event.key==pygame.K_RIGHT:
                print("R")

