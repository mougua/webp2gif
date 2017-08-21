#!/usr/bin/env python

# Convert PNG images to GIF, preserving transparency
# 2008 - http://www.coderholic.com/png2gif

import sys
from PIL import Image
import random
import optparse
import os
import os.path

def unique_color(image):
	"""find a color that doesn't exist in the image
	"""
	colors = image.getdata()
	while True:
		# Generate a random color
		if image.mode == "LA":    
			 color = random.randint(0, 255),
		else:
			color = (
			  random.randint(0, 255),
			  random.randint(0, 255),
			  random.randint(0, 255)
			)

		if color not in colors:
			return color

def fill_transparent(image, color, threshold=0): 
	"""Fill transparent image parts with the specified color 
	"""
	def quantize_and_invert(alpha):
		if alpha <= threshold:
			return 255
		return 0
	# Get the alpha band from the image
	if image.mode == 'RGBA':
		red, green, blue, alpha = image.split()
	elif image.mode == 'LA':
		gray, alpha = image.split()
	# Set all pixel values below the given threshold to 255,
	# and the rest to 0
	alpha = Image.eval(alpha, quantize_and_invert)
	# Paste the color into the image using alpha as a mask
	image.paste(color, alpha)


def color_index(image, color):
	"""Find the color index
	"""
	palette = image.getpalette()
	palette_colors = list(zip(palette[::3], palette[1::3], palette[2::3]))
	index = palette_colors.index(color)
	return index

def convert_image(image, new_name):
	if image.mode == 'P':
		if image.info.has_key('transparency'): # check to see if the image has any transparency
			transparency = image.info['transparency']
			image.save(new_name, transparency=transparency)
		else: image.save(new_name)
	elif image.mode == 'RGBA': # RGB images need to be converted to Palette mode
		threshold = 0
		colour = unique_color(image)
		fill_transparent(image, colour, threshold)
		image = image.convert('RGB').convert('P', palette=Image.ADAPTIVE)
		image.save(new_name, transparency=color_index(image, colour))
	elif image.mode == 'LA':
		threshold = 0
		colour = unique_color(image)
		fill_transparent(image, colour, threshold)
		image = image.convert('L').convert('P', palette=Image.ADAPTIVE)
		image.save(new_name, transparency=color_index(image, (colour[0], colour[0], colour[0])))
	else:
		raise "Unsupported PNG file"

os.system(r'D:\libwebp-0.6.0-windows-x86\bin\dwebp.exe D:\用户目录\我的图片\sticker.webp -o d:\mylab\lab\out.png')

im = Image.open(r'd:\mylab\lab\out.png')
convert_image(im, r'd:\mylab\lab\image.gif')

from PIL import Image
 
im = Image.open(r'd:\mylab\lab\out.png')
# Get the alpha band
alpha = im.split()[3]

# Convert the image into P mode but only use 255 colors in the palette out of 256
im = im.convert('RGB').convert('P', palette=Image.ADAPTIVE, colors=255)

# Set all pixel values below 128 to 255,
# and the rest to 0
mask = Image.eval(alpha, lambda a: 255 if a <=100 else 0)

# Paste the color of index 255 and use alpha as a mask
im.paste(255, mask)
# The transparency index is 255
im.save(r'd:\mylab\lab\image3.gif', transparency=255)
