
import time
import json

import requests
import random

#
hour=7 #打卡的小时设置 0-23
min=10 #打卡时间的分钟设置
#这样就是 7点10分了
token='_session=dsdsdsdsdsdsdsds'
#设置token
location="皇家洛阳师范图书馆"
#设置打卡位置，要和公众号的一样，直接复制过来







#此文件是每天控制的主函数
def get_next_like_inter_time_hour(hour):
    #24小时格式
    #返回与下一个相同小时的小时间隔，返回的是秒数
    localtime = time.localtime(time.time())
    now_time_hour = localtime.tm_hour
    if now_time_hour <=hour:
        return (hour-now_time_hour)*60*60
    else:
        return (24-now_time_hour+hour)*60*60

def get_next_like_inter_time_min(min):
    #60分钟
    #返回与下一个相同分钟的分钟间隔，返回的是秒数
    localtime = time.localtime(time.time())
    now_time_min = localtime.tm_min
    if now_time_min <=min:
        return (min-now_time_min)*60
    else:
        return (60-now_time_min+min)*60

def main(f,set_time_hour,min):
    set_time_min=min
    while True:
        try:
            localtime = time.localtime(time.time())
            if localtime.tm_hour == set_time_hour:#达到设定的时小时了
                print("到达小时："+str(localtime.tm_hour))
                if (localtime.tm_min-set_time_min <= 5 and localtime.tm_min-set_time_min >= 0) or (localtime.tm_min-set_time_min >= -5 and localtime.tm_min-set_time_min <=0 ) :#达到设定的分钟间隔了

                    print("到达指定分钟："+str(localtime.tm_min))
                    f()
                    print("函数执行成功，该小时内不再执行")
                    time.sleep(60*60) #延迟执行一小时防止在该一小时内一直执行
                    print("从该时刻延迟 " + str((get_next_like_inter_time_hour(set_time_hour) - 60 * 60 + (
                                60 - localtime.tm_min) * 60) / 60 / 60) + " 小时后执行")
                    time.sleep(get_next_like_inter_time_hour(set_time_hour) - 60 * 60 + (60 - localtime.tm_min) * 60)
                else:
                    print("目前的分钟为 "+str(localtime.tm_min))
                    print("延迟 "+str(get_next_like_inter_time_min(set_time_min)/60)+" 分钟")
                    print(('本次系统延迟，今天打卡失败，明天打卡'))
                    time.sleep(get_next_like_inter_time_min(set_time_min))#每一个小时开始的时候肯定会执行，这里已经不会执行了，前面的函数会精确到分，这里已经没用了，除非系统卡了，程序延迟过了指定时间，转移到下一个小时运行，但是下一个小时又错过了小时时间，会重新排到第二天继续执行
            else:

                print("从该时刻延迟 "+str((get_next_like_inter_time_hour(set_time_hour)-60*60+ (60-localtime.tm_min)*60)/60/60)+" 小时后执行")
                time.sleep(get_next_like_inter_time_hour(set_time_hour)-60*60+ (60-localtime.tm_min)*60 ) #本小时内是不可能执行到这里的（排除0小时减一个小时的意外），不是本小时内的该小时到下一个小时应该减去一个小时的时间，计算该小时到这一个小时最后一刻结束的时间，再加上剩余的小时时间，这样就可以从某时刻到达某个小时开始的时候
        except Exception:
            time.sleep(60 * 30)  # 出现异常延迟半个小时再试一次


def daka ():
    headers = {
        'Host': 'shixi.gmedu.cc',
        'Content-Length': '106',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 11; Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/86.0.4240.99 XWEB/4309 MMWEBSDK/20220303 Mobile Safari/537.36 MMWEBID/3674 MicroMessenger/8.0.21.2120(0x280015F0) Process/toolsmp WeChat/arm64 Weixin NetType/4G Language/zh_CN ABI/arm64'
        ,
        'Cookie': token
        ,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json;charset=UTF-8'
    }
    url_location_qqmap = "https://apis.map.qq.com/ws/place/v1/suggestion/"
    headers_location = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36",
        "Referer": "https://lbs.qq.com/tool/getpoint/getpoint.html"
    }
    param = {
        "keyword": location,
        "region": "",

    }
    response = requests.get(url_location_qqmap, params=param, headers=headers_location)
    if response.status_code==200:
        print('获取地址成功')
    lat = json.loads(response.text)['data'][0]['location']['lat']
    lng = json.loads(response.text)['data'][0]['location']['lng']
    p = {"plan_id": 95,
         "photo": "",
         "longitude": lng,
         "latitude": lat,
         "signForMember": 'true'
         }
    response = requests.request("POST", 'http://shixi.gmedu.cc/wx/student/sign', headers=headers, data=json.dumps(p))
    #
    print(response.content.decode())


#执行
main(daka,hour,min)