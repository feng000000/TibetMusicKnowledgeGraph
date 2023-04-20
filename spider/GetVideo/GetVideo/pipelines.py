# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from urllib import request
import os


class GetvideoPipeline:
    def process_item(self, item, spider):
        url = item['url']

        if not url:
            raise DropItem('Missing video_url in %s' % item)

        filepath = "Data/Videos/%s.mp4" % item['title']
        titlepath = "Data/VideoList.txt"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        os.makedirs(os.path.dirname(titlepath), exist_ok=True)

        # print("download url: " + url)
        request.urlretrieve(url, filepath)

        with open(titlepath, "a+") as f:
            f.write(item['title'] + '\n')

        return item