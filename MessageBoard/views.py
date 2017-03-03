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
import math
import MessageBoard.kittycode
import pytz

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

            return HttpResponse("ok")
        except BaseException as e:
            print(e)
        return HttpResponseServerError(None)
    else:
        return HttpResponseNotAllowed(None)


def index(request):
    if request.method == 'GET':
        try:
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
            data_list = Thread.objects.all()[count - back:count - front+1:-1]
            context['data_list'] = []
            for i in range(0, len(data_list)):
                context['data_list'].append({'index': i, 'data': data_list[i]})

            return render(request, 'MessageBoard/index.html', context)

        except BaseException as e:
            print(e)
        return HttpResponseServerError(None)
    else:
        return HttpResponseNotAllowed(None)