# DirSeperator.py
# code in shift-jis

import os, sys, platform
from tkinter import filedialog
# IMPORT module FROM LandmasterLibrary
import InputController

def DecideSaveFileName(dirname, list_of_ext):
    '''
    list_of_ext  : List String extension
    dirname      : String absolutely directory of default folder
    saveFilePath : String absolutely path of selected file
    '''
    if list_of_ext == []:
        list_of_ext = InputExtList()
    else:
        pass
    saveFilePath = filedialog.asksaveasfilename(filetypes=DecideExt(list_of_ext), initialdir=dirname ,title = "Save As")
    print("File's Absolutely Path: {quotation}{filepath}{quotation}".format(quotation='"',filepath=saveFilePath))
    return saveFilePath

def GenerateFileName(dirname, sep, filenameWithExt):
    '''
    dirname           : String directory name.
    sep               : String seperator of direcotry.
    filenameWithExt   : String filename with extension. (name of directory is also OK.)
    GeneratedFileName : String FileName Generated in this function.
    '''
    GeneratedFileName = '{dirname}{sep}{filename}'.format(dirname=dirname,sep=sep,filename=filenameWithExt)
    return GeneratedFileName

def MakeDirectory(filename):
    '''
    filename  : String fullname of selected file.
    new_name  : String name of folder having rotated files.
    made_path : String path of folder having rotated files.
    '''
    new_name = input("Input a name of new folder: ")
    # made_path = '{dirname}{sep}{newpath}'.format(dirname=os.path.dirname(filename),sep=DecideSeperator(),newpath=new_name)
    made_path = GenerateFileName(os.path.dirname(filename), DecideSeperator(), new_name)
    while os.path.isdir(made_path) == True:
        new_name = input("That name already exists. Reinput: ")
        # new path entry
        # made_path = '{dirname}{sep}{newpath}'.format(dirname=os.path.dirname(filename),sep=DecideSeperator(),newpath=new_name)
        made_path = GenerateFileName(os.path.dirname(filename), DecideSeperator(), new_name)

    # make new directory if new directory is none.
    if os.path.isdir(made_path) == False:
        os.mkdir(made_path)

    return made_path

def InputExtList(ext_range=10):
    '''
    ext_range   : Integer number of extensions you can selecet
    list_of_ext : List String extension
    moreFile    : String extension
    '''
    list_of_ext = []
    for i in range(0, ext_range):
        # Varify message by times.
        if i == 0:
            moreFile = input("What filetype (extension)?: ")
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
    list_of_ext  : List String extension
    fileTypes    : List type of file for choose file in the dialog

    ext          : String extension
    ext_by_semic : String extension in arrangement by semicolon (if Windows)
    ext_by_list  : String extension in arrangement by list (if Mac)
    ext_by_tuple : String extension in arrangement by tuple (if Mac)
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
            ext_by_list  = ['{ext} files'.format(ext=ext),'*.{ext}'.format(ext=ext)]
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
    list_of_ext : List String extension
    nowDir      : String absolutely directory of default folder
    nowFilePath : String absolutely path of selected file
    '''
    if list_of_ext == []:
        list_of_ext = InputExtList()
    else:
        pass
    nowDir = os.path.abspath(os.path.dirname(__file__))
    nowFilePath = filedialog.askopenfilename(filetypes=DecideExt(list_of_ext), initialdir=nowDir)
    print("File's Absolutely Path: {quotation}{filepath}{quotation}".format(quotation='"',filepath=nowFilePath))
    return nowFilePath

def DecideNowDir():
    '''
    nowDir     : String absolutely directory default folder
    nowDirPath : String absolutely path selected folder
    '''
    nowDir = os.path.abspath(os.path.dirname(__file__))
    nowDirPath = filedialog.askdirectory(initialdir=nowDir)

    # Discrimination whether Windows or Mac.
    pf = platform.system()
    if pf == 'Windows': # OS is Windows
        nowDirPath = nowDirPath.replace('/', '\\')
    print("Folder's Absolutely Path: {quotation}{folderpath}{quotation}".format(quotation='"',folderpath=nowDirPath))
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
    # test code for DecideSeperator()
    DecideSeperator()

if __name__ == "__main__":
    main()
