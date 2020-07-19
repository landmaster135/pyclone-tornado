# TextEditor.py
# code in shift-jis

import os, sys, platform
# IMPORT module FROM LandmasterLibrary
import InputController
import DirEditor
sep = DirEditor.DecideSeperator() # String seperator of directory.

def WritePlaylist(fileName, extracted_dir, PlaylistType):
    '''
    fileName      : String absolutely filename of target file.
    extracted_dir : String directory to save file exported extracted data.
    PlaylistType  : String type of Playlist.
    head_Windows  : String directory of music you wanna listen to in Windows. Edit suitably.
    head_Walkman  : String directory of music you wanna listen to in Walkman. Edit suitably.
    head_Android  : String directory of music you wanna listen to in Android. Edit suitably.
    data_line     : String text data for playlist.
    headDict      : Dictionary of String directory of music you wanna listen to.
    extDict       : Dictionary of String extension of a file of playlist.
    sepDict       : Dictionary of String seperator for playlist.
    exportName    : String absolutely filename to export.
    '''

    head_Windows = 'C:\\Users\\Riku\\Music\\MusicBee\\Music\\'
    head_Walkman = '#EXTINF:,\n'
    head_Android = '/sdcard/Music/Musik/'
    data_line    = ''

    headDict = {'0': head_Windows, '1': head_Walkman, '2': head_Android}
    extDict  = {'0': '.m3u', '1': '.M3U8', '2': '.m3u'}
    sepDict  = {'0': '\\',   '1': '/',     '2': '/'}

    with open(fileName, encoding="utf-8") as f: # ファイルを読み込み
        data_line = f.read()

    data_line = data_line.replace("\n", "\n{}".format(headDict[PlaylistType])) # テキストデータ内の先頭のパスを編集
    data_line = data_line.replace('\\', sepDict[PlaylistType])                 # テキストデータ内の区切り文字を編集
    data_line = headDict[PlaylistType] + data_line                             # テキストデータ内の1行目の先頭のパスを編集
    # only Walkman.
    if PlaylistType == '1':
        data_line = '#EXTM3U\n' + data_line

    exportName = DirEditor.GenerateFileName(extracted_dir, sep, os.path.basename(fileName).replace('.txt', extDict[PlaylistType]))
    with open(exportName, mode="w", encoding="utf-8") as f:
        f.write(data_line)


def WriteCSV(targetFile, targetList):
    '''
    targetFile : String absolutely filename of target file.
    targetList : List of contents to write.
    '''
    # write 1 line.
    with open(targetFile, mode='a') as f:
        for m in range(0, len(targetList)):
            # memorize to "should_not_exist_yubin.csv" sheet
            if m != len(targetList) - 1:
                f.write("%s," % targetList[m])
            else:
                f.write("%s" % targetList[m])
        f.write("\n")

def WriteText(fileName, nowList):
    '''
    fileName : String absolutely path of selected file
    nowList  : List of statement to write
    '''
    with open(fileName, 'w') as f:
        for n in nowList:
            f.write("%s\n" % n)

def main():
    # test code for WriteText()
    WriteText(DirEditor.DecideNowDir(), ['apple', 'banana', 'orange'])

if __name__ == "__main__":
    main()
