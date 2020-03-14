# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from meitu_spider.items import MeituSpiderItem


class MtSpider(CrawlSpider):
    name = 'mt'
    allowed_domains = ['meitulu.com']
    start_urls = ['https://www.meitulu.com/item/20779.html']

    rules = (
        Rule(LinkExtractor(allow=r'.*?/item/.*?\.html'), callback='parse_detail', follow=True),
        # Rule(LinkExtractor(allow=r'.*/item/\d+_\d+\.html'), callback='parse_detail', follow=True),
    )

    def parse_detail(self, response):
        publish_from = response.xpath("//div[@class='c_l']/p[contains(text(), '发行机构：')]/a/text()").get()
        img_num = response.xpath("//div[@class='c_l']/p[contains(text(), '图片数量：')]/text()").get()
        #讲图片数量提取出来并转换成int类型(”图片数量：96张“ --> 96)
        if img_num:
            img_num = int(img_num.split("：")[-1].split("张")[0].strip())
        name = response.xpath("//div[@class='c_l']/p[contains(text(), '模特姓名：')]/a/text()").get()
        if not name:
            name = response.xpath("//div[@class='c_l']/p[contains(text(), '模特姓名：')]/text()").get().replace("模特姓名：", "")
        publish_date = response.xpath("//div[@class='c_l']/p[contains(text(), '发行时间：')]/text()").get()
        if publish_date:
            publish_date = publish_date.split("：")[-1].strip()
        image_urls = response.xpath("//img[@class='content_img']/@src").getall()

        item = MeituSpiderItem(
            publish_from=publish_from,
            img_num=img_num,
            name=name,
            publish_date=publish_date,
            image_urls=image_urls,
            origin_url=response.url
        )

        yield item



