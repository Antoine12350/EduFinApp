from django.contrib import admin
from .models import Budget
from core.models import Testing, Transaction
admin.site.register(Testing)
admin.site.register(Transaction)
admin.site.register(Budget)