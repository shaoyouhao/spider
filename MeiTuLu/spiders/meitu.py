# -*- coding: utf-8 -*-
import scrapy

from MeiTuLu.items import MeituluItem


class MeituSpider(scrapy.Spider):
    name = 'meitu'
    allowed_domains = ['meitulu.com']
    start_urls = ['https://www.meitulu.com/t/changtui/']

    def parse(self, response):
        img_type = response.xpath("//div[@class='listtags_r']/h1[1]/text()").extract_first()
        img_type = img_type.split("_")[0].replace("美女图片", "")
        li_list = response.xpath("//div[@class='boxs']/ul[@class='img']/li")
        for li in li_list:
            jigou = li.xpath("./p[2]/a/text()").get()
            mote = li.xpath("./p[3]/a/text()").get()
            if mote is None:
                mote = li.xpath("./p[3]/text()").get().replace("模特：", "")
            biaoqian = li.xpath("./p[4]/a/text()").getall()
            item = MeituluItem(img_type=img_type, jigou=jigou, mote=mote, biaoqian=biaoqian)
            url = li.xpath("./a/@href").get()
            if url is None:
                print("未获取的图片详细地址")
            else:
                yield scrapy.Request(url=url, callback=self.get_img_detail, meta={"item": item})

    def get_img_detail(self, response):
        item = response.meta.get("item")
        img_list = response.xpath("//div[@class='content']/center/img")
        for img in img_list:
            image_urls = img.xpath("./@src").getall()
            img_name = img.xpath("./@alt").get()
            item["img_name"] = img_name
            item["image_urls"] = image_urls
            # print(item)
            yield item

        #获取详情页的下一页url
        next_url = response.xpath("//div[@id='pages']/a[text()='下一页']/@href").get()
        span = response.xpath("//div[@id='pages']/span/text()").get()
        last_page = response.xpath("//div[@id='pages']/a[text()='下一页']/preceding-sibling::a[1]/text()").get()

        if span == last_page:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.get_img_detail, meta={"item": item})
            print("当前图片已爬取完毕")
            return
        else:
            yield scrapy.Request(url=response.urljoin(next_url), callback=self.get_img_detail, meta={"item": item})