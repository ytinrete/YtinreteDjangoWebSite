from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^getList', views.get_list, name='getList'),
    url(r'^addThread', views.add_thread, name='addThread'),
    url(r'^imgUpload', views.img_upload, name='imgUpload'),

    url(r'^$', views.index, name='index'),
    url(r'^postThread', views.post_thread, name='postThread'),
    url(r'^visitInfo', views.get_visit_info, name='visitInfo'),
]
