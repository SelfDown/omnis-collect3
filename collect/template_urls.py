# -*- coding: utf-8 -*-
from django.conf.urls import url

from collect.template_data import TemplateData

urlpatterns = [
    url(r'^data$', TemplateData.as_view()),

]
