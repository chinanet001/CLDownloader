import urllib.request
import re
import os
import threading
import time

# 配置部分
headers = ('User-Agent', 'Mozilla/5.0ko)')
proxy = '127.0.0.1:1080'
proxy_support = urllib.request.ProxyHandler({'http': proxy})
opener = urllib.request.build_opener(proxy_support)
urllib.request.install_opener(opener)
opener.addheaders = [headers]


class cl:
    def __init__(self):
        pass

    def start(self, PageNumber):
        print('开始爬取...')
        self.spider1(PageNumber)

    def spider1(self, PageNumber):
        url = 'http://t66y.com/thread0806.php?fid=16&search=&page=' + str(PageNumber)
        page = self.urlreq(url)
        comp = re.compile(r'<h3><a href=\"(.+)\" target="_blank" id="">(.+)</a></h3>')
        self.findurl = comp.findall(page)
        for i in range(len(self.findurl)):
            try:
                if '<font' in self.findurl[i][1]:
                    os.mkdir(self.findurl[i][1][18:-7])
                else:
                    os.mkdir(self.findurl[i][1])
            except:pass
            self.spider2(i)

    def spider2(self, num):
        url2 = 'http://t66y.com/' + self.findurl[num][0]
        page = self.urlreq(url2)
        comp = re.compile(r'<br><br><input src=\'(.*?)\' type=\'image\' onclick="window\.open')
        picurl = comp.findall(page)
        self.threads(picurl,num)

    def urlreq(self, url):
        req = urllib.request.Request(url)
        page = urllib.request.urlopen(req).read().decode('gbk')
        return page

    def threads(self,picurl,num):#多线程
        for thread in range(4):
            t=threading.Thread(target=self.PicDownloader,args=(picurl,num,thread))
            t.start()



    def PicDownloader(self, picurl, num,thread):
        for i in range(thread,len(picurl),4):
            filename =  str(self.findurl[num][1]) + '/' + str(i) + '.jpg'
            if os.path.exists(filename):
                #print(filename)
                pass
            else:
                req = urllib.request.Request(picurl[i])
                try:
                    page = urllib.request.urlopen(req).read()
                    file = open(filename, 'wb')
                    file.write(page)
                    file.close()
                    print(filename)

                except:
                    pass


if __name__ == '__main__':
    print('需要使用代理，默认端口为1080')
    test = cl()
    test.start(input('输入要爬取的页码:'))  # 页码
