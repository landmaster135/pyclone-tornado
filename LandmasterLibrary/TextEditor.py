# TextEditor.py
# code in shift-jis

import os, sys, platform
# IMPORT module FROM LandmasterLibrary
import DirEditor

def WriteCSV(targetFile, targetList):
    '''
    targetFile : String absolutely filename of target file.
    targetList : List of contents to write.
    '''
    # write 1 line.
    with open(targetFile, mode='a') as f:
        for m in range(0, len(targetList)):
            # memorize to "should_not_exist_yubin.csv" sheet
            if m != len(targetList) - 1:
                f.write("%s," % targetList[m])
            else:
                f.write("%s" % targetList[m])
        f.write("\n")

def WriteText(fileName, nowList):
    '''
    fileName : String absolutely path of selected file
    nowList  : List of statement to write
    '''
    with open(fileName, 'w') as f:
        for n in nowList:
            f.write("%s\n" % n)

def main():
    # test code for WriteText()
    WriteText(DirEditor.DecideNowDir(), ['apple', 'banana', 'orange'])

if __name__ == "__main__":
    main()
