# coding=utf-8
import sys
import html_parser, url_manager, html_downloader
import requests
from bs4 import BeautifulSoup
import urllib2
import json
import time
import urllib3.contrib.pyopenssl

reload(sys)
sys.setdefaultencoding('utf-8')


class SpiderMain(object):
    def __init__(self):
        self.alldata = []
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmDownloader()
        self.parser = html_parser.HtmParser()

    def craw(self, root_url):
        count = 1
        # 分页模式的  第一页   首页50个li标签进行循环  每个li标签  1。找到name 2 进去之后在进行构建新的URL 在找到地址构成一个对象，存储在一个数组中
        # 难点 ----  如果找到第二页，循环

        # 携程
        headers = {
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        }
        hotel_array = []
        requests.adapters.DEFAULT_RETRIES = 5
        requests.packages.urllib3.disable_warnings()
        urllib3.contrib.pyopenssl.inject_into_urllib3()

        for i in range(11, 115):
            print i
            if i % 5 == 0:
                time.sleep(3)
            index = str(i)
            p_url = 'p' +str(index)
            test_url = root_url + p_url
            html_cont = requests.get(test_url, headers=headers, verify=False)
            print html_cont
            soup = BeautifulSoup(html_cont.content, 'html.parser', from_encoding='utf-8')
            hotel_nodes = soup.find_all('div', class_='hlist_item')

            iii = 0
            for x in hotel_nodes:
                iii += 1
                if iii % 5 == 0:
                    time.sleep(5)
                hotel_dict = {}
                jstr = ''
                hotel_dict['name'] = x.find('div', class_='hlist_item_name').find('a').get_text().encode("utf-8")
                hotel_dict['ename'] = x.find('div', class_='hlist_item_ename').find('a').get_text().encode("utf-8")
                new_url = 'https://hotels.ctrip.com/' + x.find('div', class_='hlist_item_name').find('a').attrs['href']
                new_html_cont = requests.get(new_url, headers=headers, verify=False)
                address_soup = BeautifulSoup(new_html_cont.content, 'html.parser', from_encoding='utf-8')
                hotel_dict['address'] = address_soup.find('span', class_='address_text').get_text().encode("utf-8")
                hotel_dict['latitude'] = address_soup.find('div', attrs={'itemprop':'geo'}).find_all('meta')[0]['content']
                hotel_dict['longitude'] = address_soup.find('div', attrs={'itemprop':'geo'}).find_all('meta')[1]['content']
                # hotel_array.append(hotel_dict)
                print hotel_dict

                s = requests.session()
                s.keep_alive = False
                jstr = json.dumps(hotel_dict, ensure_ascii=False)

                with open('batiya.json', 'a+b') as f:
                    f.write(jstr)
                    f.write(',')

        print hotel_array
        # agoda
        # headers = {
        #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
        # }
        # html_cont = requests.get(root_url, headers=headers)
        # print html_cont
        # soup = BeautifulSoup(html_cont.content, 'html.parser', from_encoding='utf-8')
        # hotel_nodes = soup.find_all('div', class_='LoginBanner')


        # print '...........................'


if __name__ == '__main__':
    # 携程网的网站
    root_url = 'http://hotels.ctrip.com/international/pattaya622'      # 芭提雅
    root_url8 = 'http://hotels.ctrip.com/international/huahinchaam3759'  # 华欣
    root_url9 = 'http://hotels.ctrip.com/international/phuket725'   # 普吉岛
    root_url11 = 'http://hotels.ctrip.com/international/beit35981'   # 拜县
    root_url12 = 'http://hotels.ctrip.com/international/phiphi1228'  # 皮皮岛    1-7
    root_url10 = 'http://hotels.ctrip.com/international/kohsamui1229'  # 苏梅岛
    root_url4 = 'https://hotels.ctrip.com/international/bangkok359/'
    root_url5 = 'http://hotels.ctrip.com/international/chiangmai623'
    root_url6 = 'http://hotels.ctrip.com/international/chiangrai647'
    root_url3 = 'https://weather.com/zh-CN/weather/today/l/61d235a12c8f0b158c472bb5cf4a6a2de4ebb97b0fc580d441a6ac059e16d77f'
    root_url1 = 'https://www.baidu.com'
    root_url2 = 'https://www.agoda.com/zh-cn/pages/agoda/default/DestinationSearchResult.aspx?asq=jyeoc2Cq5RUFbM4d4Mn64PdB8G0GxwnEuv4y9%2B8jSZJ3jp3qdXtr56jOJtcK2bt7aHCCFa2By49WJavLIHbLR9t97sFmUJfg0rs%2BIxncUgYyvzhpqnZ39XQafsUKr5aLuD%2Bawn5jfi8x72geCShXnG99Cp8%2FVnc6mkVrMJ504obV%2Fi0y0KRQ5wboBBIWaS5itbE23B8cYzTyE7xumsHHmw%3D%3D&city=9395&cid=-38&tick=636700138298&languageId=8&userId=5ad97632-cd07-41e5-8509-80da712ea882&pageTypeId=103&origin=CN&locale=zh-CN&aid=130589&currencyCode=CNY&htmlLanguage=zh-cn&cultureInfoName=zh-CN&ckuid=5ad97632-cd07-41e5-8509-80da712ea882&prid=0&checkIn=2018-09-11&checkOut=2018-09-15&rooms=1&adults=1&children=0&priceCur=CNY&los=4&textToSearch=%E6%9B%BC%E8%B0%B7&productType=-1'

    obj_spider = SpiderMain()
    obj_spider.craw(root_url)

    # print(type(response))
    # print(response.status_code)
    # print(type(response.text))
    # print(response.text)
    # print(response.cookies)
    # print(response.content)
    # print(response.content.decode())

    # get
    # data = {
    #     "name": "zhaofan",
    #     "age": 22
    # }
    # response = requests.get("http://httpbin.org/get", params=data)
    # print(response.url)
    # print(response.text)

    # obj_spider = SpiderMain()
    # obj_spider.craw(root_url)
    # test()

