import json

mult = 2

def formatted_key(timestamp):
	return str(int((mult*int(timestamp))/100))

textfile_name = 'toms(8)'


with open('./texts/' + textfile_name + '.txt') as json_file:
	local_dict = json.load(json_file)

output_string = ''

for key in local_dict:
	value = local_dict[key]
	print(value)
	output_string = output_string + formatted_key(int(key)) + ": (" + str(value) + "), "

print(output_string)