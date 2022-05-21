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
import pygame_textinput
from notifypy import Notify


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

text_input_font = pygame.font.SysFont("comicsans", 15)
manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 19)
textinput = pygame_textinput.TextInputVisualizer(manager=manager,font_object=text_input_font)

number_input_font = pygame.font.SysFont("comicsans", 15)
manager = pygame_textinput.TextInputManager(validator = lambda input: len(input) <= 4)
strobeinput = pygame_textinput.TextInputVisualizer(manager=manager,font_object=number_input_font)
# def slide():
# 	pass
# #create music position slider
# my_slider=ttk.Scale(from_=0,to=100,orient=tkinter.HORIZONTAL,value=0,command=slide)
# my_slider.pack(pady=20)	


	
	

def change_real_color(rgb_color, ball_number):
	#print("rgb_color",rgb_color)
	#print("hex_color_codes",hex_color_codes)

	color_code = [ int(x) for x in rgb_color.split(',') ]
	rgb_code=tuple(color_code)

	hex_color = '#%02x%02x%02x' % rgb_code
	#hex_color = hex_color_codes[rgb_color]
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

def notification_message(message):
	notification = Notify()
	notification.title = "Juggling Balls"
	notification.message = message
	notification.send()

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
	audio = MP3('./MP3 Song File/'+user_input+'.mp3')
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
		#print(self.color)
		pygame.draw.rect(display, self.color, (self.x, self.y, self.length, 30))
		# if need_line:
		# 	pygame.draw.line(display, self.color,(self.x+2, self.y), (self.x+2,self.y-10),5)

class color_circle():
	def __init__(self, color, x):
		self.color=color
		self.x=x

	def draw(self,win,outline=None):
		#pygame.draw.circle (display, outline,(self.x-2,348),74,)
		pygame.draw.circle(display, self.color, (self.x, 350),70,0)
		pygame.draw.circle(display, (0,0,0), (self.x, 350),71,2)


def draw_color_rects(temporary_color_codes):
	#previous_this_rgb_code=[(0,0,0),(0,0,0),(0,0,0)]
	for key in temporary_color_codes:
		value = temporary_color_codes[key]
		#print("value",value)
		
		for ball_number,color_code in enumerate(value.split(";")):
			if color_code!='x':	
				#print("color_code",color_code)
				color_code = [ int(x) for x in color_code.split(',') ]
				this_rgb_code=tuple(color_code)
				
				#print("this_rgb_code",this_rgb_code)
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
				this_color_rect.draw(display)#,this_rgb_code==previous_this_rgb_code[ball_number]
				#previous_this_rgb_code[ball_number]=this_rgb_code

def draw_color_circles(colors):#colors=lıst
	for ball_number,color_code in enumerate(colors):
		if color_code!='x':
			color_code = [ int(x) for x in color_code.split(',') ]
			rgb_code=tuple(color_code)
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
			pygame.draw.rect(display, (255,255,255), (bar_start_position, 200, bar_length, 30)),

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
# 	loadSongButton.draw (display, (0,0,0))
	

loadSongButton = button((0,255,0), 20, 5, 80, 30, user_input+'.mp3')
loadButton = button((0,255,0), 1090, 5, 80, 30, 'LOAD')
#saveasButton=button((0,255,0), 980, 5, 80, 30, 'Save As')
saveButton=button((0,255,0), 980, 5, 80, 30, 'Save')
restartButton=button((0,255,0), 1090, 250, 80, 30, 'Restart')
textinputButton=button((255,255,255), 790, 5, 160, 30, '')
strobeinputButton=button((255,255,255), 710, 5, 50, 30, '')


	

def get_line_position(current_song_timestamp,total_length):

	percent_through_song = (current_song_timestamp)/(total_length)
	line_position = (percent_through_song * bar_length)+bar_start_position
	return line_position

def get_song_position(x,total_length):
	x_position=(x-20)
	song_multiplier=x_position/bar_length
	return(song_multiplier*total_length)


def create_file (textinput):
	file_name=''
	count=0
	looking_for_file=True
	while looking_for_file:
			
		if path.exists('./texts/'+  textinput +'.txt'):	
			count+=1
		else:
			looking_for_file=False
			file_name='./texts/'+ textinput +'.txt'
			open(file_name, "w") 

	return file_name

