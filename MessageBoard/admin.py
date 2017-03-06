from django.contrib import admin

# Register your models here.
from .models import Thread
from .models import VisitInfo

admin.site.register(Thread)
admin.site.register(VisitInfo)