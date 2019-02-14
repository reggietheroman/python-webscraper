from requests import get
from requests.exceptions import RequestException
from  contextlib import closing
from bs4 import BeautifulSoup
import pprint

def simple_get(url):
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    print (e)


def get_stuff():
    url = 'https://www.theknowledgeacademy.com/'
    response =  simple_get(url)

    if response is not None:
        html = BeautifulSoup(response, 'html.parser')
        sub_category_titles = set()
        anchors = html.select('.navbox > a:nth-of-type(1)')
        
        for anchor in anchors:
            sub_category_titles.add(anchor.contents[0])

        return sub_category_titles

    raise Exception('Error retrieving contents at {}'.format(url))

def objectavize(sub_category_lists):
    sub_categories = [];
    for id, sub_cat in enumerate(sub_category_lists):
        sub_categories.append({'title': sub_cat, 'slug': sub_cat.replace('& ', '').lower().replace(' ', '-'), 'priority': id + 1})
    return sub_categories

stuff = objectavize(get_stuff())
pp = pprint.PrettyPrinter(indent=4, width=200, stream='text.txt')
pp.pprint(stuff)

