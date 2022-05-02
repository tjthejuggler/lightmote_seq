import time
from pygame import mixer
import argparse
from os import path
import json
import pygame
import sys

key_colors={}

if path.exists('./key_color.txt'):	
	#print('file exists')		
	with open('./key_color.txt') as json_file:
		key_colors = json.load(json_file)
		
parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="the base prompt (comma seperate each weighted section")
#parser.add_argument("songname", help="enter the name of the song")
args = parser.parse_args()
#song_name=args.songname
user_input = args.prompt

pygame.init()

# creating display
display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Juggling Balls')
clock = pygame.time.Clock()
# basic font for user typed
font_color=(0,150,250)
base_font = pygame.font.Font(None, 32)
text_obj=base_font.render(user_input,True,font_color)
# create rectangle
#input_rect = pygame.Rect(200, 200, 140, 32)

def create_file():
	file_name=''
	count=0
	looking_for_file=True
	while looking_for_file:
				
		if path.exists(user_input +'('+str(count)+').txt'):	
			count+=1
		else:
			looking_for_file=False
			file_name=user_input +'('+str(count)+').txt'
			open(file_name, "w") 

	return file_name


def main():
# creating a running loop
	display.fill((255,255,255))
	display.blit(text_obj,(22,0))
	while True:

		# creating a loop to check events that
		# are occuring
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			pygame.display.update()
			# checking if keydown event happened or not
			if event.type == pygame.KEYDOWN:
			
				# if keydown event happened
				# than printing a string to output
				#print(event.unicode)   
				current=''
				timestamp=''
				content=''

				if str(event.unicode) in key_colors:

					with open(file_name, "r") as file:
						current = file.read()
					with open(file_name, "w+") as file:
						content = key_colors[str(event.unicode)]
						timestamp = str(pygame.mixer.music.get_pos())
						file.writelines(current + '"' + timestamp + '" : "' + content + '",\n')
					
				
				if event.key == pygame.K_SPACE and not mixer.music.get_busy():
					mixer.init()
					mixer.music.load(user_input+'.mp3')
					mixer.music.set_volume(0.8)
					mixer.music.play()
					file_name=create_file()
					with  open(file_name, "w") as file:
						line=['{\n']
						file.writelines(line)
					#while mixer.music.get_busy():
				elif event.key == pygame.K_SPACE and mixer.music.get_busy():
					pygame.mixer.music.pause()
					with  open(file_name, "r") as file:
						current = file.read()
					with  open(file_name, "w") as file:
						file.writelines(current[:-2] + '\n}')

main()