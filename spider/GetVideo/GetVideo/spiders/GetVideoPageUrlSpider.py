import scrapy
from GetVideo.items import GetvideoItem
from selenium import webdriver
from selenium.common.exceptions import TimeoutException

class GetVideoPageUrlSpider(scrapy.Spider):
    name = "getVideo"

    start_urls = [
        # 百度视频搜索 西藏音乐
        r'https://www.baidu.com/sf/vsearch?pd=video&tn=vsearch&wd=%E8%A5%BF%E8%97%8F%E9%9F%B3%E4%B9%90&oq=%E8%A5%BF%E8%97%8F%E9%9F%B3%E4%B9%90'

    ]

    for i in range(10, 310, 10):
        tempurl = "https://www.baidu.com/sf/vsearch?pd=video&tn=vsearch&wd=%E8%A5%BF%E8%97%8F%E9%9F%B3%E4%B9%90&oq=%E8%A5%BF%E8%97%8F%E9%9F%B3%E4%B9%90&pn=" + str(i)
        start_urls.append(tempurl)
        # print("temp_url: " + tempurl)

    def parse(self, response):
        # 好看视频的urls
        urls = response.xpath('//div[@class="video_list video_short"]/a/@href')

        for ele in urls:
            url = ele.extract()
            if url == "":
                continue

            print("\npage_url: " + url)

            browser = webdriver.Chrome(executable_path="/home/feng/Downloads/chromedriver/chromedriver")

            try:
                # 设置超时时间为10秒
                browser.set_page_load_timeout(5)

                browser.get(url)

            except TimeoutException as e:
                # 处理页面超时异常
                print("Page load timed out: ", e)

            finally:
                video_url = browser.execute_script("""
                    return document.querySelectorAll('.art-video')[0].src;
                """)
                # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                print("\nvideo_url: " + video_url)
                # 关闭浏览器
                browser.quit()

            yield scrapy.Request(url, callback=self.getVideo, meta={'url': video_url})

    def getVideo(self, response):
        print("getVideo")
        item = GetvideoItem()
        title = response.xpath('//title/text()')

        item['title'] = title.extract()[0]
        item['url'] = response.meta['url']

        return item
