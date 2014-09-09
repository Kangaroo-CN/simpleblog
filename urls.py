from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import login, logout

admin.autodiscover()

#%This is Blog's url
urlpatterns = patterns('simpleblog.dblog.views',
    #index
    (r'^$', 'index'),
    (r'^about/$', 'about'),
    (r'^bloglist/$', 'bloglist'),
    (r'^moodlist/$', 'moodlist'),
   
    #blog
    (r'^blog/(?P<blog_id>\d+)/$', 'readBlog'),
    (r'^writeBlog/$', 'writeBlog'),
    (r'^blog/postEntry/$', 'postEntry'),

    #comment
    (r'^blog/(?P<blog_id>\d+)/comment/add/$', 'addComment'),
    (r'^blog/(?P<blog_id>\d+)/comment/$', 'comment'),
    (r'^blog/(?P<blog_id>\d+)/postComment/$', 'postComment'), 
          )   
urlpatterns += patterns('',
    #User                    
    (r'^accounts/$', login),
    (r'^accounts/login/$', login),
    (r'^accounts/logout/$', logout),
    (r'^accounts/profile/$', 'simpleblog.dblog.views.viewProfile'),
    (r'^accounts/newUser/$', 'simpleblog.dblog.views.newUser'),

    #admin
    (r'^admin/', include(admin.site.urls)),
    )

#%This is BBS's url
urlpatterns += patterns('simpleblog.dbbs.views',
                        )