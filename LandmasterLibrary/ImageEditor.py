# ImageEditor.py
# code in shift-jis

import os, sys
import cv2 # opencv 3.4.2
# IMPORT module FROM LandmasterLibrary
import InputController
import DirEditor
sep = DirEditor.DecideSeperator() # String seperator of directory.
import FileListGetter
import TextEditor

def SelectArea(filename):
    '''
    filename   : String absolutely path of selected file

    img       : PIL.JpegImagePlugin.JpegImageFile
    frameDict  : Dictionary of integer ([top : bottom, left : right])
    '''
    from PIL import Image
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.widgets import Slider

    img = Image.open(filename) # this function has no exception handling
    width, height = img.size

    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.25, bottom=0.35)
    plt.xlim(0, width)
    plt.ylim(0, height)

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    delta_f = 1.0
    ax.imshow(img, extent=[*xlim, *ylim], aspect='auto')

    # set borderline. (Top and Bottom turn over.)
    borderTop,    = plt.plot([0, width], [0, 0], lw=0.7)
    borderBottom, = plt.plot([0, width], [height, height], lw=0.7)
    borderLeft,   = plt.plot([0, 0], [0, height], lw=0.7)
    borderRight,  = plt.plot([width, width], [0, height], lw=0.7)

    axcolor = 'lightgoldenrodyellow'
    axTop    = plt.axes([0.25, 0.20, 0.65, 0.03], facecolor=axcolor)
    axBottom = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    axLeft   = plt.axes([0.25, 0.10, 0.65, 0.03], facecolor=axcolor)
    axRight  = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)

    sliderTop    = Slider(axTop, 'Top', 0, height/2 - 1, valinit=0, valstep=delta_f)
    sliderBottom = Slider(axBottom, 'Bottom', 0, height/2 - 1, valinit=0, valstep=delta_f)
    sliderLeft   = Slider(axLeft, 'Left', 0, width/2 - 1, valinit=0, valstep=delta_f)
    sliderRight  = Slider(axRight, 'Right', 0, width/2 - 1, valinit=0, valstep=delta_f)

    def update(val):
        '''
        top    : String number of y-coordinate of top (global variable)
        bottom : String number of y-coordinate of bottom (global variable)
        left   : String number of x-coordinate of left (global variable)
        right  : String number of x-coordinate of right (global variable)
        '''
        global top
        global bottom
        global left
        global right
        top    = sliderTop.val
        bottom = height - sliderBottom.val
        left   = sliderLeft.val
        right  = width - sliderRight.val
        borderTop.set_ydata([height - top, height - top])
        borderBottom.set_ydata([height - bottom, height - bottom])
        borderLeft.set_xdata([left, left])
        borderRight.set_xdata([right,right])
        fig.canvas.draw_idle()

    # attach a trigger to Slider
    sliderTop.on_changed(update)
    sliderBottom.on_changed(update)
    sliderLeft.on_changed(update)
    sliderRight.on_changed(update)
    plt.show()

    frameDict = {'top': int(top), 'bottom': int(bottom), 'left': int(left), 'right': int(right)}
    print("FrameSize for trimming is ", frameDict)
    return frameDict

