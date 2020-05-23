"""
WSGI config for EduMS project.

It exposes the WSGI callable as a module-level variable named ``application``.
#它将WSGI作为模块级变量调用，称为“应用程序”。

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EduMS.settings')

application = get_wsgi_application()
