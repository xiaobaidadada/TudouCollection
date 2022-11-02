
import time
import json

import requests
import random

#
hour=0 #打卡的小时设置 0-23
min=24 #打卡时间的分钟设置
# #这样就是 7点10分了

username='' #账号
password='' #密码
lat=100.99
lng=200.7  #经纬度
dizhi='' #全地址名
dizhi_center=''
recommend=''
district_code=''
district_name=''
town_code=''
town_name=''


class daka_wy():
    def __init__(self,username,password,lat,lng,dizhi,dizhi_center,recommend,district_code,district_name,town_code,town_name):
        self.username=username
        self.password=password
        self.lat=lat
        self.lng=lng
        self.dizhi=dizhi
        self.dizhi_center=dizhi_center
        self.recommend=recommend
        self.district_code=district_code
        self.district_name=district_name
        self.town_code=town_code
        self.town_name=town_name
        self.url = "https://apii.lynu.edu.cn/v1/temperatures/"#把tempratures换成noons是打中午的卡
        self.headers = {
            "Host": "apii.lynu.edu.cn",
            "Connection": "keep-alive",
            "Content-Length": "521",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "content-type": "application/json; charset=utf-8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept": "application/json"
        }

    def run(self):
        data = {"username": self.username, "password": self.password, "type": "account"}
        url = "https://smart.lynu.edu.cn/api/accounts/login/"
        token = " "
        null = 'null'  # 防止字符串内的null不被解析，eval不能解析
        true = 'true'
        false = 'false'
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.54 Safari/537.36",
            "Content-Length": "63",
            "Content-Type": "application/json; charset=utf-8",
            "Referer": "https://smart.lynu.edu.cn/exams/exams",
            "Connection": "keep-alive",
            "Host": "smart.lynu.edu.cn",

        }
        response = requests.post(url, data=json.dumps(data), headers=headers)
        if response.status_code == 200 or response.status_code == 201:
            print("获取token成功")

            token = 'JWT ' + eval(response.content)['token']
            self.headers["Authorization"] = token
        else:
            print(response.status_code)
        # 前面是获取token，登陆


        #下面是打卡

        self.data = {"code_color": "A", "condition": "A", "home_condition": "A", "high_risk_status": "A",
                     "vaccine_status": "A", "value": "36.2",
                     "location": {"status": 0, "lat":self.lat , "lng": self.lng, "nation": "中国",
                                  "nation_code": "156", "address": self.dizhi, "famous": self.dizhi_center,
                                  "recommend": self.recommend, "district_code": self.district_code, "district_name": self.district_name,
                                  "district_lat": self.lat, "district_lng": self.lng, "town_code": self.town_code,
                                  "town_name": self.town_name, "town_lat": self.lat, "town_lng": self.lng}}


        response = requests.post(
            self.url, data=json.dumps(self.data), headers=self.headers)
        if response.status_code == 200 or response.status_code == 201:
            print("成功")
        else:
            print("打卡失败")


def get_next_like_inter_time_hour(hour):

    localtime = time.localtime(time.time())
    now_time_hour = localtime.tm_hour
    if now_time_hour <=hour:
        return (hour-now_time_hour)*60*60
    else:
        return (24-now_time_hour+hour)*60*60

def get_next_like_inter_time_min(min):

    localtime = time.localtime(time.time())
    now_time_min = localtime.tm_min
    if now_time_min <=min:
        return (min-now_time_min)*60
    else:
        return (60-now_time_min+min)*60
def daka ():
    dk = daka_wy(username=username_wy, password=password_wy, lat=lat_wy, lng=lng_wy,
              dizhi=dizhi_wy
              , dizhi_center=dizhi_center_wy,
              recommend=recommend_wy  # 最好县政府
              , district_code=district_code_wy  # 省市县区号六位数
              , district_name=district_name_wy  # 县区名字
              , town_code=town_code_wy  # 省市县加上三位 镇/区 号
              , town_name=town_name_wy  # 镇区的名字
              )

    dk.run()


def main(f,set_time_hour,min):
    set_time_min=min
    while True:
        try:
            localtime = time.localtime(time.time())
            if localtime.tm_hour == set_time_hour:
                print("到达小时："+str(localtime.tm_hour))
                if (localtime.tm_min-set_time_min <= 5 and localtime.tm_min-set_time_min >= 0) or (localtime.tm_min-set_time_min >= -5 and localtime.tm_min-set_time_min <=0 ) :

                    print("到达指定分钟："+str(localtime.tm_min))
                    f()
                    print("函数执行成功，该小时内不再执行")
                    time.sleep(60*60)
                    print("从该时刻延迟 " + str((get_next_like_inter_time_hour(set_time_hour) - 60 * 60 + (
                                60 - localtime.tm_min) * 60) / 60 / 60) + " 小时后执行")
                    time.sleep(get_next_like_inter_time_hour(set_time_hour) - 60 * 60 + (60 - localtime.tm_min) * 60)
                else:
                    print("目前的分钟为 "+str(localtime.tm_min))
                    print("延迟 "+str(get_next_like_inter_time_min(set_time_min)/60)+" 分钟")
                    print(('本次系统延迟，今天打卡失败，明天打卡'))
                    time.sleep(get_next_like_inter_time_min(set_time_min))
            else:

                print("从该时刻延迟 "+str((get_next_like_inter_time_hour(set_time_hour)-60*60+ (60-localtime.tm_min)*60)/60/60)+" 小时后执行")
                time.sleep(get_next_like_inter_time_hour(set_time_hour)-60*60+ (60-localtime.tm_min)*60 )
        except Exception:
            time.sleep(60 * 30)





#执行
main(daka,hour,min)