def TrimImage(trimmed_img_ext):
    '''
    fileList                 : List of file filtered with extension in the selected folder.
    basefilename_without_ext : String name of base file without extension.
    selectTimes              : String of times to input.
    extracted_dir            : String absolutely path of directory has selected file.
    img                      : Dictionary of pixels of image. (img [height] [width] [color channel])
    trimmed_img              : Dictionary of pixels of image.
    trimmed_img_ext          : String of extension of trimmed_img.
    trimmed_img_name         : String of filename of trimmed_img.
    '''
    fileList = FileListGetter.GetFileList(DirEditor.DecideNowDir(),trimmed_img_ext)

    # Error Handling
    if len(fileList) == 0:
        print('\nImageEditor exits because of no target files.')
        sys.exit(0)

    # Error Handling
    basefilename_without_ext = os.path.splitext(os.path.basename(__file__))[0]
    if InputController.CheckerWhetherSjisExists(fileList[0], basefilename_without_ext) == True:
        sys.exit(0)
    # checkStr = re.compile('[\\a-zA-Z0-9\-\_\.\-\s\:\~\^\=]+')
    # if checkStr.fullmatch(fileList[0]) == None:
    #     print('\nImageEditor exits because of the directory containing shift-jis character.')


    selectTimes = input('What times do you choosing? ("1" or "every"): ')
    while selectTimes != '1' and selectTimes != 'every':
        selectTimes = input('Retry. ("1" or "every"): ')
    extracted_dir = DirEditor.MakeDirectory(fileList[0])

    for i in range(0, len(fileList)):
        if selectTimes == '1':
            if i == 0:
                frameDict = SelectArea(fileList[i])
        elif selectTimes == 'every':
            frameDict = SelectArea(fileList[i])
        # img[top : bottom, left : right]
        img = cv2.imread(fileList[i])
        trimmed_img      = img[frameDict['top'] : frameDict['bottom'], frameDict['left'] : frameDict['right']]
        trimmed_img_name = "image{num:0=3}.{trimmed_img_ext}".format(num=i,trimmed_img_ext=trimmed_img_ext)
        cv2.imwrite("{dirname}{sep}{trimmed_img_name}".format(dirname=extracted_dir,sep=sep,trimmed_img_name=trimmed_img_name), trimmed_img)
        print("saved: {trimmed_img_name}".format(trimmed_img_name=trimmed_img_name))
    print('Check directory "{dirname}"'.format(dirname=extracted_dir))

def JudgeMatchRateByFeaturePoint(fileName1, fileName2):
    '''
    fileName1     : String absolutely path of selected file
    fileName2     : String absolutely path of selected file
    img1          : List of pixels of image. (img [height] [width] [color channel])
    img2          : List of pixels of image. (img [height] [width] [color channel])
    ret           : Float
    '''
    processingMethod = 99
    if os.path.splitext(os.path.basename(fileName1))[1] == '.DS_Store':
        while processingMethod != 0 and processingMethod != 10000:
            processingMethod = int(input('This is not image. Decide degree of similarity by yourself. (0 or 10000:less similar)'))
        return processingMethod
    if os.path.splitext(os.path.basename(fileName2))[1] == '.DS_Store':
        while processingMethod != 0 and processingMethod != 10000:
            processingMethod = int(input('This is not image. Decide degree of similarity by yourself. (0 or 10000:less similar)'))
        return processingMethod
    # Grayscale is more correctly than RGB: 3 channel.
    img1 = cv2.imread(fileName1, cv2.IMREAD_GRAYSCALE)
    img2 = cv2.imread(fileName2, cv2.IMREAD_GRAYSCALE)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    detector = cv2.AKAZE_create()
    (img1_kp, img1_des) = detector.detectAndCompute(img1, None)
    try:
        (img2_kp, img2_des) = detector.detectAndCompute(img2, None)
        matches = bf.match(img1_des, img2_des)
        dist = [m.distance for m in matches]
        similarity = sum(dist) / len(dist)
    except cv2.error:
        while processingMethod != 0 and processingMethod != 10000:
            processingMethod = int(input('cv2.error occured. Decide degree of similarity by yourself. (0 or 10000:less similar)'))
        return processingMethod
    except ZeroDivisionError:
        while processingMethod != 0 and processingMethod != 10000:
            processingMethod = int(input('ZeroDivisionError occured. Decide degree of similarity by yourself. (0 or 10000:less similar)'))
        return processingMethod

    return similarity

def JudgeMatchRateByPixelMatch(fileName1, fileName2):
    '''
    fileName1     : String absolutely path of selected file
    fileName2     : String absolutely path of selected file
    coloeMode     : Integer color mode for cv2.imread
    img1          : List of pixels of image. (img [height] [width] [color channel])
    img2          : List of pixels of image. (img [height] [width] [color channel])
    match_count   : Integer number of matching between img1 and img2
    num_all_pixel : Integer number of all pixels
    match_rate    : Float rate
    '''
    colorMode = cv2.IMREAD_GRAYSCALE
    # coloeMode = 1
    img1 = cv2.imread(fileName1, colorMode) # 2nd variable =0: monochrome, >0: 3 channel, <0: original
    img2 = cv2.imread(fileName2, colorMode)
    match_count = 0
    if len(img1) == len(img2):
        # j: pixels in the height, k: pixels in the width
        for j in range(0, len(img1)):
            for k in range(0, len(img1[j])):
                if colorMode == cv2.IMREAD_GRAYSCALE:
                    # judge by shading whether they match or not
                    if img1[j][k] == img2[j][k]:
                        match_count = match_count + 1
                elif colorMode == 1:
                    # judge by color whether they match or not
                    for m in range(0, len(img1[j][k])): # 3
                        if img1[j][k][m] != img2[j][k][m]:
                            break
                        if m == 2:
                            match_count = match_count + 1
    num_all_pixel = len(img1) * len(img1[0])
    match_rate = match_count/num_all_pixel

    return match_rate

