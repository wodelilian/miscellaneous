import requests
from bs4 import BeautifulSoup
import os
import time
src_list = []  # 创建一个空图片地址列表
headers = {"User-Agent": '请求头信息'}
for i in range(1,3):  # 爬取一到三页
    url = "https://网站地址{}".format(i)
    response = requests.get(url=url,headers=headers)  # 访问网页
    date = response.text
    soup = BeautifulSoup(date,"html.parser")  # 通过BeautifulSoup的方法解析网址内容
    # print(soup)
    for i in range (1,27):
        src = soup.select("body > div > div.l-body > div.l-layout.l-layout_wide > div > div.content-main > div.wallpapers.wallpapers_zoom.wallpapers_main > ul > li:nth-child("+str(i)+") > a > span.wallpapers__canvas > img")
        # 通过CSS选择器找规律
        # print(src)
        for src in src:
            src = src.get("src")  # 查找标签中引号内容属性的值
            src = src.replace("300x168","1920x1080")
            # print(src)
            src_list.append(src)  # 将找出来的图片地址添加至开始创建的表中
    # print(src_list)
count = 0
for src in src_list:
    count = count+1
    response = requests.get(src,headers=headers)
    date = response.content
    downlaod ="D:/下载/动漫壁纸/"+time.strftime("%Y_%m_%d_%H_%M_%S")+str(count)+".png"
    print('成功下载第{}张图片'.format(count))
    with open(downlaod,"wb") as f: # 通过wb的方法将找到的内容写进文件夹里
        f.write(date)