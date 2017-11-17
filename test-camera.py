
import cv2

width = 420
height = 340

if __name__ == '__main__':
	
	print('camera capture on!!')
	cam = cv2.VideoCapture(0)
	cam.set(3, width)
	cam.set(4, height)

	while True:
		cv2.imshow("Captured Photo", cam.read()[1])

		key = cv2.waitKey(10)
		if key == 27:
			cv2.destroyAllWindows()
			cam.release()
			break

