from django.contrib import admin
from site_pages.models import PageFlatText

@admin.register(PageFlatText)
class PageFlatTextAdmin(admin.ModelAdmin):
    list_display = ('title', 'path')



