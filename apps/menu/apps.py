# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MenuConfig(AppConfig):
    name = 'apps.menu'
    label = 'menu'
    verbose_name = _('Menu')
