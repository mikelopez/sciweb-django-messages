"""
Author: Marcos Lopez
Unit Tests to test the flow of messages
- Sending messages
- Reading inbox
- Reading messages
- Replying to messages
- Basic rules for message privacy
"""

from django.test import TestCase, Client
from django.core.urlresolvers import reverse, resolve

settings_urls  = ['INBOX', 'POST_MESSAGE', 'GET_MESSAGE']
settings_vars = ['INBOX_TAG', 'OUTBOX_TAG', ]
reverse_urls = ['inbox', 'post_message', 'get_message']

import logging
import simplejson

from django.conf import settings
from django.contrib.auth.models import User

from lxml import html
from xml.dom import minidom

from django_pm.forms import SendMessageForm
from django_pm.models import Message

class TestURLS(TestCase):
    """
        Test the app_folder_name application
    """
    user1 = None
    user2 = None
    user3 = None

    def setUp(self):
        'Creating users......'
        users = ['user1', 'user2', 'user3']
        for u in users:
            try:
                setattr(self, u, User.objects.get(username=u))
            except User.DoesNotExist:
                createuser = User.objects.create(username=u, email='%s@scidentify.info'% u)
                createuser.set_password('user123')
                createuser.save()
                setattr(self, u, createuser)

    def tearDown(self):
        print 'Deleting messages.......'
        users = ['user1', 'user2', 'user3']
        for u in users:
            try:
                deluser=User.objects.get(username=u)
                deluser.delete()
            except User.DoesNotExist:
                pass

    def test_urls(self):
        """ test the urls """
        for r in reverse_urls:
            response = Client().get(reverse(r))
            # make sure the url is found, its ok if we get redirection or 500
            self.assertTrue(response.status_code != '404')

    def test_settings(self):
        """ 
        check settings for vars we need 
        """
        for value in settings_urls:
            self.assertTrue(getattr(settings, value, False))
        try:
            from settings import PROJECT_ROOTDIR
        except:
            print 'Warning: PROJECT_ROOTDIR not found in settings'
            #raise AssertionError

        try:
            from settings import STATIC_BOOTSTRAP
        except:
            print 'Warning: STATIC_BOOTSTRAP not found in settings'
            #raise AssertionError

    def test_model_forms(self):
        """
        Test the Model forms which will be used by the templates and views
        """
        # send a message to user2 - resemble a POST
        msg = "Hello I am user1"
        data = {
            'recipient': self.user2.id,
            'sender': self.user1.id,
            'text': msg,
            'read_date': None,

        }
        send_msg = SendMessageForm(data)
        message_object = None
        if send_msg.is_valid():
            message_object = send_msg.save()
        print "Saved object: %s" % message_object
        # delete when done
        if message_object:
            message_object.delete()


    def test_inbox(self):
        """
        This will test calling the page, and making sure the 
        output returned is correct
        Testing the utilization of template tags also
        """
        browser = Client()
        self.assertTrue(browser.login(username=self.user1.username, password='user123'))
        # get the page
        response = browser.get(reverse('inbox'))
        dom = html.fromstring(response.content)
        self.assertTrue("INBOX-PAGE" in response.content)

        # test as json
        """browser = Client()
        self.assertTrue(browser.login(username=self.user1.username, password='user123'))
        # get the page
        response = browser.get("%s?json=y" % reverse('inbox'))
        print "RESPONSE = %s" % response.content
        dom = simplejson.loads(response.content)
        self.assertTrue('result' in dom.keys())
        self.assertTrue('messages' in dom.keys())"""


    def test_outbox(self):
        """
        Go in as user1 and try to submit a message
        """
        browser = Client()
        self.assertTrue(browser.login(username=self.user1.username, password='user123'))
        # get the page
        response = browser.get(reverse('outbox'))
        dom = html.fromstring(response.content)

        self.assertTrue("OUTBOX-PAGE" in response.content)

        # send a message to user2 - resemble a POST
        msg = "Hello I am user1"
        data = {
            'recipient': self.user2.id,
            'sender': self.user1.id,
            'text': msg,
            'read_date': None,
 
        }
        post_response = browser.post(reverse('post_message'), data, follow=True)
        self.assertTrue(post_response.status_code, 200)
        redirect = False
        for url, status_code in post_response.redirect_chain:
            if status_code == 302:
                redirect = url
                print "REDIRECTED TO: %s" % url
        # check for proper redirection page of skip..

        # now, check your mail as user2, you should have a message
        self.assertTrue(len(Message.objects.filter(sender=self.user1)) == 1)
        browser2 = Client()
        self.assertTrue(browser2.login(username=self.user2.username, password='user123'))
        # get the page
        response = browser2.get(reverse('inbox'))
        try:
            dom = html.fromstring(response.content)
        except:
            dom = ''

        self.assertTrue("1 Message" in response.content)
        # delete from the database
        for i in Message.objects.all():
            i.delete()


    def test_model_methods(self):
        """
        Test the model methods for a message
        - Is Message Deleted
        - Is Message New
        - Get New messages
        - Get ALL messages
        - Get Messages count
        - Get New Messages count
        - Get Parent Message
        - Can View Message
        -------
        - Set as read 
        - Set as deleted
        """
        msg = "Hello I am user1"
        data = {
            'recipient': self.user2.id,
            'sender': self.user1.id,
            'text': msg,
            'read_date': None,

            'deleted_date': None
        }
        send_msg = SendMessageForm(data)
        if send_msg.is_valid():
            message_object = send_msg.save()

        # check is deleted
        self.assertFalse(message_object.is_deleted())
        # check is new
        self.assertTrue(message_object.is_new())
        # get list of new messages - should have 1
        self.assertTrue(len(Message.objects.get_inbox_messages(user=self.user2)) == 1)

        # get inbox count
        self.assertTrue(Message.objects.get_new_messages_count(user=self.user2) == 1)

        # read the message
        self.assertTrue(message_object.set_as_read())
        self.assertFalse(Message.objects.get_inbox_messages(user=self.user2)[0].is_new())
       
        # get inbox count
        self.assertTrue(Message.objects.get_new_messages_count(user=self.user2) == 0)

        # delete the message
        self.assertTrue(message_object.set_as_deleted())
        self.assertTrue(message_object.is_deleted())


    def test_not_allowed(self):
        """
        Test pages and not allowed stuff
        - user cannot view messages that are not to him
        """
        msg = "Hello I am user1"
        data = {
            'recipient': self.user2.id,
            'sender': self.user1.id,
            'text': msg,
            'read_date': None,

            'deleted_date': None
        }
        send_msg = SendMessageForm(data)
        if send_msg.is_valid():
            message_object = send_msg.save()

        self.assertFalse(message_object.can_view(self.user3))

        browser = Client()
        self.assertTrue(browser.login(username=self.user3.username, password='user123'))
        # get the page
        response = browser.get("%s?message=%s" % (reverse('get_message'), message_object.id))
        # should return 404 cause you(user3) did not sent or receive 
        self.assertTrue(response.status_code, 404)


    def test_reply(self):
        """
        Test replying a message from a user
        """
        # original first message sent (message1)
        msg = "Hello I am user1"
        data = {
            'recipient': self.user2.id,
            'sender': self.user1.id,
            'text': msg,
            'read_date': None,
            'deleted_date': None
        }
        send_msg = SendMessageForm(data)
        if send_msg.is_valid():
            message_object = send_msg.save()


        # allow this reply - message object has no parent, 
        # so it will use message_object as parent 
        msg = "Hello I am user2 Nice to meet you"
        data = {
            'recipient': self.user1.id,
            'sender': self.user2.id,
            'text': msg,
            'read_date': None,
            'parent_msg': message_object.id,
            'deleted_date': None
        }
        send_msg2 = SendMessageForm(data)
        if send_msg2.is_valid():
            message_object2 = send_msg2.save()

        # reply back to second message, which will use message2 as parent
        # btu since that contains parent, parent will really be message1
        msg = "Hello I am user2 Nice to meet you"
        data = {
            'recipient': self.user2.id,
            'sender': self.user1.id,
            'text': msg,
            'read_date': None,
            'parent_msg': message_object2.id,
            'deleted_date': None
        }
        send_msg22 = SendMessageForm(data)
        if send_msg22.is_valid():
            message_object22 = send_msg22.save()
        # should equal first parent cause thats what message2 has
        print message_object.id
        print message_object22.id
        print message_object22.parent_msg.id
        self.assertTrue(message_object22.parent_msg.id == message_object.id)

        # reply back to second message, which will use message2 as parent
        # btu since that contains parent, parent will really be message1
        msg = "Hello I am user2 Nice to meet you"
        data = {
            'recipient': self.user1.id,
            'sender': self.user2.id,
            'text': msg,
            'read_date': None,
            'parent_msg': message_object22.id,
            'deleted_date': None
        }
        send_msg222 = SendMessageForm(data)
        if send_msg222.is_valid():
            message_object222 = send_msg222.save()
        # should equal first parent cause thats what message2 has
        self.assertTrue(message_object222.parent_msg.id == message_object.id)


        # DO NOT allow this reply cause user3 is not in parents recipient/sender
        msg = "Hello I am user2 Nice to meet you"
        data = {
            'recipient': self.user2.id,
            'sender': self.user3.id,
            'text': msg,
            'read_date': None,
            'parent_msg': message_object.id,
            'deleted_date': None
        }
        send_msg3 = SendMessageForm(data)
        if send_msg3.is_valid():
            message_object3 = send_msg3.save()

        self.assertFalse(message_object3)

        # both sender/recipient can reply to msg
        self.assertTrue(message_object.can_reply(self.user2))
        self.assertTrue(message_object.can_reply(self.user1))
        # howeverrandom users cannot!
        self.assertFalse(message_object.can_reply(self.user3))


    def test_read_flagging(self):
        """
        Make sure the message gets set as read as soon as its loaded on the page!
        """
        msg = "Hello I am user1"
        data = {
            'recipient': self.user2.id,
            'sender': self.user1.id,
            'text': msg,
            'read_date': None,
            'deleted_date': None
        }
        send_msg = SendMessageForm(data)
        if send_msg.is_valid():
            message_object = send_msg.save()
        self.assertTrue(message_object.is_new())

        browser = Client()
        self.assertTrue(browser.login(username=self.user1.username, password='user123'))
        # get the page
        response = browser.get("%s?message=%s" % (reverse('get_message'), message_object.id))
        dom = html.fromstring(response.content)
        self.assertFalse(Message.objects.get(pk=message_object.id).is_new())





