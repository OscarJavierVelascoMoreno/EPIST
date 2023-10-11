from django.contrib import admin
from Knowledge.models import *

# Register for Knowledge models.
admin.site.register(KnowledgeType)
admin.site.register(Knowledge)
admin.site.register(KnowledgeStep)
