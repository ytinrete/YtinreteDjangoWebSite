import math
import requests
import threading
from bs4 import BeautifulSoup


def get(url, params=None, headers=None):
    try:
        r = requests.get(url, params=params, headers=headers)
        print(r.text)
    except BaseException as e:
        print(e)


def post(url, data=None, params=None, headers=None, files=None):
    try:
        r = requests.post(url, data=data, params=params, headers=headers, files=files)
        print(r.text)
    except BaseException as e:
        print(e)

    pass


def page():
    page_size = 10
    page_group_size = 5  # don't change this at present
    context = {}

    index = 7
    count = 100

    front = page_size * (index - 1) + 1
    if front > count:
        index = 1
        front = 1
    context['index'] = index
    back = front + page_size - 1
    if back > count:
        back = count
    if index == 1:
        context['pre'] = False
    else:
        context['pre'] = True

    if back == count:
        context['next'] = False
    else:
        context['next'] = True

    page_count = math.ceil(float(count) / 10)

    context['page_list'] = []
    if page_count <= page_group_size:
        for i in range(1, page_group_size + 1):
            context['page_list'].append(i)
    else:
        if index <= (page_group_size - 1) / 2 + 1:
            for i in range(1, page_group_size + 1):
                context['page_list'].append(i)
        elif index >= page_count - (page_group_size - 1) / 2:
            for i in range(page_count - page_group_size + 1, page_count + 1):
                context['page_list'].append(i)
        else:
            for i in range(int(index - (page_group_size - 1) / 2), int(index + (page_group_size - 1) / 2 + 1)):
                context['page_list'].append(i)

    print(page_count)
    print(context)


def test_thread(data):
    if data and data.get('Addr'):
        try:
            r = requests.get('http://whatismyipaddress.com/ip/' + data.get('Addr'))
            if r.status_code == 200:
                html_tree = BeautifulSoup(r.text, 'lxml')
                for meta in html_tree.head.select('meta'):
                    if meta.get('name') == 'description':
                        # print(meta.get('content'))
                        location = meta.get('content')
                        break
        except BaseException as e:
            print(e)

        print('end')


if __name__ == "__main__":
    # get("http://localhost:8000/python/TestOne")

    # post()

    threading.Thread(target=test_thread, args=[{'Addr': '140.205.201.6'}]).start()

    print("ok")

    pass
