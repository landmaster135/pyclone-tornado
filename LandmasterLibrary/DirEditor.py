# DirSeperator.py
# code in shift-jis

import os, sys, platform
# IMPORT module FROM LandmasterLibrary
import FileListGetter
import InputController

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
    fileList = FileListGetter.GetFileList(FileListGetter.DecideNowDir(), ext)
    print('')
    inputMessage = 'Select mode. [ A: Add, D: Delete, R: Replace, E: Exit ]'
    ModeSelected = InputController.RepeatInputWithMultiChoices(inputMessage, ['A', 'D', 'R', 'E'])
    if ModeSelected == 'E':
        print('Exit.')
        sys.exit(0)

    TargetCharacterAlignment  = ''
    ReplaceCharacterAlignment = ''
    ModeDict_declare             = {'A': '--- Add mode ---', 'D': '--- Delete mode ---', 'R': '--- Replace mode ---'}
    ModeDict_message_for_target  = {'A': '', 'D': 'What character do you wanna delete? : ', 'R': 'What character do you wanna edit? : '}
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
            replaceFileName = '{dirname}{sep}{filename}.{ext}'.format(dirname=os.path.dirname(i),sep=sep,filename=AfterReplaceName,ext=ext)
            os.rename(targetFileName, replaceFileName)
    else:
        sys.exit(0)

def MakeDirectory(filename):
    '''
    filename  : String fullname of selected file.
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
    # # test code for ConfirmExecution()
    # ConfirmExecution('a', 'b')

    # # test code for DecideSeperator()
    # DecideSeperator()

    # test code for EditFileName()
    EditFileName()

if __name__ == "__main__":
    main()
