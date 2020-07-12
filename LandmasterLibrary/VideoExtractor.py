# VideoExtractor.py
# code in shift-jis

import os, sys
import cv2 # opencv 3.4.2
# IMPORT module FROM LandmasterLibrary
import DirEditor
sep = DirEditor.DecideSeperator() # String seperator of directory.
import FileListGetter

def RemoveDuplication(folderList):
    '''
    folderList    : list of file filtered with extension in the selected folder.
    img1          : List of pixels of image. (img [height] [width] [color channel])
    img2          : List of pixels of image. (img [height] [width] [color channel])
    match_count   : Integer number of matching between img1 and img2
    num_all_pixel : Integer number of all pixels
    match_rate    : Float rate
    border_line   : border line
    '''
    img1 = ''
    img2 = ''
    border_line = 0.9
    folderList.reverse()

    if len(folderList) == 0:
        print('\nVideoExtractor exits because of no target files.')
        sys.exit(0)
    # compare both image to remove img1 or not
    for i in range(0, len(folderList) - 1):
        img1 = cv2.imread(folderList[i], 1) # =0: monochrome, >0: 3 channel, <0: original
        img2 = cv2.imread(folderList[i+1], 1)
        match_count = 0
        num_all_pixel = len(img1) * len(img1[0])
        if len(img1) == len(img2):
            # j: pixels in the height, k: pixels in the width
            for j in range(0, len(img1)):
                for k in range(0, len(img1[j])):
                    # judge by color whether they match or not
                    for m in range(0, len(img1[j][k])): # 3
                        if img1[j][k][m] != img2[j][k][m]:
                            break
                        if m == 2:
                            match_count = match_count + 1
        # Decide to remove or don't
        match_rate = match_count/num_all_pixel
        print("match rate is {rate}".format(rate=match_rate))
        if match_rate >= border_line:
            os.remove(folderList[i])

def ExtractPicture(video_name):
    '''
    video_name    : String absolutely path of selected file
    extracted_dir : String absolutely path of directory has selected file
    frame_count   : Integer number of frame of selected video
    num_of_image  : Integer number of extracted images from video
    '''
    if video_name == '':
        print("ERROR: No file is selected.")
        sys.exit(0)

    extracted_dir = DirEditor.MakeDirectory(video_name)
    # extracted_path = os.path.dirname(video_name)

    cap = cv2.VideoCapture(video_name)
    # 幅
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # 高さ
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # number of frame
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # fps
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("ddddddddddddddddddddd", width, height)

    for num_of_image in range(1, int(frame_count), int(fps)):
        # set a property, where frame in this case, in the VideoCapture
        cap.set(cv2.CAP_PROP_POS_FRAMES, num_of_image)
        # read the next video frame to extract image file ("cap.read()[1]" is arrays of image's pixels.)
        cv2.imwrite("{dirname}{sep}image{num:0=3}.jpg".format(dirname=extracted_dir,sep=sep,num=int((num_of_image-1)/int(fps))), cap.read()[1])
        # cv2.imwrite("{video_dir}image{:0=3}.jpg".format(int((num_of_image-1)/int(fps))), cap.read()[1])
        print("saved: image{num:0=3}.jpg".format(num=int((num_of_image-1)/int(fps))))
    print('Check directory "{dirname}"'.format(dirname=extracted_dir))
    cap.release()

def main():
    # list_of_ext = ["mp4"]
    # ExtractPicture(FileListGetter.DecideNowFile(list_of_ext))
    RemoveDuplication(FileListGetter.GetFileList(FileListGetter.DecideNowDir(),'jpg'))

if __name__ == "__main__":
    main()
