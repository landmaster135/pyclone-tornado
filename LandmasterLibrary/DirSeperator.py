# DirSeperator.py
# code in shift-jis

import platform

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
  DecideSeperator()

if __name__ == "__main__":
  main()
