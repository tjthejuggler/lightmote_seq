import time
from pygame import mixer
import argparse
from os import path
import json
import pygame
import sys

key_colors={}

if path.exists('./key_color.txt'):	
	print('file exists')		
	with open('./key_color.txt') as json_file:
		key_colors = json.load(json_file)


parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="the base prompt (comma seperate each weighted section")
args = parser.parse_args()
user_input = args.prompt

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
            current=''
            timestamp=''
            content=''
            if str(event.unicode) in key_colors:
                
                with  open(user_input+'.txt', "r") as file:
                    current = file.read()

                with  open(user_input+'.txt', "w+") as file:
                    content = key_colors[str(event.unicode)]
                    timestamp = str(pygame.mixer.music.get_pos())
                    file.writelines(current + '"' + timestamp + '" : "' + content + '",\n')
                
            
            if event.key == pygame.K_SPACE and not mixer.music.get_busy():
                mixer.init()
                mixer.music.load(user_input+'.mp3')
                mixer.music.set_volume(0.8)
                mixer.music.play()
                with  open(user_input+'.txt', "w") as file:
                    line=['{\n']
                    file.writelines(line)
                #while mixer.music.get_busy():
            elif event.key == pygame.K_SPACE and mixer.music.get_busy():
                pygame.mixer.music.pause()
                with  open(user_input+'.txt', "r") as file:
                    current = file.read()
                with  open(user_input+'.txt', "w") as file:
                    file.writelines(current + '\n}')

