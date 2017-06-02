from __future__ import absolute_import
from celery import shared_task
from celery import task
from .models import VisitInfo
import pytz
from urllib import request as req
import zlib
from bs4 import BeautifulSoup


@task
def search_req(time_str):
    if time_str is None or time_str == '':
        return
    try:
        for v in VisitInfo.objects.raw('SELECT * FROM MessageBoard_visitinfo WHERE TimeStr = %s', [time_str]):
            if v.Addr and v.Location == '':
                html_str = get_response_str(req_maker('http://whatismyipaddress.com/ip/' + v.Addr))
                html_tree = BeautifulSoup(html_str, 'lxml')
                for meta in html_tree.head.select('meta'):
                    if meta.get('name') == 'description':
                        # print(meta.get('content'))
                        v.Location = meta.get('content')
                        v.save()  # just find first
                        break
    except BaseException as e:
        print(e)


def req_maker(path):
    if path:
        reqs = req.Request(path)
        reqs.add_header("User-Agent",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36")
        reqs.add_header("Accept", "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
        reqs.add_header("Accept-Encoding", "gzip, deflate, sdch")
        reqs.add_header("Accept-Language", "zh-CN,zh;q=0.8,en;q=0.6")
        return reqs
    else:
        return None


def get_response_str(reqs):
    with req.urlopen(reqs, timeout=5) as f:
        decompressed_data = zlib.decompress(f.read(), 16 + zlib.MAX_WBITS)
        return str(decompressed_data, "utf-8", errors='replace')
