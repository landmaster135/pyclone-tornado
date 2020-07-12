# DirSeperator.py
# code in shift-jis

import os
import platform
from tkinter import filedialog

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

def DecideNowFile():
  '''
  nowDir       ： String absolutely path default folder
  nowFilePath  ： String absolutely path selected file
  '''
  nowDir = os.path.abspath(os.path.dirname(__file__))
  nowFilePath = filedialog.askopenfilename(filetypes=DecideExt(InputExt()), initialdir=nowDir)
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
