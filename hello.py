from tkinter import filedialog
from PIL import Image
from PIL.ExifTags import TAGS
import os
import glob 

def getImageDate(input_image_path):
    img = Image.open(input_image_path)
    exif = img.getexif()
    dic_ = {}
    if exif: #exif情報があるとき
        for id, value in exif.items():
            dic_[TAGS.get(id,id)] = value
    print(dic_['DateTime'].split(' ')[0])



input_initial_dir = 'C:/Users/TamaruShugo/Documents/' 
input_dir_path = filedialog.askdirectory(initialdir = dir) 

input_file_path = input_dir_path +"/*"
files = glob.glob(input_file_path)
for file in files:
    # print("入力写真:" +file)
    getImageDate(file)

# print("input_dir_path: " +input_dir_path)


output_initial_dir = 'C:/Users/TamaruShugo/Documents/OpenGL' 
output_dir_path = filedialog.askdirectory(initialdir = dir) 

# print("output_dir_path: " + output_dir_path)


existed_dir_list = glob.glob(os.path.join(output_dir_path ,'**' + os.sep)) #フォルダの一覧を取得

for dir in existed_dir_list:
    dir_name = os.path.basename(dir.rstrip(os.sep)) #フォルダ名のみ抽出
    print(dir_name)