def make_color_rect(ball_numbers,colors,color_rect_list,line_position):

	pygame.draw.rect(display, (255,255,255), (bar_start_position, 100, bar_length, 30))
	pygame.draw.rect(display, (255,255,255), (bar_start_position, 150, bar_length, 30))
	pygame.draw.rect(display, (255,255,255), (bar_start_position, 200, bar_length, 30))


	return color_rect_list

def change_circle_and_real_colors_if_needed(temporary_color_codes,current_time_in_secs,color_circle_colors):
	for key in temporary_color_codes:
		value = temporary_color_codes[key]
		if int(int(key)/100)==int(current_time_in_secs*10):
			for index,color in enumerate(value.split(";")):
				if color!='x':
					color_circle_colors[index]=color
					change_real_color(color,index)
	
	return color_circle_colors

def sort_dict(my_dict):
    sorted_dict = sorted(my_dict.items(), key=lambda x: int(x[0]))
    return dict(sorted_dict)

def combine_dict_values_for_strobe(item1, item2):
	split_new_item = ['x','x','x']
	split_item1 = item1.split(';')
	split_item2 = item2.split(';')
	for i in range (0,3):
		if split_item1[i] != 'x':
			split_new_item[i] = split_item1[i]
		if split_item2[i] != 'x':
			split_new_item[i] = split_item2[i]
	return ";".join(split_new_item)

def add_strobes(temporary_color_codes, color, ball_number, timestamp, strobe_end_time):
	print("color", color, ball_number)
	new_temporary_color_codes = temporary_color_codes
	next_strobe_time=int(timestamp)
	next_strobe_is_color=True
	split_strobe_color_content = ['x','x','x']
	split_strobe_color_content[ball_number] = color
	strobe_color_content = ";".join(split_strobe_color_content)
	split_strobe_black_content = ['x','x','x']
	split_strobe_black_content[ball_number] = '0,0,0'
	strobe_black_content = ";".join(split_strobe_black_content)
	while next_strobe_time<strobe_end_time:	
		print("color", color, ball_number, next_strobe_time)	
		strobe_to_add = strobe_black_content						
		if next_strobe_is_color:
			strobe_to_add = strobe_color_content
		if next_strobe_time in temporary_color_codes:
			strobe_to_add = combine_dict_values_for_strobe(temporary_color_codes[next_strobe_time], strobe_to_add)
		temporary_color_codes[next_strobe_time] = strobe_to_add
		next_strobe_is_color = not next_strobe_is_color
		next_strobe_time+=int(1000/float(strobeinput.value))	
	return new_temporary_color_codes

def calculate_fade(start_time,end_time,start_color,end_color):
	print("jj",start_time,end_time,start_color,end_color)
	fade_time_increment = 500
	total_steps = int((end_time - start_time) / fade_time_increment)
	if total_steps == 0:
		total_steps = 1
	fade_dictionary={}
	start_color_r = int(start_color.split(",")[0])
	start_color_g = int(start_color.split(",")[1])
	start_color_b = int(start_color.split(",")[2])
	end_color_r = int(end_color.split(",")[0])
	end_color_g = int(end_color.split(",")[1])
	end_color_b = int(end_color.split(",")[2])
	step_size_r = (end_color_r - start_color_r) / total_steps 
	step_size_g = (end_color_g - start_color_g) / total_steps 
	step_size_b = (end_color_b - start_color_b) / total_steps 
	# start_rgb_code=tuple(map(int,color_codes[start_color].split(",")))
	# end_rgb_code=tuple(map(int,color_codes[end_color].split(",")))
	current_step = 0
	while current_step <= total_steps:		
		new_r = int(start_color_r + (step_size_r*current_step))
		new_g = int(start_color_g + (step_size_g*current_step))
		new_b = int(start_color_b + (step_size_b*current_step))
		color_fade_time = start_time + (fade_time_increment*current_step)
		fade_dictionary[color_fade_time] = str(new_r) + "," + str(new_g) + "," + str(new_b)
		current_step += 1
	return fade_dictionary
	print("fade_dictionary", fade_dictionary)
#calculate_fade(0,20000,"255,127,0","0,0,0")
def add_timestamp_to_temporary_color_codes(timestamp,temporary_color_codes,content):
	
	if timestamp in temporary_color_codes:
		new_item=combine_dict_values_for_strobe(temporary_color_codes[timestamp],content)
		temporary_color_codes[timestamp]=new_item
	else:
		temporary_color_codes[timestamp] = content

	return temporary_color_codes

