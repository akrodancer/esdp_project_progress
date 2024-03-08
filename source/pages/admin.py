from django.contrib import admin
from pages.models import PageModel

@admin.register(PageModel)
class PageFlatTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'path')



