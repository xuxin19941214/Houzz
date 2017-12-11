# -*- coding: utf-8 -*-
import scrapy
from scrapy.http.request import Request
from Houzz.items import HouzzItem
import re
import humanfriendly


class HouzzSpider(scrapy.Spider):
    name = 'houzz'
    allowed_domains = ['houzz.com']
    start_urls = ['https://www.houzz.com/professionals']

    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
    }

    # 起始url
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, headers=self.header, callback=self.parse)

    # 各类设计师的分类
    def parse(self, response):
        designer_lists = response.xpath('//li[@class="sidebar-item"]/a/@href').extract()[1:2]
        print(designer_lists)
        for i, designer_list in enumerate(designer_lists):
            for i in range(0, 335):
                ordinal = 0 + i * 15
                designer_link = designer_list + '/p/' + str(ordinal)
                print(designer_link)
                yield Request(url=designer_link, headers=self.header, callback=self.parse_designerHtml)
        # 策展库各分类的名字
        # Li_class_name = response.xpath('//h2[@class="rf-curated-galleries-cover__label qa-curated-galleries-cover__label"]/text()').extract()

        # for i, Li_img_link in enumerate(Li_link_list):
        #     # https://www.behance.net/v2/galleries/2/projects?ordinal=48
        #     # https://www.behance.net/galleries/2/Graphic-Design?tracking_source=view-all
        #     item = BehanceItem()
        #     parten = re.compile(r'.*?/galleries/(\d+)/.*')
        #     num1 = parten.findall(Li_img_link)[0]
        #     # item['Li_classes'] = Li_class_name[i]
        #     for i in range(50000 // 48):
        #         ordinal = 0 + i * 48
        #         # 各图片集的链接
        #         Li_img_link = 'https://www.behance.net/v2/galleries/' + num1 + '/projects?ordinal=' + str(ordinal)

                # yield Request(url=Li_img_link, headers=self.second_header, callback=self.Li_jsonData,
                #               meta={'meta_1': item})

    # 提取各设计师
    def parse_designerHtml(self, response):
        project_links = response.xpath('//div[@class="pro-cover-photos"]/a/@href').extract()
        # print(link_lists1)
        for project_link in project_links:
            yield Request(url=project_link, headers=self.header, callback=self.parse_allProject)

    # 进入设计师主页内提取所有项目链接
    def parse_allProject(self, response):
        try:
            allProject_links = response.xpath('//div[@class="profile-content-wide"]//div[@class="header-6 top"]/a/@href').extract()
            for allProject_link in allProject_links:
                yield Request(url=allProject_link, headers=self.header, callback=self.parse_project)
        except Exception as e:
            pass

    # 提取项目链接
    def parse_project(self, response):
        project_lists = response.xpath('//a[@class="whiteCard project-card "]/@href').extract()
        for project_list in project_lists:
            yield Request(url=project_list, headers=self.header, callback=self.parse_projectHtml)

    # 发送项目链接请求获取信息
    def parse_projectHtml(self, response):
        item = HouzzItem()
        item['project_url'] = response.url
        # 项目简介
        project_info = response.xpath('//div[@id="projectDescTrimmed"]/text()[1]').extract()
        try:
            project_info = project_info[0].strip()
            print(project_info)
            item['project_info'] = project_info
        except Exception as e:
            item['project_info'] = ''

        # 项目的名字
        project_name = response.xpath('//div[@id="rightSideContent"]//h1/text()').extract()
        try:
            project_name = project_name[0]
            item['project_name'] = project_name
        except Exception as e:
            item['project_name'] = ''

        # 项目年份
        # project_time = response.xpath('//div[@class="project-year"]/text()').extract()
        # try:
        #     project_time = re.sub('^(.*?\:)', '', project_time[0]).strip()
        #     print(project_time)
        #     item['project_time'] = project_time
        # except Exception as e:
        #     item['project_time'] = ''
        # 项目城市
        # project_country = response.xpath('//div[@class="project-country"]/text()').extract()
        # try:
        #     project_country = re.sub('^(.*?\:)', '', project_country[0]).strip()
        #     print(project_country)
        #     item['project_country'] = project_country
        # except Exception as e:
        #     item['project_country'] = ''
        # 提取图片链接
        img_links = response.xpath('//div[@class="imageArea "]//a/@href') .extract()
        for img_link in img_links:
            # item['img_link'] = img_link
            yield Request(url=img_link, headers=self.header, callback=self.parse_imgLink, meta={'meta_1': item})

    # 提取图片页面链接进行处理图片页面
    def parse_imgLink(self, response):
        img_link = response.url
        # l = response.meta['meta_1']
        item = HouzzItem()
        item['img_link'] = img_link
        m = response.meta['meta_1']

        # img_url = response.xpath('//img[@id="mainImage"]/@src').extract()
        # print("=================================")
        # print(img_url)
        # print("=================================")
        # try:
        #     img_bigUrl = img_url[0].replace('_4', '_9')
        #     print("----------------------------------")
        #     print(img_bigUrl)
        #     print("----------------------------------")
        #     item['img_bigUrl'] = img_bigUrl
        # except Exception as e:
        #     item['img_bigUrl'] = ''

        designer_name = response.xpath('//div[@class="userDetails"]//a[@class="blackLabel hzHouzzer hzHCUserName header-5 top"]/text()').extract()
        try:
            print(designer_name)
            item['designer_name'] = designer_name[0]
        except Exception as e:
            item['designer_name'] = ''

        img_collection = response.xpath('//span[@id="addToIdeabookBtn"]/span[2]/text()').extract()
        try:
            img_collection = humanfriendly.parse_size(img_collection[0])
            print(img_collection)
            item['img_collection'] = img_collection
        except Exception as e:
            item['img_collection'] = ''

        img_name = response.xpath('//div[@class="spaceDetails"]/h1/text()').extract()
        try:
            print(img_name)
            item['img_name'] = img_name[0]
        except Exception as e:
            item['img_name'] = ''

        relevant_theme = response.xpath('//div[@id="relatedSearches"]/div[@class="related-searches-links"]//text()').extract()
        try:
            relevant_theme = ','.join(relevant_theme)
            print(relevant_theme)
            item['relevant_theme'] = relevant_theme
        except Exception as e:
            item['relevant_theme'] = ""

        # 图片类别
        img_Category = response.xpath('//div[@id="keywordsDiv"]//dd[1]/a/text()').extract()
        try:
            print(img_Category)
            item['img_Category'] = img_Category[0]
        except Exception as e:
            item['img_Category'] = ""

        # 图片样式
        img_Style = response.xpath('//div[@id="keywordsDiv"]//dd[2]/a/text()').extract()
        try:
            print(img_Style)
            img_Style = img_Style[0]
        except Exception as e:
            img_Style = ""

        # 图片位置
        img_Location = response.xpath('//div[@id="keywordsDiv"]//dd[3]/a/text()').extract()
        try:
            print(img_Location)
            img_Location = img_Location[0]
        except Exception as e:
            img_Location = ""

        #图片关键字
        img_Keyword = response.xpath('//div[@id="keywordsDiv"]//dd[4]/text()[1]').extract()
        try:
            img_Keyword = img_Keyword[0].strip()
            print(img_Keyword)
        except Exception as e:
            img_Keyword = ""

        try:
            img_Keywords = img_Style + ';' + img_Location + ';' + img_Keyword
            print(img_Keywords)
            item['img_Keywords'] = img_Keywords
        except Exception as e:
            item['img_Keywords'] = ""

        img_urls = response.xpath('//img[@id="mainImage"]/@src').extract()
        for img_url in img_urls:
            img_bigUrl = img_url.replace('_4', '_9')
            item['img_bigUrl'] = img_bigUrl
            item['project_info'] = m['project_info']
            item['project_name'] = m['project_name']
            item['project_url'] = m['project_url']

            yield item