def main():
# creating a running loop
	#redrawWindow()	
	color_circle_colors=["0,0,0","0,0,0","0,0,0"]
	# Drawing Rectangle
	global total_length
	temporary_color_codes={	"1":"0,0,0;0,0,0;0,0,0"	}
	pygame.display.update()
	text_file = "<No File Selected>"
	formatted_song_length =show_details()
	current_song_name=user_input
	#label = myfont.render(current_song_name, 1, (0,0,0))
	song_offset = 0
	mixer.init()
	mixer.music.load('./MP3 Song File/'+current_song_name+'.mp3')
	mixer.music.set_volume(0.8)
	textinput.value='default'
	strobeinput.value='2'
	while True:
		# print("song_offset",song_offset)
		# print("pygame.mixer.music.get_pos()",pygame.mixer.music.get_pos())
		textinput.value=textinput.value.strip()
		strobeinput.value=strobeinput.value.strip()
		temporary_color_codes = sort_dict(temporary_color_codes)
		current_time_in_secs=song_offset + pygame.mixer.music.get_pos()/1000
		minutes = math.floor(current_time_in_secs/60)
		seconds = math.floor(current_time_in_secs %60)
		formatted_current_time='{:02d}:{:02d}'.format(minutes,seconds)
		if formatted_current_time == "-1:59":
			formatted_current_time = "00:00"
		display.fill((255,255,255))
		events=pygame.event.get()
		text_obj=base_font.render(formatted_song_length,True,font_color)
		text_time=base_font.render(formatted_current_time,True,font_color)
		if formatted_current_time==formatted_song_length:
			formatted_current_time=='{:00}:{:00}'
		display.blit(text_obj,(180,10))
		display.blit(text_time,(110,10))
		#display.blit(label, (760, 6))
		textinputButton.draw (display, (0,0,0))
		display.blit(textinput.surface, (790, 8))
		strobeinputButton.draw (display, (0,0,0))
		display.blit(strobeinput.surface, (710, 8))
		loadSongButton.draw(display, (0,0,0))
		loadButton.draw (display, (0,0,0))
		#saveasButton.draw (display, (0,0,0))
		saveButton.draw (display, (0,0,0))
		restartButton.draw (display, (0,0,0))

		#green.draw(display)
		#print("temporary_color_codes", temporary_color_codes)
		draw_color_rects(temporary_color_codes)
		draw_color_circles(color_circle_colors)
		color_circle_colors = change_circle_and_real_colors_if_needed(temporary_color_codes,current_time_in_secs,color_circle_colors)
		line_position=get_line_position(current_time_in_secs,total_length)
		pygame.draw.line(display, (255,0,0),(line_position, 50), (line_position, 80), 5)
		pygame.display.update()
		# creating a loop to check events that
		# are occuring

    # Blit its surface onto the screen
		for event in events:			
			pos = pygame.mouse.get_pos()			
			if event.type == pygame.QUIT:
				#print(file_name)
				pygame.quit()
				sys.exit()
			#pygame.display.update()
			# checking if keydown event happened or not
			if event.type == pygame.KEYDOWN:
				if strobeinputButton.isOver(pos) and not mixer.music.get_busy():
					strobeinput.update(events)
				if textinputButton.isOver(pos) and not mixer.music.get_busy():
					textinput.update(events)
				current=''
				timestamp=''
				content=''
				letter_key_pressed=pygame.key.name(event.key)
				ctrl_pressed=False
				shift_pressed=False
				alt_pressed=False
				if pygame.key.get_mods() & pygame.KMOD_LCTRL and (pygame.key.name(event.key)!='left ctrl') :
					print ("pressed: ctrl + "+pygame.key.name(event.key))
					ctrl_pressed=True
					letter_key_pressed=pygame.key.name(event.key)
				elif pygame.key.get_mods() & pygame.KMOD_SHIFT and (pygame.key.name(event.key)!='right shift'):
					print ("pressed: shift + "+pygame.key.name(event.key))
					shift_pressed=True
					letter_key_pressed=pygame.key.name(event.key)
				elif pygame.key.get_mods() & pygame.KMOD_ALT  and (pygame.key.name(event.key)!='left alt'):
					print("pressed: alt + "+pygame.key.name(event.key))
					alt_pressed=True
					letter_key_pressed=pygame.key.name(event.key).lower()
				else:
					letter_key_pressed = str(event.unicode).lower()

				if letter_key_pressed in key_colors:
					content = key_colors[letter_key_pressed]
					ball_numbers_used=[]
					for ball_number,color_letter in enumerate(content.split(";")):
						if color_letter!='x':
							ball_numbers_used.append(ball_number)
					timestamp = str(int(song_offset*1000) + pygame.mixer.music.get_pos())
					temporary_color_codes=add_timestamp_to_temporary_color_codes(timestamp,temporary_color_codes,content)
					#temporary_color_codes[timestamp] = content
					temporary_color_codes = sort_dict(temporary_color_codes)
					if shift_pressed:
						for key in temporary_color_codes.copy():
							value = temporary_color_codes[key]
							if int(timestamp)<int(key):
								if len(ball_numbers_used)>1:
									del temporary_color_codes[key]
								else:
									split_value=value.split(';')
									split_value[ball_numbers_used[0]]="x"
									temporary_color_codes[key]=";".join(split_value)
					if alt_pressed:
						for ball in ball_numbers_used:
							split_content = content.split(';')
							color = split_content[ball]
							have_reached_timestamp = False
							strobe_end_time = total_length*1000
							for key in temporary_color_codes:
								if have_reached_timestamp:
									split_content = temporary_color_codes[key].split(';')
									#print("split_content",split_content, ball)
									this_keys_balls_color = split_content[ball]
									if this_keys_balls_color != 'x':
										strobe_end_time = int(key)
										break
								if key == timestamp:
									have_reached_timestamp = True
							temporary_color_codes = add_strobes(temporary_color_codes, color, ball, timestamp, strobe_end_time)							

					if ctrl_pressed:
						new_fade_items_dicts = [{},{},{}]
						print("timestamp",timestamp)
						for ball in ball_numbers_used:
							print("timestamp",timestamp)
							fade_start_time = 0
							fade_start_color = "0,0,0"
							have_found_a_lower_key = False
							split_content = content.split(';')
							color = split_content[ball]
							for key in reversed(temporary_color_codes):
								if int(key) < int(timestamp):
									have_found_a_lower_key = True
								if have_found_a_lower_key:
									split_content = temporary_color_codes[key].split(';')
									print("found lower key", split_content, ball_numbers_used, ball)
									this_keys_balls_color = split_content[ball]
									print("this_keys_balls_color", this_keys_balls_color)
									if this_keys_balls_color != 'x': 
										fade_start_time = key
										fade_start_color = this_keys_balls_color
										break
							new_fade_items_dicts[ball] = calculate_fade(int(fade_start_time),int(timestamp),fade_start_color,color)	
						consolidated_dict = {}
						for ball_number, indiv_ball_dict in enumerate(new_fade_items_dicts):
							for key in indiv_ball_dict:
								value = indiv_ball_dict[key]
								current_value = 'x;x;x'
								if key in consolidated_dict:
									current_value = consolidated_dict[key]
								split_current_value = current_value.split(';')
								split_current_value[ball_number] = indiv_ball_dict[key]
								consolidated_dict[key] = ";".join(split_current_value)
						temporary_color_codes.update(consolidated_dict)
						print("temporary_color_codes2", temporary_color_codes)
					for ball_number,color_letter in enumerate(content.split(";")):
						if color_letter!='x':
							change_real_color(color_letter,ball_number)
							color_circle_colors[ball_number]=color_letter

				if event.key == pygame.K_SPACE and not mixer.music.get_busy() and not textinputButton.isOver(pos):
					if textinput.value!='':
						# mixer.init()
						# mixer.music.load(current_song_name+'.mp3')
						# mixer.music.set_volume(0.8)
						mixer.music.play(0,song_offset)
						#file_name=create_file(current_song_name)
						# with  open(file_name, "w") as file:
						# 	line=['{\n']
						# 	file.writelines(line)
						#while mixer.music.get_busy():
					else:
						notification_message('You must enter the file name to play the song.')
						#notification must have textinput to play the song
				elif event.key == pygame.K_SPACE and mixer.music.get_busy():
					pygame.mixer.music.stop()
					song_offset = get_song_position(line_position,total_length)
					# if os.path.getsize(file_name) != 0:
					# 	with  open(file_name, "r") as file:
					# 		current = file.read()
					# 	with  open(file_name, "w") as file:
					# 		file.writelines('{\n'+ current[:-2] + '\n}')
					# else:
					# 	os.remove(file_name)

				
			if event.type == pygame.MOUSEBUTTONDOWN:
				if loadSongButton.isOver(pos):
					path_of_user_selected_file = prompt_file()
					#print ('clicked the button')
					if path.exists(path_of_user_selected_file):	
						user_selected_file = path_of_user_selected_file.split("/")[-1]
						loadSongButton.text = user_selected_file
						pygame.mixer.music.stop()
						current_song_name=user_selected_file.split(".mp3")[0]
						#file_name=create_file(current_song_name)
						audio = MP3(path_of_user_selected_file)
						mixer.music.load(path_of_user_selected_file)
						total_length=audio.info.length
						mins,secs=divmod(total_length,60)
						mins=math.floor(mins)
						secs=math.floor(secs)
						formatted_song_length='{:02d}:{:02d}'.format(mins,secs)
						#pygame.mixer.music.stop()
						song_offset=0
						notification_message('Song file succesfully loaded.')
					else:
						notification_message('You did not chose the song file.')
				if loadButton.isOver(pos):
					path_of_user_selected_file = prompt_file()
					user_selected_file = path_of_user_selected_file.split("/")[-1]
					#label = myfont.render(user_selected_file.split(".txt")[0], 1, (0,0,0))
					#textButton.text = user_selected_file.split(".txt")[0]
					#temporary_color_codes=(user_selected_file_2.split(".txt")[0])
					textinput.update(events)
					textinput.value=user_selected_file.split(".txt")[0]
					if path.exists(path_of_user_selected_file):	
						#print('file exists')		
						with open(path_of_user_selected_file) as json_file:
							temporary_color_codes = json.load(json_file)
						notification_message('Text file succesfully loaded.')
					else:
						notification_message('You did not chose the text file.')
				# if saveasButton.isOver(pos):
				# 	text_file = asksaveasfile(initialfile = 'Untitled.txt',defaultextension=".txt",filetypes=[("All Files","*.*"),("Text Documents","*.txt")])
				# 	if text_file is not None:
				# 		print('text_file.name',text_file.name)
				# 		with open(text_file.name, 'w') as fp:
				# 			json.dump(temporary_color_codes, fp,indent = 6)
				# 			label = myfont.render(text_file.name.split(".txt")[0].split("/")[-1], 1, (0,0,0))
				# 			fp.close()
				
						
				if saveButton.isOver(pos):
					if textinput.value and len(temporary_color_codes)>1:
						textfile_path= './texts/'+textinput.value+'.txt'
						with open(textfile_path, 'w') as fp:
							json.dump(temporary_color_codes, fp,indent = 6)
						notification_message('File succesfully saved.')
					else:
						notification_message('There is nothing to save.')
				#notification must have text in textinput
					
				if restartButton.isOver(pos):
					pygame.mixer.music.stop()
					textinput.update(events)
					strobeinput.update(events)
					#textinput.value=''
					temporary_color_codes={	"1":"0,0,0;0,0,0;0,0,0"	}
					color_circle_colors=["0,0,0","0,0,0","0,0,0"]
					song_offset=0
					# x,y=pos
					# x=0
					# song_offset = get_song_position(x,total_length)					

			if event.type == pygame.MOUSEMOTION:
				if loadSongButton.isOver(pos):
					loadSongButton.color = (255,0,0)
				else:
					loadSongButton.color = (0,255,0)

			if event.type == pygame.MOUSEBUTTONUP:
				x,y=pos
				if 20<x<1170 and 50<y<80:
					if mixer.music.get_busy():
						#print(pos)
						pygame.mixer.music.play(0,(get_song_position(x,total_length)))
						song_offset = get_song_position(x,total_length)
					else:
						# pygame.mixer.music.play(0,(get_song_position(x,total_length)))
						# pygame.mixer.music.pause()
						
						song_offset = get_song_position(x,total_length)
				for ball_number in range(0,3):
					#print(song_offset*1000)
					click_time_in_ms=int(song_offset*1000)
					have_found_a_lower_key=False
					for key in reversed(temporary_color_codes):
						if int(key) < click_time_in_ms:
							have_found_a_lower_key = True
						if have_found_a_lower_key:
							split_content = temporary_color_codes[key].split(';')
							this_keys_balls_color = split_content[ball_number]
							if this_keys_balls_color != 'x': 
								color = this_keys_balls_color
								color_circle_colors[ball_number]=color
								change_real_color(color,ball_number)
								break
					
main()