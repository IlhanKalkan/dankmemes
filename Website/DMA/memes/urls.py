from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create/$', views.upload, name='upload'),
    url(r'^create_comment/$', views.comment_create, name='comment_create'),
    url(r'^create_reply/$', views.reply_create, name='reply_create'),
    url(r'^posts/(?P<id>\d+)/$', views.post_detail, name='detail'),
    url(r'^post_delete/(?P<id>\d+)', views.post_delete, name='delete_post'),
    url(r'^about/cookies', views.about_cookies, name='cookies'),
    url(r'^about/privacy', views.about_privacy, name='privacy'),
    url(r'^about/tos', views.about_tos, name='tos'),
    url(r'^about/rules', views.about_rules, name='rules'),
    url(r'^profile', views.selfprofile, name='selfprofile'),
    url(r'^u/(?P<id>\d+)/$', views.profile, name='profile'),
]