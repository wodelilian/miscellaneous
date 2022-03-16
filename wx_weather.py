import json
import requests
from lxml import etree
import re


def weather():
    cd_url = "http://www.weather.com.cn/weather/101270101.shtml#search"  # 天气预报网址
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36"
    }
    response = requests.get(url=cd_url,headers=header)
    response.encoding = "utf-8"  # 解决返回乱码
    weather_page = response.text
    tree = etree.HTML(weather_page)
    dweather = tree.xpath("//div[@id='7d']/ul/li")
    # 定位到近七天天气所在的标签
    conte = 1
    weather_list = []
    for li in dweather:
        day = li.xpath("./h1/text()")  # 日期
        day = ''.join(day)  # 列表转字符串
        # print(day)
        weaherinfo = li.xpath("./p/@title")  # 天气状况
        weaherinfo = ''.join(weaherinfo)
        # print(weaherinfo)
        max_temperature = li.xpath("./p[2]/span/text()")  # 最高温度
        max_temperature = ''.join(max_temperature)
        # print(max_temperature)
        min_temperature = li.xpath("./p[2]/i/text()")  # 最低温度
        min_temperature = ''.join(min_temperature)
        # print(min_temperature)
        info = "第{}天天气详情：\n日期：{}\n天气状况：{}\n最高温度：{}\n最低温度：{}\n\n".format(conte,day,weaherinfo,max_temperature,min_temperature)
        weather_list.append(info)
        conte = conte+1
    return (weather_list)


def workweixin():
    url = "https://qyapi.weixin.qq.com/cgi-bin/gettoken"
    parms = {
        "corpid":"",  # 企业微信corpid
        "corpsecret":"",  # 应用secret
    }
    response = requests.get(url=url,params=parms)
    access_token = response.json()["access_token"]
    text = weather()
    # print(text)
    wx_text = ''.join(text)
    # print(wx_text)
    data = {
            "touser": "",  # 推送用户
            "msgtype": "text",  # 推送类型
            "agentid": "",  # 应用ID
            "text": {
                "content": wx_text
            },
            "safe": 0
    }
    # print(data)
    try:
        wx_url = "https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token="+access_token
        response = requests.post(url=wx_url,data=json.dumps(data)).text
        # print(response)
        print("*******************************************")
        print("***************天气预报推送成功***************")
        print("*******************************************")
    except:
        print("*******************************************")
        print("***************天气预报推送失败***************")
        print("*******************************************")


if __name__ == '__main__':
    workweixin()