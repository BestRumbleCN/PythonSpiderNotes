'''
Created on 2017年11月30日

@author: fly
'''
from bs4 import BeautifulSoup
from urllib import request
content = request.urlopen("https://book.douban.com/tag/python?start=0&type=T")
soup = BeautifulSoup(content)
#print(soup.head)
items = soup.find_all('li', "subject-item")
for item in items:
    img = item.find('a').img.get("src")
    infoNode = item.find('div',"info")
    title = infoNode.h2.a.get("title")
    baseinfo = infoNode.find('div',"pub").string
    starinfo = infoNode.find('div',"star").find_all("span")
    star = starinfo[1].string
    amount = starinfo[2].string
    print("title:{},image:{},baseInfo:{}".format(title,img,baseinfo))
    print("star:{},amount:{}".format(star,amount))
