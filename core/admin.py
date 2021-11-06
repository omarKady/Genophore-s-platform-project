from django.contrib import admin
from .models import Protein, Document, Notification, Comment
# Register your models here.

admin.site.register(Protein, )
admin.site.register(Document)
admin.site.register(Notification)
admin.site.register(Comment)
