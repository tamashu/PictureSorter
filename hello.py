from tkinter import filedialog
import os
import glob 

input_initial_dir = 'C:\\Users\\TamaruShugo\\Documents\\' #エスケープシーケンスで\\は\\\\で表記
input_dir_path = filedialog.askdirectory(initialdir = dir) 
print("input_dir_path: " +input_dir_path)

output_initial_dir = 'C:\\Users\\TamaruShugo\\Documents\\OpenGL' #エスケープシーケンスで\\は\\\\で表記
output_dir_path = filedialog.askdirectory(initialdir = dir) 

print("output_dir_path: " + output_dir_path)



# fld += '/**/'
files = glob.glob(os.path.join(output_dir_path ,'**' + os.sep)) #フォルダの一覧を取得

for file in files:
    file_name = os.path.basename(file.rstrip(os.sep)) #フォルダ名のみ抽出
    print(file_name)

