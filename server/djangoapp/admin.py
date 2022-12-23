from django.contrib import admin
from .models import *


# Register your models here.

# CarModelInline class

# CarModelAdmin class

# CarMakeAdmin class with CarModelInline

# Register models here


class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 1 


class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
    
    list_display = ['name']
    search_fields = ['name']


class CarModelAdmin(admin.ModelAdmin):
    
    list_display = ('name', 'type')
    search_fields = ['name']



admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)