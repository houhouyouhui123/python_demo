import requests
import re
from requests.exceptions import ProxyError
from computer import Computer
from pymongo import MongoClient
from bs4 import BeautifulSoup
class ComputerInfo:
    def get_index_page(self,page=1):
        url='https://list.jd.com/list.html?cat=670,671,1105&page='+str(page)
        headers = {

        }
        reponse=requests.get(url, headers=headers)
        return reponse.content.decode()

    def get_list(self,page):
        soup=BeautifulSoup(self.get_index_page(page),'lxml')
        plist=soup.select('#plist .p-name a')
        pc_list = []
        for phone in plist:
            pc_list.append(('https:'+phone['href'])+'#product-detail')
        return pc_list

    def getOnePageInfo(self,page):
        computerList=[]
        for phone_url in self.get_list(page):
            response=None
            price=None
            try:
                response=requests.get(phone_url).content.decode('gbk')
            except UnicodeDecodeError as e:
                print(e)
                continue

            try:
                price_url = 'https://p.3.cn/prices/mgets?skuIds=J_' + phone_url[20:-20]
                price = requests.get(price_url).json()[0]['p']
            except ProxyError as p_e:
                price=None
                print(p_e)
            soup=BeautifulSoup(response,'lxml')
            detials=soup.select('#detail .tab-con .p-parameter .parameter2')
            detials=str(detials)
            brand = soup.select('#parameter-brand li a')[0].text
            brand=re.search('（(.*?)）', brand)
            name=re.search('商品名称：(.*?)<', detials)
            graphics = re.search('显卡型号：(.*?)<', detials)
            gMemory = re.search('显存容量：(.*?)G<', detials)
            memory = re.search('内存容量：(.*?)G<', detials)
            hDisk = re.search('硬盘容量：(.*?)<', detials)
            computer=Computer()
            computer.brand=get_group1(brand)
            computer.name=get_group1(name)
            computer.graphics=get_group1(graphics)
            computer.gMemory=get_group1(gMemory)
            computer.memory=get_group1(memory)
            computer.hDisk=get_group1(hDisk)
            computer.price=price
            computerList.append(computer)
        return computerList

    def getMutiPageInfo(self,count=1):
        computerList=[]
        response=self.get_index_page()
        soup=BeautifulSoup(response,'lxml')
        pageConut=soup.select('#J_bottomPage > span.p-skip > em:nth-child(1) > b')
        pageConut=int(pageConut[0].text)
        if count>pageConut:
            count=pageConut
        for i in range(1,count+1):
            computerList=computerList+self.getOnePageInfo(i)
        return computerList

def get_group1(info):
    if info!=None:
        return info.group(1)
    return None

def getCollectionName():
    client = MongoClient('localhost', 27017)
    demo_db = client['demo']
    return demo_db['pcInfo']

# computer=ComputerInfo()
# print('start spider!')
# computerList=computer.getMutiPageInfo(3)
# cName=getCollectionName()
# for computer in computerList:
#     print('start insert!')
#     cName.insert_one({
#         'brand':computer.brand,
#         'name':computer.name,
#         'graphics':computer.graphics,
#         'gMemory':computer.gMemory,
#         'memory':computer.memory,
#         'hDisk':computer.hDisk,
#         'price':computer.price
#     })
#     print('insert one')
# print('Done!')

def getDatas(names,counts):
    dList=[]
    for name,count in zip(names,counts):
        data={
            'name':name,
            'y':count
        }
        dList.append(data)
    return dList

def getBrand():
    cName=getCollectionName()
    computerList=cName.find()
    brandList=[]
    for computer in computerList:
        brandList.append(computer['brand'])
    brands=set(brandList)
    brands.remove(None)
    bCounts=[]
    for brand in brands:
        bCounts.append(brandList.count(brand))
    return getDatas(brands, bCounts)

def getBar():
    brands=getBrand()[2:10];
    nList=[]
    cList=[]
    for brand in brands:
        nList.append(brand['name'])
        cList.append(brand['y'])
    bar={
        'nList':nList,
        'cList':cList
    }
    return  bar