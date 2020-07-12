# DirSeperator.py
# code in shift-jis

import os
import platform

def MakeDirectory(filename):
  '''
  filename : String fullname of selected file.
  new_name  : String name of folder having rotated files.
  made_path : String path of folder having rotated files.
  '''
  new_name = input("Input a name of new folder: ")
  made_path = '{dirname}{sep}{newpath}'.format(dirname=os.path.dirname(filename),sep=DecideSeperator(),newpath=new_name)
  while os.path.isdir(made_path) == True:
    new_name = input("That name already exists. Reinput: ")
    # new path entry
    made_path = '{dirname}{sep}{newpath}'.format(dirname=os.path.dirname(filename),sep=DecideSeperator(),newpath=new_name)

  # make new directory if new directory is none.
  if os.path.isdir(made_path) == False:
    os.mkdir(made_path)
  return made_path

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
