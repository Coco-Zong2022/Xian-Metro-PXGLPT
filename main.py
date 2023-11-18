# -*- coding: utf-8 -*-
import json
import requests
from Server import server


class PracticePaper:
    def __init__(self, username1, password1, name1):
        self.username = username1
        self.password = password1
        self.name = name1
        self.token = None
        self.log = []
        self.base_url = 'https://pxmb.xa-metro.com:1038/training_system'

    def login(self):
        url = f'{self.base_url}/sys/mLogin'
        data = {
            "username": self.username,
            "password": self.password
        }
        headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2006J10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
            'Connection': 'Keep-Alive',
            'Charset': 'UTF-8',
            'Accept-Encoding': 'gzip',
            'X-Access-Token': 'null',
            'Content-Type': 'application/json',
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            self.token = result['result']['token']
            self.log.append(f'用户 {self.name} 登陆成功')
        except requests.exceptions.RequestException as e:
            self.log.append(f'用户 {self.name} 登陆失败  {str(e)}')

    def add_major(self):
        url = f'{self.base_url}/practice/selfPracticePaper/addMajor'
        data = {
            "id": 1478181052575940610  # 每日一题ID
        }
        headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2006J10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
            'Connection': 'Keep-Alive',
            'Charset': 'UTF-8',
            'Accept-Encoding': 'gzip',
            'X-Access-Token': self.token,
            'Content-Type': 'application/json',
            'Host': 'pxmb.xa-metro.com:1038',
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            query_id = result['result']
            self.log.append(f'用户 {self.name} 添加试卷')
            self.log.append(f'用户 {self.name} 试卷ID: {query_id}')
            return query_id
        except requests.exceptions.RequestException as e:
            self.log.append(f'用户 {self.name} 添加试卷失败  {str(e)}')

    def get_test_paper(self, query_id):
        url = f'{self.base_url}/practice/selfPracticePaper/queryById'
        params = {
            "id": query_id
        }
        headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2006J10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
            'Connection': 'Keep-Alive',
            'Charset': 'UTF-8',
            'Accept-Encoding': 'gzip',
            'X-Access-Token': self.token,
            'Content-Type': 'application/json',
            'Host': 'pxmb.xa-metro.com:1038',
        }
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            result = response.json()
            questions = json.loads(result['result']['questions'])
            self.log.append(f'用户 {self.name} 的试卷获取成功')
            return questions
        except requests.exceptions.RequestException as e:
            self.log.append(f'用户 {self.name} 的试卷获取失败  {str(e)}')

    def submit_test_paper(self, query_id, questions):
        url = f'{self.base_url}/practice/selfPracticePaper/submit'
        data = {
            "id": query_id,
            "questionJsonBOList": questions
        }
        headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2006J10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
            'Connection': 'Keep-Alive',
            'Charset': 'UTF-8',
            'Accept-Encoding': 'gzip',
            'X-Access-Token': self.token,
            'Content-Type': 'application/json',
            'Host': 'pxmb.xa-metro.com:1038',
        }
        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            message = result['message']
            total_point = result['result']['totalPoint']
            self.log.append(f'用户 {self.name} 提交试卷成功')
            self.log.append(f'用户 {self.name} Message: {message} 总分:{total_point}')
        except requests.exceptions.RequestException as e:
            self.log.append(f'用户 {self.name} 提交试卷失败  {str(e)}')

    def logout(self):
        url = f'{self.base_url}/sys/getAppId'
        headers = {
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 11; M2006J10C Build/RP1A.200720.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.131 Mobile Safari/537.36',
            'Connection': 'Keep-Alive',
            'Charset': 'UTF-8',
            'Accept-Encoding': 'gzip',
            'X-Access-Token': self.token,
            'Content-Type': 'application/json',
            'Host': 'pxmb.xa-metro.com:1038',
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self.log.append(f'用户 {self.name} 退出成功')
        except requests.exceptions.RequestException as e:
            self.log.append(f'用户 {self.name} 退出失败  {str(e)}')

    def run(self):
        self.log.append(f'用户 {self.name} 开始每日一题')
        self.login()
        query_id = self.add_major()
        questions = self.get_test_paper(query_id)
        if questions:
            for item in questions:
                answer = item['rightAnswer']
                item['choose'] = [answer]
                item['mark'] = False
        self.submit_test_paper(query_id, questions)
        self.logout()
        self.log.append(f'用户 {self.name} 结束每日一题\n')

    def get_log(self):
        return self.log


if __name__ == '__main__':
    with open('config.json', encoding='utf-8') as f:
        users = json.load(f)
    for user in users:
        username = user['username']
        password = user['password']
        name = user['name']
        sckey = user['sckey']
        paper = PracticePaper(username, password, name)
        paper.run()
        # 为每个用户推送 Server酱
        log_everyone = '\n'.join(paper.get_log())
        server(name, sckey, '每日一题', log_everyone)

