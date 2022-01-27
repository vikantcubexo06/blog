from django.contrib import admin

# Register your models here.
from django.utils.html import format_html

from .models import Info, Blog, CommentPost, ReplyComment, Query


class BlogAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'write_blog', 'approval']


admin.site.register(Blog, BlogAdmin)


class InfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'firstname', 'gender', 'image_tag']
    readonly_fields = ('image_tag',)

    def image_tag(self, obj):
        return format_html(f'<img style="height:100px;" src="/{obj.imag}"/>')


admin.site.register(Info, InfoAdmin)


class CommentInfo(admin.ModelAdmin):
    list_display = ['id', 'blog', 'title', 'comment_text', ]

    def title(self, obj):
        return obj.blog.title


admin.site.register(CommentPost, CommentInfo)


class ReplyInfo(admin.ModelAdmin):
    list_display = ['id', 'comment_text', 'reply', ]

    # def title(self, obj):
    #     return obj.blog.title


admin.site.register(ReplyComment, ReplyInfo)


class QueryInfo(admin.ModelAdmin):
    list_display = ['id', 'name', 'email', 'mobile', 'query']


admin.site.register(Query, QueryInfo)
