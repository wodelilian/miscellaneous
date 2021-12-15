import time
import requests
import json
def sqlmap_check(service,url):
    check_url = {
        'url':url
    }
    datas = json.dumps(check_url)
    headers = {
        'Content-Type': 'application/json'
    }
    # print(headers)
    data = requests.get(service + '/task/new')
    taskid = data.json()
    taskids = taskid['taskid']
    if data.status_code == 200:
        print('creat task success!\ntaskid = ' + taskid['taskid'])
        set_task_url = service + '/option/' + taskids + '/set'
        set_task_data = requests.post(url=set_task_url,data=datas,headers=headers)
        # print(set_task_data.content.decode('utf-8'))
        if 'success' in set_task_data.content.decode('utf-8'):
            check_url = service + '/scan/' + taskids + '/start'
            # print(check_url)
            start_check = requests.post(url=check_url, data=datas, headers=headers)
            # print(start_check)
            if 'success' in start_check.content.decode('utf-8'):
                print('***************SCAN***************')
                print("开始任务：{}  URL：{}".format(taskids,urls))
                while True:
                    scan_url = service + '/scan/' + taskids + '/status'
                    data = requests.get(scan_url)
                    if 'running' in data.content.decode('utf-8'):
                        print('正在检测URL:{}'.format(urls))
                        time.sleep(5)
                        pass
                    else:
                        scan_data = service + '/scan/' + taskids + '/data'
                        # print(scan_data)
                        scan_url_data = requests.get(scan_data)
                        # print(scan_url_data)
                        scan_sesults = scan_url_data.content.decode('utf-8')
                        # print(scan_sesults)
                        head = str('**********{}检测状态**********\n'.format(urls))
                        bottom = str('**********{}检测结束**********\n'.format(urls))
                        content = head + scan_sesults + '\n' + bottom + '\n' + '\n' + '\n'
                        f = open('scan_data.txt','a+')
                        f.write(content)
                        print('URL:{}检测结束'.format(urls))
                        break
            else:
                print('set option fail!')
        else:
            print('creat scan fail！')
    else:
        print('creat task fail!')

if __name__ == '__main__':
    for url in open('url.txt'):
        urls = url.replace('\n', '')
        print(url)
        sqlmap_check('http://127.0.0.1:8775',urls)
