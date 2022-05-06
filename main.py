import time
from numpy import timedelta64
from pygame import mixer
import argparse
import os
from os import path
import json
import pygame
import sys
from mutagen.mp3 import MP3
#from tkinter import filedialog as fd
import tkinter
import tkinter.filedialog
import pygame
import tkinter.ttk as ttk
import math 

key_colors={}
color_codes={}
bar_length=1150
bar_start_position=20
total_length=1
temporary_color_codes={

}



#filename = fd.askopenfilename()

if path.exists('./key_color.txt'):	
	#print('file exists')		
	with open('./key_color.txt') as json_file:
		key_colors = json.load(json_file)

if path.exists('./color_codes.txt'):	
	#print('file exists')		
	with open('./color_codes.txt') as json_file:
		color_codes = json.load(json_file)


parser = argparse.ArgumentParser()
parser.add_argument("prompt", help="the base prompt (comma seperate each weighted section")
#parser.add_argument("songname", help="enter the name of the song")
args = parser.parse_args()
#song_name=args.songname
user_input = args.prompt

pygame.init()

# def slide():
# 	pass
# #create music position slider
# my_slider=ttk.Scale(from_=0,to=100,orient=tkinter.HORIZONTAL,value=0,command=slide)
# my_slider.pack(pady=20)	

def prompt_file():
    #"""Create a Tk file dialog and cleanup when finished"""
    top = tkinter.Tk()
    top.withdraw()  # hide window
    file_name = tkinter.filedialog.askopenfilename(parent=top)
    top.destroy()
    return file_name


def show_details():
	global total_length
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
display = pygame.display.set_mode((1200, 300))
pygame.display.set_caption('Juggling Balls')
clock = pygame.time.Clock()
# basic font for user typed
font_color=(0,150,250)
#songLength = (user_input+'.mp3').length
base_font = pygame.font.Font(None, 32)

#text_obj=base_font.render(user_input+'  '+show_details(),True,font_color)
# text_obj=base_font.render(show_details(),True,font_color)
# pygame.draw.rect(display, (0,250,0),(150,450,100,50))
# pygame.draw.rect(display, red,(550,450,100,50))
# create rectangle
#input_rect = pygame.Rect(200, 200, 140, 32)


class color_rect():
	def __init__(self, color, x,y,length):
		self.color=color
		self.x=x
		self.y=y
		self.length=length

	def draw(self,win):
		outline=(255,255,255)
	#Call this method to draw the button on the screen
		# pygame.draw.rect (display, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
		# pygame.draw.rect (display, self.color, (self.x,self.y,self.width,self.height),0)
		# pygame.draw.rect (display, outline, (bar_start_position-2,50-2,bar_length+4,30+4),0)
		# pygame.draw.rect(display, (255,255,255), (bar_start_position, 50, bar_length, 30))
		# pygame.draw.rect (display, outline, (bar_start_position-2,100-2,bar_length+4,30+4),0)
		# pygame.draw.rect(display, (255,255,255), (bar_start_position, 100, bar_length, 30))
		# pygame.draw.rect (display, outline, (bar_start_position-2,150-2,bar_length+4,30+4),0)
		# pygame.draw.rect(display, (255,255,255), (bar_start_position, 150, bar_length, 30))
		pygame.draw.rect (display, outline, (self.x-2,self.y-2,self.length+4,30+4),0)
		pygame.draw.rect(display, self.color, (self.x, self.y, self.length, 30))
		#pygame.draw.line(display, (255,0,0),(22, 50), (22, 80), 5)

def draw_color_rects():
	previous_end_xs = [20,20,20]
	previous_colors=['k','k','k']
	sortedlist=[(k,temporary_color_codes[k]) for k in sorted(temporary_color_codes)]
	for key in temporary_color_codes:
		value = temporary_color_codes[key]
		for ball_number,color_letter in enumerate(value.split(",")):
			if color_letter!='x':	
				this_rgb_code=tuple(map(int,color_codes[previous_colors[ball_number]].split(",")))
				y_cord =0
				if ball_number==0:
					y_cord = 100
				if ball_number==1:
					y_cord = 150
				if ball_number==2:
					y_cord = 200
				this_length = get_line_position(float(key)/1000,total_length)
				min_length = min(this_length,bar_length-previous_end_xs[ball_number]+22)
				this_color_rect = color_rect(this_rgb_code, previous_end_xs[ball_number], y_cord,min_length)
				previous_end_xs[ball_number] = this_length
				previous_colors[ball_number] = color_letter
				this_color_rect.draw(display)



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
			pygame.draw.rect (display, outline, (bar_start_position-2,50-2,bar_length+4,30+4),0)
			pygame.draw.rect(display, (255,255,255), (bar_start_position, 50, bar_length, 30))
			pygame.draw.rect (display, outline, (bar_start_position-2,100-2,bar_length+4,30+4),0)
			pygame.draw.rect(display, (255,255,255), (bar_start_position, 100, bar_length, 30))
			pygame.draw.rect (display, outline, (bar_start_position-2,150-2,bar_length+4,30+4),0)
			pygame.draw.rect(display, (255,255,255), (bar_start_position, 150, bar_length, 30))
			pygame.draw.rect (display, outline, (bar_start_position-2,200-2,bar_length+4,30+4),0)
			pygame.draw.rect(display, (255,255,255), (bar_start_position, 200, bar_length, 30))
			#pygame.draw.line(display, (255,0,0),(22, 50), (22, 80), 5)

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

