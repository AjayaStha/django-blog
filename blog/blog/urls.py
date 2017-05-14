from django.conf.urls import url

from .views import post_list,post_detail,post_new,post_edit,post_remove,signup,login_view,logout_view

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^post/(?P<pk>\d+)/$', post_detail, name='post_detail'),
    url(r'^post/new/$', post_new ,name='post_new'),
    url(r'^post/(?P<pk>\d+)/edit/$', post_edit, name='post_edit'),
    url(r'^post/(?P<pk>\d+)/remove/$', post_remove, name='post_remove'),
    url(r'^signup/$',signup,name='signup'),
    url(r'^login/$',login_view,name='login'),
    url(r'^logout/$',logout_view,name='logout'),
    ]
