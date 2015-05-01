import urllib.request
import re
from time import clock as now
import json
#单线程
#主要函数
def getjd(pid):
    #通过京东服务器查
    pid = str(pid)
    # 上面获取了商品ID，下面就是把ID添加到京东那个查价格的json地址里
    url = 'http://p.3.cn/prices/get?skuid=J_' + str(pid)
    html = urllib.request.urlopen(url).read().decode('utf-8')
    nprice = re.search(r'"p":"(.*?)"', html).group(1)
    oprice = re.search(r'"m":"(.*?)"}', html).group(1)
    price = nprice
    _url = r'http://club.jd.com/productpage/p-{}-s-0-t-3-p-0.html'.format(pid)
    #设置报头，伪装成浏览器，来访问json
    headers1 = {'GET': '',
                'Host': "club.jd.com",
                'User-Agent': "Mozilla/5.0 (Windows NT 6.2; rv:29.0) Gecko/20100101 Firefox/29.0",
                'Referer': 'http://item.jd.com/%s.html' % (pid)}#Refer告诉服务器从哪个页面请求
    req = urllib.request.Request(_url, headers=headers1)
    scode = urllib.request.urlopen(req).read().decode('gbk')
    global rs
    rs = json.loads(scode)
    return (pid)
 

#获取商品颜色，有的商品无颜色信息
def getProductColor(json_str):
 if('productColor' in json_str):
  return json_str['productColor']
 else:
  return "本商品无颜色信息"


#获取用户终端
def getUserClient(_str):
 pattern = re.compile(r'>(.+?)</a>')
 _rs = pattern.findall(_str)
 if(len(_rs) != 0):
  return _rs[0]
 else:
  return "来自网页"

#获取评论相关信息
def getComment(lis):
 _count = 0
 for j in lis:
  _count += 1
  print("第"+str('%d' % (_count))+"条评论:")
  print("评论内容:"+j['content'],"\n")
  print("买家:"+j['nickname'],"\n")
  print("买家级别:"+j['userLevelName'],"\n")
  print("买家地点:"+j['userProvince'],"\n")
  print("买家打分:"+str(j['score'])+"星","\n")
  print("购买时间："+j['referenceTime'],"\n")
  print("评论时间："+j['creationTime'],"\n")
  print("评论称赞数："+str(j['usefulVoteCount']),"\n")
  #抓取买家印象，由于有的买家没有，故需特判
  if('commentTags' in j):
   print("买家印象：")   
   for m in j['commentTags']:
    print(m['name']," ",end='\r')
  print("")  
  print("购买商品型号："+j['productSize'],"\n")
  print("商品颜色:",getProductColor(j))
  print("用户终端: ",getUserClient(j['userClientShow']))

#获取最大页码
def getMaxPage(pid):
 Mpage = rs['productCommentSummary']['commentCount']  // 10 #获取最大页码
 return Mpage + 1
 
 
 
#主体函数

def Main(pid):
 start = now()
 print('商品ID :\n')
 print(getjd(pid))
 print("\n买家印象:\n")
 for i in rs['hotCommentTagStatistics']:
  print(i['name'].encode('gbk').decode('gbk')+' X '+str(i['count']))
 print("==================================\n评论信息：\n")
 getComment(rs['comments'])
 finish = now()
 _time = finish - start
 print('本次爬虫执行时间约为：', round(_time, 2),'s')
#pid = "1411056"
pid = "1196255"
Main(pid)

