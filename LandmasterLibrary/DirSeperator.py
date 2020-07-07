# DirSeperator.py
# code in shift-jis

import platform

def DecideSeperator():
    '''
    pf  : String system name of OS.
    sep : String seperator of directory.
    '''

    pf = platform.system() # WindowsかMacか判別
    print(type(pf))
    print(pf)
    sep = '' # ディレクトリのセパレータ
    if pf == 'Windows': # OS is Windows
        sep = '\\'
    elif pf == 'Darwin': # OS is Mac
        sep = '/'
    return sep

def main():
  DecideSeperator()

if __name__ == "__main__":
  main()
