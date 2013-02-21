__author__ = 'Marcos Lopez'

import time
import os
import mimetypes
import simplejson

from datetime import datetime, timedelta

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404, render
from django.template import RequestContext, loader, Context
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse, resolve
from django.core.context_processors import csrf

from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout

from models import *
from forms import *

from django.conf import settings

PROJECT_ROOTDIR = getattr(settings, 'PROJECT_ROOTDIR', None)
STATIC_BOOTSTRAP = getattr(settings, 'STATIC_BOOTSTRAP', None)
MEDIA_URL = getattr(settings, 'MEDIA_URL', None)

import ipaddr
import datetime

import logging
log = logging.getLogger('django_pm.views')

@login_required
def inbox(request):
    """
    Return the messages in the inbox
    """

    return render(request, 'django_pm/inbox.html')

@login_required
def outbox(request):
    """
    Return the messages in the outbox 

    """
    if request.GET.get('json', None):
        messages = []
        for i in Message.objects.get_outbox_messages(request.user):
            messages.append({'recipient_id': i.recipient.id, \
                'recipient_name': i.recipient.name, \
                'sender_id': i.sender.id, 'sender_name': i.sender_name})
        response = {'result': 'ok', 'messages': messages}
        return HttpResponse(simplejson.dumps(response), mimetype="application/json")

    return render(request, 'django_pm/outbox.html')

@login_required
def post_message(request):
    """
    Return the messages in the inbox
    """
    if request.method == 'POST':
        msg = "Hello I am user1"
        data = {
            'recipient': request.POST.get('recipient', None),
            'sender': request.user.id,
            'text': request.POST.get('text', None),
            'read_date': None,
            'parent_msg': request.POST.get('parent_msg', None),
        }
        send_msg = SendMessageForm(data)
        message_object = None
        if send_msg.is_valid():
            message_object = send_msg.save()  
        return HttpResponseRedirect(reverse('inbox'))

    try:
        send_to_user_object = User.objects.get(pk=int(request.GET.get('user', None)))
    except (User.DoesNotExist, TypeError):
        send_to_user_object = None
        log.debug('User id is not valid')
        return render(request, 'django_pm/post_message.html', \
            {'userlist': User.objects.filter(is_superuser=False, is_staff=False, is_active=True)})
    return render(request, 'django_pm/post_message.html')

@login_required
def get_message(request):
    """
    Return the messages in the inbox
    """
    return render(request, 'django_pm/get_message.html')



