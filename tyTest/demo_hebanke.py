#-*- coding: UTF-8 -*-
import requests

password=0
while True:
    url = "http://www.heibanke.com/lesson/crawler_ex01/"
    params = {'username':'heibanke','password': str(password)}
    r = requests.post(url,data=params)

    if r.text.find(u"错误") > 0:#判断某次输入是否正确
        password=password+1
    else:
        print password #最后打印出password为6，居然输入06,006，0006都是对的
        break