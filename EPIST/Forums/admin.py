from django.contrib import admin
from Forums.models import *

# Register for Forum models.
admin.site.register(Forum)
admin.site.register(Discussion)
admin.site.register(Message)
