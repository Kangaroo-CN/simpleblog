from django.contrib import admin
from simpleblog.dblog.models import Blog, Comment, Mood

admin.site.register(Blog)
admin.site.register(Comment)
admin.site.register(Mood)
