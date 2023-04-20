import scrapy

class GetArticleSpider(scrapy.Spider):
    name = "getArticle"

    # 大百科全书 网站搜索url
    temp_url = "https://www.zgbk.com/ecph/search/result?SiteID=1&Query=%E8%A5%BF%E8%97%8F%E9%9F%B3%E4%B9%90"
