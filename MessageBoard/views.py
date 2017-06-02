from django.shortcuts import render

# Create your views here.
import os
import datetime
from django.http import HttpResponse
from django.http import HttpResponseNotAllowed
from django.http import HttpResponseServerError
from django.http import JsonResponse
from django.shortcuts import render
from .models import Thread
from .models import VisitInfo
import math
import MessageBoard.kittycode
import pytz
from urllib import request as req
import zlib
from bs4 import BeautifulSoup
from .tasks import search_req
from .tasks import send_new_thread_mail

from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def get_list(request):
    if request.method == 'GET':
        try:
            return HttpResponseServerError("interface is not in use yet!")
        except BaseException as e:
            print(e)
        return HttpResponseServerError(None)
    else:
        return HttpResponseNotAllowed(None)


@csrf_exempt
def add_thread(request):
    if request.method == 'POST':
        try:
            return HttpResponseServerError("interface is not in use yet!")
        except BaseException as e:
            print(e)
        return HttpResponseServerError(None)
    else:
        return HttpResponseNotAllowed(None)


@csrf_exempt
def img_upload(request):
    if request.method == 'POST':
        if request.FILES['file']:
            try:
                save_file_name = str(datetime.datetime.now().timestamp()) + "_" + request.FILES['file'].name
                with open(os.getcwd() + '/imagesUpload/' + save_file_name, 'wb+') as destination:
                    for chunk in request.FILES['file'].chunks():
                        destination.write(chunk)
            except BaseException as e:
                print(e)
                return HttpResponseServerError(None)
            # 返回成功
            return JsonResponse({'uploadImgFile': save_file_name})
        else:
            return HttpResponseServerError(None)
    else:
        return HttpResponseNotAllowed(None)


@csrf_exempt
def post_thread(request):
    if request.method == 'POST':
        try:
            record_visit(request)
            if not request.POST.get("author"):
                return HttpResponseServerError(None)

            if not request.POST.get("content"):
                return HttpResponseServerError(None)

            t = Thread()
            t.Author = request.POST.get("author")
            t.Content = request.POST.get("content")
            t.ContentEncode = MessageBoard.kittycode.encode(t.Content)

            tz = pytz.timezone('Asia/Shanghai')
            t.Timestamp = int(datetime.datetime.now().timestamp())
            t.TimeStr = datetime.datetime.fromtimestamp(int(t.Timestamp), tz=tz).strftime('%Y-%m-%d %H:%M:%S')
            # t.Time = datetime.datetime.fromtimestamp(int(obj['Time']))

            if request.FILES.get("file"):
                save_file_name = str(t.Timestamp) + "_" + request.FILES.get("file").name
                with open(os.getcwd() + '/media/imagesUpload/' + save_file_name, 'wb+') as destination:
                    for chunk in request.FILES['file'].chunks():
                        destination.write(chunk)
                t.ImageUpload = save_file_name

            t.save()

            if t.Author != 'ytinrete':
                mail_str = t.Content
                if request.FILES.get("file"):
                    mail_str += " with picture:" + t.ImageUpload
                send_new_thread_mail.delay(t.Author, mail_str)

            return HttpResponse("ok")
        except BaseException as e:
            print(e)
        return HttpResponseServerError(None)
    else:
        return HttpResponseNotAllowed(None)


def index(request):
    if request.method == 'GET':
        try:
            record_visit(request)
            page_size = 10
            page_group_size = 5
            context = {}
            if request.GET.get('page'):
                index = int(request.GET.get('page'))
                if index < 0:
                    index = 1
            else:
                index = 1
            count = Thread.objects.count()

            front = page_size * (index - 1) + 1
            if front > count:
                index = 1
                front = 1
            context['index'] = index
            back = front + page_size - 1
            if back > count:
                back = count
            if index != 1:
                context['pre'] = index - 1

            if back != count:
                context['next'] = index + 1

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
            data_list = Thread.objects.all()[count - back:count - front + 1:-1]
            context['data_list'] = []
            for i in range(0, len(data_list)):
                context['data_list'].append({'index': i, 'data': data_list[i]})

            return render(request, 'MessageBoard/index.html', context)

        except BaseException as e:
            print(e)
        return HttpResponseServerError(None)
    else:
        return HttpResponseNotAllowed(None)


def get_visit_info(request):
    if request.method == 'GET':
        try:
            count_default = -50
            if request.GET.get('count'):
                req_count = int(request.GET.get('count'))
                if req_count <= 0:
                    count = count_default
                else:
                    count = -req_count
            else:
                count = count_default
            total = VisitInfo.objects.count()
            if total == 0:
                return HttpResponse('Empty')
            front = total + count
            if front < 0:
                front = 0
            data_list = VisitInfo.objects.all()[front:total:-1]
            context = {}
            context['data_list'] = data_list

            for item in reversed(data_list):
                if item.Addr and item.Location == '':
                    html_str = get_response_str(req_maker('http://whatismyipaddress.com/ip/' + item.get('Addr')))
                    html_tree = BeautifulSoup(html_str, 'lxml')
                    for meta in html_tree.head.select('meta'):
                        if meta.get('name') == 'description':
                            # print(meta.get('content'))
                            item.Location = meta.get('content')
                            item.save()  # just find first
                            break
                    break
            return render(request, 'MessageBoard/visit_info.html', context)
        except BaseException as e:
            print(e)
            return HttpResponseServerError(None)
    else:
        return HttpResponseNotAllowed(None)


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


def record_visit(request):
    if request:
        if request.META:
            try:
                v = VisitInfo()
                v.TimeStr = datetime.datetime.now(pytz.timezone('Asia/Shanghai')).strftime('%Y-%m-%d %H:%M:%S')
                v.Url = request.get_full_path()
                v.UserAgent = request.META.get("HTTP_USER_AGENT")
                v.Addr = request.META.get("REMOTE_ADDR")
                v.save()
                search_req.delay(v.TimeStr)
            except BaseException as e:
                print(e)
                return
