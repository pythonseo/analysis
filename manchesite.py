import requests
from bs4 import BeautifulSoup
import pymysql
import numpy as np
import matplotlib.pyplot as plt
#定义字体以解决plt图片中文显示乱码问题
plt.rcParams['font.sans-serif'] = ['SimHei'] # 步骤一（替换sans-serif字体）
plt.rcParams['axes.unicode_minus'] = False   # 步骤二（解决坐标轴负数的负号显示问题）
class Manchesite(object):
    #数据库信息
    def __init__(self,ip,user,password,db,char='utf8'):
        self.ip=ip
        self.user=user
        self.password=password
        self.db=db
        self.char=char
        self.sqlcon=pymysql.connect(
            host=self.ip,
            user=self.user,
            password=self.password,
            db=self.db,
            charset=self.char
        )
        print('start')
    def getxml(self,api):
        #获取数据
        response=requests.get(api)
        if str(response.status_code) =='200':
            soup=BeautifulSoup(response.content,'lxml')
            titledegrees=soup.find_all('a')
            durations=soup.select('.duration')
            titlelist=[]
            degreelist=[]
            durationlist=[]
            for title in titledegrees:
                titlecopy=title.get_text().split(' ')
                degree=titlecopy.pop(-1)
                titlelist.append(' '.join(titlecopy))
                degreelist.append(degree)
            print(len(titlelist))
            print(len(degreelist))
            for duration in durations:
                durationlist.append(duration.get_text())
            print(len(durationlist))
            datas=zip(titlelist,degreelist,durationlist)
            for data in datas:
                print(data)
                self.sqlexe(data)
    def sqlexe(self,data):
        cursor=self.sqlcon.cursor()
        #将数据存入mysql
        sql='insert into test0 values ("%s","%s","%s")'%(data[0],data[1],data[2])
        print(sql)
        try:
            cursor.execute(sql)
            self.sqlcon.commit()
            print('done')
        except Exception as e:
            print(e)
    def subjectana(self):
        cursor = self.sqlcon.cursor()
        # 读取数据并按照学位分类
        sql = 'select duration,count(*) from test0 group by duration order by count(*) desc'
        try:
            cursor.execute(sql)
            results=cursor.fetchall()
            print(results)
            subname=[]
            subnum=[]
            for subcount in results:
                subname.append(subcount[0])
                subnum.append(subcount[1])
            plt.figure(figsize=(8,5))
            plt.bar(subname,subnum)
            plt.title(u'曼彻斯特大学2020招生学制分布图')
            plt.xlabel('学制')
            plt.ylabel('年')
            plt.savefig('ma.png')
            plt.show()


        except Exception as e:
            print(e)
# api='https://www.manchester.ac.uk/study/undergraduate/courses/2020/xml/'
if __name__=="__main__":
    mcst=Manchesite('localhost','root','123456','test',char='utf8')
    # mcst.getxml(api)
    mcst.subjectana()