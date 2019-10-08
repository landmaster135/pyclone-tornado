import os

# ！！！「playlist_maker」のディレクトリで行うこと。！！！

#------------ 曲一覧のテキストファイルの作成 --------------
trigger = 1
if trigger == 0:
    data = ""
    file_name = 'ダムルー.txt'

    with open(file_name, encoding="utf-8") as f:
        data = f.read()

    data = data.replace("C:\\Users\\Riku\\Music\\MusicBee\\Music\\", "")

    with open(file_name, mode="w", encoding="utf-8") as f:
        f.write(data)

#------------- プレイリストの作成 --------------

list_type = -1

print('このプログラムではプレイリストの編集を行います。')
print('プレイリストのタイプはどれにしますか？')
while(list_type == -1):
    list_type = input('0:Windows, 1:Walkman, 2:Android,,,,,')
    if str.isdigit(list_type):
        if int(list_type) < 0 or int(list_type) > 2:
            print('入力値が不正です。もう一度入力して下さい。')
            list__type = -1
        else:
            pass
    else:
        print('入力値が不正です。もう一度入力して下さい。')
print('{}ですね'.format(int(list_type)))

head_Windows = 'C:\\Users\\Riku\\Music\\MusicBee\\Music\\' # list_type = 0、適当に変更すべし。
head_Walkman = '#EXTINF:,\n'                               # list_type = 1、適当に変更すべし。
head_Android = '/sdcard/Music/Musik/'                      # list_type = 2、適当に変更すべし。
file_name = '' # 基のテキストファイル名
data_line = '' # テキストデータ

os.chdir(os.path.dirname(os.path.abspath(__file__))) # 実行ファイルのディレクトリに移動

if file_name[:-4] != '.txt':
    file_name = input('それでは、基となるテキストファイル名を入力して下さい。')

with open(file_name, encoding="utf-8") as f: # ファイルを読み込み
    data_line = f.read()

head_list = [head_Windows, head_Walkman, head_Android] # 先頭のパスのリスト
ex_list = [".m3u", ".M3U8", ".m3u"]                    # 拡張子のリスト
sep_list = ['\\', '/', '/']                            # 区切り文字のリスト

data_line = data_line.replace("\n", "\n{}".format(head_list[int(list_type)])) # テキストデータ内の先頭のパスを編集
data_line = data_line.replace('\\', sep_list[int(list_type)])                 # テキストデータ内の区切り文字を編集
data_line = head_list[int(list_type)] + data_line                             # テキストデータ内の1行目の先頭のパスを編集
if int(list_type) == 1:                                                       # Walkman用の場合だけ、
    data_line = '#EXTM3U\n' + data_line

with open(file_name.replace('.txt', ex_list[int(list_type)]), mode="w", encoding="utf-8") as f: # ファイルに書き込み
    f.write(data_line)
