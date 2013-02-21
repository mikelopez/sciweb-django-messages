from django.conf.urls import patterns, include, url
from django.conf import settings

INBOX_URL = getattr(settings, "INBOX", "inbox")
OUTBOX_URL = getattr(settings, "OUTBOX", "outbox")
POST_MESSAGE_URL = getattr(settings, "POST_MESSAGE", "post_message")
GET_MESSAGE_URL = getattr(settings, "GET_MESSAGE", "get_message")

urlpatterns = patterns('',
    url(r'%s/$' % INBOX_URL,'django_pm.views.inbox', name='inbox'),
    url(r'%s/$' % OUTBOX_URL,'django_pm.views.outbox', name='outbox'),
    url(r'%s/$' % POST_MESSAGE_URL,'django_pm.views.post_message', name='post_message'),
    url(r'%s/$' % GET_MESSAGE_URL,'django_pm.views.get_message', name='get_message'),

    #url(r'^$', 'app_folder_name.views.main_index', name='main_index'),
)
