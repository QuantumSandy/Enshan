import requests, re, json, time, os, sys
sys.path.append('.')
requests.packages.urllib3.disable_warnings()
try:
    from pusher import pusher
except:
    pass
from lxml import etree

cookies = os.environ.get("cookie_enshan")

def run(cookie):
    msg = []

    # 签到
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36",
        'Connection': 'keep-alive',
        'Host': 'www.right.com.cn',
        'Upgrade-Insecure-Requests': '1',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate, br',
        "Cookie": cookie,
    }
    response = requests.get(
        url="https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1",
        headers=headers,
        verify=False,
    )
    try:
        coin = re.findall("恩山币: </em>(.*?)&nbsp;", response.text)[0]
        point = re.findall("<em>积分: </em>(.*?)<span", response.text)[0]
        msg = [
            {
                "name": "恩山币",
                "value": coin,
            },
            {
                "name": "积分",
                "value": point,
            },
        ]
    except Exception as e:
        msg = [
            {
                "name": "签到失败",
                "value": str(e),
            }
        ]
    return str(msg)

def main(*arg):
    msg = ""
    if "\\n" in cookies:
        clist = cookies.split("\\n")
    else:
        clist = cookies.split("\n")
    i = 0
    while i < len(clist):
        msg += f"第 {i+1} 个账号开始执行任务\n"
        msg += run(clist[i])
        i += 1
    print(msg[:-1])
    return msg[:-1]


if __name__ == "__main__":
    if cookies:
        print("----------恩山论坛开始尝试签到----------")
        main()
        print("----------恩山论坛签到执行完毕----------")
