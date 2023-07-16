import customtkinter
from tkinter import filedialog  #ディレクトリのパス取得用
from PIL import Image           #画像の情報取得用
from PIL.ExifTags import TAGS   #
import shutil                   #ファイルのコピー用
import os                       
import glob 

FONT_TYPE = "meiryo"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # メンバー変数の設定
        self.fonts = (FONT_TYPE, 18)

        # フォームのセットアップをする
        self.setup_form()

    def setup_form(self):
        # CustomTkinter のフォームデザイン設定
        customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
        customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

        # フォームサイズ設定
        self.geometry("600x700")
        self.title("Picture Sorter")
        
        #が目サイズ変更時にテキストボックスのみサイズ可変にする
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        #ファイル選択のフレーム
        self.read_file_frame = SelectInputOutputDirFrame(master=self)
        self.read_file_frame.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        #状態を表示するテキストボックス
        self.result_textbox = customtkinter.CTkTextbox(master=self, width=200, corner_radius=5, state="disabled", font=self.fonts)
        self.result_textbox.grid(row=1, column=0, sticky="nsew")
        self.insertStringToTextBox("Select Input and Output Folder")

       #実行ボタンの表示
        self.Execute_button = customtkinter.CTkButton(master=self, text="Execute!!", command=self.executeButtonFunction, font=self.fonts)
        self.Execute_button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")
        

    #実行ボタンが押されたときの処理
    def executeButtonFunction(self):
        #入力ファイルのみ選び,出力先を選んでいない時
        if self.read_file_frame.is_select_input_file and not self.read_file_frame.is_select_output_dir:
            self.insertStringToTextBox("Chose Output File")
        
        #入力ファイルが選ばれず,出力ファイルが選ばれている時
        elif not self.read_file_frame.is_select_input_file and self.read_file_frame.is_select_output_dir:
            self.insertStringToTextBox("Chose Input File")
            
        #どちらも選ばれていない時
        elif not self.read_file_frame.is_select_input_file and not self.read_file_frame.is_select_output_dir:
            self.insertStringToTextBox("Chose Input And Output File")
            
        #どちらも選ばれている時
        else:
            self.insertStringToTextBox("Now Executing ...")

            self.movePictureFiles(self.read_file_frame.input_file_path,self.read_file_frame.output_dir_path)

            self.insertStringToTextBox("Done ...")
            
        
    #テキストボックスに文字列を表示するための関数
    def insertStringToTextBox(self,string):
        self.deleteStringInTextBox()
        self.result_textbox.configure(state = "normal")
        self.result_textbox.insert("0.0", string )
        self.result_textbox.configure(state = "disable")
    
    def deleteStringInTextBox(self):
        self.result_textbox.configure(state = "normal")
        self.result_textbox.delete("0.0","3.0")
        self.result_textbox.configure(state = "disable")


    def getImageDate(self,input_image_path): #引数は画像のパス 戻り値は画像の日付
        date = ""
        img = Image.open(input_image_path)
        exif = img.getexif()
        dic_ = {}

        if exif: #exif情報があるとき
            for id, value in exif.items():
                dic_[TAGS.get(id,id)] = value
            date = dic_['DateTime'].split(' ')[0].replace(':','-') #画像の日付

        return date


    def getDateList(self,output_dir_path): #引数はディレクトリのリスト 戻り値は日付のリスト
        dir_list =[]

        existed_dir_list = glob.glob(os.path.join(output_dir_path ,'**' + os.sep)) #フォルダの一覧を取得
        for dir in existed_dir_list:
            dir_name = os.path.basename(dir.rstrip(os.sep)) #フォルダ名のみ抽出
            dir_list.append(dir_name)

        date_list = [] #フォルダにある日付のリスト
        for dir in dir_list:
            date = dir[0:10]
            date_list.append(date)

        return date_list 
    
    def movePictureFiles(self,input_dir_path,output_dir_path):
    
        #入力元のファイルのパスを取得
        new_dir_list = [] #作成したディレクトリの名前
        #出力先のディレクトリのフォルダの日付のリスト(プログラム始動前にあるディレクトリの日付のリスト)
        date_list = self.getDateList(output_dir_path)

        input_file_path = input_dir_path +"/*"
        files = glob.glob(input_file_path)

        #それぞれの画像について繰り返し
        for file in files: #ファイルは画像の絶対パス
            if file[-4:] == ".jpg" or file[-4:] == ".JPG" or file[-4:] == ".JPEG" : #拡張子が画像ファイルのとき
                date = self.getImageDate(file) #画像の日付を得る
                if date in date_list: #画像の日付のディレクトリが既にあるなら(既に取り込んでいるなら)
                    print("既にファイルがあるため終了します")
                    return #return でいいのか検討(exit()の方がいい？)
                
                elif(date in new_dir_list):#画像の日付が新しく作成したディレクトリに含まれているなら
                    output_dir = output_dir_path + '/' + date
                    shutil.copy2(file,output_dir)

                else: #画像の日付がディレクトリに無いなら
                    new_dir_name = output_dir_path + '/' + date

                    os.mkdir(new_dir_name) #日付でディレクトリの作成
                    new_dir_list.append(date)#作成したディレクトリの日付を覚えておく
                    shutil.copy2(file,new_dir_name)


