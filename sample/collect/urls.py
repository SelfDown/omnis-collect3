# -*- coding: utf-8 -*-
from django.conf.urls import url

from collect.download_excel import ExcelDownload
from collect.import_excel import ExcelImport

urlpatterns = [
    url(r'^download$', ExcelDownload.as_view()),
    url(r'^import$', ExcelImport.as_view()),

]
