# GetFileList.py
# code in shift-jis

import glob2
import os, sys, platform
from tkinter import filedialog
# IMPORT module FROM LandmasterLibrary
import DirEditor
sep = DirEditor.DecideSeperator() # String seperator of directory.

def InputExt():
  '''
  list_of_ext ： List String extension
  moreFile    ： String extension
  '''
  list_of_ext = []
  # Number of extensions you can selecet is under 10.
  for i in range(10):
    # Varify message by times.
    if i == 0:
      moreFile = input("What filetype do you wanna take?: ")
    else:
      moreFile = input('more filetype?(* or "nothing"): ')
    # Store in a list or not.
    if moreFile != "nothing":
      list_of_ext.append(moreFile)
    else:
      break
  return list_of_ext

def DecideExt(list_of_ext):
  '''
  list_of_ext ： List String extension
  fileTypes   ： List type of file for choose file in the dialog

  ext          ： String extension
  ext_by_semic ： String extension in arrangement by semicolon (if Windows)
  ext_by_list  ： String extension in arrangement by list (if Mac)
  ext_by_tuple ： String extension in arrangement by tuple (if Mac)
  '''
  # Discrimination whether Windows or Mac.
  pf = platform.system()
  # Select extension to choose file
  if pf == 'Windows': # OS is Windows
    # wanted to make like this...  ex. fileTypes = [('data files','*.pdf;*.py')]
    ext_by_semic = ''
    for ext in list_of_ext:
      if ext == list_of_ext[0]:
        ext_by_semic = '*.{ext}'.format(ext=ext)
      else:
        ext_by_semic = ext_by_semic + '{semicolon}*.{ext}'.format(ext=ext,semicolon=';')
    fileTypes = [('data files', ext_by_semic)]
  elif pf == 'Darwin': # OS is Mac
    # wanted to make like this...  ex. fileTypes = [("csv files","*.csv"),("txt files","*.txt")]
    for ext in list_of_ext:
      ext_by_list = ['{ext} files'.format(ext=ext),'*.{ext}'.format(ext=ext)]
      ext_by_tuple = tuple(ext_by_list)
      if ext == list_of_ext[0]:
        fileTypes = [ext_by_tuple]
      else:
        fileTypes.append(ext_by_tuple)
      # set default "ext_by_tuple"
      ext_by_tuple = ""
  return fileTypes

def DecideNowFile(list_of_ext):
  '''
  list_of_ext ： List String extension
  nowDir      ： String absolutely directory of default folder
  nowFilePath ： String absolutely path of selected file
  '''
  if list_of_ext == []:
    list_of_ext = InputExt()
  else:
    pass
  nowDir = os.path.abspath(os.path.dirname(__file__))
  nowFilePath = filedialog.askopenfilename(filetypes=DecideExt(list_of_ext), initialdir=nowDir)
  print("File's Absollutely Path: {quotation}{filepath}{quotation}".format(quotation='"',filepath=nowFilePath))
  return nowFilePath

def DecideNowDir():
  '''
  nowDir     ： String absolutely directory default folder
  nowDirPath ： String absolutely path selected folder
  '''
  nowDir = os.path.abspath(os.path.dirname(__file__))
  nowDirPath = filedialog.askdirectory(initialdir=nowDir)
  print("Folder's Absollutely Path: {quotation}{folderpath}{quotation}".format(quotation='"',folderpath=nowDirPath))
  return nowDirPath

def GetFileList(folderdir, ext):
  '''
  folderdir : Selected folder's absolutely directory.
  ext        : extension
  folderlist : list about selected folder
  '''

  if folderdir == '':
    print("ERROR: No directory is selected.")
    sys.exit(0)

  folderList = glob2.glob('{folderpath}{sep}*.{ext}'.format(folderpath=folderdir,sep=sep,ext=ext))
  # sort order of list is irregulary if you use "glob"
  list.sort(folderList, reverse=False)
  print('Get file list in this folder.\n"', folderdir, '"\n\n........................\n')
  # Get list about files.
  for file in folderList:
    print(file)
  return folderList

def main(folderdir):
  GetFileList(folderdir)

if __name__ == "__main__":
  main(DirEditor.DecideNowDir())