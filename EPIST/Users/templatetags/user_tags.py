# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from django import template
from urllib.parse import urlencode

register = template.Library()


@register.filter('has_group')
def has_group(user, group_name):
    """
    Verifica si este usuario pertenece a um grupo
    """
    groups = user.groups.all().values_list('name', flat=True)
    return True if group_name in groups else False

@register.simple_tag
def url_replace (request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value

    return dict_.urlencode()
