import requests
from lxml import etree
import re


def weather():
    cd_url = "http://www.weather.com.cn/weather/101270101.shtml#search"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }
    response = requests.get(url=cd_url,headers=header)
    response.encoding = "utf-8"  # 解决返回乱码
    weather_page = response.text
    tree = etree.HTML(weather_page)
    dweather = tree.xpath("//div[@id='7d']/ul/li")
    # 定位到近七天天气所在的标签
    # print(dweather)
    conte = 1
    for li in dweather:
        day = li.xpath("./h1/text()")  # 日期
        # print(day)
        day = str(day).replace("['","")
        day =day.replace("']","")
        # print(one_day)
        weaherinfo = li.xpath("./p/@title")  # 天气状况
        weaherinfo = str(weaherinfo).replace("['", "")
        weaherinfo = weaherinfo.replace("']", "")
        # print(weaherinfo)
        max_temperature = li.xpath("./p[2]/span/text()")  # 最高温度
        max_temperature = str(max_temperature).replace("['", "")
        max_temperature = max_temperature.replace("']", "")
        # print(max_temperature)
        min_temperature = li.xpath("./p[2]/i/text()")  # 最低温度
        min_temperature = str(min_temperature).replace("['", "")
        min_temperature = min_temperature.replace("']", "")
        # print(min_temperature)
        print("第{}天天气详情：".format(conte))
        print("日期：{}".format(day))
        print("天气状况：{}".format(weaherinfo))
        print("最高温度：{}".format(max_temperature))
        print("最低温度：{}\n" .format(min_temperature))
        conte = conte+1


if __name__ == '__main__':
    weather()