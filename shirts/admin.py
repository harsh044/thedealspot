from django.contrib import admin
from .models import *

# Register your models here.

class SizeVariantConfig(admin.TabularInline):
    model = Sizevariant

class TshirtConfig(admin.ModelAdmin):
    inlines = [SizeVariantConfig]    

admin.site.register(TheDealSpot, TshirtConfig)