# 爬取豆瓣读书
## 一、第一个爬虫collect20books.py
### 作用
	收集豆瓣图书python分类下前20本书，并将内容输入到文本中，格式如下图
![](http://p09g2sw3y.bkt.clouddn.com/python_spider_1_0.png)
### 目标
	① 简单运用beautifulsoup，抓取网页内容
	② 简单巩固文件操作
### 步骤
	① 打开将要抓取的网页，进入调试模式
![](http://p09g2sw3y.bkt.clouddn.com/spider_1_1.jpg)
	② 分析所需内容并创建图书类，我们需要标题、基础信息、打分、打分人数以及图书图片
	```
	class bookItem:
	    def __init__(self,title,base_info,star,star_amount,img):
	        self.title=title.strip()
	        self.base_info = base_info.strip()
	        self.star = star.strip()
	        self.star_amount = star_amount.strip()
	        self.img = img.strip()
	```
	同时我们可以在类中加上将对象转成字符的方法。
	```
	def itemString(self):
        result = "-------------------------------------------------------\n"
        result += self.title+"\n"
        result += self.base_info+"\n"
        result += self.star+"\n"
        result += self.star_amount+"\n"
        return result
	```
	③ 接下来添加文本输入文件的方法
	```
	def writeToFile(save_path,filename,content):
	    if not os.path.exists(save_path):
	        os.makedirs(save_path)
	    path = save_path+"/"+filename
	    with open(path,"a+") as fp:
	        fp.write(content)
	```
	④ 最后就是使用beautifulsoup解析网页了，这里可以参考[beautifulsoup中文网](https://www.crummy.com/software/BeautifulSoup/bs4/doc/index.zh.html)，因为是现学现用，有些抓取方法可能用的不够优雅，o(*￣︶￣*)o
我们通过分析页面元素可以看到所有的图书信息都是在<li class="subject-item">节点中，可以使用soup.find_all('li', "subject-item")获取所有图书节点，然后针对单个图书节点进一步分析，以标题为例，其所在节点为 <div class="info"> → <h2> → <a>, 我们就可以这样获取标题：item.find('div',"info").h2.a.get("title")。
	单个图书的所有数据都获取完毕后，我们可以调用bookItem的构造方法创建对象，然后调用对象的itemString()获取需要录入到txt文件中的字符串信息，最终调用writeToFile方法就大功告成啦。
