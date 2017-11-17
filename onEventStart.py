
import datetime, os

# 現在の時刻を文字列で取得する
now = datetime.datetime.now()
nowStr = '{0:%Y%m%d%H%M%S}'.format(now) 
print(nowStr)

# 現在の時刻でファイルをオープンする
txtFile = open(r'/home/pi/Documents/medical-camera/fileNames/' + nowStr, 'w')
# txtFile.write('hoge\n')
txtFile.close()

