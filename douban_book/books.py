'''
收集豆瓣图书python分类下前20本书

@author: xfx
'''
from bs4 import BeautifulSoup
from urllib import request
import os

def writeToFile(save_path,filename,content):
    '''  
    将文本内容追加到指定目录文件中，若目录或文件不存在则先创建
    :Args:
     - save_path - 文件所在目录
     - filename - 文件名（带后缀）
     - content - 追加的文本内容
    '''
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    path = save_path+"/"+filename
    with open(path,"a+") as fp:
        fp.write(content)

def readSource():
    content = request.urlopen("https://book.douban.com/tag/python?start=0&type=T")
    soup = BeautifulSoup(content)
    items = soup.find_all('li', "subject-item")
    for item in items:
        img = item.find('a').img.get("src")
        infoNode = item.find('div',"info")
        title = infoNode.h2.a.get("title")
        baseinfo = infoNode.find('div',"pub").string
        starinfo = infoNode.find('div',"star").find_all("span")
        star = starinfo[1].string
        amount = starinfo[2].string
        book_item = bookItem(title,baseinfo,star,amount,img)
        writeToFile("D:\\", "豆瓣图书.txt", book_item.itemString())

class bookItem:
    '''
    图书对象
    '''
    def __init__(self,title,base_info,star,star_amount,img):
        self.title=title.strip()
        self.base_info = base_info.strip()
        self.star = star.strip()
        self.star_amount = star_amount.strip()
        self.img = img.strip()

    def itemString(self):
        result = "-------------------------------------------------------\n"
        result += self.title+"\n"
        result += self.base_info+"\n"
        result += self.star+"\n"
        result += self.star_amount+"\n"
        return result

if __name__ == '__main__':
    readSource()
