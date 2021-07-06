from bs4 import BeautifulSoup
from product.extractors.extractor_utils import get_text_li, get_level, clean_tagged_elements, tagged_elements, \
    get_text_li_span


# Extract Product from the single HTML page.
def extract_product(html_content, url):
    # Read page and read to extract product infomation
    parser = BeautifulSoup(html_content, "html.parser")
    product = {}
    add_title(parser, product)
    add_categories(parser, product)
    add_price(parser, product)
    add_price_per_quantity(parser, product)
    add_product_description(parser, product)
    add_product_features(parser, product)
    add_pack_size(parser, product)
    # TODO: Alergens tags are lost.
    add_ingredients_alergens(parser, product)
    add_storage_details(parser, product)
    add_origin_info(parser, product)
    add_return_address(parser, product)
    add_net_contents(parser, product)
    add_nutrition(parser, product)

    return product, []


def add_nutrition(parser, product):
    nutrition_table = parser.find("table", attrs={"class": "product__info-table"})
    if nutrition_table:
        th_keys = nutrition_table.find_all('th')
        keys = [th_key.get_text() for th_key in th_keys]
        nutrition_values = []
        for contents in nutrition_table.find_all('tr'):
            td_values = contents.find_all('td')
            nutrition_values.append([td_value.get_text() for td_value in td_values])
        nutrition = {"nutrition_keys": keys, "nutrition_values": nutrition_values}
        product["nutrition"] = nutrition


def add_categories(parser, product):
    category_list = get_text_li_span(parser, "div", attrs={"class": "breadcrumbs__content"})
    if category_list:
        product["categories"] = category_list


def add_title(parser, product):
    title = parser.find("h1", attrs={"class": "product-details-tile__title"})
    if title:
        product["title"] = title.get_text()
    return product


def add_price(parser, product):
    product_price_div = parser.find("div", attrs={"class": "price-control-wrapper"})
    if product_price_div:
        price_value = product_price_div.find("span", attrs={"data-auto": "price-value"}).get_text()
        currency = product_price_div.find("span", attrs={"class": "currency"}).get_text()
        product["price"] = {"value": price_value, "currency": currency}
    return product


def add_price_per_quantity(parser, product):
    price_per_quantity_div = parser.find("div", attrs={"class": "price-per-quantity-weight"})
    if price_per_quantity_div:
        weight_price_value = price_per_quantity_div.find("span", attrs={"data-auto": "price-value"}).get_text()
        weight_currency = price_per_quantity_div.find("span", attrs={"class": "currency"}).get_text()
        weight = price_per_quantity_div.find("span", attrs={"class": "weight"}).get_text()
        product["price_per_quantity"] = {"value": weight_price_value, "currency": weight_currency, "weight": weight}
    return product


def add_product_description(parser, product):
    product_description = get_text_li(parser, name="div", attrs={"id": "product-description"})
    if product_description:
        product["product_description"] = product_description
    return product


def add_product_features(parser, product):
    features = get_text_li(parser, name="div", attrs={"id": "features"})
    if features:
        product["features"] = features
    return product


def add_pack_size(parser, product):
    pack_size = get_text_li(parser, name="div", attrs={"id": "pack-size"})
    if pack_size:
        product["pack_size"] = pack_size
    return product


def add_ingredients_alergens(parser, product):
    ingredients = get_level(parser, [("div", {"id": "ingredients"}), ("p", {"class": "product-info-block__content"})])
    if ingredients:
        # print(ingredients)
        ingredients_list = ingredients.split(',')
        product["alergens"] = tagged_elements(ingredients_list)
        product["ingredients"] = clean_tagged_elements(ingredients_list)
        # print("alergens: {}".format(product["alergens"]))
        # print("ingredients: {}".format(product["ingredients"]))
    return product


def add_storage_details(parser, product):
    storage_details = get_level(parser,
                                [("div", {"id": "storage-details"}), ("p", {"class": "product-info-block__content"})])
    if storage_details:
        product["storage_details"] = storage_details
    return product


def add_origin_info(parser, product):
    origin_info = get_level(parser, [("div", {"id": "origin-information-produce-of"}),
                                     ("p", {"class": "product-info-block__content"})])
    if origin_info:
        product["origin_info"] = origin_info
    return product


def add_return_address(parser, product):
    return_address = get_text_li(parser, name="div", attrs={"id": "return-address"})
    if return_address:
        product["return_address"] = return_address
    return product


def add_net_contents(parser, product):
    net_contents = get_level(parser, [("div", {"id": "net-contents"}), ("p", {"class": "product-info-block__content"})])
    if net_contents:
        product["net_contents"] = net_contents
    return product


# food_icons_list = []
# icons_list = parser.find("ul", attrs={"class": "food-icons-list"})
# if icons_list:
#     for span in icons_list.find_all("li"):
#         food_icons_list.append(span.find("span").get_text())
#     product["food_icons_list"] = food_icons_list

# Guideline Daily Amount (GDA)
# gda_list = []
# gda = parser.find("div", attrs={"class": "gda"})
# if gda:
#     gda_title = gda.find("span", attrs={"class": "title"})
#     for span in gda.find_all("li"):
#         gda_item = span.find("span", attrs={"class": "title"})
#         gda_energy = span.find("span", attrs={"class": "value energy"})
#         gda_percentage = span.find("span", attrs={"class": "value"})
#         gda_list.append({"gda_item": gda_item, "gda_energy": gda_energy, "gda_percentage": gda_percentage})
#     product["gda"] = {gda_title: gda_list}