def get_line_position(current_song_timestamp,total_length):

	percent_through_song = (current_song_timestamp)/(total_length)
	line_position = (percent_through_song * bar_length)+bar_start_position
	return line_position

def create_file(song_name):
	file_name=''
	count=0
	looking_for_file=True
	while looking_for_file:
			
		if path.exists('./texts/'+ song_name +'('+str(count)+').txt'):	
			count+=1
		else:
			looking_for_file=False
			file_name='./texts/'+song_name +'('+str(count)+').txt'
			open(file_name, "w") 

	return file_name

def make_color_rect(ball_numbers,colors,color_rect_list,line_position):

	pygame.draw.rect(display, (255,255,255), (bar_start_position, 100, bar_length, 30))
	pygame.draw.rect(display, (255,255,255), (bar_start_position, 150, bar_length, 30))
	pygame.draw.rect(display, (255,255,255), (bar_start_position, 200, bar_length, 30))


	return color_rect_list

def main():
# creating a running loop
	#redrawWindow()	
	
	# Drawing Rectangle
	global total_length
	pygame.display.update()
	greenButton.draw (display, (0,0,0))
	f = "<No File Selected>"
	formatted_song_length =show_details()
	current_song_name=user_input
	while True:
		current_time_in_secs=pygame.mixer.music.get_pos()/1000
		minutes = math.floor(current_time_in_secs/60)
		seconds = math.floor(current_time_in_secs %60)
		formatted_current_time='{:02d}:{:02d}'.format(minutes,seconds)
		display.fill((255,255,255))
		draw_color_rects()
		text_obj=base_font.render(formatted_song_length,True,font_color)
		text_time=base_font.render(formatted_current_time,True,font_color)
		if formatted_current_time==formatted_song_length:
			formatted_current_time=='{:00}:{:00}'
		display.blit(text_obj,(180,10))
		display.blit(text_time,(110,10))
		greenButton.draw(display, (0,0,0))
		draw_color_rects()
		#green.draw(display)
		line_position=get_line_position(current_time_in_secs,total_length)
		pygame.draw.line(display, (255,0,0),(line_position, 50), (line_position, 80), 5)
		pygame.display.update()
		# creating a loop to check events that
		# are occuring
		for event in pygame.event.get():

			pos = pygame.mouse.get_pos()
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			#pygame.display.update()
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
						temporary_color_codes[timestamp] = content

								
				if event.key == pygame.K_SPACE and not mixer.music.get_busy():
					mixer.init()
					mixer.music.load(current_song_name+'.mp3')
					mixer.music.set_volume(0.8)
					mixer.music.play()
					file_name=create_file(current_song_name)
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
					#print ('clicked the button')
					path_of_user_selected_file = prompt_file()
					user_selected_file = path_of_user_selected_file.split("/")[-1]
					greenButton.text = user_selected_file
					pygame.mixer.music.pause()
					current_song_name=user_selected_file.split(".mp3")[0]
					# mixer.init()
					# mixer.music.load(user_selected_file)
					# mixer.music.set_volume(0.8)
					# mixer.music.play()
					file_name=create_file(current_song_name)
					# greenButton = button((0,255,0), 20, 5, 80, 30, f)
					# greenButton.draw (display, (0,0,0))
					print (f)
					
					#if file_data[1] == '.mp3':
					audio = MP3(user_selected_file)
					total_length=audio.info.length
					mins,secs=divmod(total_length,60)
					mins=math.floor(mins)
					secs=math.floor(secs)
					formatted_song_length='{:02d}:{:02d}'.format(mins,secs)
					# display.blit(text_obj,(110,10))
					# text_obj=base_font.render(timeformat,True,font_color)
			if event.type == pygame.MOUSEMOTION:
				if greenButton.isOver(pos):
					greenButton.color = (255,0,0)
				else:
					greenButton.color = (0,255,0)

main()