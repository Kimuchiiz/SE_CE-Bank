from django.contrib import admin
from .models import TransactionLog,Favorite
# Register your models here.
admin.site.register(TransactionLog)
admin.site.register(Favorite)