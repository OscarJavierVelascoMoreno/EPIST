from django.contrib import admin
from Projects.models import *

# Models registered for Projects module
admin.site.register(Project)
admin.site.register(User)
