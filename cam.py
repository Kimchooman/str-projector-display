from cv2 import *
import numpy as np

cam = VideoCapture(0)
ret = cam.set(3,420)
ret = cam.set(4,240)

def current_multiple(val, dimensions):
 	if val % dimensions == 0:
		return val // dimensions
	else:
		return val // dimensions +1 

def mean_rgb_thread(thread):

	terms = len(thread) * 3
	sum = 0

	for rgb in thread:
		for color in rgb:
			color += sum
	return sum // terms

def chunck_img(dimensions, rgb_points):
	if len(rgb_points) % dimensions == 0:
			c_ar_height = len(rgb_points) //dimensions
	else:
		c_ar_height = len(rgb_points) //dimensions +1
	if len(rgb_points[0]) % dimensions == 0 :
		c_ar_width = len(rgb_points[0]) //dimensions
	else:
		c_ar_width = len(rgb_points[0]) //dimensions +1

	ar = []

	for r in range(0, c_ar_height):
		ar.append([])

		for c in range(0, c_ar_width):
			ar[r].append([])

	for r in range(0, len(rgb_points)):
		r_segment = current_multiple(r, dimensions)

		for c in range(0, len(rgb_points[0])):
			c_segment = current_multiple(c, dimensions)

		ar[r_segment -1][c_segment -1].append(rgb_points[r,c])

	for chunk_row in range(len(ar)):
		for chunck_column in range(len(ar[chunck_row])):
			ar[chunck_row][chunck_column] = mean_rgb_thread(ar[chunck_row][chunck_column])
			
	for row in range(len(ar)):
		for column in range(len(ar[row])):
			ar[row][column] = mean_rgb_thread(ar[row][column])

	return ar

step = 0 
max_step = 10

rtn, base_img = cam.read()

if rtn:
	base_img = cv2.medianBlur(base_img,5)
	base_ar = chunck_img(base_img)

while True:
	
	r, img = cam.read()

	if step is max_step or r is False: break
	img = cv2.medianBlur(img,5)

	ar = chunck_img(img)

	waitKey(100)

	step += 1
