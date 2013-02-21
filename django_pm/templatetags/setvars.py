import re
from django import template
from django.contrib.contenttypes.models import ContentType 
from django.core.urlresolvers import reverse
from django_pm.models import *
from django_pm.texts import SEND_MESSAGE_RECIPIENT_HTML

register = template.Library()


class SetVarNode(template.Node):
    def __init__(self, new_val, var_name):
        self.new_val = new_val
        self.var_name = var_name
    def render(self, context):
        context[self.var_name] = self.new_val
        return ''

@register.tag
def setvar(parser,token):
    # This version uses a regular expression to parse tag contents.
    # referenced from - http://stackoverflow.com/questions/1070398/how-to-set-a-value-of-a-variable-inside-a-template-code
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments" % tag_name
    new_val, var_name = m.groups()
    #if not (new_val[0] == new_val[-1] and new_val[0] in ('"', "'")):
    #    raise template.TemplateSyntaxError, "%r tag's argument should be in quotes" % tag_name
    return SetVarNode(new_val[1:-1], var_name)