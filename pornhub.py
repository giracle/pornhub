#! -*- coding=utf-8 -*-
"""
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9
Cache-Control: max-age=0
Connection: keep-alive
Cookie: ## "更换成自己登录账号的cookie"
DNT: 1
Host: cn.pornhub.com
Referer: https://cn.pornhub.com/view_video.php?viewkey=ph5d1f0622872de
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36

"""
import re
import time
import requests
from bs4 import BeautifulSoup
import os
import json

eachVideoInfoDict = {}
def requestsHtml(url):
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36",
        "Cookie": "ua=666332998c62658cc43216116351bf1f; platform=pc; bs=ggpena7cmn7htgb440yi1v83tfsxv5rv; ss=332300981904640493; _ga=GA1.2.479303012.1566991944; _gid=GA1.2.1198553738.1566991944; lang=cn; RNLBSERVERID=ded6884; ARSC2_3=1567078355; SMPop_0=1566991992295; desired_username=address7%7Caddress%40giracle.cn; il=v14ElojGl1ZFU5Z6CSo2fSzRRQapztVWoJYxyiLcdVYIcxNTY3MDgyMTc5SHVqS2pEQkpiR1E1R3p0QmhXdHJLY0JjVHRVdWdzeVR4RHZDSkk0Rw..; expiredEnterModalShown=1; performance_timing=video; _gat=1",
        "Referer": "https://cn.pornhub.com/view_video.php?viewkey=ph5d1f0622872de"
    }
    try:
        response = requests.get(url=url,headers=headers)
        response.Encoding = 'utf-8'
        # print(response.text)
        # string = response.text
        # with open('result.html','w',encoding='utf-8')as f:
        #     f.write(string)
    except Exception as e:
        print("Requests Error:",e)
    return response

def paraseHtml(response):
    soup = BeautifulSoup(response,'html.parser')
    # print(soup)
    video_list = soup.find_all('a',class_='linkVideoThumb img')
    # print(video_list)
    pattern = re.compile(r'<a class=".*?" data-related-url=".*?" href="(.*?)" title="(.*?)"><img .*?data-mediabook="(.*?)".*?',re.S)
    eachUrl = re.findall(pattern,str(video_list).replace('\n',''))
    # url title mediabook
    # print(eachUrl)
    for i in range(len(eachUrl)):
        videourl = 'https://cn.pornhub.com'+eachUrl[i][0]
        eachVideoInfoDict[videourl] = [eachUrl[i][1],eachUrl[i][2]]

def getDownloadUrl(jsonfile):
    with open(jsonfile,'r')as fr:
        jsonDict = json.load(fr)
    for key in jsonDict:
        print(key)
        try:
            response = requestsHtml(key)
            # print(response)
            soup = BeautifulSoup(response,'html.parser')
            souplist = soup.find_all('a',class_='downloadBtn greyButton')
            print(souplist)
            pattern = re.compile(r'<a class="downloadBtn greyButton" download=".*?" href="(.*?)" rel=.*?</a>',re.S)
            downloadurl = re.findall(pattern,str(souplist))
            print(downloadurl)
            print(len(downloadurl))
            if len(downloadurl) == 0:
                del eachVideoInfoDict[key]
                continue
            else:
                print('存在下载链接，已加入')
                eachVideoInfoDict[key].append(downloadurl[0])
        except Exception as e:
            print('ERROR:',e)
            with open(r'C:\Users\giracle\Desktop\error.txt','a')as fr:
                fr.write("Error:{}\n".format(e))

def downloadVideo():
    jsonfile = r'C:\Users\giracle\Desktop\pornhubWithDownloadUrl.json'
    with open(jsonfile,'r')as fr:
        dict = json.load(fr)
    for key in dict:
        path =r'C:\Users\giracle\Desktop\video'+'\\'+ str(dict[key][0]).strip(r'?')
        if os.path.exists(path):
            pass
        else:
            os.makedirs(path)
        # print(dict[key][1])
        # print(dict[key][2])
        gifurl = dict[key][1]
        downloadurl = dict[key][2]
        try:
            print("正在请求网址")
            # responseGIF = requestsHtml(gifurl)
            # responsevideo = requestsHtml(downloadurl)
            # print(type(responsevideo.content))
            print('正在下载{}'.format(dict[key][0]))
            # with open(r'{}\{}.webm'.format(path,str(dict[key][0])),'ab')as fw1:
            #     fw1.write(responseGIF.content)
            with open(r'{}\{}.txt'.format(path,str(dict[key][0])),'w')as fw2:
                fw2.write(str(dict[key][2]).strip(r'?'))
            # with open(r'{}\{}.mp4'.format(path,str(dict[key][0])),'ab')as fw2:
            #     fw2.write(responsevideo.content)
            print('{}下载完成'.format(dict[key][0]))
        except Exception as e:
            print("下载失败：",e)


if __name__ == "__main__":
    jsonfile = r"C:\Users\giracle\Desktop\pornhub.json"
    for i in range(1,25):
        url = r"https://cn.pornhub.com/video?c=111&page={page}".format(page=i) # https://cn.pornhub.com/video?c=111&page=2     #page =336
        response = requestsHtml(url)
        paraseHtml(response.text)
        print("已经爬取了{}/24页".format(i))
        time.sleep(3)
    with open(r"C:\Users\giracle\Desktop\pornhub.json",'w',encoding='utf-8')as fw:
        fw.write(json.dumps(eachVideoInfoDict))
    getDownloadUrl(jsonfile)
    with open(r'C:\Users\giracle\Desktop\pornhubWithDownloadUrl.json','w',encoding='utf-8')as fw:
        fw.write(json.dumps(eachVideoInfoDict))
    downloadVideo()
        
