import requests, re, json, time, os, sys
sys.path.append('.')
requests.packages.urllib3.disable_warnings()
try:
    from pusher import pusher
except:
    pass
from lxml import etree

cookies = str(os.environ.get("cookie_enshan"))

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.5359.125 Safari/537.36",
    'Connection': 'keep-alive',
    'Host': 'www.right.com.cn',
    'Upgrade-Insecure-Requests': '1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
}

use_proxies = False

def proxies(try_num):
    url = 'https://proxy.scdn.io/api/get_proxy.php'
    params = {
        'protocol': 'https',
        'count': 20
    }
    response = requests.get(url=url, params=params)
    get_proxy = None
    try:
        for index, proxy in enumerate(response.json()["data"]["proxies"]):
            try:
                print(f"正在测试代理{index+1}: {proxy}")
                response = requests.get("https://www.right.com.cn/", proxies={'https': proxy}, headers=headers, timeout=5)
                if response.status_code == 200:
                    get_proxy = proxy
                    break
                else:
                    print(f"错误代码: {response.status_code}")
                    pass
            except Exception as e:
                continue
            time.sleep(1)
        if get_proxy is not None:
            print(f"找到可用代理{proxy}")
            return {'https': get_proxy}
        else:
            if try_num > 0:
                print("无法找到有用的代理，正在重新获取代理")
                return proxies(try_num-1)
            else:
                raise Exception("无法找到有用的代理")
    except Exception as e:
        print(e)
        return None

def run(cookie):
    msg = []

    # 签到
    headers.update({"Cookie": cookie})
    response = requests.get(
        url="https://www.right.com.cn/FORUM/home.php?mod=spacecp&ac=credit&showcredit=1",
        headers=headers,
        verify=False,
        proxies=(proxies(try_num=5) if use_proxies else None)
    )
    if response.status_code == 200:
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
    else:
        msg = [{"Bad request": f"{response.status_code}"}]
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
    print(msg)
    return


if __name__ == "__main__":
    if cookies:
        print("----------恩山论坛开始尝试签到----------")
        main()
        print("----------恩山论坛签到执行完毕----------")
