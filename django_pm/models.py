__author__ = 'Marcos Lopez'
__email__ = 'dev@scidentify.info' 

from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.contenttypes.models import ContentType 

from datetime import datetime 

# UPDATE your models here.

from countrycodes import COUNTRY_STATES
from django.conf import settings

PROJECT_ROOTDIR = getattr(settings, "PROJECT_ROOTDIR", None)

class MessageManager(models.Manager):
  """
  Custom manager for messages
  """
  def get_content_type(self, obj):
    """ 
    return contenttype for an object
    """
    return ContentType.objects.get_for_model(type(obj))

  def get_new_messages_count(self, user):
    """
    Get the messages count or any NEW messages
    """
    return inbox_count(user)

  def get_inbox_messages_count(self, user):
    """
    Get the total inbox messages - exclude deleted 
    """
    return len(Message.objects.filter(recipient=user, deleted_date__isnull=True))

  def get_inbox_messages(self, user):
    """
    get my messages (user)
    """
    return Message.objects.filter(recipient=user, deleted_date__isnull=True).order_by('-id')

  def get_outbox_messages(self, user):
    """
    Get sent outbox messages 
    """
    return Message.objects.filter(sender=user, deleted_date__isnull=True)

  def get_parent_messages(self):
    """
    Return parent messages back to model method 
    """
    return Message.objects.filter(parent_msg=self)




class Message(models.Model):
  """
  Define the message class database structure
  """
  sender = models.ForeignKey(User, related_name='sent_messages')
  recipient = models.ForeignKey(User, related_name='inbox_messages')
  parent_msg = models.ForeignKey('self', null=True, blank=True)
  read_date = models.DateTimeField(null=True, blank=True)
  deleted_date = models.DateTimeField(null=True, blank=True)
  text = models.TextField()
  date_sent = models.DateTimeField(null=True, blank=True, default=datetime.now())
  objects = MessageManager()

  def is_deleted(self):
    """ check if message is deleted """
    if not self.deleted_date:
      return False
    return True

  def is_new(self):
    if not self.read_date:
      return True
    return False

  def set_as_read(self):
    """
    Set the message as read by the user
    """
    self.read_date = datetime.now()
    self.save()
    return True

  def set_as_deleted(self):
    """
    Set the message as deleted (but dont delete until permanently deleted)
    """
    self.deleted_date = datetime.now()
    self.save()
    return True

  def can_view(self, user):
    """
    returns if the user is in sent/received thread 
    """
    if not user.id == self.recipient.id:
      if not user.id == self.sender.id:
        return False
    return True

  def can_reply(self, user):
    """
    check if a user can reply to this
    """
    if not self.can_view(user):
      return False
    return True

  def get_parents(self):
    """
    Get the parent messages for a message via manager 
    tries parent if available, otherwise, tries child msgs for itself
    """
    msgs = []
    if self.parent_msg:
      for i in Message.objects.filter(parent_msg=self.parent_msg).order_by('-id'):
        msgs.append(i)
      msgs.append(self.parent_msg)
    else:
      for i in self.get_child_messages():
        msgs.append(i)
    return msgs
    
  def get_child_messages(self):
    """ 
    Get any child messages 
    """
    return Message.objects.filter(parent_msg=self).order_by('-id')
    



def inbox_count(user):
  """ get the inbox count for messages """
  return Message.objects.filter(recipient=user, read_date__isnull=True,\
             deleted_date__isnull=True).count()
