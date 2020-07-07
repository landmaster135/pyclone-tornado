# GetFileList.py
# code in shift-jis

import glob2
import os
from tkinter import filedialog
# IMPORT module FROM LandmasterLibrary
import DirSeperator
sep = DirSeperator.DecideSeperator() # String seperator of directory.

def GetFileList(folderpath):
  '''
  folderpath : Selected folder's absolutely path.
  ext        : extension
  folderlist : list about selected folder
  '''

  ext = 'pdf'
  folderList = glob2.glob('{folderpath}{sep}*.{ext}'.format(folderpath=folderpath,sep=sep,ext=ext))
  print('Get file list in this folder.\n"', folderpath, '"\n\n........................\n')
  # Get list about files.
  for file in folderList:
    print(file)
  return folderList

def main(folderpath):
    GetFileList(folderpath)

if __name__ == "__main__":
  nowDir = os.path.abspath(os.path.dirname(__file__))
  nowDirPath = filedialog.askdirectory(initialdir=nowDir)
  main(nowDirPath)