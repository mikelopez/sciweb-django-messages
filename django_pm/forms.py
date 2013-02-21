from django import forms
from models import Message
from django.contrib.auth.models import User
from django.forms.util import ErrorList

import logging
log = logging.getLogger('django_pm.views')

class SendMessageForm(forms.ModelForm):
    """
    Message form to post
    """
    class Meta:
        # exclude any fields from the db here
        # exclude = ('accounts', 'status')
        exclude = ('recipient','sender','parent_msg', 'deleted_date', 'read_date', 'date_sent')
        model = Message

    def clean(self):
        return self.cleaned_data

    def post(self):
        self.save()

    def save(self):
        """
        Save the message - post
        """
        # find the recipient and sender
        try:
            recipient = User.objects.get(pk=int(self.data.get('recipient')))
        except (ValueError, User.DoesNotExist):
            recipient = None
            self._errors = ErrorList(['Not a valid recipient'])
        try:
            sender = User.objects.get(pk=int(self.data.get('sender')))
        except (ValueError, User.DoesNotExist):
            sender = None
            self._errors = ErrorList(['Not a valid sender']) 

        parent = None
        if self.data.get('parent_msg', None):
            try:
                parent = Message.objects.get(pk=int(self.data.get('parent_msg')))
                if not parent.can_reply(sender):
                    self._errors = ErrorList(['Not allowed to response'])
                # chain the letters
                if parent.parent_msg:
                    parent = parent.parent_msg
            except Message.DoesNotExist:
                self._errors = ErrorList(['Error no parent'])
                parent = None
            
        if not self._errors:
            # populate the data for the data
            data = {}
            for k, v in self.data.items():
                data[k] = v
            data['sender'] = sender
            data['recipient'] = recipient
            if parent:
                data['parent_msg'] = parent
            log.info(data)
            # save the object to db
            msg = Message(**data)
            msg.save()
            return msg





