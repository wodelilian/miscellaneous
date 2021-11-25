import requests
import time
src_list = []  # 创建一个空图片地址列表
headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'}
for i in range(947255,947500):
    url = "https://mfiles.alphacoders.com/947/thumb-1920-{}.jpg".format(i)
    src_list.append(url)
count = 0
for src in src_list:
    try:
        count = count+1
        response = requests.get(src,headers=headers)
        # time.sleep(1)
        date = response.content
        downlaod ="D:/下载/iphone/"+time.strftime("%Y_%m_%d_%H_%M_%S")+str(count)+".png"
        with open(downlaod,"wb") as f:  # 通过wb的方法将找到的内容写进文件夹里
            f.write(date)
            print("成功下载第{}张".format(count))
    except:
        print("第{}张下载失败".format(count))
