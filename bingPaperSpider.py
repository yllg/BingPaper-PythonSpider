
"""
Bing壁纸爬虫
"""

import urllib
import urllib.request
import ssl
import time
import json
import os.path

class BingBgDownloader(object):

    # 接口 下载数量n和时间戳nc为变量%d
    _bing_interface = 'https://cn.bing.com/HPImageArchive.aspx?format=js&idx=0&n=%d&nc=%d&pid=hp&FOR'
    # 域名常量
    _bing_url = 'https://cn.bing.com/'
    # 文件名格式化
    _img_filename = '[%s%s][%s].%s'

    def __init__(self):
        super(BingBgDownloader, self).__init__()
        # 初始化ssl
        ssl._create_default_https_context = ssl._create_unverified_context

    # 下载壁纸图片，对外暴露的方法
    def download(self, num=1, local_path='./'):
        if num <1 :
            num = 1
        url = self._bing_interface%( num, int(time.time()))
        img_info = self._get_img_infos(url)
        for info in img_info:
            print(self._get_imgurl(info))
            print(self._get_img_filename(info))
            self._down_img(self._get_imgurl(info),
                            self._get_img_filename(info))

    # 从接口获取图片资源json信息
    def _get_img_infos(self, url):
        request = urllib.request.urlopen(url).read()
        # 请求的接口数据转成json格式
        bgObjs = json.loads( bytes.decode(request) )
        return bgObjs['images']
    
    # 得到图片资源URL
    def _get_imgurl(self, img_info):
        return self._bing_url + img_info['url']

    # 从接口数据提取图片文件名
    def _get_img_filename(self, img_info):
        # 中文名
        zh_name = ''
        # 英文和中文两种括号都要考虑
        pos = max(img_info['copyright'].find(
            '('), img_info['copyright'].find('（'))
        if pos < 0:
            zh_name = img_info['copyright']
        else :
            zh_name = img_info['copyright'][0:pos]
        # 英文名
        entmp = img_info['url']
        # rindex从后往前查找
        en_name = entmp[entmp.rindex('/') + 1 : entmp.rindex('_ZH')]
        # 分辨率
        pix = entmp[entmp.rindex('_') + 1 : entmp.rindex('.')]
        # 后缀名
        ex_name = entmp[entmp.rindex('.') + 1 : len(entmp)]

        img_name = self._img_filename%(zh_name, en_name, pix, ex_name)
        return img_name

        """
        示例数据
        {
        startdate: "20180825",
        fullstartdate: "201808251600",
        enddate: "20180826",
        url: "/az/hprichbg/rb/JeanLafitte_ZH-CN11969195990_1920x1080.jpg",
        urlbase: "/az/hprichbg/rb/JeanLafitte_ZH-CN11969195990",
        copyright: "吉恩拉菲特国家历史公园和保护区内的巴拉塔里亚小路，美国路易斯安那州 (© Karine Aigner/Tandem Stills + Motion)",
        copyrightlink: "/search?q=%e5%90%89%e6%81%a9%e6%8b%89%e8%8f%b2%e7%89%b9%e5%9b%bd%e5%ae%b6%e5%8e%86%e5%8f%b2%e5%85%ac%e5%9b%ad%e5%92%8c%e4%bf%9d%e6%8a%a4%e5%8c%ba&form=hpcapt&mkt=zh-cn",
        title: "",
        quiz: "/search?q=Bing+homepage+quiz&filters=WQOskey:%22HPQuiz_20180825_JeanLafitte%22&FORM=HPQUIZ",
        wp: true,
        hsh: "e892f887caa2b20ea1641760e43eb94a",
        drk: 1,
        top: 1,
        bot: 1,
        hs: [ ]
        }
        """

    # 下载图片
    def _down_img(self, img_url, img_pathname):
        # 请求图片资源存到内存中
        img_data = urllib.request.urlopen(img_url).read()
        # wb以二进制的方式写到文件夹中
        f = open(img_pathname, 'wb')
        f.write(img_data)
        f.close()
        print('success saved image:', img_url)

if __name__ == '__main__':
   dl = BingBgDownloader()
   dl.download(1)
