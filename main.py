import time
from pygame import mixer
import argparse
import os
from os import path
import json
import pygame
import sys
from mutagen.mp3 import MP3


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

def show_details():

	#file_data=os.path.splitext(user_input)
	total_length=0
	#if file_data[1] == '.mp3':
	audio = MP3(user_input+'.mp3')
	total_length=audio.info.length
	mins,secs=divmod(total_length,60)
	mins=round(mins)
	secs=round(secs)
	timeformat='{:02d}:{:02d}'.format(mins,secs)
	
	return timeformat

# creating display
display = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Juggling Balls')
clock = pygame.time.Clock()
# basic font for user typed
font_color=(0,150,250)
#songLength = (user_input+'.mp3').length
base_font = pygame.font.Font(None, 32)
#text_obj=base_font.render(user_input+'  '+show_details(),True,font_color)
text_obj=base_font.render(show_details(),True,font_color)
# pygame.draw.rect(display, (0,250,0),(150,450,100,50))
# pygame.draw.rect(display, red,(550,450,100,50))
# create rectangle
#input_rect = pygame.Rect(200, 200, 140, 32)

class button():
	def __init__(self, color, x,y, width,height, text=''):
		self.color=color
		self.x=x
		self.y=y
		self.width=width
		self.height=height
		self.text=text

	def draw(self,win,outline=None):
	#Call this method to draw the button on the screen
		if outline:
			pygame.draw.rect (display, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
			pygame.draw.rect (display, self.color, (self.x,self.y,self.width,self.height),0)

		if self.text != '':
			font = pygame.font.SysFont ('comicsans', 15)
			text = font.render (self.text, 1, (0,0,0))
			display.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))
	
	def isOver(self, pos):
	#Pos is the mouse position or a tuple of (x,y) coordinates
		if pos[0] > self.x and pos[0] < self.x + self.width:
			if pos[1] > self.y and pos[1] < self.y + self.height:
				return True
	
			return False

# def redrawWindow():
# 	#display.fill((255,255,255))
# 	greenButton.draw (display, (0,0,0))
	

greenButton = button((0,255,0), 20, 5, 80, 30, user_input+'.mp3')

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
	#redrawWindow()	
	pygame.display.update()
	display.fill((255,255,255))
	display.blit(text_obj,(110,10))
	greenButton.draw (display, (0,0,0))
	while True:
		
		# creating a loop to check events that
		# are occuring
		for event in pygame.event.get():

			pos = pygame.mouse.get_pos()

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
				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if greenButton.isOver(pos):
					print ('clicked the button')
			if event.type == pygame.MOUSEMOTION:
				if greenButton.isOver(pos):
					greenButton.color = (255,0,0)
				else:
					greenButton.color = (0,255,0)

main()