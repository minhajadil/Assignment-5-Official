from django.contrib import admin
from .models import Category,Book

# Register your models here.

admin.site.register(Book)
# admin.site.register(Brand)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('name',)}
    list_display = ['name', 'slug']
    
admin.site.register(Category, CategoryAdmin)