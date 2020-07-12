# DirSeperator.py
# code in shift-jis

import os
import platform
from tkinter import filedialog

def DecideNowFile():
  '''
  list_of_ext ： List String extension
  fileTypes   ： List type of file for choose file in the dialog
  moreFile    ： String extension

  ext          ： String extension
  ext_by_semic ： String extension in arrangement by semicolon (if Windows)
  ext_by_list  ： String extension in arrangement by list (if Mac)
  ext_by_tuple ： String extension in arrangement by tuple (if Mac)
  nowDir       ： String absolutely path default folder
  nowFilePath  ： String absolutely path selected file
  '''
  list_of_ext = []
  # Number of extensions you can selecet is under 10.
  for i in range(10):
    if i == 0:
      moreFile = input("What filetype do you wanna take?: ")
    else:
      moreFile = input('more filetype?(* or "nothing"): ')
    if moreFile != "nothing":
      list_of_ext.append(moreFile)
    else:
      break

  # Discrimination whether Windows or Mac.
  pf = platform.system()
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
    fileTypes = [("csv files","*.csv"),("txt files","*.txt")]
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

  nowDir = os.path.abspath(os.path.dirname(__file__))
  nowFilePath = filedialog.askopenfilename(filetypes=fileTypes, initialdir=nowDir)
  print("File's Absollutely Path: {quotation}{filepath}{quotation}".format(quotation='"',filepath=nowFilePath))
  return nowFilePath

def DecideNowDir():
  '''
  nowDir     ： String absolutely path default folder
  nowDirPath ： String absolutely path selected folder
  '''
  nowDir = os.path.abspath(os.path.dirname(__file__))
  nowDirPath = filedialog.askdirectory(initialdir=nowDir)
  print("Folder's Absollutely Path: {quotation}{folderpath}{quotation}".format(quotation='"',folderpath=nowDirPath))
  return nowDirPath

def DecideSeperator():
    '''
    pf  : String system name of OS.
    sep : String seperator of directory.
    '''

    # Discrimination whether Windows or Mac.
    pf = platform.system()
    sep = ''
    if pf == 'Windows': # OS is Windows
        sep = '\\'
    elif pf == 'Darwin': # OS is Mac
        sep = '/'
    return sep

def main():
  # DecideSeperator()
  DecideNowFile()

if __name__ == "__main__":
  main()
