from django.contrib import admin

from .models import ExpenseModel

# Register your models here.

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('owner','category', 'amount','created_at')
    list_filter = ('owner','category','amount')

    search_fields = ['owner', 'category']


admin.site.register(ExpenseModel, ExpenseAdmin)
