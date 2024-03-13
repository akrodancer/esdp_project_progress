from django.contrib import admin
from pages.models import PageModel, CarouselMainModel, CarouselReviewsModel, CarouselSponsorsModel, CarouselAdvantagesModel

class CarouselMainInline(admin.StackedInline):
    model = CarouselMainModel
    extra = 0
    fields = [field.name for field in model._meta.get_fields()]

class CarouselReviewsInline(admin.StackedInline):
    model = CarouselReviewsModel
    extra = 0
    fields = [field.name for field in model._meta.get_fields()]

class CarouselSponsorsInline(admin.StackedInline):
    model = CarouselSponsorsModel
    extra = 0
    fields = [field.name for field in model._meta.get_fields()]

class CarouselAdvantagesInline(admin.StackedInline):
    model = CarouselAdvantagesModel
    extra = 0
    fields = [field.name for field in model._meta.get_fields()]

@admin.register(PageModel)
class PageFlatTextAdmin(admin.ModelAdmin):
    inlines = (CarouselMainInline, 
               CarouselReviewsInline, 
               CarouselSponsorsInline, 
               CarouselAdvantagesInline)
    
    list_display = ('title', 'path')



