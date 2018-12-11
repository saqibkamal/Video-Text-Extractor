import cv2
import pytesseract
import shutil
from PIL import Image
import os
import json
import requests

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'

def ocr_space_file(filename, overlay=False, api_key='e932b5689b88957', language='eng'):
    payload = {'isOverlayRequired': overlay,'apikey': api_key,'language': language,}

    with open(filename, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',files={filename: f},data=payload,)

    c=json.loads(r.text)

    return c["ParsedResults"][0]["ParsedText"]

def extract_text(path_of_image):

	image = cv2.imread(path_of_image)
	image = cv2.resize(image, (0,0), fx=6, fy=6)

	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.threshold(gray, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	text = pytesseract.image_to_string(Image.open(filename))
	os.remove(filename)

	return text


def parse_video(path_of_video):

	shutil.rmtree('test')
	os.mkdir('test')

	vidcap = cv2.VideoCapture(path_of_video)
	frame_rate = int(vidcap.get(cv2.CAP_PROP_FPS))

	success,image = vidcap.read()
	count = 0
	img_num = 0

	while success:

		if count%frame_rate != 0:
			success,image = vidcap.read()
			count += 1
			continue

		print("Reading frame %d" % img_num)
		cv2.imwrite("test/frame%d.jpg" % img_num, image)       

		success,image = vidcap.read()
		count += 1
		img_num +=1


def check_all_images():

	shutil.rmtree('matched')
	os.mkdir('matched')

	image_folder = 'test'
	images = [img for img in os.listdir(image_folder) if img.endswith(".jpg")]

	for image in images:
		filename1='test' + '\\'+image 

		#Using online OCR . Takes time but more efficient
		#text = ocr_space_file(filename=filename1)  

		#Using Tesseract . Fast but less efficient    
		text = extract_text(filename1)
		

		if to_search.lower() in text.lower():
			shutil.copy(filename1,'matched')
			print('Match found in %s' % image)


# Text we want to search in the file
to_search = "flutter"

#Name of video in which we want to search a text with its location 
parse_video('b.mp4')

check_all_images()