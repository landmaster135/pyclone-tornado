# InputController.py
# code in shift-jis

import os, sys
import re # regular expression

def CheckWhetherSjisExists(targetStrList, callingfilename_with_ext):
    '''
    targetStrList            : String List target for check.
    callingfilename_with_ext : String absolutely name of calling file with extension
    checkStr                 : String filter for check.
    isSjisContained          : Boolean.
    basefilename_without_ext : String name of calling file without extension.
    '''
    checkStr = re.compile('[\\a-zA-Z0-9\-\_\.\-\s\:\~\^\=]+')
    isSjisContained = False
    for i in targetStrList:
        if checkStr.fullmatch(i) == None:
            isSjisContained = True
        print('\nCheckWhetherSjisExists : targetStr is "{}" ・・・・・・ isSjisContained == {}'.format(i, isSjisContained))

    basefilename_without_ext = os.path.splitext(os.path.basename(callingfilename_with_ext))[0]
    if isSjisContained == True:
        print('\n\n{} exits because of the directory containing shift-jis character.'.format(basefilename_without_ext))
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
            if type(choiceList[0]) is int:
                if int(inputChr) >= 0 and int(inputChr) <= 100:
                    isInputCorrect = True
                    inputChr = int(inputChr)
                else:
                    pass
            elif type(choiceList[0]) is str:
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
