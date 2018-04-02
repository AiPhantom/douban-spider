import expanddouban
from bs4 import BeautifulSoup
import csv


# 任务1:获取每个地区、每个类型页面的URL

# 经分析，tags后的参数顺序与搜索结果无关
base_url='https://movie.douban.com/tag/#/?sort=S&range=0,10&tags={}'

def getMovieUrl(category, location,base_url=base_url):
    query_string = category+',' if len(category)>0 else ''
    query_string += location if len(location)>0 else ''
    url = base_url.format(query_string)
    return url



# 任务2: 获取电影页面 HTML

# html = expanddouban.getHtml(url)

# print(html)

# 任务3: 定义电影类

class Movie:
    def __init__(self, name, rate, location, category, info_link, cover_link):
        self.name = name
        self.rate = rate
        self.location = location
        self.category = category
        self.info_link = info_link
        self.cover_link = cover_link


# 任务4: 获得豆瓣电影的信息

def getMovies(category, location):
    movie_array=[]
    url = getMovieUrl(category,location)
    html = expanddouban.getHtml(url)
    soup = BeautifulSoup(html, 'html.parser')
    content_div=soup.find(class_="list-wp")
    for element in content_div.find_all("a", recursive=False):
    	info_link=element.get('href')
    	cover_link=element.find("img").get('src')
    	name=element.find(class_="title").string
    	rate=element.find(class_="rate").string
    	print(element.find(class_="title").string)
    	m = Movie(name, rate, location, category, info_link, cover_link)
    	movie_array.append(m);
    return movie_array


# 任务5: 构造电影信息数据表

with open("test.csv","w") as csvfile: 
    writer = csv.writer(csvfile)
    result = getMovies('动作','美国')
    #写入多行用writerows
    rows=[]
    for item in result:
    	rows.append([item.name,item.rate,item.location,item.category,item.info_link,item.cover_link])
    print(result)
    writer.writerows(rows)







