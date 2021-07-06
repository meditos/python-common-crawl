import re


def get_text_li_span(parser, name=None, attrs={}):
    span_list = []
    find = parser.find(name, attrs=attrs)
    if find:
        for li in find.find_all("li"):
            span = li.find("span")
            if span and span.get_text() != "":
                span_list.append(span.get_text())
    return span_list


def get_text_li(parser, name=None, attrs={}):
    li_list = []
    find = parser.find(name, attrs=attrs)
    if find:
        for li in find.find_all("li"):
            li_list.append(li.get_text())
    return li_list


def get_level(parser, name_attrs_list):
    for name, attrs in name_attrs_list:
        parser = parser.find(name, attrs=attrs)
        if not parser:
            return None
    return parser.get_text()


def tagged_elements(elements):
    tagged_elements_list = []
    for element in elements:
        tagged_element = re.search('<.+>(.+)</.+>', element)
        if tagged_element:
            tagged_elements_list.append(tagged_element.group(1))
    return tagged_elements_list


def clean_tagged_elements(elements):
    cleaned_elements = []
    for element in elements:
        cleaned_element = re.search('<.+>(.+)</.+>', element)
        if cleaned_element:
            cleaned_elements.append(cleaned_element.group(1))
        else:
            cleaned_elements.append(element)
    return cleaned_elements

