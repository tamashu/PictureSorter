dir_name1 = "2023-01-30"
dir_name2 = "2021-05-10-日産"
dir_name3 = "2022-07-01_神奈川"
dir_name4 = "2018-02-25_test2"

dir_list = [dir_name1,dir_name2,dir_name3,dir_name4]
date_list = []

for dir in dir_list:
    date = dir[0:10]
    date_list.append(date)

for date in date_list:
    print(date)