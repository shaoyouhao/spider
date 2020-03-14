# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import scrapy

from scrapy.pipelines.images import ImagesPipeline

from meitu_spider.settings import IMAGES_STORE


# class MeituSpiderPipeline(object):
#     def process_item(self, item, spider):
#
#         return item

class ImagesDownloadPipeline(ImagesPipeline):


    def get_media_requests(self, item, info):
        request_objs = super(ImagesDownloadPipeline, self).get_media_requests(item,info)
        for request_obj in request_objs:
            request_obj.item = item
            # print(request_obj)
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(ImagesPipeline, self).file_path(request, response, info).replace("full", "")
        name = request.item.get("name")
        print(name)
        img_path = os.path.join(IMAGES_STORE, "images")
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        last_path = os.path.join(img_path, name)
        if not os.path.exists(last_path):
            os.mkdir(last_path)
        return last_path + path

