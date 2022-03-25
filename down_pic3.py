import requests
from lxml import etree
import time


def dowm_img():
    urls = []
    for url in range(1,20):
        src = "https://wallhaven.cc/search?q=id%3A1&sorting=random&ref=fp&seed=PCSguD&page={}".format(url)
        urls.append(src)
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36",
    }
    img_src_list = []
    for url in urls:
        response = requests.get(url=url,headers=header)
        response.encoding = "utf-8"  # 解决返回乱码
        weather_page = response.text
        tree = etree.HTML(weather_page)  # 实例化返回数据为一个对象
        for li in range(1,25):
            img_src = tree.xpath('//*[@id="thumbs"]/section[1]/ul/li[{}]/figure/a/@href'.format(li))
            # print(img_src)
            image_src = "".join(img_src)
            # print(image_src)
            img_src_list.append(image_src)
            # break

    imag_src_list = []
    for image_src_list in img_src_list:
        response = requests.get(url=image_src_list, headers=header)
        response.encoding = "utf-8"  # 解决返回乱码
        weather_page = response.text
        img_tree = etree.HTML(weather_page)  # 实例化返回数据为一个对象
        image = img_tree.xpath('//*[@id="wallpaper"]/@src')
        # print(image)
        image_url = "".join(image)
        imag_src_list.append(image_url)

    conte = 0
    # print(imag_src_list)
    try:
        for img_url in imag_src_list:
            # print(type(img_url))
            if img_url != '':
                conte = conte + 1
                responses = requests.get(url=img_url, headers=header)
                date = responses.content
                filename = "D:/下载/壁纸/" + time.strftime("%Y_%m_%d_%H_") + str(conte) + ".png"
                with open(filename, "wb") as f:
                    f.write(date)
                    print("成功下载第{}张图片~~".format(conte))
            else:
                pass
    except:
        pass


if __name__ == '__main__':
    dowm_img()