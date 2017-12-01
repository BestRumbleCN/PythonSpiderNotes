'''
收集豆瓣图书python分类下前20本书

@author: xfx
'''
from bs4 import BeautifulSoup
from urllib import request
import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import sessionmaker
import re

Base = declarative_base()
engine = create_engine('mysql+mysqlconnector://root:mhbnm4RozN@120.25.151.148:3306/spider')
DBSession = sessionmaker(bind=engine)

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
        
def firstMatch(pattern,content):
    pattern = re.compile(pattern,re.S)
    return re.findall(pattern, content)[0]
 
def readSource():
    content = request.urlopen("https://book.douban.com/tag/python?start=420&type=T")
    soup = BeautifulSoup(content)
    items = soup.find_all('li', "subject-item")
    session = DBSession()
    for item in items:
        img = item.find('a').img.get("src")
        infoNode = item.find('div',"info")
        title = infoNode.h2.a.get("title")
        href = infoNode.h2.a.get("href")
        book_id = re.sub("https://book.douban.com/subject/(.*?)/", r'\1', href)
        baseinfo = infoNode.find('div',"pub").string
        starinfo = infoNode.find('div',"star").find_all("span")
        if(len(starinfo) == 1):
            star = "0";
            amount = "0";
        else:
            star = starinfo[1].string
            amount = firstMatch("\\((.*?)人评价\\)",starinfo[2].string)
        book_item = bookItem(title,baseinfo,star,amount,img,book_id)
        #writeToFile("D:\\", "豆瓣图书.txt", book_item.itemString())
        session.add(book_item)
    session.commit()
    session.close()
        

class bookItem(Base):
    '''
    图书对象
    '''
    __tablename__ = 'book_item'
    id = Column(Integer,primary_key=True)
    title = Column(String)
    base_info = Column(String)
    star = Column(Integer)
    star_amount = Column(Integer)
    img = Column(String)
    book_id = Column(String)
    
    def __init__(self,title,base_info,star,star_amount,img,book_id):
        self.title=title.strip()
        self.base_info = base_info.strip()
        self.star = star.strip()
        self.star_amount = star_amount.strip()
        self.img = img.strip()
        self.book_id = book_id

    def itemString(self):
        result = "-------------------------------------------------------\n"
        result += self.title+"\n"
        result += self.base_info+"\n"
        result += self.star+"\n"
        result += self.star_amount+"\n"
        return result

if __name__ == '__main__':
   readSource()
