import collections

my_dict = {
"2051" : "x,r,x",
"2285" : "x,x,r",
"2547" : "x,r,x",
"2817" : "x,x,r",
"340" : "x,r,x",
"621" : "x,x,r",
"898" : "x,r,x",
"1333" : "x,o,x",
"1612" : "x,x,o",
"3107" : "x,r,x"
}

#make a python function that reorders this dictionary based on the keys numeric value from low to high

def sort_dict(my_dict):
    sorted_dict = sorted(my_dict.items(), key=lambda x: int(x[0]))
    return sorted_dict

print(sort_dict(my_dict))