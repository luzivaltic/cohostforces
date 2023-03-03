# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ContestItem(scrapy.Item):
    Id = scrapy.Field()
    Name = scrapy.Field()
    Start_time = scrapy.Field()
    Rank = scrapy.Field()
    Solved = scrapy.Field()
    Rating_change = scrapy.Field()
    New_rating = scrapy.Field()
    
class UserItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = scrapy.Field()
    Title = scrapy.Field()
    Rating = scrapy.Field()
    Max_rating = scrapy.Field()
