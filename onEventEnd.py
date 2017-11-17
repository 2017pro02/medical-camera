
from bs4 import BeautifulSoup
import cv2, requests, os, re, shutil, sys
import numpy as np
from dotenv import load_dotenv
from os.path import join, dirname


## .envファイルの取得
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


def getTargetFilePath():
	basePath = r'/home/pi/Documents/medical-camera/fileNames'

	# 最新のファイルを取得する
	txtFiles = os.listdir(basePath)
	txtFiles.sort()
	txtFileName = txtFiles[len(txtFiles)-1]
	txtFile = open(basePath + '/' + txtFileName, 'r')
	print('Files Name = ' + txtFileName)

	# ファイル行数を取得
	lineNum = sum(1 for line in open(basePath + '/' + txtFileName))
	print('Line Number = ' + str(lineNum))
	targetLine = int(lineNum)
	print('Target Line = ' + str(targetLine))
	
	# 送信するファイル名を取得
	for i in range(targetLine):
		targetFilePath = txtFile.readline().split('\n')[0]
	txtFile.close()
	print('Target File Path = ' + targetFilePath)
	return targetFilePath


def getBackgroundPath():
	basePath = r'/home/pi/Documents/medical-camera/backImages'
	# 最新のファイルを取得する
	files = os.listdir(basePath)
	files.sort()
	fileName = files[len(files)-1]
	filePath = r'' + basePath + '/' + fileName

	print('File Path = ' + filePath)
	return filePath


def isBackground(backImagePath, targetImagePath, th, blur):
	width = 320
	height = 240

	backImage = cv2.imread(backImagePath, cv2.IMREAD_GRAYSCALE)
	targetImage = cv2.imread(targetImagePath, cv2.IMREAD_GRAYSCALE)

	mask = cv2.absdiff(targetImage, backImage)

	mask[mask < th] = 0
	mask[mask >= th] = 255

	if np.count_nonzero(mask) > width*height*0.5:
		return False
	else:
		return True


def get_token(url):
	html  = client.get(url).text
	soup  = BeautifulSoup(html, "html.parser")
	return soup.find("input", attrs={"name": "authenticity_token"}).get("value")
	


if __name__ == '__main__':
	filePath = getTargetFilePath()
	if isBackground(filePath, getBackgroundPath(), 5, 7):
		print('Taked Image is Bakcground!! So this image is not sent!!')
		os.system('sh create_voice.sh "写真を取る準備ができたよ!!．ボックスに食事を入れてね"')
		sys.exit(0)
	

	client = requests.session()
	base_url = os.environ.get("BASE_URL")
	
	## ログアウト
	url = "{0}/users/sign_out".format(base_url)
	client.delete(url)
	
	
	## ログイン
	url = "{0}/users/sign_in".format(base_url)
	payload = {
	    "authenticity_token": get_token(url),
	    "user[email]": os.environ.get("E_MAIL"),
	    "user[password]": os.environ.get("PASSWORD"),
	}
	client.post(url, data=payload)
	
	user_name = os.environ.get("USER_NAME")
	
	## 投稿
	url = ("{0}/@{1}/meals/new").format(base_url, user_name)
	payload = {
	    "authenticity_token": get_token(url),
	}
	
	
	img = {"meal[img]": open(filePath, "rb")}
	url = ("{0}/@{1}/meals").format(base_url, user_name)
	res = client.post(url, data=payload, files=img)
	os.system('sh create_voice.sh "写真が取れたよ!!．ボックスから食事を取り出してね"')
	print(res)


