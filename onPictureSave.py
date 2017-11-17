
import os, sys

basePath = r'/home/pi/Documents/medical-camera/fileNames'

# 最新のファイルを取得する
files = os.listdir(basePath)
files.sort()
fileName = files[len(files)-1]
# print(fileName)

imageName = sys.argv[1]
# print(imageName)

targetFile = open(basePath+ '/' + fileName, 'a')
targetFile.write(imageName + '\n')
targetFile.close()