def RemoveDuplication(folderList):
    '''
    folderList    : List String absolutely path, of file filtered with extension in the selected folder.
    extracted_dir : String absolutely path of directory has selected file
    match_rate    : Float rate
    border_line   : border line
    '''
    border_line = 70

    if len(folderList) == 0:
        print('\nImageEditor exits because of no target files.')
        sys.exit(0)

    extracted_dir = os.path.dirname(folderList[0])
    # Decide to remove or don't
    isRmoveMode = InputController.RepeatInputWithMultiChoices('You wanna remove files in condition? (y/n)', ['y', 'n'])

    assessMode = 'a'
    listForText = []
    # compare both image to remove img1 or not
    for i in range(0, len(folderList) - 1):
        imgName1 = os.path.splitext(os.path.basename(folderList[i]))[0]
        imgName2 = os.path.splitext(os.path.basename(folderList[i+1]))[0]
        # Decide method of assessment
        while assessMode != 'F' and assessMode != 'P':
            assessMode = input('Which method to assess?\n[ F: FeaturePoint, P: PixelMatch ] : ')
        if assessMode == 'F':
            match_rate = JudgeMatchRateByFeaturePoint(folderList[i], folderList[i+1])
            print('degree of similarity between "{imgName1}" and "{imgName2}" is {rate}'.format(imgName1=imgName1,imgName2=imgName2,rate=match_rate))
        elif assessMode == 'P':
            match_rate = JudgeMatchRateByPixelMatch(folderList[i], folderList[i+1])
            print('match rate between "{imgName1}" and "{imgName2}" is {rate}'.format(imgName1=imgName1,imgName2=imgName2,rate=match_rate))
        listForText.append('"{imgName1}" and "{imgName2}" is {rate}'.format(imgName1=imgName1,imgName2=imgName2,rate=match_rate))
        # Remove files
        if isRmoveMode == 'y':
            if assessMode == 'F':
                if match_rate <= border_line:
                    os.remove(folderList[i])
            elif assessMode == 'P':
                if match_rate >= border_line:
                    os.remove(folderList[i])
    # write to .txt file
    TextEditor.WriteText(DirEditor.GenerateFileName(extracted_dir, sep, 'match_rate.txt'), listForText)

    print('RemoveDuplication is terminated.\nCheck directory "{dirname}"'.format(dirname=extracted_dir))

def ExtractImage(video_name):
    '''
    video_name    : String absolutely path of selected file
    extracted_dir : String absolutely path of directory has selected file
    frame_count   : Integer number of frame of selected video
    fps           : Integer number of fps of selected video
    num_of_image  : Integer number of extracted images from video
    '''
    # Error Handling
    if video_name == '':
        print("ERROR: No file is selected.")
        sys.exit(0)

    extracted_dir = DirEditor.MakeDirectory(video_name)

    # Error Handling
    basefilename_without_ext = os.path.splitext(os.path.basename(__file__))[0]
    if InputController.CheckWhetherSjisExists(extracted_dir, basefilename_without_ext) == True:
        sys.exit(0)

    cap = cv2.VideoCapture(video_name)
    # width
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    # height
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    # number of frame
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    # fps
    fps = cap.get(cv2.CAP_PROP_FPS)
    print("movie's width: ", width, ", height: ", height)

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
    # # test code for SelectArea()
    # list_of_ext = ["jpg"]
    # SelectArea(DirEditor.DecideNowFile(list_of_ext))

    # # test code for TrimImage()
    # TrimImage('jpg')

    # test code for RemoveDuplication()
    # fileList = FileListGetter.GetFileList(DirEditor.DecideNowDir(),'jpg')
    # RemoveDuplication(fileList)

    # # test code for ExtractImage()
    list_of_ext = ["mp4"]
    ExtractImage(DirEditor.DecideNowFile(list_of_ext))

if __name__ == "__main__":
    main()
