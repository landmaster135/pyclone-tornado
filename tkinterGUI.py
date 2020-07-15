# code by utf-8
# tkinterGUI.py

# from Tkinter import Tk, Label, Button, BOTTOM
# from Tk import Tk, Label, Button, BOTTOM
from tkinter import *
from tkinter import Tk, Label, Button, BOTTOM, Entry, messagebox, ttk
# from cx_Freeze import setup, Executable

def DisplayUI():
    '''
    '''
    # ".pack()" and ".grid()" cannot use at the same time.

    def button1_click():
        input_value = input_box.get()
        messagebox.showinfo("クリックイベント",input_value + "が入力されました。")

    root = Tk()
    root.title('Button')
    root.geometry("500x300")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    # input_box = Entry(width=100)
    # input_box.place(x=10, y=100)
    # Label(text='I am a button').pack(pady=15)
    # button1 = Button(text='Button',command=button1_click).pack(side=BOTTOM)

    # Frame
    frame = ttk.Frame(root, padding=10)
    frame.grid(sticky=(N, W, S, E))
    frame.columnconfigure(0, weight=1)
    frame.rowconfigure(0, weight=1)

    # スケールの作成
    val = DoubleVar()
    sc = ttk.Scale(
        frame,
        variable=val,
        orient=HORIZONTAL,
        length=200,
        from_=0,
        to=255,
        command=lambda e: print('val:%4d' % val.get()))
    sc.grid(row=0, column=0, sticky=(N, E, S, W))

    root.mainloop()

def main():
    DisplayUI()

if __name__ == "__main__":
    main()