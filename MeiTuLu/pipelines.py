# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
from MeiTuLu.settings import IMAGES_STORE

from scrapy.pipelines.images import ImagesPipeline

class MeituluPipeline(object):
    def process_item(self, item, spider):
        return item

class MeituluImagePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        request_objs = super(MeituluImagePipeline, self).get_media_requests(item, info)
        for request_obj in request_objs:
            request_obj.item = item
        return request_objs

    def file_path(self, request, response=None, info=None):
        path = super(MeituluImagePipeline, self).file_path(request)
        path = path.replace("full", "")
        img_type = request.item.get("img_type")
        img_name = request.item.get("img_name")
        print(img_name)
        img_path = os.path.join(IMAGES_STORE, img_type)
        print(img_path)
        if not os.path.exists(img_path):
            os.mkdir(img_path)
        # print(img_path + img_name + ".jpg")
        return img_path + path


