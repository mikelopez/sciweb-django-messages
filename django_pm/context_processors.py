__author__ = 'Marcos Lopez' 
"""
Boatsetter mainweb controller context processor
At the end of the views.py execution, these methods will execute 
returning a Context() to your templates to bypass duplicate views code

"""
from django.template import Context
from django.http import HttpResponse


import simplejson
import logging
log = logging.getLogger('django_pm.context_processors')

from django.conf import settings
from forms import SendMessageForm
from models import Message
from datetime import datetime

def get_args(request):
    """
    Return any consistent get args that will be used through the project
    """
    message = None
    sender = None
    recipient = None
    if request.GET.get('message', None):
        try:
            m = Message.objects.get(pk=int(request.GET.get('message')))
            if m.can_view(request.user):
                message = m
                sender = m.sender
                recipient = m.recipient
                # only recipient can flag it as read
                if m.is_new():
                    if m.recipient.id = request.user.id:
                        m.read_date = datetime.now()
                        m.save()

        except (Message.DoesNotExist, ValueError):
            m = None
    

    response_data  = {'message_id': request.GET.get('message', None), \
        'send_message_form': SendMessageForm(), 'send_to_user': request.GET.get('user', None), \
        'message': message, 'sender': sender, 'recipient': recipient}
    return Context(response_data)
