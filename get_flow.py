import requests
import json
'''
需要在53行
get_flow("邮箱","密码")
处将邮箱和密码替换为自己的账号信息
'''


def login(email, passwd):
    login_url = "https://j02.space/signin"
    headers = {

    }
    data = {"email": email, "passwd": passwd}
    try:
        login = requests.post(login_url, headers=headers, data=data, timeout=5)
        cookies = login.cookies
        return cookies
    except Exception as err:
        print("***********************")
        print("获取cookie失败！")
        print("***********************")


def get_flow(email, passwd):
    sign_in = "https://j02.space/user/checkin"
    headers = {
        "User-Agent": "Mozilla / 5.0(Windows NT 6.1;Win64;x64;rv: 94.0) Gecko / 20100101"
    }
    cookie = login(email, passwd)
    try:
        flow = requests.post(sign_in, headers=headers, cookies=cookie)
        all_msg = json.loads(flow.text)
        status = flow.status_code
        if status == 200 and all_msg["ret"] == 1:
            print("***********************")
            print("签到成功！")
            print(all_msg["msg"])
            print(f"账户剩余流量:{all_msg['traffic']}")
            print("***********************")
        else:
            print("***********************")
            print(all_msg["msg"])
            print("***********************")
    except Exception as err:
        print("***********************")
        print("连接服务器失败!")
        print("***********************")


if __name__ == '__main__':
    get_flow("xxxxx", "xxxxxx")