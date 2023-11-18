import requests


def server(name, sckey, title, content):
    url = f'https://sctapi.ftqq.com/{sckey}.send'
    data = {
        'title': title,
        'desp': f"```\n{content}"
    }
    res = requests.post(url, data=data)
    if res.status_code == 200:
        print(name + 'Server酱推送成功')
    else:
        print(name + 'Server酱推送失败')
