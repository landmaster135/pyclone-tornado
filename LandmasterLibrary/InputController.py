# InputController.py
# code in shift-jis

import os, sys
import re # regular expression

def CheckWhetherSjisExists(targetStr, callingfilename_without_ext):
    '''
    targetStr                : String target for check.
    basefilename_without_ext : String name of calling file without extension.
    checkStr                 : String filter for check.
    '''
    print("targetStr:   " + targetStr)
    print("callingfilename_without_ext:   " + callingfilename_without_ext)
    checkStr = re.compile('[\\a-zA-Z0-9\-\_\.\-\s\:\~\^\=]+')
    if checkStr.fullmatch(targetStr) == None:
        print('\n{} exits because of the directory containing shift-jis character.'.format(callingfilename_without_ext))
        return True
    return False

def RepeatInputWithMultiChoices(firstMessage, choiceList=[]):
    '''
    firstMessage   : String message for the first input.
    choiceList     : List of String choice.
    isInputCorrect : Boolean input is correct or not.
    isFirstInput   : Boolean this input is the first time or not.
    inputMessage   : String message for input.
    inputChr       : String input character.
    '''
    isInputCorrect = False
    isFirstInput   = True
    inputMessage   = ''
    inputChr       = ''
    while isInputCorrect == False:
        if isFirstInput == True:
            # Create message for the first input.
            inputMessage = firstMessage
        else:
            # Create message.
            inputMessage = 'Retry.'
            if choiceList == []:
                pass
            else:
                inputMessage += ' [ "'
                for i in range(0, len(choiceList)):
                    if i == 0:
                        inputMessage += '{choice}"'.format(choice=choiceList[i])
                    else:
                        inputMessage += ' or "{choice}"'.format(choice=choiceList[i])
                inputMessage += ' ]: '
        inputChr = input(inputMessage)
        # Check by message.
        if inputChr == '':
            pass
        else:
            if choiceList == []:
                isInputCorrect = True
            else:
                for choice in choiceList:
                    if inputChr == choice:
                        isInputCorrect = True
                        break
        isFirstInput = False
    return inputChr

def main():
    # test code for RepeatInputWithMultiChoices()
    RepeatInputWithMultiChoices()

if __name__ == "__main__":
    main()
