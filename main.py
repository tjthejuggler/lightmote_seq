import colorsys
from pdb import Restart
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
from socket import *
import struct
from tkinter.filedialog import asksaveasfile
from tkinter import *



udp_header = struct.pack("!bIBH", 66, 0, 0, 0)
s = socket(AF_INET, SOCK_DGRAM)
ball_size = 120

key_colors={}
color_codes={}
hex_color_codes={}
bar_length=1150
bar_start_position=20
total_length=1

#we can also do something about current time of the song = "3246" write "x,g,x"

#filename = fd.askopenfilename()

if path.exists('./key_color.txt'):	
	#print('file exists')		
	with open('./key_color.txt') as json_file:
		key_colors = json.load(json_file)

if path.exists('./color_codes.txt'):	
	#print('file exists')		
	with open('./color_codes.txt') as json_file:
		color_codes = json.load(json_file)

if path.exists('./hex_color_codes.txt'):	
	#print('file exists')		
	with open('./hex_color_codes.txt') as json_file:
		hex_color_codes = json.load(json_file)


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


	
	

def change_real_color(color_key, ball_number):
	hex_color = hex_color_codes[color_key]
	ip=''
	if ball_number==0:#35,172,237
		ip="85"#81,19,172,35,237,85
	if ball_number==1:
		ip="81"#81,19,172,35,237,85
	if ball_number==2:
		ip="19"#81,19,172,35,237,85	
	rgb = tuple(int(hex_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
	data = struct.pack("!BBBB", 0x0a, rgb[0], rgb[1], rgb[2])
	s.sendto(udp_header+data, ('192.168.43.'+ip, 41412))
	#("ball with ip "+ ip + " " + hex_color )



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
display = pygame.display.set_mode((1200, 450))
pygame.display.set_caption('Juggling Balls')
clock = pygame.time.Clock()
# basic font for user typed
font_color=(0,150,250)
#songLength = (user_input+'.mp3').length
base_font = pygame.font.Font(None, 32)
myfont = pygame.font.SysFont("comicsans", 20)

# render text


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
		pygame.draw.rect(display, self.color, (self.x, self.y, self.length, 30))
		#pygame.draw.line(display, (255,0,0),(22, 50), (22, 80), 5)

class color_circle():
	def __init__(self, color, x):
		self.color=color
		self.x=x

	def draw(self,win):
		pygame.draw.circle(display, self.color, (self.x, 350),70,0)

def draw_color_rects(temporary_color_codes):
	for key in temporary_color_codes:
		value = temporary_color_codes[key]
		for ball_number,color_letter in enumerate(value.split(",")):
			if color_letter!='x':	
				this_rgb_code=tuple(map(int,color_codes[color_letter].split(",")))
				y_cord =0
				if ball_number==0:
					y_cord = 100
				if ball_number==1:
					y_cord = 150
				if ball_number==2:
					y_cord = 200
				line_position=get_line_position(float(key)/1000,total_length)
				this_length = (bar_length+20)-line_position
				this_color_rect = color_rect(this_rgb_code, line_position, y_cord,this_length)
				this_color_rect.draw(display)

def draw_color_circles(colors):#colors=lıst
	for ball_number,color_letter in enumerate(colors):
		if color_letter!='x':
			rgb_code=tuple(map(int,color_codes[color_letter].split(",")))
			x_cord =0
			if ball_number==0:
				x_cord = 150
			if ball_number==1:
				x_cord = 350
			if ball_number==2:
				x_cord = 550
			this_color_circle = color_circle(rgb_code, x_cord)
			#this_color_circle.fill=(rgb_code)
			this_color_circle.draw(display)

class button():
	def __init__(self, color, x,y, width,height, text=''):
		self.color=color
		self.x=x
		self.y=y
		self.width=width
		self.height=height
		self.text=text

	def draw(self,win,outline=None):
	#Call this method to draw the button on the screen 20 50 1150 30 
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
loadButton = button((0,255,0), 1090, 5, 80, 30, 'LOAD')
saveasButton=button((0,255,0), 980, 5, 80, 30, 'Save As')
saveButton=button((0,255,0), 870, 5, 80, 30, 'Save')
restartButton=button((0,255,0), 1090, 250, 80, 30, 'Restart')

	

def get_line_position(current_song_timestamp,total_length):

	percent_through_song = (current_song_timestamp)/(total_length)
	line_position = (percent_through_song * bar_length)+bar_start_position
	return line_position

def get_song_position(x,total_length):
	x_position=(x-20)
	song_multiplier=x_position/bar_length
	return(song_multiplier*total_length)


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

def compare_current_time(temporary_color_codes,current_time_in_secs,color_circle_colors):
	for key in temporary_color_codes:
		value = temporary_color_codes[key]
		if int(int(key)/100)==int(current_time_in_secs*10):
			for index,color in enumerate(value.split(",")):
				if color!='x':
					color_circle_colors[index]=color
					change_real_color(color,index)
	
	return color_circle_colors

def sort_dict(my_dict):
    sorted_dict = sorted(my_dict.items(), key=lambda x: int(x[0]))
    return dict(sorted_dict)

def main():
# creating a running loop
	#redrawWindow()	
	color_circle_colors=["k","k","k"]
	# Drawing Rectangle
	global total_length
	temporary_color_codes={
	"1":"k,k,k"
	}
	pygame.display.update()
	f = "<No File Selected>"
	formatted_song_length =show_details()
	current_song_name=user_input
	label = myfont.render(current_song_name, 1, (0,0,0))
	song_offset = 0
	while True:
		temporary_color_codes = sort_dict(temporary_color_codes)
		current_time_in_secs=song_offset + pygame.mixer.music.get_pos()/1000
		minutes = math.floor(current_time_in_secs/60)
		seconds = math.floor(current_time_in_secs %60)
		formatted_current_time='{:02d}:{:02d}'.format(minutes,seconds)
		display.fill((255,255,255))
		text_obj=base_font.render(formatted_song_length,True,font_color)
		text_time=base_font.render(formatted_current_time,True,font_color)
		if formatted_current_time==formatted_song_length:
			formatted_current_time=='{:00}:{:00}'
		display.blit(text_obj,(180,10))
		display.blit(text_time,(110,10))
		display.blit(label, (760, 6))
		greenButton.draw(display, (0,0,0))
		loadButton.draw (display, (0,0,0))
		saveasButton.draw (display, (0,0,0))
		saveButton.draw (display, (0,0,0))
		restartButton.draw (display, (0,0,0))
		#green.draw(display)
		draw_color_rects(temporary_color_codes)
		draw_color_circles(color_circle_colors)
		color_circle_colors = compare_current_time(temporary_color_codes,current_time_in_secs,color_circle_colors)
		line_position=get_line_position(current_time_in_secs,total_length)
		pygame.draw.line(display, (255,0,0),(line_position, 50), (line_position, 80), 5)
		pygame.display.update()
		# creating a loop to check events that
		# are occuring

		for event in pygame.event.get():

			pos = pygame.mouse.get_pos()
			
			if event.type == pygame.QUIT:
				#print(file_name)
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
				if pygame.key.get_mods() & pygame.KMOD_LCTRL:
					print ("pressed: ctrl + "+pygame.key.name(event.key))
				if str(event.unicode) in key_colors and mixer.music.get_busy():
					# print(str(event))
					# with open(file_name, "r") as file:
					# 	current = file.read()
					# with open(file_name, "w+") as file:
					content = key_colors[str(event.unicode)]
					timestamp = str(int(song_offset*1000) + pygame.mixer.music.get_pos())
					# 	file.writelines(current + '"' + timestamp + '" : "' + content + '",\n')
					temporary_color_codes[timestamp] = content
					
					for ball_number,color_letter in enumerate(content.split(",")):
						if color_letter!='x':
							change_real_color(color_letter,ball_number)
							color_circle_colors[ball_number]=color_letter
				
				# if event.key == pygame.K_LCTRL:
				# 	print("ctrl is pressed")
					# keys = pygame.key.get_pressed()
					# if keys[pygame.K_LCTRL] and keys[pygame.K_f]:
					# 	print("ctrl AND F are pressed")
			

								
				if event.key == pygame.K_SPACE and not mixer.music.get_busy():
					mixer.init()
					mixer.music.load(current_song_name+'.mp3')
					mixer.music.set_volume(0.8)
					mixer.music.play()
					#file_name=create_file(current_song_name)
					# with  open(file_name, "w") as file:
					# 	line=['{\n']
					# 	file.writelines(line)
					#while mixer.music.get_busy():
				elif event.key == pygame.K_SPACE and mixer.music.get_busy():
					pygame.mixer.music.pause()
					# if os.path.getsize(file_name) != 0:
					# 	with  open(file_name, "r") as file:
					# 		current = file.read()
					# 	with  open(file_name, "w") as file:
					# 		file.writelines('{\n'+ current[:-2] + '\n}')
					# else:
					# 	os.remove(file_name)

				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if greenButton.isOver(pos):
					#print ('clicked the button')
					path_of_user_selected_file = prompt_file()
					user_selected_file = path_of_user_selected_file.split("/")[-1]
					greenButton.text = user_selected_file
					pygame.mixer.music.pause()
					current_song_name=user_selected_file.split(".mp3")[0]
					file_name=create_file(current_song_name)
					print (f)
					audio = MP3(user_selected_file)
					total_length=audio.info.length
					mins,secs=divmod(total_length,60)
					mins=math.floor(mins)
					secs=math.floor(secs)
					formatted_song_length='{:02d}:{:02d}'.format(mins,secs)
				if loadButton.isOver(pos):
					path_of_user_selected_file = prompt_file()
					user_selected_file = path_of_user_selected_file.split("/")[-1]
					label = myfont.render(user_selected_file.split(".txt")[0], 1, (0,0,0))
					#textButton.text = user_selected_file.split(".txt")[0]
					#temporary_color_codes=(user_selected_file_2.split(".txt")[0])
					if path.exists(path_of_user_selected_file):	
						#print('file exists')		
						with open(path_of_user_selected_file) as json_file:
							temporary_color_codes = json.load(json_file)
				if saveasButton.isOver(pos):
					f = asksaveasfile(initialfile = 'Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
					print('f.name',f.name)
					with open(f.name, 'w') as fp:
						json.dump(temporary_color_codes, fp,indent = 6)
						label = myfont.render(f.name.split(".txt")[0].split("/")[-1], 1, (0,0,0))
						fp.close()
				
				if saveButton.isOver(pos):
					with open(f.name, 'w') as fp:
						json.dump(temporary_color_codes, fp)
					print(f.name)
					if os.path.getsize(f.name) != 0:
						with  open(f.name, "r") as file:
							current = file.read()
							if os.path.getsize(f.name) == 0:
								file.close()
								os.remove(f.name)
							else:
								print('File is not empty')
								out_file = open(f.name, "w")
  
								json.dump(temporary_color_codes, out_file, indent = 6)
								
								out_file.close()

				if restartButton.isOver(pos):
					pygame.mixer.music.pause()
					temporary_color_codes={
					"1":"k,k,k"
					}
					color_circle_colors=["k","k","k"]

					

			if event.type == pygame.MOUSEMOTION:
				if greenButton.isOver(pos):
					greenButton.color = (255,0,0)
				else:
					greenButton.color = (0,255,0)

			if event.type == pygame.MOUSEBUTTONUP:
				x,y=pos
				if 20<x<1170 and 50<y<80:
					print(pos)
					pygame.mixer.music.play(0,(get_song_position(x,total_length)))
					song_offset = get_song_position(x,total_length)
main()