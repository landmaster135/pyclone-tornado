# FileListGetter.py
# code in shift-jis

import glob2
import os, sys, platform
import time
# IMPORT module FROM LandmasterLibrary
import InputController
import DirEditor
sep = DirEditor.DecideSeperator() # String seperator of directory.
import TextEditor

def ExtractFileName_BOOK():
    '''
    nowDir         : String name of now direcotry.
    fileList       : List of String filename.
    fileName       : String exported filename.
    ExportFileName : String exported absolutely filename.
    dataListEXP    : List to export as CSV.           [[], [], ...]
    dataList       : List to memorize to dataListEXP. [, , ...]
    time_mod       : String data of date and time.
    '''
    nowDir         = DirEditor.DecideNowDir()
    fileList       = GetFileList(nowDir,DirEditor.InputExtList(ext_range=1)[0])
    ExportFileName = DirEditor.DecideSaveFileName(nowDir, ["csv"])

    dataListEXP = []
    dateFormat = '%Y/%m/%d %H:%M:%S' # 日付の出力用
    for f in fileList:
        dataList = []
        # get date and time this file is updated
        time_mod = time.strftime(dateFormat,time.localtime(os.path.getmtime(f)))
        dataList.append(f)
        dataList.append(time_mod)
        dataListEXP.append(dataList)
    for data in dataListEXP:
        TextEditor.WriteCSV(ExportFileName, data)

    print('ExtractFileName_BOOK is terminated')
    print('Check directory "{dirname}"'.format(dirname=ExportFileName))

def ConfirmExecution(target, replace):
    '''
    target              : String character you wanna delete or replace from.
    replace             : String character you wanna add or replace to.
    inputMessage        : String message for first input.
    ExecuteConfirmation : String Yes or No. [ 'y' / 'n' ]
    '''
    inputMessage        = ''
    ExecuteConfirmation = ''
    if target == '' and replace == '':
        print('Nothing to edit fileName.')
        return 'n'
    elif target == '':
        inputMessage = 'I will add with "{replace}", OK? [ y / n ] : '.format(replace=replace)
    elif replace == '':
        inputMessage = 'I will delete "{target}", OK? [ y / n ] : '.format(target=target)
    else:
        inputMessage = 'I will rename {target} → {replace}, OK? [ y / n ] : '.format(target=target,replace=replace)
    ExecuteConfirmation = InputController.RepeatInputWithMultiChoices(inputMessage, ['y', 'n'])
    return ExecuteConfirmation

def EditFileName():
    '''
    sep                          : String sperator of directory. It varies by os platform.
    ext                          : String extension.
    fileList                     : List, String absolutely path, of file filtered with extension in the selected folder.
    ModeSelected                 : String selected mode.
    ModeDict_declare             : Dictionary of String to declare current mode.
    ModeDict_message_for_target  : Dictionary of String message for inputting target character in current mode.
    ModeDict_message_for_replace : Dictionary of String message for inputting replace character in current mode.
    inputMessage                 : String message for input.
    ForwardOrBack                : String which point do you input new character, Forward or Back. [ 'F' / 'B' ]
    TargetCharacterAlignment     : String character you wanna delete or replace from.
    ReplaceCharacterAlignment    : String character you wanna add or replace to.
    ExecuteConfirmation          : String Yes or No. [ 'y' / 'n' ]
    AfterReplaceName             : String replaced filename. (only filename)
    targetFileName               : String absolutely target filename.
    replaceFileName              : String absolutely replaced filename.
    '''
    sep = DecideSeperator()
    ext = input('What Extension? (without ".") : ')
    fileList = FileListGetter.GetFileList(DirEditor.DecideNowDir(), ext)
    inputMessage = 'Select mode. [ A: Add, D: Delete, R: Replace, E: Exit ]'
    ModeSelected = InputController.RepeatInputWithMultiChoices(inputMessage, ['A', 'D', 'R', 'E'])
    if ModeSelected == 'E':
        print('Exit.')
        sys.exit(0)

    TargetCharacterAlignment  = ''
    ReplaceCharacterAlignment = ''
    ModeDict_declare             = {'A': '--- Add mode ---', 'D': '--- Delete mode ---', 'R': '--- Replace mode ---'}
    ModeDict_message_for_target  = {'A': '', 'D': 'What character do you wanna delete? : ', 'R': 'What character do you wanna edit?\n(You should copy character from target file.) : '}
    ModeDict_message_for_replace = {'A': 'What character do you wanna add with? : ', 'D': '', 'R': 'What character do you wanna edit with? : '}
    print(ModeDict_declare[ModeSelected])
    if ModeSelected == 'A':
        # F : edit by using directory's seperator, B : edit by using extension's dot.
        inputMessage  = 'Which point do you wanna edit, Forward or Back? [ F / B ] : '
        ForwardOrBack = InputController.RepeatInputWithMultiChoices(inputMessage, ['F', 'B'])
    try:
        if ModeSelected != 'A':
            TargetCharacterAlignment  = input(ModeDict_message_for_target[ModeSelected])
        if ModeSelected != 'D':
            ReplaceCharacterAlignment = input(ModeDict_message_for_replace[ModeSelected])
        ExecuteConfirmation = ConfirmExecution(TargetCharacterAlignment, ReplaceCharacterAlignment)
    except KeyError:
        print('Error. Exit.')
        sys.exit(0)

    if ExecuteConfirmation == 'y':
        for i in fileList:
            AfterReplaceName = ''
            if ModeSelected == 'A':
                if ForwardOrBack == 'F':
                    AfterReplaceName = ReplaceCharacterAlignment + os.path.splitext(os.path.basename(i))[0]
                elif ForwardOrBack == 'B':
                    AfterReplaceName = os.path.splitext(os.path.basename(i))[0] + ReplaceCharacterAlignment
            elif ModeSelected == 'D' or ModeSelected == 'R':
                AfterReplaceName = os.path.splitext(os.path.basename(i))[0].replace(TargetCharacterAlignment, ReplaceCharacterAlignment)
            targetFileName  = i
            replaceFileName = GenerateFileName(os.path.dirname(i), sep, '{filename}.{ext}'.format(filename=AfterReplaceName, ext=ext))
            os.rename(targetFileName, replaceFileName)
    else:
        sys.exit(0)

def GetFileList(folderdir, ext):
    '''
    folderdir  : String selected folder's absolutely directory.
    ext        : String extension
    folderlist : List about selected folder
    '''

    if folderdir == '':
        print("ERROR: No directory is selected.")
        sys.exit(0)

    folderList = glob2.glob(DirEditor.GenerateFileName(folderdir, sep, '*.{ext}'.format(ext=ext)))

    # sort order of list is irregulary if you use "glob"
    list.sort(folderList, reverse=False)
    print('Get file list in this folder.\n"', folderdir, '"\n\n........................\n')
    # Get list about files.
    for file in folderList:
        print(file)
    return folderList

def main():
    # # test code for ExtractFileName_BOOK()
    # ExtractFileName_BOOK()

    # # test code for ConfirmExecution()
    # ConfirmExecution('a', 'b')

    # # test code for EditFileName()
    # EditFileName()

    # test code for GetFileList()
    GetFileList(DirEditor.DecideNowDir(), 'jpg')

if __name__ == "__main__":
    main()