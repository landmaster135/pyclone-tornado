# GetFileList.py
# code in shift-jis

import glob2
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
  for file in folderList:
    print(file)
  return folderList

def main(folderpath):
    GetFileList(folderpath)

if __name__ == "__main__":
  main("C:{sep}Users{sep}OCT--{sep}Dropbox{sep}ブログ{sep}Pythonの練習".format(sep=sep))