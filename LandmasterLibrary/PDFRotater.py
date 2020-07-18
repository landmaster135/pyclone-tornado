# PDFRotater.py
# code in shift-jis

import os, sys
# IMPORT module FROM LandmasterLibrary
import DirEditor
sep = DirEditor.DecideSeperator() # String seperator of directory.
import FileListGetter

def MakeVertical(folderList):
    '''
    folderList        : list of file filtered with extension in the selected folder.
    filename          : fullname of selected file.
    original          : PdfFileReader of original files.
    rotated           : PdfFileWriter of rotated files.
    rotated_dir       : path of folder having rotated files.
    sum_page          : sum of page.
    sum_rotating_page : rotating pages. count 1 if make their vertical.
    '''
    # PyPDF2 version is 1.26.0
    from PyPDF2 import PdfFileWriter, PdfFileReader
    if len(folderList) != 0:
        filename = folderList[0]
    else:
        print('\nPDFRotater exits because of no target files.')
        sys.exit(0)

    rotated_dir = DirEditor.MakeDirectory(filename)

    for filename in folderList:
        print("Rotate all page of PDF:", filename)

        original = PdfFileReader(filename)
        rotated  = PdfFileWriter()

        # Display number of pages of original PDF file
        sum_page = original.getNumPages()
        print("page_num: ", sum_page)

        # Count pages at the same time as making vertical.
        sum_rotating_page = 0
        for i in range(0, sum_page, 1):
            print("Page ", i, " is ", original.getPage(i).get('/Rotate'), " degrees rotating")
            angle_rotating = original.getPage(i).get('/Rotate')
            if angle_rotating != 0:
                sum_rotating_page += 1
            rotated.addPage(original.getPage(i).rotateClockwise(360 - angle_rotating))

        # new file entry
        # output_filename = '{dirname}{sep}{basename}'.format(dirname=rotated_dir, sep=sep, basename=os.path.basename(filename))
        output_filename = DirEditor.GenerateFileName(rotated_dir, sep, os.path.basename(filename))
        with open(output_filename, "wb") as outputStream:
            rotated.write(outputStream)

        print("\nPDFRotater is terminated.\nsum_rotating_page: ", sum_rotating_page, " / ", sum_page)

    print('\n\nCheck new folder. "{}"'.format(rotated_dir))

def main():
    MakeVertical(FileListGetter.GetFileList(DirEditor.DecideNowDir(),'pdf'))

if __name__ == "__main__":
    main()