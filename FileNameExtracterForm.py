import os, sys, time, platform
import tkinter as tk
from tkinter import messagebox, filedialog, ttk, IntVar
import glob # ファイル走査に必要
import csv
from operator import itemgetter # リストのソートに必用

def FileNameExtracter(dirname):
    filenum = 0
    pf = platform.system() # WindowsかMacか判別
    if pf == 'Windows': # OSがWindows
        files = [] # ファイルの情報を格納する
        csv_file = str(textbox2.get()) # 書き込むCSVファイル名
        date_format = '%Y/%m/%d %H:%M:%S' # 日付の出力用

        if (dirname[-4:] == 'BOOK'): # 書籍のディレクトリから抽出する場合、
            for i in os.listdir(dirname): # 配列にファイル名を格納
                tp = dirname + '/' + i # ファイルのディレクトリを取得
                if os.path.isfile(tp): # そのパスが示すファイルが存在する場合はTrue、拡張子のないファイル名を示すパスの場合はFalse。
                    if tp == csv_file: # CSVファイルの場合、
                        pass
                    elif tp.find('.') == tp.find('_') - 1: # MAC用の一時ファイルの場合、
                        pass
                    else:
                        time_mod = time.strftime(date_format,time.localtime(os.path.getmtime(tp))) # ファイル作成日時を取得。
                        files.append([i,time_mod])
                else:
                    pass
            files.sort(key=lambda x: x[0])

    elif pf == 'Darwin': # OSがMac
        # ファイルの名前取得
        path_name = ''
        path = path_name & '.txt'
        files = os.listdir(path)
        files_file = [f for f in files if os.path.isfile(os.path.join(path,f))]

        # ファイルの名前のリストを作成
        if os.path.isfile(path):
            with open(path,mode='w') as f:
                f.write(files_file)
        else:
            with open(path,mode='x') as f:
                f.write(files_file)
    
    return filenum

def SelectDirectory():
    tk.messagebox.showinfo(title='FileNameExtracter',message='抽出するディレクトリを選択してください。')
    dirname = tk.filedialog.askdirectory()
    textbox1.insert(tk.END,dirname)
    for i in os.listdir(dirname):
        if os.path.isfile(dirname +'/' + i):
            if(i[-4:] == '.csv'):
                textbox2.insert(tk.END, dirname +'/' + i)
                break
    return dirname


def button1Pushed(event):
    dirname = ''
    textbox1.delete(0, tk.END)
    textbox2.delete(0, tk.END)
    dirname = SelectDirectory()
    tk.messagebox.showinfo(title="抽出完了",message="ファイル名の抽出が完了しました。\nCSVに書き込みます")
    filenum = FileNameExtracter(dirname)
    tk.messagebox.showinfo(title="書き込み完了",message="ファイル名の書き込みが完了しました。\nファイル数：" + str(filenum))


root = tk.Tk() #メインウィンドウを作成する
root.title("ファイル名を抽出")
widthRoot = 640
heightRoot = 480
root.geometry(str(widthRoot) + "x" + str(heightRoot)) #メインウィンドウのサイズを変える。

label1 = tk.Label(root, text="ディレクトリ")
label1.place(x=widthRoot, y=30)
label1.grid()

button1 = tk.Button(root, text="参照 & 抽出", background='#dddddd') #command="SelectDirectory","FileNameExtracter"
button1.place(x=100, y=40)
button1.bind("<Button-1>",button1Pushed) #"<Button-1>"はクリック、"<Button-2>"はホイールクリック、"<Button-3>"は右クリック。
button1.grid()

button2 = tk.Button(root, text='追加機能。。。', background='#dddddd') #ディレクトリ選択
button2.place(x=200, y=120)
button2.grid()

widthTB1 = 60
textbox1 = tk.Entry(width=widthTB1) #ディレクトリ表示
textbox1.place(x=100, y=60)
textbox1.grid()

widthTB2 = 60
textbox2 = tk.Entry(width=widthTB2) #CSVファイル名
textbox2.place(x=100, y=60)
textbox2.grid()

val1 = tk.BooleanVar()
val1.set(False)
checkbox1 = tk.Checkbutton(text=u"項目1", variable=val1)
checkbox1.grid()

scale1 = tk.Scale(root, variable=IntVar(), orient='h', label='↓ book_num_digit ↓', length = 150, from_=2, to=6)
scale1.pack
scale1.grid()

root.mainloop() #rootを表示し無限ループする。
