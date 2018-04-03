import expanddouban
from bs4 import BeautifulSoup
import csv
import requests

# 抓取所有地区电影，不能获取电影对应的地区，故采用循环地区方式拉取数据
category_list=['剧情','爱情','喜剧','科幻','动作','悬疑','犯罪','恐怖','青春','励志','战争','文艺','黑色幽默','传记','情色','暴力','音乐','家庭']
location_list=['大陆','美国','香港','台湾','日本','韩国','英国','法国','德国','意大利','西班牙','印度','泰国','俄罗斯','伊朗','加拿大','澳大利亚','爱尔兰','瑞典','巴西','丹麦']
# 任务1:获取每个地区、每个类型页面的URL

# 经分析，tags后的参数顺序与搜索结果无关
base_url='https://movie.douban.com/tag/#/?sort=S&range=0,10&tags=电影,{}'

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

def getMovies(category='', location=''):
    movie_array=[]
    url = getMovieUrl(category,location)
    html = expanddouban.getHtml(url)
    soup = BeautifulSoup(html, 'html.parser')
    content_div=soup.find(class_="list-wp")
    try:  
        for element in content_div.find_all("a", recursive=False):
            info_link=element.get('href')
            cover_link=element.find("img").get('src')
            name=element.find(class_="title").string
            rate=element.find(class_="rate").string
            m = Movie(name, rate, location, category, info_link, cover_link)
            movie_array.append(m);
    except Exception as err:  
        print(err)
    
    return movie_array


# 任务5: 构造电影信息数据表
my_favorite=['动作','爱情','喜剧']
# 抓取所有的电影种类



# for element in content_div.find_all("span"):
#     print(element.find("span").string)

# with open("movies.csv","w") as csvfile: 
#     writer = csv.writer(csvfile)
#     result=[]
#     for location in location_list:
#         for favorite in my_favorite:
#             result.extend(getMovies(favorite,location))
#     #写入多行用writerows
#     rows=[]
#     for item in result:
#     	rows.append([item.name,item.rate,item.location,item.category,item.info_link,item.cover_link])
#     print(result)
#     writer.writerows(rows)


# 任务6: 统计电影数据


all_list=[]
obj_list={}

with open("movies.csv","r") as f: 
    f_csv = csv.reader(f)
    all_list= [(row[2],row[3]) for row in f_csv]
    for item in all_list:
        if item[1] in obj_list:
            if item[0] in obj_list[item[1]]:
                obj_list[item[1]][item[0]]+=1
            else:
                obj_list[item[1]][item[0]]=1
        else:
            obj_list[item[1]]={item[0]:1}



def objectSort(obj_list):
    f = open("./output.txt", 'w+')
    for favorite in my_favorite:
        obj=obj_list[favorite]
        all_number= sum([obj[key] for key in obj.keys()])
        obj_tuples= [(key,obj[key]) for key in obj.keys()]
        sorted_tuples= sorted(obj_tuples, key=lambda obj: obj[1],reverse=True)[:3]
        index=1
        for item in sorted_tuples:
            print('{}类：{}. {}:{:.2%}'.format(favorite,index,item[0],item[1]/all_number), file=f)
            index+=1
 
    
objectSort(obj_list)

        







