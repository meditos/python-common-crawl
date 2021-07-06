import hashlib
from time import gmtime, strftime


# Tesco Product Class
class TescoProduct:

    def __init__(self, json_product):
        # Initialise Object with a Json array instead of using Setters.
        self.title = json_product.title
        self.brand = json_product.brand
        self.url = json_product.url
        self.source_id = json_product.source_id
        print("New Product object Initialised in memory")

    def to_json(self):
        # Returns Object infomation in form of a Json array
        json_product = {
            'title': self.title,
            'brand': self.brand,
            'url': self.url,
            'sid': self.source_id
        }
        return json_product
