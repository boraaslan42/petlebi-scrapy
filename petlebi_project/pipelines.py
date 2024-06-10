# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
"""
f = open('data.json', 'w')
json.dump(extracted_data, f, indent=4)
f.close()

    Returns:
        _type_: _description_
    """
class PetlebiProjectPipeline:
    def process_item(self, item, spider):  # default method
        # calling dumps to create json data.
        line = json.dumps(item)+","
        
        self.file.write(line)
        return item
 
    def open_spider(self, spider):
        self.file = open('petlebi_products.json', 'w')
        self.file.write("[")
 
    def close_spider(self, spider):
        self.file.write('{"end":"end"}]')
        self.file.close()