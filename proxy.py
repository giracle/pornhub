#!-*- coding=utf-8 -*-
# __author__ = giracle
# __version__ = 1.0
# __time__ = 2019/8/29
# 
"""
TODO:获取国外代理
可用的国外代理：http代理  http://www.66daili.cn/showProxySingle/3159/
"""
import requests
from lxml import etree
import re
import threading
ip_ports = []
def gethtml(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "Referer": "http://www.66daili.cn/showProxySingle/3159/",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Connection": "keep-alive"

    }
    response = requests.get(url=url,headers=headers)
    response.encoding='utf-8'
    with open(r'C:\Users\Administrator\Desktop\forigenIP.html','w')as fw:
        fw.write(response.text)
    print(response.text)
    return response.text
lock = threading.Lock()
def verfyIP(i):
    url = "http://www.whatismyip.com.tw"
    # url = "https://www.google.com.hk"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}
    
    proxies = {"http":"http://{}".format(ip_ports[i])}
    # proxies = {"http":"http://60.13.42.74:9999","http":"http://59.172.27.6:38380","https":"https://59.172.27.6:38380","https":"https://60.13.42.74:9999"}
    try:
        response = requests.get(url=url,headers=headers,proxies=proxies,timeout=10)
        print(response.status_code)
        lock.acquire() #获得锁
        if response.status_code == 200:
            print("{}可用".format(ip_ports[i]))
            with open(r"C:\Users\Administrator\Desktop\usefullIP.txt",'a')as fw:
                fw.write("{}\n".format(ip_ports[i]))
        # else:
        #     print("{}不可用".format(ip_ports[i]))
        #     ip_ports.remove(ip_ports[i])
        lock.release() # 释放锁
    except Exception as e:
        lock.acquire()
        print("{}不可用".format(ip_ports[i]))
        # ip_ports.remove(ip_ports[i])
        print("网络请求失败:{}".format(e))
        lock.release()
    
def parseHtml(response):
    # html = etree.HTML(web_data)
    # ips = html.xpath('//th/text()')
    # ports = html.xpath('//td/text()')
    web_data = response
    ips = re.findall(r"<th>(\d+.\d+.\d+.\d+)</th>",web_data)
    ports = re.findall(r"<td>(\d+)</td>",web_data)
    verfyTime = re.findall(r"<td>(\d+年\d+月\d+日.*?验证)</td>",web_data)
    print(ips)
    print(ports)
    print(verfyTime)
    for i in zip(ips,ports,verfyTime):
        print(i)
        ip_ports.append("{}:{}".format(i[0],i[1]))
        with open(r"C:\Users\Administrator\Desktop\forigenIP.txt",'a')as fw:
            fw.write("{}:{}\t{}\n".format(i[0],i[1],str(i[2])))
    print(ip_ports)
    threads = []
    for k in range(len(ips)):
        thread = threading.Thread(target=verfyIP,args=[k])
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
if __name__ == "__main__":
    url = r"http://www.66daili.cn/showProxySingle/3159"
    response = gethtml(url)
    parseHtml(response)