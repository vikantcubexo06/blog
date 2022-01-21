from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from .models import Info, Blog


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'write_blog']


admin.site.register(Blog, BlogAdmin)


class InfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'firstname', 'gender', 'image_tag']
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        return format_html(f'<img style="height:100px;" src="/{ obj.imag }"/>')


admin.site.register(Info, InfoAdmin)
# admin.site.register(socialapp)
