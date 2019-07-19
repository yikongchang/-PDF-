import requests
import json                              # 类似BeautifulSoup,加载js的
import time
import logging
import pdfkit                             # url转pdf,不能直接跑，要配置wkhtmltox windows包

url = 'https://mp.weixin.qq.com/mp/profile_ext'      # 手机进入公众号历史消息复制的链接
logging.captureWarnings(True)
headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'Accept-Language: zh-CN,en-US;q=0.9',
        'User-Agent': 'User-Agent: Mozilla/5.0 (Linux; Android 9; LLD-AL00 Build/HONORLLD-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/880 MMWEBSDK/190102 Mobile Safari/537.36 MMWEBID/6775 MicroMessenger/7.0.3.1400(0x2700033C) Process/toolsmp NetType/4G Language/zh_CN',
        'X-Requested-With': 'XMLHttpRequest'
}

cookies = {
    'devicetype': 'android-28',
    'lang':'zh_CN',
    'pass_ticket': 'rmiwGYhz6h2OtRZeeEsl675W1Gtt4pn21m4TU5Lq+celnObNLbOyxna6UdHLOvan',
    'version':'2700033c',
    'wap_sid2': 'CO+a8aAEElxldEt6MTRiWjVPWWowRWgzRV9EeHFSeGJqVXlYcThzUHdqb3RvY1AwdFk2NklaQ29udVpQX0QzLTZLNlFJdXVxWklYMU9Qd09CaHRUdE1pMFVrNTN2dm9EQUFBfjCoysXpBTgNQJVO',
    'wxuin': '1142705519',
    'wxtokenkey':'777',
    'sd_userid':'18411554876722376',
    'sd_cookie_crttime': '1554876722376'

}

def control_offset(offset):

    params = {
        'action': 'getmsg',
        '__biz': 'MzU1NTUwMjY3Mg==',
        'f': 'json',
        'offset': '{}'.format(offset),              #控制每次加载的数量
        'count':'10',
        'is_ok': '1',
        'scene': '126',
        'uin': '777',
        'key': '777',
        'pass_ticket': 'rmiwGYhz6h2OtRZeeEsl675W1Gtt4pn21m4TU5Lq+celnObNLbOyxna6UdHLOvan',
        'wxtoken': '',
        'appmsg_token': '1018_0SVv2SIUtk9El9dQRrS2cTrHNDw4-AIhd64BSQ~~',
        'x5': '0',
        'f': 'json'
    }

    return params

def get_data(offset):
    res = requests.get(url,headers = headers,cookies = cookies,params= control_offset(offset),verify = False)
    # verify就是关闭网页证书验证的
    data = json.loads(res.text)                #读取js
    can_msg_continue = data['can_msg_continue']   # js里面的一些参数  类似标签
    next_offset = data['next_offset']
    general_msg_list = data['general_msg_list']
    list_data = json.loads(general_msg_list)['list']

    for data in list_data:
        try:
            if data['app_msg_ext_info']['copyright_stat'] ==11:
                msg_info = data['app_msg_ext_info']
                title = msg_info['title']
                content_url = msg_info['content_url']
                print("获取原创文章：%s :%s"%(title,content_url))
                pdfkit.from_url(content_url,'D:/spider/'+title+'.pdf')     #转pdf

        except:
            print("非原创文章不爬取")
    if can_msg_continue == 1:          # 控制递归
        time.sleep(2)
        get_data(next_offset)

get_data(1)
