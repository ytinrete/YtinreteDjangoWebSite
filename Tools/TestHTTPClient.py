import math
import requests


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


if __name__ == "__main__":
    # get("http://localhost:8000/python/TestOne")

    # post()

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
            for i in range(int(index - (page_group_size - 1) / 2), int(index +  (page_group_size - 1) / 2 +1)):
                context['page_list'].append(i)

    print(page_count)
    print(context)
    print("ok")

    pass
