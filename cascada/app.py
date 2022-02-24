# Library by default
import sys
# Library by third party
import cv2
# Library in the local

args = sys.argv


image = cv2.imread('sample_img.jpg')

cascade_file = 'haarcascade_frontalface_alt2.xml'
cascade_face = cv2.CascadeClassifier(cascade_file)

# 顔を探して配列で返す
face_list = cascade_face.detectMultiScale(image, minSize=(20, 20))

for (x, y, w, h) in face_list:
    border_color = (0, 0, 255)

    border_size = 2
    cv2.rectangle(image, (x, y), (x+w, y+h), border_color, thickness=border_size)

cv2.imwrite('out.jpg', image)
