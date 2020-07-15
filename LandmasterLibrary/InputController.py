# DirSeperator.py
# code in shift-jis

import os, sys

def RepeatInputWithMultiChoices(firstMessage, choiceList):
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
            inputMessage = 'Retry. [ "'
            for i in range(0, len(choiceList)):
                if i == 0:
                    inputMessage += '{choice}"'.format(choice=choiceList[i])
                else:
                    inputMessage += ' or "{choice}"'.format(choice=choiceList[i])
            inputMessage += ' ]: '
        inputChr = input(inputMessage)
        # Check by message.
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
