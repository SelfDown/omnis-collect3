# -*- coding: utf-8 -*-
import os

os.system('python manage.py inspectdb > sample/models/models.py')

print('更新models.py成功！')


