# TextEditor.py
# code in shift-jis

import os, sys, platform
# IMPORT module FROM LandmasterLibrary
import DirEditor
sep = DirEditor.DecideSeperator() # String seperator of directory.
import FileListGetter

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
    WriteText(FileListGetter.DecideNowDir(), ['apple', 'banana', 'orange'])

if __name__ == "__main__":
    main()
