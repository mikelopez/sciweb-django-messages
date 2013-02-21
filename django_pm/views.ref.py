__author__ = 'Marcos Lopez'

import time
import os
import mimetypes
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

# as new apps are built, you can import them here and 
# record if we found a match
try:
    from other_reusable_app.models import *
    from other_reusable_app.forms import *
    load_reusable_app = True
except ImportError:
    load_reusable_app = False


from django.conf import settings

PROJECT_ROOTDIR = settings.PROJECT_ROOTDIR
STATIC_BOOTSTRAP = settings.STATIC_BOOTSTRAP
MEDIA_URL = settings.MEDIA_URL

import ipaddr
import datetime

import logging
log = logging.getLogger('django_pm.views')


"""
data structure
service_name: dictionary with keys as model_name, and 
returns list of Model and Form instance 
E.g: get the model = data.get('customers').get('customer')[0]
E.g: get the form = data.get('customers').get('customer')[1]
"""
data = {
    #'other_apps': {
    #   'table-alias-name': [TableClass, TableClassForm],
    #   'other-table-alias': [TableClass, TableClassForm]
    #}
    'app_folder': {
        'student': [Customer, CustomerForm],
        'school': [Contacts, ContactsForm],
    },
}

# check if any other reusable apps are ok to call
# if load_reusable_app:
#     data['services'] = {'after-school-care': [AfterSchoolCare, AfterSchoolCareForm]}

def get_object(Table, object_id):
    """
    privately used
    standard method to get the object from model
    raise 404 if not found
    """
    log.info('Get %s from object_id: %s ' % (Table.__name__, object_id))
    try:
        tbl = Table.objects.get(pk=int(object_id))
        return tbl
    except Table.DoesNotExist:
        raise Http404


def process_post(request, form=None, obj_to_update=None):
    """ 
    privately used
    If post is sent, process it and update the fields
    pass obj to do an edit-save or leave blank
    to create new object
    """
    log.info('Processing Post...')
    if not form: 
        return None

    if request.method == 'POST':
        # set post data into the form
        postdata = request.POST.copy()
        form = form(postdata)
        if form.is_valid():
            log.info('form is valid')
            form.save(obj=obj_to_update)
        return form


def process_url(request, service_name, model_name, action_name, object_id):
    """
    used privately
    Process the URl and find the right model/form data for this
    returns a data context
    object_id is required with None if there is no value
    """
    log.info('process_url service, model, action, objid: %s %s %s %s' % (\
        service_name, model_name, action_name, object_id))
    if not data.get(service_name):
        log.info('No service name or service name not found - 404!')
        raise Http404
    if not data.get(service_name).get(model_name):
        log.info('No modelname - 404!')
        raise Http404

    if not action_name:
        action_name = 'show'

    # get the model and form classes
    try:
        model = data.get(service_name).get(model_name)[0]
    except IndexError:
        model = None
    try:
        form = data.get(service_name).get(model_name)[1]
    except IndexError:
        form = None

    # get the object if searching by ID or none - which will get list in model
    objectget = get_object(model, object_id) if object_id else None
    # get the form with object instance or just the blank form
    objectform = form() if not objectget else form(instance=objectget)
    posted = True if request.method == 'POST' else False

    # process post
    updated_form = process_post(request, form=form, \
        obj_to_update=model() if not objectget else objectget)
    if updated_form:
        objectform = updated_form
    if objectform.errors:
        posted = False

    # get customer list AFTEr post so we can get any updated data back
    object_list = model.objects.all() if not object_id else None
    show_url = '/main/%s/%s/show' % (service_name, model_name)
    edit_url = '/main/%s/%s/edit' % (service_name, model_name)
    delete_url = '/main/%s/%s/delete' % (service_name, model_name)
    add_url = '/main/%s/%s/add' % (service_name, model_name)

    context_data = {
        'form': objectform,
        'object': objectget,
        'object_list': object_list,
        'posted': posted,

        'service_name': service_name,
        'action_name': action_name,
        'object_id': object_id,
        'model_name': model_name,

        'showurl': show_url,
        'edit_url': edit_url,
        'delete_url': delete_url,
        'add_url': add_url
    }

    #return model, form
    return context_data



@login_required()
def main_index(request, service_name=None, model_name=None, action_name=None, object_id=None):
    """
    Customer index page
    read service_name (blogs, news, students, w/e) which is based on app-name
    service_name is an alias of the app_name 
    Then we will generate the form and submit the proper action for the form if needed

    * model_name is the name of the model or name of the key in a dictionary containing that Model instance
    * action_name would be either: show/view, edit, save, delete
    * object_id will be the value of the ID you want to show/edit, blank will show all! :D 

    """
    context_data = process_url(request, service_name, model_name, action_name, object_id)

    log.info('INDEX: service_name: %s' % (service_name))
    log.info('INDEX: model_name: %s' % (model_name))
    log.info('INDEX: action_name: %s' % (action_name))
    log.info('INDEX: object_id: %s' % (object_id))

    # returns RequestContext by default
    # return render(request, 'customers/index.html', {}, content_type='application/xhtml+xml')

    return render_to_response('customers/index.html', context_data, RequestContext(request))















