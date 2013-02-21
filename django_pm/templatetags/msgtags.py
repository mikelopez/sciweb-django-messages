__author__ = "Marcos Lopez"
import re
from django import template
from django.contrib.contenttypes.models import ContentType 
from django.core.urlresolvers import reverse
from django_pm.models import *
from django_pm.texts import SEND_MESSAGE_RECIPIENT_HTML, SEND_MESSAGE_PARENT_HTML

register = template.Library()

@register.filter
def get_inbox_count(user):
    """
    Get the inbox messages count
    """
    return len(Message.objects.get_inbox_messages(user))

@register.filter
def generate_recipient(send_to):
    """
    Read some html data with RECIPIENT placeholder text 
    replace with the user ID supplied
    checks if has attribute id (if its an object)
    or just a raw ID sent
    """
    try:
        return SEND_MESSAGE_RECIPIENT_HTML.replace('#RECIPIENT#', str(send_to.id))
    except:
        return SEND_MESSAGE_RECIPIENT_HTML.replace('#RECIPIENT#', send_to)

@register.filter
def generate_parent(msg):
    """
    Read some html data with RECIPIENT placeholder text 
    replace with the user ID supplied
    checks if has attribute id (if its an object)
    or just a raw ID sent
    """
    if msg.parent_msg:
        parent = msg.parent_msg
    else:
        parent = msg
    try:
        return SEND_MESSAGE_PARENT_HTML.replace('#PARENT#', str(msg.id))
    except:
        return SEND_MESSAGE_PARENT_HTML.replace('#PARENT#', msg)

@register.filter
def generate_parent_message(msg):
    pass
    

@register.filter
def get_inbox_messages(user):
    """
    Get the inbox messages for the user specified
    """
    return Message.objects.get_inbox_messages(user)