#ファイル選択用のフレーム
class SelectInputOutputDirFrame(customtkinter.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.fonts = (FONT_TYPE, 15)

        self.input_file_path = "Select Input Folder"     #入力ファイルのパス
        self.output_dir_path = "Select Output Folder"    #出力ファイルのパス
        self.is_select_input_file = False                #入力ファイルが選択されているか
        self.is_select_output_dir = False                #出力ファイルが選択されているか

        # フォームのセットアップをする
        self.setup_form_in_out_frame()
    
    def setup_form_in_out_frame(self):
        
        #が目サイズ変更時にテキストボックスのみサイズ可変にする
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)


        #入力のテキストボックス
        self.input_file_textbox = customtkinter.CTkEntry(master=self, placeholder_text= self.input_file_path, width=220, font=self.fonts)
        self.input_file_textbox.configure(state="disabled")
        self.input_file_textbox.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # 入力ボタンを表示する
        self.input_file_select_button = customtkinter.CTkButton(master=self, text="chose input folder", command=self.inputFileButtonFunction, font=self.fonts)
        
        self.input_file_select_button.grid(row=0, column=1, padx=20, pady=20, sticky="ew")

        #出力のテキストボックス
        self.output_dir_textbox = customtkinter.CTkEntry(master=self, placeholder_text= self.output_dir_path, width=220, font=self.fonts)
        self.output_dir_textbox.configure(state="disabled")
        self.output_dir_textbox.grid(row=1, column=0, padx=20, pady=20, sticky="ew")

        # 出力ボタンを表示する
        self.output_dir_select_button = customtkinter.CTkButton(master=self, text="chose output folder", command=self.outputDirButtonFunction, font=self.fonts)
        self.output_dir_select_button.grid(row=1, column=1, padx=20, pady=20, sticky="ew")

        #input_file_select_buttonが押されたときの処理(input_file_pathの選択)
    def inputFileButtonFunction(self):
        #画像の入力元のパスの選択
        input_initial_dir = 'C:/Users/TamaruShugo/Documents/' 
        self.input_file_path = filedialog.askdirectory(initialdir = dir) 
        
        #テキストボックスに文字を表示
        self.input_file_textbox.configure(state="normal")
        self.input_file_textbox.insert(0, self.input_file_path)  # insert at line 0 character 0
        self.input_file_textbox.configure(state="disabled")
        self.is_select_input_file = True
    
    def outputDirButtonFunction(self):
        # テキストボックスに入力されたテキストを表示する
        #画像の出力先のパスの選択
        output_initial_dir = 'C:/Users/TamaruShugo/Documents/OpenGL' 
        self.output_dir_path = filedialog.askdirectory(initialdir = dir)

         #テキストボックスに文字を表示
        self.output_dir_textbox.configure(state="normal")
        self.output_dir_textbox.insert(0, self.output_dir_path)  # insert at line 0 character 0
        self.output_dir_textbox.configure(state="disabled")
        self.is_select_output_dir = True
        
    


if __name__ == "__main__":
    # アプリケーション実行
    app = App()
    app.mainloop()