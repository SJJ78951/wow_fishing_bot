import cv2
import pyscreenshot as ImageGrab
import pyautogui
import numpy as np
import psutil
import win32gui
import sys
from mss import mss
from sklearn.cluster import DBSCAN
import win32api, win32con
import time


def make_screenshot(window):
	print('Capturing screen')
	screenshot = ImageGrab.grab(bbox=window)
	return screenshot


def kmeans_apply(image, centroids):
	if len(image.shape) > 2 and image.shape[2] == 4:
		# convert the image from RGBA2RGB
		image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
	Z = image.reshape((-1, 3))
	for i, point in enumerate(Z):
		Z[i] = centroids[np.argmin([np.linalg.norm(point - centroid) for centroid in centroids])]
	return Z.reshape((image.shape))


def kmeans_centroids(image):
	if len(image.shape) > 2 and image.shape[2] == 4:
		# convert the image from RGBA2RGB
		image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)

	# define criteria, number of clusters(K) and apply kmeans()
	criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)

	Z = image.reshape((-1, 3))
	# convert to np.float32
	Z = np.float32(Z)
	K = 2
	_, label, centroids = cv2.kmeans(Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

	centroids = np.uint8(centroids)
	res = centroids[label.flatten()]
	res2 = res.reshape((image.shape))

	return res2


def binarize(image):
	image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
	unique, counts = np.unique(image, return_counts=True)
	water_color = unique[np.argmax(counts)]
	image[image == water_color] = 0
	image[image != 0] = 255

	return image


def strictly_increasing(L):
	return all(x < y for x, y in zip(L, L[1:]))


def distance(p1, p2):
	dist = np.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
	return dist


def get_window(window_name):
	return win32gui.GetWindowRect(win32gui.FindWindow(None, window_name))


def check_process(wow_name):
	print('Checking WoW is running')
	if wow_name in [psutil.Process(pid).name() for pid in psutil.pids()]:
		print('WoW is running')
		return True
	else:
		print('WoW is not running')
		return False


def move_mouse(place):
	print("Moving cursor to " + str(place) + "...")
	pyautogui.moveTo(place)


def logout():
	pyautogui.hotkey('return')
	pyautogui.hotkey('1')

	time.sleep(0.1)
	for c in u'/logout':
		time.sleep(0.1)
		pyautogui.hotkey('c')

	time.sleep(0.1)
	pyautogui.hotkey('return')


def clickRight():
	win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)
	win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)
